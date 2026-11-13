#!/bin/bash
# verify_A6-4: regenerate the L1 CNF (c5_n35L) from a copy of the repository generator (hash-checked copy in gen/),
# run from this directory so no __pycache__ lands in the read-only worktree (-I -B), hash it, then delete it.
# Recorded: c5_n35L.cnf 283,069,961 bytes, sha256 90dea1cf87d3d8500dffff9d9741e84abc9babe4e1ac4e32035448ce7c0668a8.
set -u
OUT=$(cd "$(dirname "$0")" && pwd); W=$OUT/work; mkdir -p "$W"; cd "$W" || exit 1
/usr/bin/time -l python3 -I -B "$OUT/gen/symcnf_layers.py" 35 7 5 -o c5_n35L.cnf --map c5_n35L.json > gen.out 2> gen.time
rc=$?
echo "gen exit $rc rss_bytes $(awk '/maximum resident/ {print $1}' gen.time) real_s $(awk '/real/ {print $1; exit}' gen.time)"
echo "c5_n35L.cnf bytes $(stat -f %z c5_n35L.cnf) sha256 $(shasum -a 256 c5_n35L.cnf | cut -d' ' -f1) header: $(grep -m1 '^p cnf' c5_n35L.cnf)"
echo "c5_n35L.json sha256 $(shasum -a 256 c5_n35L.json | cut -d' ' -f1) (repo SYM5 has c5_n35.json only)"
rm -f c5_n35L.cnf
ls -la "$W"
