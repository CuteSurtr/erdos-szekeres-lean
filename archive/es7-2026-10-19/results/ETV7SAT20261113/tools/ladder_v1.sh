#!/bin/bash
# ladder.sh TAG "N1 N2 ..." TLIM [--nosig]: owner model (3,5,7,N) + rows S1,S2,B1,B2,ALL:N,
# CaDiCaL 2.1.3 --lrat, cake_lpr.  One line per N in run/ladder_TAG.log.
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
tag=$1; Ns=$2; tl=$3; sig=$4
for N in $Ns; do
  name=lad_${tag}_N$N
  $PY owner_v1.py 3 5 7 $N om/$name.base.cnf --names $sig > run/$name.gen.log 2>&1
  $PY addrows.py om/$name.base.cnf run/$name.cnf S1:25 S2:25 B1:16 B2:16 ALL:$N >> run/$name.gen.log 2>&1
  rm -f om/$name.base.cnf
  ./solve_lrat2.sh $name $tl
  v=$(grep -c "s VERIFIED UNSAT" run/$name.cake 2>/dev/null)
  echo "N=$N $(head -1 run/$name.out) $(tail -1 run/$name.out) verified=$v $(grep -E 'lrat_bytes|cake_wall' run/$name.cake 2>/dev/null | tr '\n' ' ') conflicts=$(grep -E '^c conflicts:' run/$name.log | awk '{print $3}') cnf_sha=$(sha256sum run/$name.cnf | cut -c1-64)" >> run/ladder_$tag.log
  if [ "$v" = "1" ]; then rm -f run/$name.lrat; fi
done
