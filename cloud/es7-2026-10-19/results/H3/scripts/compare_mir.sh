#!/bin/bash
# Byte-for-byte comparison of `lake exe mir_dimacs` with gen_etv.py + mirgen.py.
# Usage: compare_mir.sh BIN WORKDIR [N:K ...]   (default: a grid, then 33:7)
#   BIN = path to the mir_dimacs binary (e.g. .lake/build/bin/mir_dimacs)
set -u
BIN="$1"; W="$2"; shift 2
HERE="$(cd "$(dirname "$0")" && pwd)"; R="$HERE/../../.."
G="$R/tools/etv/gen_etv.py"; M="$R/results/C/scripts/mirgen.py"
mkdir -p "$W"; cd "$W"
LIST="$*"
if [ -z "$LIST" ]; then
  for N in 3 4 5 6 7 8 9 10 11 12 13 15 17; do for K in 4 5 6 7; do LIST="$LIST $N:$K"; done; done
fi
ok=0; bad=0
for nk in $LIST; do
  N=${nk%:*}; K=${nk#*:}
  python3 "$G" $N $K $K $K --mirror --hull -o h.cnf > /dev/null
  python3 "$M" h.cnf $N --hull -o h.sub.py > /dev/null
  "$BIN" hull $N $K h.sub.lean
  if cmp -s h.sub.py h.sub.lean; then ok=$((ok+1)); else bad=$((bad+1)); echo "DIFF hull $N $K"; fi
  if [ $((N % 2)) = 1 ] && [ $N -ge 3 ]; then
    python3 "$G" $N $K $K $K --mirror -o m.cnf > /dev/null
    python3 "$M" m.cnf $N --interior --yflip-unit -o m.sub.py > /dev/null
    "$BIN" interior $N $K m.sub.lean
    if cmp -s m.sub.py m.sub.lean; then ok=$((ok+1)); else bad=$((bad+1)); echo "DIFF interior $N $K"; fi
  fi
done
echo "identical: $ok  different: $bad"
