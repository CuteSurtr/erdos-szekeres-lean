#!/bin/bash
# A6 audit: regenerate CNFs (and maps) with the repository generators, one at a time, record SHA-256 and peak RSS,
# then delete the regenerated CNF (only hashes are kept). Writes only inside OUTDIR/regen.
# usage: regen.sh RESULTS_DIR OUTDIR
set -u
R=$1; W=$2/regen; mkdir -p "$W"; cd "$W" || exit 1
run() {  # name, then generator command
  local name=$1; shift
  /usr/bin/time -l "$@" > "$name.gen.out" 2> "$name.time"
  echo "$name exit $? rss_bytes $(awk '/maximum resident/ {print $1}' "$name.time") real_s $(awk '/real/ {print $1; exit}' "$name.time")"
  echo "$name.cnf $(shasum -a 256 "$name.cnf" | cut -d' ' -f1) header: $(grep -m1 '^p cnf' "$name.cnf")"
  [ -f "$name.json" ] && echo "$name.json $(shasum -a 256 "$name.json" | cut -d' ' -f1)"
  rm -f "$name.cnf"
}
run c4_n32L python3 -I "$R/SYM5/symcnf_layers.py" 32 7 4 -o c4_n32L.cnf --map c4_n32L.json
run c5_n35L python3 -I "$R/SYM5/symcnf_layers.py" 35 7 5 -o c5_n35L.cnf --map c5_n35L.json
run c5_n35 python3 -I "$R/SYM5/symcnf.py" 35 7 5 -o c5_n35.cnf --map c5_n35.json
echo "regen done $(date -u +%H:%M:%SZ)"
