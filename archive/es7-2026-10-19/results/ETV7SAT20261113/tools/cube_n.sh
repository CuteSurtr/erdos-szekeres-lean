#!/bin/bash
# cube_n.sh NAME N TLIM "ROWSPEC" "GENERATOR FLAGS" [HEAP]: one case of a split of rung N.
# The CNF is the owner model (3,5,7,N) with the given rows (e.g. "S1:25 S2:25 B1:16 B2:13 ALL:36").
# CaDiCaL 2.1.3 --lrat here; cake_lpr via vfy.sh in its own unit.  Result line in run/cubes.log.
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
name=$1; N=$2; tl=$3; rows=$4; flags=$5; heap=${6:-2600}
$PY owner.py 3 5 7 $N om/$name.base.cnf --names $flags > run/$name.gen.log 2>&1
$PY addrows.py om/$name.base.cnf run/$name.cnf $rows >> run/$name.gen.log 2>&1
rm -f om/$name.base.cnf om/$name.base.cnf.names.pkl
cadical -t $tl --lrat --no-binary run/$name.cnf run/$name.lrat > run/$name.log 2>&1
ec=$?
grep -E "^s " run/$name.log > run/$name.out
echo "exit=$ec cadical_wall=$(grep -E 'total real time since initialization' run/$name.log | awk '{print int($(NF-1))}') $(date)" >> run/$name.out
if [ $ec -eq 20 ]; then ./vfy.sh $name $heap; else rm -f run/$name.lrat; fi
if [ $ec -eq 10 ]; then grep -E "^v " run/$name.log > run/$name.model; fi
v=$(grep -c "s VERIFIED UNSAT" run/$name.cake 2>/dev/null)
echo "name=$name N=$N rows=[$rows] flags=[$flags] $(head -1 run/$name.out) $(tail -1 run/$name.out) verified=$v $(grep -E 'lrat_bytes|cake_wall' run/$name.cake 2>/dev/null | tail -2 | tr '\n' ' ') conflicts=$(grep -E '^c conflicts:' run/$name.log | awk '{print $3}') cnf_sha=$(sha256sum run/$name.cnf | cut -c1-64) lrat_sha=$(grep '\.lrat' run/$name.cake 2>/dev/null | tail -1 | cut -c1-64)" >> run/cubes.log
if [ "$v" -ge 1 ]; then rm -f run/$name.lrat; fi
