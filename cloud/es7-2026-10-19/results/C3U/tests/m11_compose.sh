#!/bin/bash
# compose.py of C3T and of C3U on the m = 11 records (real base, sha check on), paths relative to
# cloud/es7-2026-10-19.  A: the 79 files of results/C3T/tests/logs/files_setB.txt (C3WAVE1,
# C3WAVE2, C3S0); B: A + every results/C3W3/*/out.jsonl of the checkout; S: results/C3SIG/*/out.jsonl;
# S and B+S with C3U only.  Output: logs/m11_compose_*.txt
R=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19
BASE=${1:-/opt/work/base.cnf}; L=$R/results/C3U/tests/logs
cd $R
cp results/C3T/tests/logs/files_setB.txt $L/m11_files_A.txt
{ cat $L/m11_files_A.txt; ls results/C3W3/*/out.jsonl; } > $L/m11_files_B.txt
ls results/C3SIG/*/out.jsonl > $L/m11_files_S.txt
cat $L/m11_files_B.txt $L/m11_files_S.txt > $L/m11_files_BS.txt
git log -1 --format='checkout %H %cI' > $L/m11_compose_checkout.txt
run() { # SET TOOLS
  local s=$(date +%s)
  python3 results/$2/tools/compose.py $BASE $(cat $L/m11_files_$1.txt) > $L/m11_compose_$1_$2.txt 2>&1
  echo "rc $? wall $(( $(date +%s) - s )) s" >> $L/m11_compose_$1_$2.txt
}
run A C3T; run A C3U; run B C3T; run B C3U; run S C3U; run BS C3U
