#!/bin/bash
# Solve the control CNFs, compare with the known answers, and check every model with the
# independent checker symcheck.py.  usage: run_controls.sh CNF_DIR CADICAL_BIN OUT_DIR
CNF="$1"; CAD="$2"; OUT="$3"
D="$(cd "$(dirname "$0")" && pwd)"
SYM="$D/../../../tools/symmetric/symcheck.py"
mkdir -p "$OUT"
# tag expected reason
while read -r tag exp why; do
  [ -z "$tag" ] && continue
  s=$(date +%s)
  "$CAD" -q -t 1800 "$CNF/$tag.cnf" > "$OUT/$tag.out" 2>&1
  e=$(date +%s)
  res=$(grep '^s ' "$OUT/$tag.out" | awk '{print $2}')
  chk=""
  if [ "$res" = "SATISFIABLE" ]; then
    chk=$(python3 "$SYM" "$CNF/$tag.json" "$OUT/$tag.out" --sig "$OUT/$tag.sig" | tail -1 | tr -d ' ')
  fi
  verdict=FAIL
  if [ "$exp" = "?" ] || [ "$exp" = "$res" ]; then verdict=OK; fi
  echo "$tag expected=$exp got=$res time=$((e-s))s verdict=$verdict check=$chk reason=$why"
done <<'EOF'
n16k6m4 SATISFIABLE 4-fold_hexagon-free_16-point_sets_exist_(Subercaseaux_et_al._2025:_66_abstract)
n16k6m5c SATISFIABLE 5-fold_(centre_in_set)_hexagon-free_16-point_sets_exist_(Subercaseaux_et_al._2025:_948)
n18k6m3 UNSATISFIABLE ES(6)=17
n18k6m6 UNSATISFIABLE ES(6)=17
n6k5m2 SATISFIABLE small_sanity
n6k5m3 SATISFIABLE small_sanity
n8k5m2 SATISFIABLE ES(5)=9_and_saved_models
n8k5m4 SATISFIABLE ES(5)=9_and_saved_models
n8k5m8 UNSATISFIABLE one_orbit_of_8_is_convex
n9k5m3 UNSATISFIABLE ES(5)=9
n9k5m9 UNSATISFIABLE ES(5)=9
n10k5m3c UNSATISFIABLE ES(5)=9
n12k5m3 UNSATISFIABLE ES(5)=9
n13k6m3c ? not_known
n15k6m3 ? not_known
n16k6m3c ? not_known_(saved_run_said_UNSAT)
EOF
