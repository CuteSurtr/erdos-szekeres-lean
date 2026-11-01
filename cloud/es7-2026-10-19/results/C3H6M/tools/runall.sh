S=/tmp/claude-0/-home-user-erdos-szekeres-lean/1128a15e-b92d-5b38-9916-29badb00b748/scratchpad
R=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results
O=$R/C3H6M/logs/compose; mkdir -p $O $S/dump
for set in fix1A fix1B setT; do
  F=$(cat $S/$set.list)
  python3 $R/C3H6M/tools/c3t_dump.py $R/C3T/tools $S/dump/${set}_c3t_off $S/base.cnf $F > $O/${set}_c3t_off.json 2>&1
  python3 $R/C3H6M/tools/c3t_dump.py $R/C3T/tools $S/dump/${set}_c3t_on $S/base.cnf $F --mirror-h6 > $O/${set}_c3t_on.json 2>&1
  python3 $R/C3H6M/tools/mycompose.py --dump $S/dump/${set}_my_off $F > $O/${set}_my_off.json 2>&1
  python3 $R/C3H6M/tools/mycompose.py --h6m --dump $S/dump/${set}_my_on $F > $O/${set}_my_on.json 2>&1
done
echo DONE
