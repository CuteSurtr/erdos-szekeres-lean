#!/usr/bin/env bash
# K8EXACT20261106: exact check of the seven 7-fold 64-point order types (eight files) against encoder B (7,8,9) and
# encoder A (7,8,9), plus the hash checks of the recorded formulas.  Run from cloud/es7-2026-10-19/results:
#   bash K8EXACT20261106/run.sh WORKDIR
# Every heavy step runs under a one-core, 12 GB cap at idle priority (python3 -B: no bytecode caches next to the
# imported k8exact.py, PRIMEFOLD/check64/z7exact.py and C7UPPER/gen.py).  The regenerated CNFs and the dumped
# assignments are deleted at the end (reproducible); only their hashes stay in the logs.
# Exit status: 0 only if every step exited 0.  The checkers exit 1 on any violated clause, a missing H(1) flip or a
# failed assertion; regen_hashes*.sh exit 1 on a hash mismatch.  Per-step exit statuses: logs/exit_status.json.
# Standard error of each Python step goes to logs/<step>.stderr, which is removed when empty.
set -uo pipefail
W=${1:?usage: run.sh WORKDIR}
D=K8EXACT20261106
L=$D/logs
CAP=(systemd-run --user --scope --quiet -p CPUQuota=100% -p MemoryMax=12G nice -n 19 ionice -c 3)
mkdir -p "$W" "$L"
rm -f "$L"/*.stderr
SETS=(c7_64pts_small c7_64pts_9layers_centre c7_64_own_s1000 c7_64pts_9layers_centre_own
      p7_compound_64 p7_two_orbit_64 rule_p7_64pts m7_x2_G9s_centre)
PATHS=()
for s in "${SETS[@]}"; do PATHS+=("PRIMEFOLD/sets/k8/$s.pts"); done
REC_A9=bb85a9666902ab9194aff6f1695f8569cf45ac8e543376cbf7fee80f8e001c9b   # C7UPPER/SHA256SUMS.txt cnf/m7K8t9.cnf
declare -A ST
STEPS=()
step() {   # step NAME CMD... : run, record the exit status
  local name=$1; shift
  local rc=0
  "$@" || rc=$?
  ST[$name]=$rc; STEPS+=("$name")
}

# 0. inputs
{
  echo "date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  for s in "${SETS[@]}"; do
    a=$(sha256sum "PRIMEFOLD/sets/k8/$s.pts" | cut -d' ' -f1)
    if [ -f "ES8SYM/sets/$s.pts" ]; then
      b=$(sha256sum "ES8SYM/sets/$s.pts" | cut -d' ' -f1)
      [ "$a" = "$b" ] && c="ES8SYM/sets copy identical" || c="ES8SYM/sets copy DIFFERENT ($b)"
    else
      c="no ES8SYM/sets copy"
    fi
    echo "$a  PRIMEFOLD/sets/k8/$s.pts  ($c)"
  done
} > "$L/sets.txt"

# 1. self-tests of the sign routines
step test_signs "${CAP[@]}" python3 -I -B "$D/test_signs.py" > "$L/test_signs.json" 2> "$L/test_signs.stderr"

# 2. encoder B, 9 layers
CNF=$W/B_m7K8t9.cnf
gen_b() {   # explicit '|| return 1' (set -e is not in force inside 'step')
  echo "date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "generator: $(sha256sum C6UPPER/encb/gen_b2.py)"
  t0=$(date +%s)
  "${CAP[@]}" python3 -I C6UPPER/encb/gen_b2.py 7 8 9 "$CNF" || return 1
  echo "seconds: $(( $(date +%s) - t0 ))"
  echo "header: $(head -1 "$CNF")"
  echo "sha256: $(sha256sum "$CNF" | cut -d' ' -f1)  B_m7K8t9.cnf"
  echo "sha256: $(sha256sum "$CNF.map.json" | cut -d' ' -f1)  B_m7K8t9.cnf.map.json"
}
step gen_B gen_b > "$L/gen_m7K8t9.log" 2>&1

# 3. B: exact assignment of every set and mirror; clause evaluation
rm -rf "$W/assign"
step k8exact_B "${CAP[@]}" python3 -I -B "$D/k8exact.py" --dump "$W/assign" "$CNF" "${PATHS[@]}" \
  > "$L/exact_check.jsonl" 2> "$L/exact_check.stderr"

# 4. B: separate clause check of the dumped full assignments
step satcheck_B "${CAP[@]}" python3 -I -B "$D/satcheck.py" "$CNF" "$W"/assign/*.assign \
  > "$L/satcheck.jsonl" 2> "$L/satcheck.stderr"

# 5. delete B's regenerated formula and the assignments (hashes are in the logs)
rm -f "$CNF" "$CNF.map.json"
rm -rf "$W/assign"
echo "deleted: B_m7K8t9.cnf, B_m7K8t9.cnf.map.json and the 16 assignment files" >> "$L/gen_m7K8t9.log"

# 6. encoder A, 9 layers: regenerate, compare with the recorded hash
CNFA=$W/A_m7K8t9.cnf
gen_a() {
  echo "date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "generator: $(sha256sum C7UPPER/gen.py)"
  echo "generator recorded in C7UPPER/SHA256SUMS.txt: $(grep -E '^[0-9a-f]{64}  gen.py$' C7UPPER/SHA256SUMS.txt)"
  t0=$(date +%s)
  "${CAP[@]}" python3 -I C7UPPER/gen.py 7 8 9 "$CNFA" || return 1
  echo "seconds: $(( $(date +%s) - t0 ))"
  echo "header: $(head -1 "$CNFA")"
  got=$(sha256sum "$CNFA" | cut -d' ' -f1)
  echo "sha256: $got  A_m7K8t9.cnf"
  echo "recorded (C7UPPER/SHA256SUMS.txt, cnf/m7K8t9.cnf): $REC_A9"
  echo "sha256: $(sha256sum "$CNFA.json" | cut -d' ' -f1)  A_m7K8t9.cnf.json (meta file)"
  if [ "$got" = "$REC_A9" ]; then echo "MATCH"; else echo "MISMATCH"; return 1; fi
}
step gen_A gen_a > "$L/gen_A_m7K8t9.log" 2>&1

# 7. A: exact assignment of every set and mirror; clause evaluation
rm -rf "$W/assignA"
step k8exact_A "${CAP[@]}" python3 -I -B "$D/k8exact_a.py" --dump "$W/assignA" "$CNFA" "${PATHS[@]}" \
  > "$L/exact_check_A.jsonl" 2> "$L/exact_check_A.stderr"

# 8. A: separate clause check of the dumped full assignments
step satcheck_A "${CAP[@]}" python3 -I -B "$D/satcheck.py" "$CNFA" "$W"/assignA/*.assign \
  > "$L/satcheck_A.jsonl" 2> "$L/satcheck_A.stderr"

# 9. delete A's regenerated formula and the assignments
rm -f "$CNFA" "$CNFA.json"
rm -rf "$W/assignA"
echo "deleted: A_m7K8t9.cnf, A_m7K8t9.cnf.json and the 16 assignment files" >> "$L/gen_A_m7K8t9.log"

# 10. recorded encoder-B hashes (B_m7K8t10, B_m6K8t9)
step regen_hashes_B bash "$D/regen_hashes.sh" "$W/regen" > "$L/regen_hashes.log" 2>&1

# 11. recorded encoder-A 10-layer hashes (A_m7K8t10, A_m7K8t10 + unit H(1)) and H(1) = variable 7857
step regen_hashes_A bash "$D/regen_hashes_a.sh" "$W/regen" > "$L/regen_hashes_A.log" 2>&1
rmdir "$W/regen" 2>/dev/null || true

# exit statuses (strict JSON)
for f in "$L"/*.stderr; do [ -s "$f" ] || rm -f "$f"; done
overall=0
{
  printf '{"date": "%s"' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  for n in "${STEPS[@]}"; do
    printf ', "%s": %d' "$n" "${ST[$n]}"
    [ "${ST[$n]}" -eq 0 ] || overall=1
  done
  printf ', "overall": %d}\n' "$overall"
} > "$L/exit_status.json"
cat "$L/exit_status.json"
exit $overall
