#!/bin/bash
# Once every case is closed: assemble the WAVE1 leaves, write V2L/Leaves.lean and V2L/Final.lean,
# and build them (kernel cover check of all 450 leaf lists). Run from results/V2-L.
set -euo pipefail
python3 -I scripts/assemble_leaves.py .. leaves_asm | tee logs/assemble_leaves.log
python3 - <<'PY'
import json, sys
s = json.load(open("leaves_asm/status.json"))["summary"]
if s["closed"] != 450: sys.exit(f"not all cases closed: {s['closed']}/450; open: {s['open'][:20]}")
PY
python3 -I scripts/gen_leaves.py leaves_asm V2L/Leaves.lean
cp scripts/Final.lean.template V2L/Final.lean
grep -q "import V2L.Final" V2L.lean || echo "import V2L.Final" >> V2L.lean
(time lake build V2L.Final) 2>&1 | tee logs/final_build.log
