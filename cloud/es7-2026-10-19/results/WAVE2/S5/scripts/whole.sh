# whole.sh CASE : 120 s CaDiCaL with LRAT, then cake_lpr
c=$1; w=$(mktemp -d /opt/work/tmp/whole_${c}_XXXX); f=/opt/work/cases/$c.cnf
t0=$(date +%s.%N); /opt/work/bin/cadical --lrat --binary=false -q -t 120 $f $w/p.lrat > $w/out; rc=$?; t1=$(date +%s.%N)
v="-"; t2=$t1
if [ $rc = 20 ]; then v=$(/opt/work/bin/cake_lpr $f $w/p.lrat | grep '^s ' | head -1); t2=$(date +%s.%N); fi
[ $rc = 10 ] && cp $w/out /opt/work/whole_${c}.SAT.out
echo "$c rc=$rc solve=$(echo "$t1-$t0"|bc) check=$(echo "$t2-$t1"|bc) cake=[$v]" >> /opt/work/whole.log
rm -rf $w
