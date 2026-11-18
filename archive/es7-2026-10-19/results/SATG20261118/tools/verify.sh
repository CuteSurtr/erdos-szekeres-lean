#!/bin/bash
# usage: verify.sh NAME POINTS K [nb] -> exact cell check: vx1118 finder (satcells) + vx1118 trusted replay (check_cells.py),
# one JSON line per run in verify/status.jsonl (same format as vx1118/run_all.sh, plus the SHA-256 of the point file).
set -u
cd /home/jay/research/data/roadmap-20261115/pm1115/sat2
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python; V=/home/jay/research/data/roadmap-20261115/pm1115/vx1118
mkdir -p verify/logs verify/samples
FND="$V/satcells"  # nb: SAT2 copy vx/satcells_nb with the C(n,K) brute force of part (a) skipped (only change)
[ "${4:-}" = nb ] && { FND=$PWD/vx/satcells_nb; export SATCELLS_NO_BRUTE=1; }
name=$1 file=$2 k=$3; t0=$(date +%s)
"$FND" "$file" "$k" "verify/samples/$name.samples.txt" > "verify/logs/$name.cpp.log" 2>&1; rc1=$?
t1=$(date +%s)
"$PY" -I "$V/check_cells.py" "$file" "$k" "verify/samples/$name.samples.txt" 300 > "verify/logs/$name.py.log" 2>&1; rc2=$?
printf '{"name":"%s","file":"%s","sha256":"%s","K":%s,"cpp_rc":%s,"cpp_s":%s,"py_rc":%s,"py_s":%s,"cpp":"%s","py":"%s","time":"%s"}\n' \
  "$name" "$file" "$(sha256sum "$file" | cut -c1-64)" "$k" "$rc1" "$((t1 - t0))" "$rc2" "$(( $(date +%s) - t1 ))" \
  "$(grep -h '^RESULT' "verify/logs/$name.cpp.log" | tr -d '"')" "$(grep -h '^REPLAY' "verify/logs/$name.py.log" | tr -d '"')" \
  "$(date '+%F %T %Z')" >> verify/status.jsonl
tail -1 verify/status.jsonl
