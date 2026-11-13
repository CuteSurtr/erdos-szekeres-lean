#!/bin/bash
# Small-k controls for the mirror encodings (Task C, Part 1).
# usage: controls.sh <cnfdir> <bindir> <workdir>
CNF="$1"; BIN="$2"; WD="$3"; HERE="$(cd "$(dirname "$0")" && pwd)"; TOOLS="$HERE/../../../tools"
mkdir -p "$WD/etv"; cd "$WD"
ln -sfn "$TOOLS/decomp" "$WD/decomp"
solve() { # name cnf [lrat]
  local name="$1" cnf="$2" lrat="$3"; local t0=$(date +%s)
  if [ -n "$lrat" ]; then
    "$BIN/cadical" -q --lrat --binary=false "$cnf" "$name.lrat" > "$name.out" 2>&1
  else
    "$BIN/cadical" -q "$cnf" > "$name.out" 2>&1
  fi
  local st=$(grep '^s ' "$name.out"); local t1=$(date +%s)
  echo "$name: $st ($((t1-t0)) s)"
  if [ -n "$lrat" ] && [ "$st" = "s UNSATISFIABLE" ]; then
    local sz=$(du -h "$name.lrat" | cut -f1)
    "$BIN/lrat-check" "$cnf" "$name.lrat" > "$name.lratcheck" 2>&1
    echo "$name: lrat-check ($sz): $(grep -E 'VERIFIED|FAILED|failed|ERROR|error' "$name.lratcheck" | head -2 | tr '\n' ' ')"
    rm -f "$name.lrat"
  fi
}
# k = 5: 8 points (0 axis points; gen_etv --mirror with N even fixes no index) must be SAT,
# 9 points (one axis point; both frames) must be UNSAT.
solve m8k5 "$CNF/m8k5.cnf"
solve m9k5 "$CNF/m9k5.cnf" lrat
solve hm9k5 "$CNF/hm9k5.cnf" lrat
solve m9k5.sub "$CNF/m9k5.sub.cnf" lrat
# k = 6: 17 points with one axis point must be UNSAT (ES(6) = 17).  The non-hull CNF alone
# covers every mirror-symmetric 17-point set; the hull frame covers the hull-vertex sub-case.
solve m17k6.sub "$CNF/m17k6.sub.cnf" lrat
solve hm17k6.sub "$CNF/hm17k6.sub.cnf" lrat
solve m17k6 "$CNF/m17k6.cnf" lrat
solve hm17k6 "$CNF/hm17k6.cnf" lrat
# positive control at k = 7: the mirror-symmetric 32-point classical set has 0 axis points,
# which is exactly the case gen_etv --mirror encodes for N = 32.
(cd etv && python3 "$TOOLS/etv/mircheck.py")
echo "m32k7 under the 32-point set's orientations: $("$BIN/asolve" "$CNF/m32k7.cnf" < etv/m32k7_assume.txt)"
echo "m32k7.sub under the 32-point set's orientations: $("$BIN/asolve" "$CNF/m32k7.sub.cnf" < etv/m32k7_assume.txt)"
