#!/bin/bash
# After run_small.sh (cmp, sigA, sigB): C3U's checks with the C3U2 tools.  usage: post_small.sh W
W=$1; H=$(dirname $(readlink -f $0)); T=$(readlink -f $H/../tools); C3U=$(readlink -f $H/../../C3U)
L=$H/logs
python3 $H/compare_small.py $W > $L/compare_small.txt 2>&1; echo "compare_small rc=$?"
: > $L/check_small.txt; : > $L/same_as_C3U.txt
for x in "6 6 300 2" "7 6 300 2" "7 6 300 3" "7 6 100 2" "8 6 300 2" "8 6 300 3"; do set -- $x
  r=sig_m$1k$2c$3K$4
  python3 $H/check_small.py $T $1 $2 $W/base_m$1k$2.cnf $W/$r.jsonl >> $L/check_small.txt 2>&1
  python3 $H/same_records.py $W/$r.jsonl $C3U/tests/logs/small/$r.jsonl >> $L/same_as_C3U.txt
done
for x in cmp_m6k6c300 cmp_m7k6c3000 cmp_m7k6c300 cmp_m8k6c3000; do for s in new new0 old; do
  python3 $H/same_records.py $W/${x}_$s.jsonl $C3U/tests/logs/small/${x}_$s.jsonl >> $L/same_as_C3U.txt; done; done
: > $L/compose_reject.txt
for x in "6 6 300 2 m6K2" "7 6 300 3 m7K3" "8 6 300 3 m8K3"; do set -- $x
  echo "== sig_m$1k$2c$3K$4" >> $L/compose_reject.txt
  python3 $H/compose_reject.py $T $1 $2 $W/base_m$1k$2.cnf $W/sig_m$1k$2c$3K$4.jsonl $W/mut_$5 >> $L/compose_reject.txt 2>&1
done
bash $H/restart_test.sh $W 6 6 300 2 40 > $L/restart_test.txt 2>&1
echo "restarted run vs uninterrupted: $(python3 $H/same_records.py $W/restart_m6k6c300K2_N40.jsonl $W/sig_m6k6c300K2.jsonl)" >> $L/restart_test.txt
grep -c '"result": "OK"' $L/check_small.txt; grep FAILURES $L/compose_reject.txt; grep -c '"equal": true' $L/same_as_C3U.txt; tail -1 $L/restart_test.txt
