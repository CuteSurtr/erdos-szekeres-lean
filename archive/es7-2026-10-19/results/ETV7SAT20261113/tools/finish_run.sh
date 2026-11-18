#!/bin/bash
# finish_run.sh TAG N "FLAGS" [HEAP_MB]: after cadical has ended for run/lad_TAG_N$N (wrapper frozen
# or absent): record the verdict, verify in a vfy unit, append the ladder line, delete a verified LRAT.
tag=$1; N=$2; flags=$3; heap=${4:-2600}
name=lad_${tag}_N$N
grep -E "^s " run/$name.log > run/$name.out
ec=$(grep -E "^c exit" run/$name.log | awk '{print $3}')
echo "exit=${ec:-0} cadical_wall=$(grep -E 'total real time since initialization' run/$name.log | awk '{print int($(NF-1))}') $(date)" >> run/$name.out
if [ "$ec" = "20" ]; then ./vfy.sh $name $heap; fi
v=$(grep -c "s VERIFIED UNSAT" run/$name.cake 2>/dev/null)
echo "N=$N flags=[$flags] $(head -1 run/$name.out) $(tail -1 run/$name.out) verified=$v $(grep -E 'lrat_bytes|cake_wall' run/$name.cake 2>/dev/null | tail -2 | tr '\n' ' ') conflicts=$(grep -E '^c conflicts:' run/$name.log | awk '{print $3}') cnf_sha=$(sha256sum run/$name.cnf | cut -c1-64)" >> run/ladder_$tag.log
if [ "$v" -ge 1 ]; then rm -f run/$name.lrat; fi
