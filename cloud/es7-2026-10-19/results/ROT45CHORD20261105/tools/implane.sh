#!/bin/bash
f=$1; b=${f%.cnf}
timeout 600 cadical --lrat --binary=false -q $f $b.lrat > $b.out 2>&1
res=$(grep -m1 -E '^s ' $b.out | cut -c3-)
chk=$(timeout 900 lrat-check $f $b.lrat 2>&1 | grep -o -m1 -E 'VERIFIED|FAILED' || echo none)
printf "%s\t%s\t%s\n" "$f" "$res" "$chk" >> imp_results.tsv
[ "$res" = "UNSATISFIABLE" ] && [ "$chk" = "VERIFIED" ] && rm -f $f $b.lrat
