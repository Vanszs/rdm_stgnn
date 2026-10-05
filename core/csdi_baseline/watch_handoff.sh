#!/usr/bin/env bash
# Watch the real handoff: trainer exits -> chain starts evaluate_csdi -> first shard lands.
# Exits 0 when the full-test eval has demonstrably started producing shards,
# 3 on failure, 2 on timeout.
CB=/home/vanszs/Documents/Skripsi_Bevan/core/csdi_baseline
cd "$CB" || exit 3
end=$((SECONDS + 2400))

echo "[watch] waiting for trainer to exit"
while pgrep -f "train_csdi.py --epochs" >/dev/null; do
  [ $SECONDS -gt $end ] && { echo "[watch] TIMEOUT waiting for trainer"; exit 2; }
  sleep 20
done
echo "[watch] trainer gone at $(date +%H:%M:%S); ckpt epoch=$(python -c "import torch;print(torch.load('save/csdi_pangrango.pth',map_location='cpu',weights_only=False).get('epoch'))" 2>/dev/null)"
sleep 20

echo "[watch] waiting for eval to produce shards"
last=0
while :; do
  n=$(ls eval_shards/ 2>/dev/null | grep -c "^ddim_m30_s20_bs32" || true)
  if [ "$n" -gt "$last" ]; then echo "[watch] shards=$n at $(date +%H:%M:%S)"; last=$n; fi
  if [ "$n" -ge 2 ]; then
    echo "[watch] OK: real eval is running"
    tail -3 logs/evaluate.log 2>/dev/null
    exit 0
  fi
  if ! pgrep -f chain_eval.sh >/dev/null && [ "$n" -eq 0 ]; then
    echo "[watch] FAIL: chain gone with no shards"; tail -15 logs/evaluate.log 2>/dev/null; exit 3
  fi
  if [ $SECONDS -gt $end ]; then
    echo "[watch] TIMEOUT: shards=$n"; tail -15 logs/evaluate.log 2>/dev/null; exit 2
  fi
  sleep 15
done
