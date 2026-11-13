#!/bin/bash
# A6 audit: regenerate the mirror CNFs with the repository generators (one at a time), record the SHA-256 of the
# whole file and of its non-comment lines (to test "same clauses, different comment line"), then delete the CNF.
# usage: regen_mirror.sh RESULTS_DIR OUTDIR
set -u
R=$1; W=$2/regen; mkdir -p "$W"; cd "$W" || exit 1
run() {  # name, then generator command
  local name=$1; shift
  /usr/bin/time -l "$@" > "$name.gen.out" 2> "$name.time"
  echo "$name exit $? rss_bytes $(awk '/maximum resident/ {print $1}' "$name.time") real_s $(awk '/real/ {print $1; exit}' "$name.time")"
  echo "$name.cnf whole $(shasum -a 256 "$name.cnf" | cut -d' ' -f1) header: $(grep -m1 '^p cnf' "$name.cnf")"
  echo "$name.cnf non-comment-lines $(grep -v '^c' "$name.cnf" | shasum -a 256 | cut -d' ' -f1)"
  [ -f "$name.json" ] && echo "$name.json $(shasum -a 256 "$name.json" | cut -d' ' -f1)"
  rm -f "$name.cnf"
}
run m_t16k7a1 python3 -I "$R/SYMZ/zcnf.py" mirror 16 7 --axis 1 -o m_t16k7a1.cnf --map m_t16k7a1.json
run m_t17k7 python3 -I "$R/SYMZ/zcnf_v1.py" mirror 17 7 -o m_t17k7.cnf --map m_t17k7.json
run m34_final python3 -I "$R/SYMZ/zcnf.py" mirror 17 7 -o m34_final.cnf --map m34_final.json
echo "regen_mirror done $(date -u +%H:%M:%SZ)"
