#!/usr/bin/env bash
# Keep the CSDI full-test evaluation running until every shard exists.
#
# Why this exists: this machine suspends itself (it cost 4 unprompted hours during
# training). evaluate_csdi.py is resumable, but "resumable" only helps if something
# restarts it. The running chain_eval.sh instance predates the restart loop, so this
# supervisor owns that job instead:
#   - if the eval process is gone and shards are missing -> start it again
#   - once every shard is present -> exit
# Each restart redoes only the missing batches, so this is cheap.
#
#   nohup setsid bash supervise_eval.sh > logs/supervise.log 2>&1 < /dev/null &
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1
mkdir -p logs

EVAL_PAT='[e]valuate_csdi.py'
TAG="ddim_m30_s20_bs32"
TOTAL=1096
ARGS=(--nsample 30 --sampler ddim --ddim-steps 20 --batch-size 32)

echo "[sup] supervising eval, target $TOTAL shards ($(date +%H:%M:%S))"
while :; do
  have=$(ls eval_shards/${TAG}_*.npz 2>/dev/null | wc -l)
  if [ "$have" -ge "$TOTAL" ]; then
    echo "[sup] all $have shards present, done ($(date +%H:%M:%S))"
    break
  fi
  if ! pgrep -f "$EVAL_PAT" >/dev/null; then
    echo "[sup] eval absent with $have/$TOTAL shards -> restarting ($(date +%H:%M:%S))"
    python evaluate_csdi.py "${ARGS[@]}" >> logs/evaluate.log 2>&1
    echo "[sup] eval exited rc=$? (have=$(ls eval_shards/${TAG}_*.npz 2>/dev/null | wc -l)) ($(date +%H:%M:%S))"
    sleep 20
  else
    sleep 90
  fi
done
echo "[sup] finished ($(date +%H:%M:%S))"
