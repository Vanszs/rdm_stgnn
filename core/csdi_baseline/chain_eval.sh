#!/usr/bin/env bash
# Drive the CSDI full-test evaluation to completion, then build Tabel 3.18.
#
# Steps:
#   1. wait for train_csdi.py to exit (a bare "train_csdi.py" pattern also matches
#      leftover bash shells that merely mention the script, so match the interpreter)
#   2. evaluate_csdi.py, restarted on failure -- the run is resumable (one shard per
#      batch), so a restart redoes only what is missing. This survives the machine
#      suspending mid-run, which it demonstrably does.
#   3. compare.py -> renders Tabel 3.18 into docs/CSDI_COMPARISON.md
#
#   nohup setsid bash chain_eval.sh > logs/chain.log 2>&1 < /dev/null &
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1
mkdir -p logs

TRAINER_PAT='[b]in/python train_csdi.py'
EVAL_PAT='[e]valuate_csdi.py'
EVAL_ARGS=(--nsample 30 --sampler ddim --ddim-steps 20 --batch-size 32)
TAG="ddim_m30_s20_bs32"

echo "[chain] waiting for train_csdi.py ($(date +%H:%M:%S))"
while pgrep -f "$TRAINER_PAT" >/dev/null; do sleep 30; done
echo "[chain] trainer gone ($(date +%H:%M:%S))"
sleep 10

attempt=0
while :; do
  have=$(ls eval_shards/${TAG}_*.npz 2>/dev/null | wc -l)
  if ! pgrep -f "$EVAL_PAT" >/dev/null; then
    attempt=$((attempt + 1))
    if [ "$attempt" -gt 12 ]; then
      echo "[chain] giving up after $attempt attempts ($have shards) ($(date +%H:%M:%S))"
      exit 1
    fi
    echo "[chain] starting eval attempt $attempt ($have shards so far) ($(date +%H:%M:%S))"
    python evaluate_csdi.py "${EVAL_ARGS[@]}" >> logs/evaluate.log 2>&1
    rc=$?
    echo "[chain] eval exited rc=$rc ($(date +%H:%M:%S))"
    # A clean exit means every batch was written; only retry a real failure.
    if [ $rc -eq 0 ]; then break; fi
    sleep 20
  else
    sleep 60
  fi
done
echo "[chain] eval done ($(date +%H:%M:%S))"

python compare.py > logs/compare.log 2>&1
rc=$?
if [ $rc -ne 0 ]; then
  echo "[chain] COMPARE FAILED rc=$rc -- see logs/compare.log ($(date +%H:%M:%S))"
  exit $rc
fi
echo "[chain] compare done, Tabel 3.18 written ($(date +%H:%M:%S))"

# Completion criterion (d): every table number must be reproducible from the raw
# shards. verify_metrics.py recomputes all metrics from eval_shards/ and fails if
# csdi_metrics.json disagrees or the run was partial.
python verify_metrics.py > logs/verify.log 2>&1
rc=$?
echo "[chain] verify rc=$rc (see logs/verify.log) ($(date +%H:%M:%S))"
exit $rc
