#!/bin/bash
# Early (pre-final) check of closed (20,15) contexts on a read-only snapshot (track P307V).  Run inside one unit.
# usage: early_check.sh OUTDIR [PREV_BB_DIR ...]
#   copies the live master.json and every ctx file older than 2 minutes that is not already in a PREV_BB_DIR, then runs
#   tcheck_b35 (1 thread) and pycheck_b35 (`all partial`) with the rows the copied master names, and compare_py.
# A context that passes here is a valid subtree for those rows; rows are append-only (rows_stated.py), so it stays valid
# for every later version.  This is NOT the final check: the final replay re-checks every context (README section 8).
set -u
OUT=$1; shift
W=/home/jay/research/data/es308-20261114; BB=$W/runs/b35s20/bb; PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
T=$(cd "$(dirname "$0")" && pwd); CAT=$W/inputs/source-2650.json.gz
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p "$OUT/bb"; cd "$OUT" || exit 2
st() { echo "$(date +%F' '%T) $*" >> status; }
cp "$BB/master.json" bb/master.json
EX=$(python3 -c "import json;print(json.load(open('bb/master.json'))['extra'])"); V=$(basename "$(dirname "$EX")")
find "$BB" -maxdepth 1 -name 'ctx-*.json.gz' -mmin +2 -printf '%f\n' | sort > all_now.txt
for p in "$@"; do ls "$p" | grep '^ctx-'; done | sort -u > prev.txt
comm -23 all_now.txt prev.txt > new.txt
while read -r f; do cp --preserve=timestamps "$BB/$f" bb/; done < new.txt
sha256sum bb/master.json > master.sha256; st "snapshot rows=$V new_ctx=$(wc -l < new.txt) closed_now=$(wc -l < all_now.txt)"
$PY -I "$T/prep_rows.py" "$CAT" "$EX" "rows-$V.txt" > "prep-$V.json"; st "prep rc=$?"
g++ -O2 -std=c++17 -Wall -Wextra -o tcheck_b35 "$T/tcheck_b35.cpp" -lz -pthread; sha256sum tcheck_b35 >> master.sha256
/usr/bin/time -v ./tcheck_b35 "rows-$V.txt" bb 1 tc "$CAT" "$EX" > tc.stdout 2> tc.time; st "tcheck rc=$? (a partial packet: missing ctx files are expected problems)"
/usr/bin/time -v $PY -I "$T/pycheck_b35.py" "$CAT" "$EX" bb py.tsv all partial > py.log 2> py.time; st "pycheck rc=$?"
$PY -I "$T/compare_py.py" tc.contexts.tsv py.tsv > compare.txt 2>&1; st "compare rc=$?"
awk -F'\t' 'NR>1 && $10 !~ /file missing/ {n++; nodes+=$2; if ($9 != 0) bad++} END {printf "tcheck present ctx %d nodes %d with errors %d\n", n, nodes, bad}' tc.contexts.tsv > result.txt
awk -F'\t' '$1 != "master" {n++; nodes+=$2; if ($6 != 0) bad++; if ($4 == "None" || $4 < 1) low++} END {printf "pycheck ctx %d nodes %d with errors %d margin<1 %d\n", n, nodes, bad, low}' py.tsv >> result.txt
tail -1 compare.txt >> result.txt; st "DONE $(tr '\n' ';' < result.txt)"
