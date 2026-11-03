"""
Skoring terpusat untuk evaluasi RA-Diffusion (RDM-STGNN) dan baseline CSDI.

Modul ini adalah SATU sumber kebenaran untuk tiga hal yang sebelumnya disalin
berulang di ``scripts/run_eval_final.py``, ``scripts/eval_rain_robust.py``, dan
``csdi_baseline/evaluate_csdi.py``:

1. Denormalisasi target ke satuan fisik (termasuk ``expm1`` untuk presipitasi).
2. Batas fisik: presipitasi ``[0, 60]`` mm/j, angin ``>= 0``, RH ``[0, 100]``.
3. Rain gate berbasis ``wet_probability`` dan perhitungan metrik skor.

Kontrak rain gate (perbaikan bias)
----------------------------------
Implementasi lama memotong nilai presipitasi ensemble menjadi 0 SEBELUM metrik
dihitung. Akibatnya:

* CRPS/Brier/reliability dihitung pada distribusi yang sudah rusak (massa titik
  di nol), sehingga kalibrasi probabilistik model tidak lagi terukur.
* POD/FAR/CSI tampak membaik karena jendela yang di-gate tidak mungkin menjadi
  false alarm, padahal tidak ada cara mengukur apakah gate itu sendiri benar.

Modul ini memisahkan dua peran yang berbeda:

* ``ensemble`` adalah distribusi prediktif mentah. Ia SELALU dipakai apa adanya
  untuk CRPS, Brier, dan reliability, dan tidak pernah dimutasi oleh gate.
* Gate hanya diterapkan di lapisan KEPUTUSAN event (dan opsional pada point
  forecast). Metrik event yang di-gate selalu dilaporkan berdampingan dengan
  versi ``*_ungated`` agar kontribusi gate dapat diukur, bukan tersembunyi.

Karena CSDI tidak memiliki rain gate, angka ``*_ungated`` adalah yang setara
untuk perbandingan antar-model (like-for-like).

Referensi:
- Wilks, D.S. (2019). Statistical Methods in the Atmospheric Sciences.
- Hersbach, H. (2000). Decomposition of the CRPS for ensemble prediction systems.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Sequence, Tuple, Union

import numpy as np

try:  # torch bersifat opsional: jalur metrik murni numpy tetap dapat dipakai.
    import torch

    _TORCH_AVAILABLE = True
except ImportError:  # pragma: no cover - lingkungan produksi selalu punya torch
    torch = None  # type: ignore[assignment]
    _TORCH_AVAILABLE = False

from src.config import (
    FINAL_TARGET_COLS,
    LOG_PRECIP_MAX,
    PRECIP_PHYSICAL_MAX_MM,
    PROB_EVENT_THRESHOLD,
)
from src.evaluation.probabilistic_metrics import (
    compute_brier_score,
    compute_correlation,
    compute_crps,
    compute_mae,
    compute_rmse,
)

ArrayLike = Union[np.ndarray, "torch.Tensor"]

PRECIP_VAR = "precipitation"
WIND_VAR = "wind_speed"
RH_VAR = "relative_humidity"

RH_PHYSICAL_MAX = 100.0
DEFAULT_WET_PROBABILITY_THRESHOLD = 0.6
DEFAULT_RAIN_OCCURRENCE_MM = 0.1
DEFAULT_EVENT_THRESHOLDS: Tuple[float, ...] = (2.0, 5.0, 10.0)


# ==============================================================================
# HELPER BACKEND (numpy <-> torch)
# ==============================================================================

def _is_tensor(value) -> bool:
    return _TORCH_AVAILABLE and isinstance(value, torch.Tensor)


def to_numpy(value) -> np.ndarray:
    """Kembalikan ndarray numpy tanpa menyalin bila sudah numpy."""
    if _is_tensor(value):
        return value.detach().cpu().numpy()
    return np.asarray(value)


def _scalar_param(param, index: int, boundary: float) -> float:
    """Ambil parameter ke-``index`` dari skalar, sequence, atau tensor.

    ``boundary`` dipakai saat ``param is None`` (0.0 untuk mean, 1.0 untuk std).
    """
    if param is None:
        return boundary
    if isinstance(param, (int, float)):
        return float(param)
    return float(param[index])


def _threshold_key(threshold: float) -> str:
    """Kunci metrik kanonik: ``2.0 -> "2mm"``, ``0.1 -> "0p1mm"``."""
    return f"{threshold:g}".replace(".", "p") + "mm"


# ==============================================================================
# DENORMALISASI + BATAS FISIK
# ==============================================================================

def denormalize_precipitation(
    normalized: ArrayLike,
    mean: float = 0.0,
    std: float = 1.0,
    *,
    log_ceiling: float = LOG_PRECIP_MAX,
    physical_max: float = PRECIP_PHYSICAL_MAX_MM,
) -> ArrayLike:
    """
    Ubah presipitasi dari ruang z (``log1p(mm/h)`` ter-standardisasi) ke mm/j.

    Urutan operasi identik untuk kedua backend:
    ``expm1(clamp(z * std + mean, max=log_ceiling))`` lalu ``clip(0, physical_max)``.
    Clamp di ruang log mencegah overflow (``e^20 ~ 4.85e8``); clamp di ruang fisik
    adalah batas numerik 60 mm/j, jauh di atas nilai nyata (maks dataset ~21.5).

    NaN dipropagasikan apa adanya, bukan diubah menjadi nol.
    """
    if _is_tensor(normalized):
        log_mm = normalized * std + mean
        mm = torch.expm1(torch.clamp(log_mm, max=log_ceiling))
        return torch.clamp(mm, min=0.0, max=physical_max)

    log_mm = np.asarray(normalized, dtype=np.float64) * std + mean
    with np.errstate(invalid="ignore"):
        mm = np.expm1(np.minimum(log_mm, log_ceiling))
    return np.clip(mm, 0.0, physical_max)


def apply_physical_constraints(values: ArrayLike, variable: str) -> ArrayLike:
    """Terapkan batas fisik per variabel target."""
    if variable == PRECIP_VAR:
        if _is_tensor(values):
            return torch.clamp(values, min=0.0, max=PRECIP_PHYSICAL_MAX_MM)
        return np.clip(np.asarray(values, dtype=np.float64), 0.0, PRECIP_PHYSICAL_MAX_MM)
    if variable == WIND_VAR:
        if _is_tensor(values):
            return torch.clamp(values, min=0.0)
        return np.maximum(np.asarray(values, dtype=np.float64), 0.0)
    if variable == RH_VAR:
        if _is_tensor(values):
            return torch.clamp(values, min=0.0, max=RH_PHYSICAL_MAX)
        return np.clip(np.asarray(values, dtype=np.float64), 0.0, RH_PHYSICAL_MAX)
    return values


def denormalize_targets(
    normalized: ArrayLike,
    target_cols: Sequence[str] = tuple(FINAL_TARGET_COLS),
    target_mean=None,
    target_std=None,
) -> ArrayLike:
    """
    Denormalisasi tensor/array ``[..., K]`` target sekaligus, dengan batas fisik.

    ``target_mean``/``target_std`` boleh skalar, sequence, ndarray, atau tensor
    (mis. ``stats["t_mean"]``). Presipitasi memakai ``expm1``; variabel lain
    inver linear. Tipe backend hasil mengikuti tipe ``normalized``.
    """
    columns = []
    for k, variable in enumerate(target_cols):
        mean = _scalar_param(target_mean, k, 0.0)
        std = _scalar_param(target_std, k, 1.0)
        column = normalized[..., k]
        if variable == PRECIP_VAR:
            columns.append(denormalize_precipitation(column, mean, std))
        else:
            columns.append(apply_physical_constraints(column * std + mean, variable))

    if _is_tensor(normalized):
        return torch.stack(columns, dim=-1)
    return np.stack(columns, axis=-1)


# ==============================================================================
# RAIN GATE (LAPISAN KEPUTUSAN)
# ==============================================================================

class RainGateMode(str, Enum):
    """Perlakuan rain gate terhadap objek yang dinilai."""

    OFF = "off"
    DECISION = "decision"  # default: gate hanya di keputusan event + point forecast
    HARD = "hard"          # legacy: nol-kan nilai; ensemble tetap tidak disentuh di sini


@dataclass(frozen=True)
class RainGateDecision:
    """Hasil evaluasi gate pada satu batch/jendela.

    Attributes:
        allow: ``[N]`` bool - True bila gate MENGIZINKAN event presipitasi.
        fired: ``[N]`` bool - True bila ``wet_probability < wet_threshold``.
        applied: gate benar-benar dipakai (False bila OFF atau guard aktif).
        degenerate: guard anti-kolaps aktif (seluruh wet_prob di bawah ambang).
        wet_threshold: ambang probabilitas basah yang dipakai.
    """

    allow: np.ndarray
    fired: np.ndarray
    applied: bool
    degenerate: bool
    wet_threshold: float

    @property
    def fired_fraction(self) -> float:
        """Fraksi jendela tempat gate aktif."""
        if self.fired.size == 0:
            return 0.0
        return float(np.mean(self.fired))

    def dry_precision(self, observations: np.ndarray, occurrence_mm: float) -> float:
        """
        Fraksi jendela ter-gate yang benar-benar kering (``obs <= occurrence_mm``).

        Ini adalah diagnosa langsung atas klaim "CSI digembungkan": nilai rendah
        berarti gate mematikan hujan pada jam-jam yang sebenarnya basah.
        """
        fired = self.fired
        if not fired.any():
            return float("nan")
        obs = np.asarray(observations, dtype=np.float64)
        return float(np.mean(obs[fired] <= occurrence_mm))


def compute_rain_gate(
    wet_probability,
    *,
    wet_threshold: float = DEFAULT_WET_PROBABILITY_THRESHOLD,
    mode: RainGateMode = RainGateMode.DECISION,
    degenerate_guard: bool = True,
) -> RainGateDecision:
    """
    Bangun keputusan gate dari ``wet_probability``.

    ``degenerate_guard`` mempertahankan perilaku FIX #5: bila seluruh jendela
    memiliki ``wet_prob < wet_threshold`` (head basah tidak terkalibrasi), gate
    DIMATIKAN dan dicatat, alih-alih mengosongkan semua presipitasi secara senyap.
    """
    n = int(np.asarray(wet_probability).reshape(-1).shape[0])
    if mode is RainGateMode.OFF:
        return RainGateDecision(
            allow=np.ones(n, dtype=bool),
            fired=np.zeros(n, dtype=bool),
            applied=False,
            degenerate=False,
            wet_threshold=float(wet_threshold),
        )

    wet = to_numpy(wet_probability).astype(np.float64).reshape(-1)
    fired = wet < float(wet_threshold)
    finite = np.isfinite(wet)

    if not finite.any():
        return RainGateDecision(
            allow=np.ones(n, dtype=bool),
            fired=fired,
            applied=False,
            degenerate=False,
            wet_threshold=float(wet_threshold),
        )

    if degenerate_guard and float(np.max(wet[finite])) < float(wet_threshold):
        return RainGateDecision(
            allow=np.ones(n, dtype=bool),
            fired=fired,
            applied=False,
            degenerate=True,
            wet_threshold=float(wet_threshold),
        )

    return RainGateDecision(
        allow=~fired,
        fired=fired,
        applied=True,
        degenerate=False,
        wet_threshold=float(wet_threshold),
    )


def apply_point_rain_gate(
    point_forecast,
    wet_probability,
    *,
    wet_threshold: float = DEFAULT_WET_PROBABILITY_THRESHOLD,
    threshold_precip_value: float = 0.0,
    mode: RainGateMode = RainGateMode.DECISION,
    degenerate_guard: bool = True,
) -> Tuple[np.ndarray, RainGateDecision]:
    """
    Terapkan gate pada point forecast (produk deterministik), bukan pada ensemble.

    Returns:
        ``(gated_point_copy, decision)``. Salinan selalu dibuat sehingga input
        tidak pernah termutasi.
    """
    point = to_numpy(point_forecast).astype(np.float64).copy()
    decision = compute_rain_gate(
        wet_probability,
        wet_threshold=wet_threshold,
        mode=mode,
        degenerate_guard=degenerate_guard,
    )
    if decision.applied:
        point = point.copy()
        point[decision.fired] = float(threshold_precip_value)
    return point, decision


def apply_ensemble_rain_gate(
    ensemble,
    wet_probability,
    *,
    wet_threshold: float = DEFAULT_WET_PROBABILITY_THRESHOLD,
    degenerate_guard: bool = True,
) -> Tuple[np.ndarray, RainGateDecision]:
    """
    Varian HARD legacy untuk perbandingan/reproduksi artefak lama.

    Ensemble dikembalikan sebagai SALINAN yang sudah di-nol-kan. Fungsi ini
    disediakan hanya untuk mereproduksi angka lama; jalur skoring normal memakai
    :func:`compute_rain_gate` dan tidak pernah memutasi ensemble.
    """
    ens = to_numpy(ensemble).astype(np.float64).copy()
    decision = compute_rain_gate(
        wet_probability,
        wet_threshold=wet_threshold,
        mode=RainGateMode.HARD,
        degenerate_guard=degenerate_guard,
    )
    if decision.applied:
        ens[decision.fired, :] = 0.0
    return ens, decision


# ==============================================================================
# KONTIJENSI + METRIK EVENT
# ==============================================================================

def _contingency_scores(hits: int, misses: int, false_alarms: int) -> Dict[str, float]:
    """POD/FAR/CSI dari tally kontijensi; NaN bila denominator nol."""
    pod = hits / (hits + misses) if (hits + misses) > 0 else float("nan")
    far = false_alarms / (hits + false_alarms) if (hits + false_alarms) > 0 else float("nan")
    denom = hits + misses + false_alarms
    csi = hits / denom if denom > 0 else float("nan")
    return {"pod": float(pod), "far": float(far), "csi": float(csi)}


def event_metrics_from_masks(pred_event: np.ndarray, obs_event: np.ndarray) -> Dict[str, float]:
    """POD/FAR/CSI dari dua masker boolean yang sudah sejajar."""
    pred_event = np.asarray(pred_event, dtype=bool)
    obs_event = np.asarray(obs_event, dtype=bool)
    hits = int(np.sum(pred_event & obs_event))
    false_alarms = int(np.sum(pred_event & ~obs_event))
    misses = int(np.sum(~pred_event & obs_event))
    return _contingency_scores(hits, misses, false_alarms)


def event_metrics_from_ensemble(
    ensemble,
    observations,
    *,
    threshold: float,
    prob_threshold: float = PROB_EVENT_THRESHOLD,
    allow_mask: Optional[np.ndarray] = None,
) -> Dict[str, float]:
    """
    POD/FAR/CSI probabilistik: event diprediksi bila fraksi ensemble > threshold
    mencapai ``prob_threshold``. Observasi NaN dilewati (bukan dianggap kering).

    ``allow_mask`` adalah keputusan rain gate: False menekan event pada jendela itu
    tanpa mengubah nilai ensemble.
    """
    ens = to_numpy(ensemble).astype(np.float64)
    obs = to_numpy(observations).astype(np.float64).reshape(-1)
    valid = ~np.isnan(obs)
    if not valid.any():
        return {"pod": float("nan"), "far": float("nan"), "csi": float("nan")}

    allow = np.asarray(allow_mask, dtype=bool) if allow_mask is not None else None
    # PDF 3.8.4: if no window passes the gate, do not apply it at all.
    if allow is not None and not allow.any():
        allow = None

    with np.errstate(invalid="ignore"):
        prob = np.mean(ens[valid] > threshold, axis=1)
    pred_event = prob >= prob_threshold
    if allow is not None:
        pred_event &= allow[valid]  # suppression counts as a miss, not a dropped row
    obs_event = obs[valid] > threshold
    return event_metrics_from_masks(pred_event, obs_event)


def event_metrics_from_point(
    point_forecast,
    observations,
    *,
    threshold: float,
) -> Dict[str, float]:
    """
    POD/FAR/CSI deterministik: event bila ``point_forecast >= threshold``.

    Dipakai untuk crosscheck point-based (``eval_rain_robust.py``). Observasi NaN
    dilewati.
    """
    pred = to_numpy(point_forecast).astype(np.float64).reshape(-1)
    obs = to_numpy(observations).astype(np.float64).reshape(-1)
    valid = ~(np.isnan(obs) | np.isnan(pred))
    if not valid.any():
        return {"pod": float("nan"), "far": float("nan"), "csi": float("nan")}
    return event_metrics_from_masks(pred[valid] >= threshold, obs[valid] >= threshold)


# ==============================================================================
# SKORING PER VARIABEL
# ==============================================================================

def _as_ensemble(ensemble, name: str = "ensemble") -> np.ndarray:
    ens = to_numpy(ensemble).astype(np.float64)
    if ens.ndim == 1:
        ens = ens[:, None]
    if ens.ndim != 2:
        raise ValueError(f"{name} harus 1D [N] atau 2D [N, M]; dapat {ens.shape}")
    if ens.shape[1] < 1:
        raise ValueError(f"{name} harus punya minimal 1 anggota: {ens.shape}")
    return ens


def _as_observations(observations, n_expected: int) -> np.ndarray:
    obs = to_numpy(observations).astype(np.float64).reshape(-1)
    if obs.shape[0] != n_expected:
        raise ValueError(
            f"Panjang observasi ({obs.shape[0]}) != jumlah baris ensemble ({n_expected})"
        )
    return obs


def score_variable(
    ensemble,
    observations,
    *,
    variable: str,
    thresholds: Optional[Sequence[float]] = None,
    prob_threshold: float = PROB_EVENT_THRESHOLD,
    point_forecast=None,
    wet_probability=None,
    wet_threshold: float = DEFAULT_WET_PROBABILITY_THRESHOLD,
    occurrence_threshold_mm: float = DEFAULT_RAIN_OCCURRENCE_MM,
    gate_mode: RainGateMode = RainGateMode.DECISION,
    degenerate_guard: bool = True,
) -> Dict[str, float]:
    """
    Hitung seluruh metrik satu variabel dari satu ensemble.

    Args:
        ensemble: ``[N, M]`` nilai fisik (sudah didenormalisasi), bukan z-space.
        observations: ``[N]`` nilai aktual dalam satuan yang sama.
        variable: nama variabel (``precipitation`` mengaktifkan metrik event).
        thresholds: ambang mm untuk Brier/POD/FAR/CSI. Bila ``None`` dan variabel
            adalah presipitasi, dipakai ``DEFAULT_EVENT_THRESHOLDS``.
        prob_threshold: ambang probabilitas ensemble untuk mendeklarasikan event.
        point_forecast: ``[N]`` prediksi deterministik; default median ensemble.
        wet_probability: ``[N]`` output head basah/kering; mengaktifkan gate.
        wet_threshold: ambang gate.
        occurrence_threshold_mm: ambang "hari basah" untuk diagnosa gate.
        gate_mode: ``DECISION`` (default), ``OFF``, atau ``HARD`` legacy.
        degenerate_guard: matikan gate bila seluruh ``wet_probability`` di bawah ambang.

    Returns:
        Dict metrik siap-JSON. Kunci utama (``rmse``/``mae``/``correlation``/``crps``)
        SELALU dihitung dari ensemble mentah; ``crps``/``brier`` tidak pernah
        terpengaruh gate. Bila gate aktif, ditambahkan ``*_gated`` (point forecast
        ter-gate) dan ``*_ungated`` (event tanpa gate) sebagai diagnosa.
    """
    ens = _as_ensemble(ensemble)
    obs = _as_observations(observations, ens.shape[0])
    n = ens.shape[0]

    if thresholds is None:
        thresholds = DEFAULT_EVENT_THRESHOLDS if variable == PRECIP_VAR else ()

    point = (
        to_numpy(point_forecast).astype(np.float64).reshape(-1)
        if point_forecast is not None
        else np.median(ens, axis=1)
    )
    if point.shape[0] != n:
        raise ValueError(
            f"Panjang point_forecast ({point.shape[0]}) != jumlah baris ensemble ({n})"
        )

    # --- Metrik dasar: ensemble mentah, tidak pernah di-gate. ---
    result: Dict[str, float] = {
        "rmse": compute_rmse(point, obs),
        "mae": compute_mae(point, obs),
        "correlation": compute_correlation(point, obs),
        "crps": compute_crps(ens, obs),
    }

    if not thresholds:
        return result

    # --- Gate: hanya menyentuh lapisan keputusan dan point forecast. ---
    decision: Optional[RainGateDecision] = None
    if variable == PRECIP_VAR and wet_probability is not None and gate_mode is not RainGateMode.OFF:
        decision = compute_rain_gate(
            wet_probability,
            wet_threshold=wet_threshold,
            mode=gate_mode,
            degenerate_guard=degenerate_guard,
        )
    allow_mask = decision.allow if (decision is not None and decision.applied) else None

    for thr in thresholds:
        key = _threshold_key(thr)
        # Brier selalu dari ensemble mentah: skor kalibrasi, bukan skor keputusan.
        result[f"brier_{key}"] = compute_brier_score(ens, obs, threshold=thr)

        gated = event_metrics_from_ensemble(
            ens, obs, threshold=thr, prob_threshold=prob_threshold, allow_mask=allow_mask
        )
        result[f"pod_{key}"] = gated["pod"]
        result[f"far_{key}"] = gated["far"]
        result[f"csi_{key}"] = gated["csi"]

        if allow_mask is not None:
            ungated = event_metrics_from_ensemble(
                ens, obs, threshold=thr, prob_threshold=prob_threshold
            )
            result[f"pod_{key}_ungated"] = ungated["pod"]
            result[f"far_{key}_ungated"] = ungated["far"]
            result[f"csi_{key}_ungated"] = ungated["csi"]

    if decision is not None and decision.applied:
        gated_point = point.copy()
        gated_point[decision.fired] = 0.0
        result["rmse_gated"] = compute_rmse(gated_point, obs)
        result["mae_gated"] = compute_mae(gated_point, obs)
        result["correlation_gated"] = compute_correlation(gated_point, obs)
        result["gate_fired_fraction"] = decision.fired_fraction
        result["gate_dry_precision"] = decision.dry_precision(obs, occurrence_threshold_mm)
        result["gate_applied"] = 1.0
    elif decision is not None:
        result["gate_applied"] = 0.0
    if decision is not None:
        result["gate_degenerate"] = 1.0 if decision.degenerate else 0.0
        result["gate_wet_threshold"] = float(decision.wet_threshold)

    return result


def score_scenario(
    targets,
    ensemble,
    *,
    target_cols: Sequence[str] = tuple(FINAL_TARGET_COLS),
    thresholds: Optional[Sequence[float]] = None,
    prob_threshold: float = PROB_EVENT_THRESHOLD,
    point_forecast=None,
    wet_probability=None,
    wet_threshold: float = DEFAULT_WET_PROBABILITY_THRESHOLD,
    gate_mode: RainGateMode = RainGateMode.DECISION,
    degenerate_guard: bool = True,
) -> Dict[str, Dict[str, float]]:
    """
    Skor satu skenario penuh (semua variabel target).

    Ini adalah pengganti langsung ``compute_scenario_metrics`` di
    ``run_eval_final.py`` dan setara untuk CSDI (CSDI cukup tidak mengirim
    ``wet_probability``).

    Args:
        targets: ``[N, K]`` observasi fisik, urut sesuai ``target_cols``.
        ensemble: ``[N, M, K]`` sampel fisik.
        point_forecast: ``[N, K]`` opsional; default median tiap variabel.
        wet_probability: ``[N]`` opsional (hanya relevan untuk presipitasi).
        thresholds: override ambang event; default 2/5/10 mm untuk presipitasi.

    Returns:
        ``{nama_variabel: {nama_metrik: nilai}}``.
    """
    target_arr = to_numpy(targets).astype(np.float64)
    ensemble_arr = to_numpy(ensemble).astype(np.float64)
    if ensemble_arr.ndim != 3:
        raise ValueError(f"ensemble skenario harus [N, M, K]; dapat {ensemble_arr.shape}")
    if ensemble_arr.shape[0] != target_arr.shape[0]:
        raise ValueError(
            f"Jumlah baris ensemble ({ensemble_arr.shape[0]}) != target ({target_arr.shape[0]})"
        )
    if ensemble_arr.shape[2] != len(target_cols):
        raise ValueError(
            f"Dimensi variabel ensemble ({ensemble_arr.shape[2]}) != jumlah target_cols "
            f"({len(target_cols)})"
        )

    point_arr = to_numpy(point_forecast).astype(np.float64) if point_forecast is not None else None
    results: Dict[str, Dict[str, float]] = {}
    for k, variable in enumerate(target_cols):
        per_thresholds = thresholds
        if per_thresholds is None:
            per_thresholds = DEFAULT_EVENT_THRESHOLDS if variable == PRECIP_VAR else ()
        results[variable] = score_variable(
            ensemble_arr[:, :, k],
            target_arr[:, k],
            variable=variable,
            thresholds=per_thresholds,
            prob_threshold=prob_threshold,
            point_forecast=None if point_arr is None else point_arr[:, k],
            wet_probability=wet_probability if variable == PRECIP_VAR else None,
            wet_threshold=wet_threshold,
            gate_mode=gate_mode,
            degenerate_guard=degenerate_guard,
        )
    return results


__all__ = [
    "RainGateMode",
    "RainGateDecision",
    "PRECIP_VAR",
    "WIND_VAR",
    "RH_VAR",
    "DEFAULT_EVENT_THRESHOLDS",
    "DEFAULT_WET_PROBABILITY_THRESHOLD",
    "DEFAULT_RAIN_OCCURRENCE_MM",
    "to_numpy",
    "denormalize_precipitation",
    "apply_physical_constraints",
    "denormalize_targets",
    "compute_rain_gate",
    "apply_point_rain_gate",
    "apply_ensemble_rain_gate",
    "event_metrics_from_masks",
    "event_metrics_from_ensemble",
    "event_metrics_from_point",
    "score_variable",
    "score_scenario",
]
