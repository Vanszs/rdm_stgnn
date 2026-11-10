#!/usr/bin/env bash
# Gagal bila repo memuat kontradiksi yang bisa ditunjuk. Jalankan dari root repo.
set -euo pipefail
fail=0
stale=$(grep -rlnE '0,6641|0,6620|0,1953|0,1950|0,5858|0,3688|0,0710' --include='*.md' . 2>/dev/null | grep -vE 'node_modules|scratch/|archive/' || true)
if [ -n "$stale" ]; then echo "FAIL: angka lama di: $stale"; fail=1; fi
python3 - <<'PY' || fail=1
import sys, torch; sys.path.insert(0, 'core')
from src.config import FINAL_FEATURE_COLS
c = torch.load('core/models/diffusion_chkpt.pth', map_location='cpu', weights_only=False)['config']
ok = c['feature_cols'] == list(FINAL_FEATURE_COLS) + ['precipitation']
print('OK: checkpoint == CANDIDATE' if ok else 'FAIL: checkpoint != CANDIDATE')
sys.exit(0 if ok else 1)
PY
(cd core && python3 -m pytest tests -q >/dev/null) || { echo "FAIL: core tests"; fail=1; }
python3 -m pytest api/tests -q >/dev/null || { echo "FAIL: api tests"; fail=1; }
[ $fail -eq 0 ] && echo "ALL CHECKS PASSED"
exit $fail
