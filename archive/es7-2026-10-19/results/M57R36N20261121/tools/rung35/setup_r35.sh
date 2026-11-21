#!/bin/bash
# setup_r35.sh -- NOT run by the rung35-prep agent.  Prepares a fresh directory for the rung N = 35
# cube-and-conquer run (drive35.py = r36 drive.py with BASE/ORDER/TOP and the case loop changed).
# Run only after rung N = 36 has closed.  It does not touch r36.
set -euo pipefail
S=SCRATCH
P=$S/agents/rung35-prep
R35=${R35:-$S/r35}
[ -e "$R35/cubes/state.json" ] && { echo "refusing: $R35/cubes/state.json exists (driver would resume it)"; exit 1; }
mkdir -p "$R35/bin" "$R35/run"
ln -sfn "MAC_REPO/.cache/es7/bin/cadical" "$R35/bin/cadical"
ln -sfn "MAC_REPO/.cache/es7/bin/cake_lpr" "$R35/bin/cake_lpr"
cp "$P/drive35.py" "$R35/drive.py"
for c in c35_rle12_qle12 c35_rle12_ule22 c35_tle22_qle12 c35_tle22_ule22; do
  cp "$P/run/$c.cnf" "$R35/run/$c.cnf"
  want=$(grep " run/$c.cnf\$" "$P/SHA256_CNF.txt" | cut -c1-64)
  got=$(shasum -a 256 "$R35/run/$c.cnf" | cut -c1-64)
  [ -n "$want" ] && [ "$want" = "$got" ] || { echo "SHA MISMATCH $c: $got vs $want"; exit 1; }
  echo "ok $c $got"
done
echo "ready.  launch (same settings as r36):"
echo "  cd $R35 && LANES=11 TL=1500 nohup nice -n 5 python3 -B drive.py > cubes_driver.out 2>&1 &"
echo "final check after DONE:  python3 -B $P/leafcover35.py $R35/cubes/state.json --final"
