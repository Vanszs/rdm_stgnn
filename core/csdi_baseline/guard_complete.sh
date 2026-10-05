#!/usr/bin/env bash
# Safety net: ensure Tabel 3.18 gets built once the CSDI eval is complete.
#
# Exists because chain_eval.sh was edited while an instance of it was already
# running, so the running instance's behaviour on its next line is not something
# to bet an overnight run on. This guard is independent: it waits for the eval
# process to disappear and for every shard to be present, then runs compare.py.
# compare.py is idempotent, so running it twice is harmless.
#
#   nohup setsid bash guard_complete.sh > logs/guard.log 2>&1 < /dev/null &
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1
mkdir -p logs

EVAL_PAT='[e]valuate_csdi.py'
TAG="ddim_m30_s20_bs32"
TOTAL=1096

echo "[guard] watching for eval completion (expect $TOTAL shards) ($(date +%H:%M:%S))"
while :; do
  have=$(ls eval_shards/${TAG}_*.npz 2>/dev/null | wc -l)
  if [ "$have" -ge "$TOTAL" ] && ! pgrep -f "$EVAL_PAT" >/dev/null; then
    echo "[guard] all $have shards present, eval gone ($(date +%H:%M:%S))"
    break
  fi
  sleep 120
done

# Give the chain's own compare.py a moment, then ensure it ran.
sleep 60
if grep -q "DONE, Tabel 3.18 written" logs/chain.log 2>/dev/null; then
  echo "[guard] chain already wrote the table; verifying only"
else
  echo "[guard] chain did not complete; running compare.py ($(date +%H:%M:%S))"
  python compare.py > logs/compare.log 2>&1
  echo "[guard] compare rc=$? ($(date +%H:%M:%S))"
fi

if grep -q "TABEL_3_18_END" ../../docs/CSDI_COMPARISON.md 2>/dev/null; then
  echo "[guard] doc has Tabel 3.18 block"
  sed -n '/TABEL_3_18_START/,+2p' ../../docs/CSDI_COMPARISON.md
fi

# Completion criterion (d): prove every number is reproducible from the raw shards.
python verify_metrics.py > logs/verify.log 2>&1
echo "[guard] traceability verify rc=$? (see logs/verify.log)"
tail -3 logs/verify.log 2>/dev/null
echo "[guard] finished ($(date +%H:%M:%S))"
