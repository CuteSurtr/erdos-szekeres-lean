#!/bin/bash
# After the v5 assembly unit ends: require its EXACT TREE line, 32,755-style file count = summary 'files', and no file
# older than the v5 start marker; then run balcheck2 (4 threads; measured 2.3 GB on the largest context) as its own unit.
D=/home/jay/research/data/bal186-20261119/zrow; O=$D/b68zs; L=$O/steps.log
CAT=/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json
until ! systemctl --user is-active -q esr-bal-zbs68asm; do sleep 30; done
line=$(grep 'assemble+check_tree (v5) rc=' $L | tail -1)
# 22 Nov 2026 fix: the v5 summary appended to steps.log spans several lines, so the label is not on the rc line;
# read rc from the log line and the label from files/summary.json (the 22 Nov 06:06 run hit this bug; see README §5).
lab=$(python3 -I -c "import json; print(json.load(open('$O/files/summary.json')).get('label',''))" 2>/dev/null)
if ! echo "$line" | grep -q 'rc=0 ' || ! echo "$lab" | grep -q '^EXACT TREE'; then echo "$(date '+%F %T') chain303: assembly did not pass; balcheck2 not started" >> $L; exit 1; fi
K=$(find $O/files -name 'ctx-*-zb68.json.gz' | wc -l)
S=$(python3 -I -c "import json; print(json.load(open('$O/files/summary.json'))['files'])")
old=$(find $O/files -name 'ctx-*-zb68.json.gz' ! -newer $O/asm_v5_start.txt | wc -l)
echo "$(date '+%F %T') chain303: files=$K summary_files=$S older_than_v5_start=$old" >> $L
if [ "$K" -ne "$S" ] || [ "$old" -ne 0 ]; then echo "$(date '+%F %T') chain303: file check failed; balcheck2 not started" >> $L; exit 1; fi
systemd-run --user --unit=esr-bal-zbs68bc -p CPUQuota=400% -p MemoryMax=8G -p MemorySwapMax=0 -p RuntimeMaxSec=14400 --nice=10 \
  --working-directory=$D -E BALCHECK_EXTRA_ROWS=$D/zzs_rows.json -E BALCHECK_LEMMA_PATHS=0:1 /usr/bin/taskset -c 5-8 \
  bash -c "$D/../balcheck/balcheck2 $CAT 68 $K 4 '$O/files/ctx-%d-zb68.json.gz' $O/balcheck.tsv > $O/balcheck.json 2> $O/balcheck.err; rc=\$?; echo \"\$(date '+%F %T') balcheck2 rc=\$rc \$(cat $O/balcheck.json)\" >> $L; exit \$rc"
echo "$(date '+%F %T') chain303: balcheck2 unit started (rc $?)" >> $L
