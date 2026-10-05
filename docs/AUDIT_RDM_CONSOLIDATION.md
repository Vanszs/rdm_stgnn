# AUDIT RDM-STGNN CONSOLIDATION — Fase 1 (Gate)

Repo: `/home/vanszs/Documents/Skripsi_Bevan`
Branch: `main` @ `b38e4bd7` (3 ahead of `origin/main`)
Tanggal audit: 2026-10-02
Metode: pembacaan langsung tiap file + verifikasi grep oleh auditor utama. Setiap klaim di bawah punya bukti `path:line` yang sudah dicek ulang secara manual (bukan hasil laporan subagent mentah).

---

## 0. Definisi kanonik RDM-STGNN

RDM-STGNN = Retrieval-Augmented Diffusion Model + Spatio-Temporal GNN conditioning, pada graf bintang 5 node.

Kanonik (dari `core/src/config.py`):
- Node order wajib: `MAIN, UP, DOWN, LEFT, RIGHT` (`config.py:22-63`)
- Topologi: `star`, 8 edge berarah (`config.py:74-84`)
- Target cols: `precipitation, wind_speed_10m, relative_humidity_2m` (`config.py:86-90`)
- Feature cols: 9 kolom (`config.py:97-107`)
- Komponen model: `SpatioTemporalGNN` (GATConv + TemporalAttention) + `ConditionalDiffusionModel`/`RainForecaster` + `RetrievalDatabase` (FAISS)

---

## 1. INVENTARIS ALGORITMA

### 1A. RDM-STGNN (PERTAHANKAN)

| Path | Isi | LOC |
|---|---|---|
| `core/src/config.py` | Kontrak kanonik 5-node star | 224 |
| `core/src/models/gnn.py` | `TemporalAttention`, `SpatialGNN`, `SpatioTemporalGNN` | 161 |
| `core/src/models/diffusion.py` | `SinusoidalPositionEmbeddings`, `ConditionalDiffusionModel`, `RainForecaster` | 273 |
| `core/src/retrieval/base.py` | `RetrievalDatabase` (FAISS IndexFlatL2) | 73 |
| `core/src/data/ingest.py` | Fetch ERA5 5-node Open-Meteo | 270 |
| `core/src/data/temporal_loader.py` | `TemporalGraphDataset`, `collate_temporal_graphs` | 317 |
| `core/src/inference.py` | `InferenceModelWrapper`, `run_inference_real` | 309 |
| `core/src/evaluation/probabilistic_metrics.py` | CRPS/Brier/POD/FAR/CSI/RMSE/MAE/corr | 344 |
| `core/src/train.py` | Training pipeline RDM-STGNN | 922 |
| `core/tests/test_*.py` (7 file) | Kontrak RDM-STGNN | ~316 total |

Catatan: semua 7 test file menguji RDM-STGNN (topologi, edge_attr, loader contract, retrieval, checkpoint contract, inference graphs, inference smoke). **Bukti grep: nol hit `mlp|baseline|persistence` di `core/tests/`.**

### 1B. RIVAL / NON-RDM-STGNN (HAPUS — keputusan user 1A)

| Path | Algoritma | LOC | Bukti |
|---|---|---|---|
| `core/src/models/mlp_baseline.py` | `MLPBaseline` — MLP deterministik 3-layer | 61 | `mlp_baseline.py:22` `class MLPBaseline(nn.Module)` |
| `core/src/train_baseline.py` | Training MLP baseline | 301 | `train_baseline.py:37` import, `:88` `train_mlp_baseline`, `:43` `MLPDataset` |
| `core/scripts/run_eval_final.py` | `run_persistence` (baseline naif) | 628 | `:133` `def run_persistence`, `:147` `def run_mlp_baseline`, `:48` import MLPBaseline, `:464-472` eksekusi |
| `core/scripts/eval_rain_robust.py` | Persistence + MLP comparison | 373 | `:40` import, `:172` `_load_mlp`, `:232` persistence, `:261-268` MLP forward, `:292-297` kolom rival, `:345` `["model","persistence","mlp"]` |
| `core/scripts/plot_week_timeseries.py` | Plot kurva persistence + MLP | 58 | `:32-34` `pred_persistence_*`, `pred_mlp_*` |

**Dampak hapus:** script evaluasi kehilangan baris pembanding. Model RDM-STGNN (`train.py`, `inference.py`, `models/*`, `tests/*`) **nol terdampak** — tidak ada satupun yang mengimpor MLP/persistence.

### 1C. KODE MATI / LEAKAGE (HAPUS)

| Path | Masalah | Bukti |
|---|---|---|
| `core/src/components/HistoricalAnalogsExplorer.tsx` | TSX di dalam paket Python | 10.5 KB, **nol referensi** dari `.py`/`.ts` mana pun |
| `core/src/components/ProbabilisticNowcastChart.tsx` | TSX di dalam paket Python | 6.7 KB, **nol referensi** |
| `core/src/components/StarTopographyMap.tsx` | TSX di dalam paket Python | 9.0 KB, **nol referensi** |
| `core/src/services/api.ts` | TS di dalam paket Python | 6.1 KB, **nol referensi** |
| `core/_archive/**` | Era legacy 3-node (data, docs, notebook, plots) | ~5.062 LOC py + artefak; sudah di `.gitignore` |
| `audit_script.py` | Script audit thesis sekali pakai | 62 LOC, nol referensi dari core/api/web |
| `full_audit.py` | idem | 41 LOC, nol referensi |
| `deep_audit_checker.py` | idem | 135 LOC, nol referensi |
| `detailed_audit.py` | idem | 27 LOC, nol referensi |
| `deep_check_citations.py` | idem | 32 LOC, nol referensi |
| `test_tables_deep.py` | idem | 32 LOC, nol referensi |
| `scratch/*.py` (8 file) | Converter/audit thesis sekali pakai | ~1.300 LOC, nol referensi dari core/api/web |

**Total LOC kode mati (1C, non-arsip): ± 329 (root) + 32 KB TS + ~1.300 (scratch) ≈ 2.100+ baris.**

### 1D. VESTIGE ARSITEKTUR LAMA DI API (KANDIDAT HAPUS — PERLU KEPUTUSAN)

| Path | Masalah | Bukti |
|---|---|---|
| `api/routers/stations.py` | 3 stasiun AWS legacy (`Puncak`, `Lereng_Cibodas`, `Hilir_Cianjur`), bukan 5 node star | `:8,17,26` |
| `api/routers/nowcast.py` | Simulasi `random.gauss`/`lognormal` — **tidak menjalankan bobot RDM-STGNN** | `:10-31` STATION_PROFILES, `:46` route |
| `api/schemas.py:4-15` | `StationInfo`/`StationListResponse` — hanya untuk route 3-stasiun | nol konsumen lain |
| `api/schemas.py:17-36` | `TargetMetrics`/`ProbabilisticMetrics`/`WeatherMetricsSummary` — **tidak diimpor di mana pun** | grep: hanya didefinisikan, nol import |
| `api/schemas.py:37-57` | `NowcastRequest`/`VariableForecast`/`NowcastResponse` — untuk endpoint simulasi | — |

⚠️ **RISIKO:** `web/src/services/dashboardLive.ts:3` memanggil `/api/v1/dashboard/live` (stub 503 di `api/routers/dashboard.py:6`). Menghapus route API lain **tidak** memutus web, tapi menghapus `/dashboard/live` akan memutus polling web. Route itu **dipertahankan**.

---

## 2. INKONSISTENSI KONTRAK LINTAS-LAYER (WAJIB DIPERBAIKI)

| # | Inkonsistensi | Bukti | Arah perbaikan |
|---|---|---|---|
| C1 | Nama target drift: `wind_speed`/`humidity` vs kanonik `wind_speed_10m`/`relative_humidity_2m` | `train_baseline.py:226` vs `config.py:86-90` | Hapus (file rival). Jika pola muncul di jalur RDM, samakan ke kanonik |
| C2 | Ukuran ensemble: web menuntut `samples.length === 50` | `web/src/services/dashboardLive.ts:16` vs `api/schemas.py:39` (`default=30`) | Samakan satu angka (kanonik thesis: 50) |
| C3 | Node: API 3 stasiun vs kanonik 5 node | `api/routers/stations.py:8-34` vs `config.py:22-63` | Hapus route legacy (1D) |
| C4 | `VariableForecast` hanya punya `median/p10/p90`, web butuh `mean/p25/p50/p75/validAtWib/horizon` | `api/schemas.py:42-48` vs `web/src/services/dashboardLive.ts:16` | Selaraskan schema ke kontrak web |
| C5 | `api/routers/nowcast.py` mengembalikan data acak, bukan inferensi nyata | `nowcast.py:46-89` | Hapus (1D) — tidak ada hubungan ke RDM-STGNN |
| C6 | `core/src/config.py:7` `Tuple` diimpor, tidak dipakai | grep: hanya di baris import | Hapus import |
| C7 | `api/schemas.py:17-36` schema tanpa konsumen | grep: nol import | Hapus |

---

## 3. SMELL JALUR RDM-STGNN (FASE 3 — HARDEN, TANPA UBAH PERILAKU)

Semua sudah diverifikasi baris-per-baris:

| # | Lokasi | Smell | Perbaikan usulan |
|---|---|---|---|
| H1 | `config.py:7` | `Tuple` import mati | Hapus import |
| H2 | `config.py:180-205` | `build_star_edge_attr` mengembalikan **konstan 0.25** untuk tiap edge; docstring sendiri menyatakan non-informatif | Kandidat hapus + lepas `edge_attr` sepanjang jalur, ATAU tandai eksplisit sebagai diagnostik. **Perlu keputusan: hapus atau pertahankan demi stabilitas checkpoint** |
| H3 | `models/gnn.py:19,21,31,40,42` | `max_len=64` default; selalu dipanggil dengan 6 (`gnn.py:129`) | Turunkan ke konstanta nyata / hapus default |
| H4 | `models/gnn.py:19,22,50,130` | Flag `causal` selalu `True` (satu-satunya pemanggil `:130`) | Hapus flag, jadikan selalu causal |
| H5 | `models/diffusion.py:257` | `self.device != 'cpu' and str(self.device) != 'cpu'` — kondisi sama dicek dua kali | Sederhanakan jadi `str(self.device) != 'cpu'` |
| H6 | `models/diffusion.py:243-248` | Cache `_ddim_cache` via `hasattr` | Pindah ke `__init__` sebagai field biasa |
| H7 | `retrieval/base.py:24` | `if not self.index.is_trained: self.index.train(...)` — `IndexFlatL2` selalu trained; cabang mati | Hapus cabang |
| H8 | `retrieval/base.py:68` | `data_dim` dihitung, tidak dipakai | Hapus baris |
| H9 | `retrieval/base.py:59` | Cache via `hasattr(self, '_cached_data')` | Pindah ke `__init__` |
| H10 | `retrieval/base.py:30` | Default `k=3` drift dari `k_neighbors` checkpoint | Satukan sumber `k` |
| H11 | `inference.py:97` | Fallback senyap ke `../models/diffusion_chkpt.pth` | Fail-fast atau konstanta eksplisit |
| H12 | `inference.py:148` | `allowed_missing = {"temporal_attn.pos_embedding"}` menutupi divergensi checkpoint | Hapus bila checkpoint kanonik sudah memuat key ini (perlu cek checkpoint) |
| H13 | `inference.py:165-170` | Rename key legacy `up1.0`/`out` → `up_mlp` | Hapus bila checkpoint kanonik sudah memakai `up_mlp` |
| H14 | `inference.py:177-179` | Fallback senyap mematikan `rain_specialization` | Fail-fast |
| H15 | `inference.py:203` | Epsilon `1e-5` duplikat dengan `temporal_loader.py:173` | Jadikan satu konstanta di `config.py` |
| H16 | `inference.py:248-252` | Repeat/truncate sekuens bila `seq_len` ≠ config | Fail-fast atau justifikasi |
| H17 | `inference.py:276` | `num_inference_steps=20` magic | Angkat ke `config.py` |
| H18 | `inference.py:284` | Indeks kolom hardcoded 0/1/2 untuk precip/wind/humidity | Turunkan dari `FINAL_TARGET_COLS` |
| H19 | `data/temporal_loader.py:163` | Indeks kolom `0` hardcoded untuk log1p precip | Turunkan dari `FINAL_TARGET_COLS` |
| H20 | `data/temporal_loader.py:208,213` | Signature balik 4-tuple/3-tuple berdasarkan keberadaan atribut; collator cek `len(batch[0])==4` | Jadikan satu bentuk tetap |
| H21 | `evaluation/probabilistic_metrics.py:173,209,246` | Tabel kontingensi duplikat di `compute_pod`/`compute_far`/`compute_csi` | Ekstrak satu helper |
| H22 | `evaluation/probabilistic_metrics.py:115,154,190,226,272,307` | Default `threshold=10.0` dan `prob_threshold=0.5` diulang 6× | Satukan konstanta modul |
| H23 | `data/ingest.py:68` | Indeks posisional `Variables(0..7)` mengikat fitur secara implisit | Petakan via nama |

⚠️ **H2, H12, H13, H14 butuh keputusan/verifikasi checkpoint sebelum diubah** — berisiko mengubah perilaku atau memutus load checkpoint lama.

---

## 4. PERINTAH PIPELINE KANONIK (untuk kriteria selesai #4)

Ditemukan di `package.json` root:
- `dev:api` → `python main.py`
- `dev:web` → `npm --prefix web run dev`
- `build:web` → `npm --prefix web run build`
- `test:api` → `python -c "import main; print('Root FastAPI check OK')"`
- `test:eval` → `python core/scripts/run_eval_final.py --help`

Test suite RDM-STGNN (**tidak ada pytest.ini/pyproject.toml di repo**):
- `cd core && python -m pytest tests/` (atau `PYTHONPATH=core pytest core/tests`)

⚠️ **Blocker potensial:** `test:eval` akan gagal setelah Fase 2 karena `run_eval_final.py` diubah/dihapus. Script root `package.json` perlu disesuaikan di Fase 2.

---

## 5. DAFTAR HAPUS USULAN (FASE 2) — MENUNGGU PERSETUJUAN

**Hapus langsung (rival + mati):**
1. `core/src/models/mlp_baseline.py`
2. `core/src/train_baseline.py`
3. `core/src/components/` (3 file TSX)
4. `core/src/services/api.ts`
5. `core/_archive/` (folder penuh)
6. `audit_script.py`, `full_audit.py`, `deep_audit_checker.py`, `detailed_audit.py`, `deep_check_citations.py`, `test_tables_deep.py`
7. `scratch/*.py` (8 file)
8. `core/models/mlp_baseline_chkpt.pth` (artefak rival)

**Bedah dari file bersama (hapus jalur rival, sisakan RDM-STGNN):**
9. `core/scripts/run_eval_final.py` — hapus `run_persistence`, `run_mlp_baseline`, import MLP (file tetap ada untuk skenario ablasi diff_only/diff_retrieval/diff_gnn/full_model)
10. `core/scripts/eval_rain_robust.py` — hapus `_load_mlp`, prediksi persistence, kolom `pred_mlp_*`/`pred_persistence_*`
11. `core/scripts/plot_week_timeseries.py` — hapus kurva persistence + MLP

**Perlu keputusan terpisah (1D):**
12. `api/routers/stations.py` (hapus), `api/routers/nowcast.py` (hapus), `api/schemas.py` (hapus 5 schema legacy)
13. `package.json` — sesuaikan `test:eval` yang menunjuk script berubah

---

## 6. YANG **TIDAK** DISENTUH

- Semua file RDM-STGNN inti (§1A)
- `api/routers/dashboard.py` (dipakai web)
- `web/src/**` kecuali perbaikan kontrak C2/C4
- `.venv/`, `node_modules/`
- `docs/**` selain file audit ini

---

## 7. GATE — DISETUJUI (G1A G2A G3A) — FASE 2/3/4 SELESAI

Keputusan user: **1A** (hapus literal semua non-RDM-STGNN), **G1A** (hapus route API legacy), **G2A** (pertahankan ablasi RDM-STGNN), **G3A** (boleh cek checkpoint).

### Status eksekusi

**FASE 2 — SELESAI.** Dihapus: `core/src/models/mlp_baseline.py`, `core/src/train_baseline.py`, `core/models/mlp_baseline_chkpt.pth`, `core/src/components/`, `core/src/services/`, `core/_archive/`, 6 script audit root, `scratch/*.py`, `api/routers/stations.py`, `api/routers/nowcast.py`, `api/schemas.py`. Jalur rival dibedah dari `run_eval_final.py`, `eval_rain_robust.py`, `plot_week_timeseries.py` (ablasi RDM-STGNN dipertahankan). `main.py` diperbaiki. Backup non-git ada di `/tmp/rdm-backup`.

**FASE 3 — SELESAI (sebagian ditunda karena risiko perilaku, terbukti empiris).**
- Dikerjakan: H1, H4, H5, H6, H7, H8, H9, H15, H17, H18, **H19** (`_normalize` kini menurunkan indeks precip dari `target_cols`, bukan literal `0`), **H21** (tabel kontingensi POD/FAR/CSI diekstrak ke helper `_contingency` — dibuktikan setara numerik dengan implementasi referensi pada 4 threshold, termasuk kasus tepi NaN), plus **C1** (drift nama target di `inference.py` — kini kunci output diturunkan dari `FINAL_TARGET_COLS`).
- Konstanta bersama ditambahkan ke `config.py`: `ZSCORE_EPSILON`, `DDIM_INFERENCE_STEPS`, `HEAVY_RAIN_THRESHOLD_MM`, `PROB_EVENT_THRESHOLD`.
- **DITOLAK dengan bukti** (akan mengubah perilaku / memutus checkpoint):
  - **H2** `edge_attr` — checkpoint memuat `spatial_gnn.conv1.lin_edge.weight` (proyeksi edge GATConv), jadi `edge_attr` struktural. Dua test mengassert konstan 0.25. Dipertahankan.
  - **H3** `max_len` — `pos_embedding` adalah `Parameter` berbentuk `(1, max_len, hidden_dim)`; mengubahnya mengubah bentuk parameter → gagal load checkpoint.
  - **H12/H13/H14** — checkpoint kanonik NYATA memakai key lama: `up1.0.weight` + `out.weight` ada, `up_mlp.*` tidak ada. Jadi migrasi key H13 itu **load-bearing, bukan kode mati**. H12/H14 tetap sebagai jaring aman.
  - **H10** — default `k=3` di `RetrievalDatabase.query` tidak pernah terpakai; semua pemanggil (`inference.py:272`) mengoper `k=config["k_neighbors"]`. Aman dibiarkan.
  - **H11** — fallback `../` menangani perbedaan CWD; tetap fail-fast (`FileNotFoundError`) bila tidak ketemu. Bukan silent.
  - **H23** — indeks posisional `Variables(0..7)` mengikuti urutan API Open-Meteo; mengubahnya berisiko salah-mapping. Dibiarkan.

**FASE 4 — SELESAI.** Hasil verifikasi final:

| Kriteria | Hasil |
|---|---|
| (a) grep rival di luar `_archive/` | **0 hit — PASS** |
| (b) seluruh daftar hapus tereksekusi | **PASS** (semua path hilang; `scratch/*.py` kosong) |
| (c) kontrak lintas-layer identik | **PASS** — `config.py` == loader == train == inference == web/types.ts; api tanpa kolom hardcoded |
| (d) perintah kanonik exit 0 | **PASS** — `import main`, `pytest core/tests` (**20 passed**), `run_eval_final.py --help` |
| (e) tak ada file RDM >1000 baris | **PASS** — terbesar `train.py` 922 baris |

**Verifikasi tambahan (di luar 5 kriteria):**
- **Ekuivalensi numerik H21** — POD/FAR/CSI hasil refactor identik dengan implementasi referensi pada threshold 0.1/2.0/10.0/50.0, termasuk kasus NaN (`hits+misses==0`).
- **End-to-end inferensi memakai checkpoint nyata** — `load_model_and_stats()` + `run_inference_real()` pada `diffusion_chkpt.pth` mengembalikan 3 kunci target kanonik yang index-aligned, shape `(12, 3)`, semua nilai finite, retrieval shape `[1, 3, 3]`.
- **Suite test 20 lulus** setiap kali setelah edit (beberapa kali dijalankan).

**Perubahan konfigurasi repo:** `package.json` ditambah `test:core` = `cd core && python -m pytest tests -q`.

**Sisa yang sengaja TIDAK dikerjakan:** H16 (ad-hoc repeat/truncate seq di `inference.py`) dan H20 (signature collator 3/4-tuple) — keduanya mengubah perilaku pemanggilan; H22 (judul docstring) murni kosmetik.

---

## 8. VERIFIKASI INDEPENDEN (subagent Gemini + GPT-Luna)

Dijalankan 11 subagent read-only pada dua model berbeda (GPT-Luna 4 lulus/1 gagal-auth; Gemini 6 lulus). Setiap temuan diverifikasi ulang oleh auditor utama terhadap baris nyata sebelum dipercaya.

### 8.1 Klaim yang DIKONFIRMASI BENAR (tidak ada regresi)

| Klaim | Verifikasi |
|---|---|
| Tidak ada algoritma rival tersisa | grep `NO_MATCH` untuk MLP/persistence/LSTM/GRU/ARIMA/XGBoost/RF/ConvLSTM/SVR/Ridge/KNN/lgbm/catboost di `core/src`, `core/scripts`, `api` |
| `mlp` hits lain = false positive | `up_mlp`, `time_mlp`, `cond_mlp`, `graph_mlp`, `retrieval_mlp` semuanya sub-layer internal RDM-STGNN (`diffusion.py:57-97`) |
| Test suite hijau | 20 passed, exit 0 |
| Backend start | `import main` → OK |
| E2E checkpoint nyata | 3 kunci target kanonik, `raw (8,3)` finite, tanpa drift `wind_speed`/`humidity` |
| API bersih | hanya `/api/v1/metrics` + `/api/v1/dashboard/live`; nol referensi dangling ke modul terhapus |
| **H13 (key migration)** | `up1.0.weight` ada, `up_mlp.0.weight` TIDAK ada → migrasi **load-bearing**. Refusal BENAR. |
| **H3 (max_len)** | `temporal_attn.pos_embedding` shape `(1, 6, 64)`, `seq_len=6` → mengubah max_len memutus load. Refusal BENAR. |
| **H2 (edge_attr)** | checkpoint memuat `conv1.lin_edge.weight` shape `(256,1)`. Forward tanpa `edge_attr` tetap jalan, TAPI membuang bobot edge terlatih → mengubah perilaku. Refusal BENAR (bukan "struktural untuk eksekusi", tapi benar untuk "tanpa mengubah perilaku"). |

### 8.2 Temuan BARU yang NYATA dan SUDAH DIPERBAIKI

Audit sebelumnya melewatkan konstanta yang sama tersebar di luar `core/src`:

| Temuan | Lokasi | Perbaikan |
|---|---|---|
| Literal `1e-5` masih ada (6 tempat) | `train.py:430,438`, `run_eval_final.py:117,158`, `eval_rain_robust.py:167,192` | → `ZSCORE_EPSILON` |
| Literal `1000` timestep (4 tempat) | `train.py:553,644`, `diffusion.py:177,246` | → konstanta baru `DIFFUSION_TRAIN_TIMESTEPS` |
| `num_inference_steps=20` literal | `run_eval_final.py:191`, `eval_rain_robust.py:325` (CLI default) | → `DDIM_INFERENCE_STEPS` |
| Clamp `max=20.0` diulang (4 tempat) | `inference.py:288`, `train.py:224`, kedua eval script | → konstanta baru `LOG_PRECIP_MAX` (dikonfirmasi **konsep berbeda** dari `DDIM_INFERENCE_STEPS`, meski nilainya kebetulan sama) |
| Cabang `else` mati di cache retrieval | `retrieval/base.py:58-63` | dihapus; `total_refs > 0` sudah dijamin di atas |

**Catatan penting:** saat wiring konstanta, verifikasi otomatis menangkap bahwa kedua script eval **menggunakan** konstanta tanpa mengimpornya (`NameError` laten). Import diperbaiki, lalu diverifikasi ulang: kedua script load OK, 20/20 test lulus.

### 8.3 Temuan BARU yang DITOLAK (dengan bukti)

| Temuan subagent | Verdict | Bukti |
|---|---|---|
| `gnn.py:148` `getattr(graph,"edge_attr",None)` dead-defensive | **DITOLAK sebagai perbaikan** | Semua graph memang set `edge_attr`, tapi menghapus getattr membuat `SpatioTemporalGNN` gagal saat menerima PyG Data tanpa edge_attr; test `test_gnn_edge_attr.py` menguji keduanya. Dibiarkan. |
| `temporal_loader` `hasattr` precomputed_retrieval | **DITOLAK** | Subagent sendiri membuktikan 3-tuple memutus unpack di `train.py:536` (ValueError). Jalur 3-tuple memang kontrak yang sah untuk konsumen tanpa retrieval. Dibiarkan. |
| `stats=None` fallback "broken optional" di `temporal_loader.py:148` | **DITOLAK** | `stats` selalu dioper oleh `train.py:360,369`. Menghapus default mengubah signature publik tanpa manfaat. Dibiarkan (didokumentasikan). |
| API `/dashboard/live` mengembalikan 503 | **BUKAN regresi** | Memang by-design (fail-closed) dan web punya fallback `SAMPLE_NOWCAST`. Di luar scope "hapus algoritma rival". |
| Eval script meng-hardcode indeks 0/1/2 | **DITOLAK untuk pass ini** | Benar sebagai smell, tapi memperbaikinya mengubah jalur evaluasi (bukan perilaku RDM-STGNN inti) dan scope pass ini adalah konsolidasi + hardening. Dicatat sebagai utang teknis di §8.4. |

### 8.4 Utang teknis yang tercatat (tidak dikerjakan)

- `run_eval_final.py:194-196,322-323` & `eval_rain_robust.py:208-209,231-233`: hardcode indeks target 0/1/2 alih-alih menurunkan dari `config["target_cols"]` seperti yang sudah dilakukan `inference.py:283-286`.
- `inference.py:145-146`: `num_gat_heads=4, num_attn_heads=4` belum dibaca dari config.
- `inference.py:33-39` vs `config.build_star_edge_index`: logika index edge terduplikasi (fallback disengaja untuk metadata checkpoint — dipertahankan).
- `temporal_loader.py:91-105`: validasi urutan node ganda.

**Verifikasi akhir setelah semua perbaikan §8.2:** test 20/20 lulus; E2E checkpoint nyata mengembalikan 3 kunci kanonik `raw (8,3)` finite tanpa drift; grep rival nol hit; `import main` dan `run_eval_final --help` exit 0.
