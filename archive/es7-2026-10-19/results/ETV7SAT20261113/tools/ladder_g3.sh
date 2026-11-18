#!/bin/bash
# ladder_g3.sh TAG "N1 N2 ..." TLIM "GENERATOR FLAGS" [HEAP_MB]: as ladder_g.sh, but memory-policy
# conformant: CaDiCaL in this unit (about 1.1 GB for the --nosig CNF), cake_lpr in a separate
# nov13c-vfy-e7-* unit with a bounded heap (vfy.sh).
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
tag=$1; Ns=$2; tl=$3; flags=$4; heap=${5:-2600}
for N in $Ns; do
  name=lad_${tag}_N$N
  $PY owner.py 3 5 7 $N om/$name.base.cnf --names $flags > run/$name.gen.log 2>&1
  $PY addrows.py om/$name.base.cnf run/$name.cnf S1:25 S2:25 B1:16 B2:16 ALL:$N >> run/$name.gen.log 2>&1
  rm -f om/$name.base.cnf om/$name.base.cnf.names.pkl
  cadical -t $tl --lrat --no-binary $CADOPTS run/$name.cnf run/$name.lrat > run/$name.log 2>&1
  ec=$?
  if [ $ec -ne 20 ] && [ $ec -ne 10 ]; then rm -f run/$name.lrat; fi
  if [ $ec -eq 10 ]; then grep -E "^v " run/$name.log > run/$name.model; rm -f run/$name.lrat; fi
  ./finish_run.sh $tag $N "$flags" $heap
done
