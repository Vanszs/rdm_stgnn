#!/usr/bin/env bash
# Tabel 3.17 — 5 skenario penalaan hiperparameter RDM-STGNN.
#
# Setiap skenario = 1 training penuh + 1 evaluasi, ditulis ke direktori sendiri
# sehingga TIDAK menimpa checkpoint kanonik (models/diffusion_chkpt.pth).
#
# Definisi skenario (persis Tabel 3.17 naskah, hal. cetak 68-69):
#   SKEN 1: lr 1e-3 | epoch 10 (patience 5)  | k 1 | DDIM 10 | M 10 | aux 0.3
#   SKEN 2: lr 1e-3 | epoch 20 (patience 8)  | k 2 | DDIM 15 | M 20 | aux 0.5
#   SKEN 3: lr 1e-3 | epoch 20 (patience 12) | k 3 | DDIM 20 | M 30 | aux 0.7  <- kontrol naskah
#   SKEN 4: lr 5e-4 | epoch 35 (patience 12) | k 4 | DDIM 30 | M 40 | aux 0.7
#   SKEN 5: lr 1e-4 | epoch 50 (patience 15) | k 5 | DDIM 50 | M 50 | aux 1.0
#
# Pemakaian:
#   ./run_5scenarios.sh              # jalankan semua (lama: ~15-25 jam training awal)
#   ./run_5scenarios.sh 3            # hanya skenario 3
#   ./run_5scenarios.sh 3 5          # skenario 3 dan 5
#   ./run_5scenarios.sh --force      # paksa latih ulang semua skenario
#   ./run_5scenarios.sh --force 3    # paksa latih ulang skenario 3
#   FORCE=1 ./run_5scenarios.sh      # alternatif env var untuk force retrain
#
# Catatan: jangan jalankan paralel di GPU 4 GB — satu training sudah ~1-4 GB.

set -uo pipefail

CORE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$CORE_DIR" || exit 1

# Skema: "<id> <lr> <epochs> <patience> <k> <ddim> <ensemble> <aux> <label>"
SCHEMES=(
  "1 1e-3 10 5  1 10 10 0.3 ultra_lightweight"
  "2 1e-3 20 8  2 15 20 0.5 moderate_fast"
  "3 1e-3 20 12 3 20 30 0.7 default_kontrol"
  "4 5e-4 35 12 4 30 40 0.7 fine_tuned"
  "5 1e-4 50 15 5 50 50 1.0 high_capacity"
)

FORCE_FLAG="${FORCE:-${FORCE_RETRAIN:-0}}"
TARGETS=()

for arg in "$@"; do
  case "$arg" in
    --force|-f)
      FORCE_FLAG=1
      ;;
    [1-5])
      TARGETS+=("$arg")
      ;;
    *)
      echo "Argumen tidak dikenal: $arg (gunakan 1-5 atau --force)"
      exit 1
      ;;
  esac
done

selected() {
  local id="$1"
  [ ${#TARGETS[@]} -eq 0 ] && return 0
  local t
  for t in "${TARGETS[@]}"; do [ "$t" = "$id" ] && return 0; done
  return 1
}

echo "=================================================================="
echo "TABEL 3.17 — 5 SKENARIO PENALAAN HIPERPARAMETER RDM-STGNN"
echo "=================================================================="
echo "GPU:"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo "  (tidak terdeteksi)"
echo "Konfigurasi Fitur : 10-fitur (--precip-mode both)"
echo "Inferensi Batched : sample_batch_size=${SAMPLE_BATCH_SIZE:-256}"
echo "Force Retrain     : $FORCE_FLAG"
echo

for spec in "${SCHEMES[@]}"; do
  read -r ID LR EPOCHS PATIENCE K DDIM ENS AUX LABEL <<< "$spec"
  selected "$ID" || continue

  RUN_DIR="results/canonical/tabel_3_17/sken_${ID}_${LABEL}"
  CKPT="${RUN_DIR}/model.pth"
  LOG="${RUN_DIR}/train.log"
  mkdir -p "$RUN_DIR"

  echo "------------------------------------------------------------------"
  echo "SKENARIO ${ID} (${LABEL})"
  echo "  lr=${LR}  epochs=${EPOCHS}  patience=${PATIENCE}  k=${K}  DDIM=${DDIM}  M=${ENS}  aux=${AUX}"
  echo "  -> ${RUN_DIR}"
  echo "------------------------------------------------------------------"

  DO_TRAIN=0
  if [ ! -f "$CKPT" ]; then
    DO_TRAIN=1
  elif [ "$FORCE_FLAG" = "1" ] || [ "$FORCE_FLAG" = "true" ]; then
    echo "  [force-retrain] checkpoint ada tetapi --force aktif. Melatih ulang..."
    DO_TRAIN=1
  else
    N_FEAT=$(python -c '
import torch, sys
try:
    c = torch.load(sys.argv[1], map_location="cpu", weights_only=False)
    print(len(c.get("config", {}).get("feature_cols", [])))
except Exception:
    print(0)
' "$CKPT" 2>/dev/null || echo 0)
    if [ "$N_FEAT" -ne 10 ]; then
      echo "  [auto-retrain] checkpoint lama terdeteksi $N_FEAT fitur (< 10 fitur). Melatih ulang dengan 10-fitur..."
      DO_TRAIN=1
    else
      echo "  [skip training] checkpoint 10-fitur valid sudah ada: $CKPT"
    fi
  fi

  if [ "$DO_TRAIN" -eq 1 ]; then
    TRAIN_START=$(date +%s)
    python src/train.py \
      --lr "$LR" \
      --epochs "$EPOCHS" \
      --early-stop-patience "$PATIENCE" \
      --k-neighbors "$K" \
      --wet-loss-weight "$AUX" \
      --cond-dropout 0.15 \
      --precip-mode both \
      --seed 1 \
      --checkpoint-path "$CKPT" \
      > "$LOG" 2>&1
    TRAIN_RC=$?
    TRAIN_SECS=$(( $(date +%s) - TRAIN_START ))
    if [ $TRAIN_RC -ne 0 ]; then
      echo "  !! TRAINING GAGAL (exit $TRAIN_RC). Lihat $LOG"
      continue
    fi
    echo "  training selesai dalam ${TRAIN_SECS}s"
  fi

  # Evaluasi: 30 sampel tetap (naskah 3.8.3 mensyaratkan jumlah sampel SAMA
  # antar-skenario); DDIM steps & ensemble di sini hanya untuk latensi/varian M.
  EVAL_DIR="${RUN_DIR}/eval"
  mkdir -p "$EVAL_DIR"
  EVAL_START=$(date +%s)
  if [ "$ID" = "3" ]; then
    SCENARIOS="all"      # kontrol naskah: ablasi penuh (4 skenario) sekali saja
  else
    SCENARIOS="full_model"
  fi
  SAMPLE_BATCH_SIZE="${SAMPLE_BATCH_SIZE:-256}"
  python scripts/run_eval_final.py \
    --checkpoint "$CKPT" \
    --num-inference-steps "$DDIM" \
    --num-ensemble "$ENS" \
    --sample-batch-size "$SAMPLE_BATCH_SIZE" \
    --eval-step 1 \
    --scenarios "$SCENARIOS" \
    --out-dir "$EVAL_DIR" \
    > "${RUN_DIR}/eval.log" 2>&1
  EVAL_RC=$?
  EVAL_SECS=$(( $(date +%s) - EVAL_START ))

  if [ $EVAL_RC -ne 0 ]; then
    echo "  !! EVALUASI GAGAL (exit $EVAL_RC). Lihat ${RUN_DIR}/eval.log"
    continue
  fi

  # Latensi per sampel (syarat naskah: <= 2 detik). n_samples = jumlah window test.
  python - "$RUN_DIR" "$EVAL_SECS" "$ENS" "$DDIM" <<'PY'
import json, sys, os
run_dir, eval_secs, ens, ddim = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
summ = os.path.join(run_dir, "eval", "comparison", "comparison_summary.json")
n = None
if os.path.exists(summ):
    try:
        n = json.load(open(summ)).get("metadata", {}).get("samples_per_scenario")
    except Exception:
        n = None
lat = {
    "eval_total_seconds": eval_secs,
    "n_samples": n,
    "num_ensemble": ens,
    "ddim_steps": ddim,
    "latency_per_sample_s": (eval_secs / n) if (n and n > 0) else None,
}
json.dump(lat, open(os.path.join(run_dir, "latency.json"), "w"), indent=2)
print(f"  eval selesai {eval_secs:.0f}s; latensi/sampel = {lat['latency_per_sample_s']}")
PY
  echo "  hasil: ${RUN_DIR}/eval/comparison/comparison_summary.json"
done

echo
echo "=================================================================="
echo "SELESAI. Ringkasan per skenario ada di results/canonical/tabel_3_17/sken_*/"
echo "Jalankan 'python scripts/collect_5scenarios.py' untuk menyusun Tabel 3.17."
echo "=================================================================="