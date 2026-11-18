#!/bin/bash
# encoding / heuristic experiments on the (7;5,6) owner model, N=26 (no proofs; COMPUTED only)
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
mkdir -p exp
out=exp/exp56.log
run_cad() { # name cnf [opts]
  n=$1; c=$2; shift; shift
  s=$(date +%s.%N); r=$(timeout 400 cadical -q "$@" $c | head -1); e=$(date +%s.%N)
  echo "$n cadical213 $* : $r $(echo "$e - $s" | bc)" >> $out
}
run_occ() { # name cnf prio [opts]
  n=$1; c=$2; p=$3; shift; shift; shift
  r=$(drv/occfirst $c $p - 400 "$@" | grep -E "^s |^c conflicts:|solve wall" | tr '\n' ' ')
  echo "$n occfirst301 $p $* : $r" >> $out
}
$PY owner.py 3 4 7 26 exp/s56_nosig.cnf --names --nosig > exp/gen_nosig.log
$PY owner.py 3 4 7 26 exp/s56_nowit.cnf --names --nowit > exp/gen_nowit.log
$PY owner.py 3 4 7 26 exp/s56_nocorner.cnf --names --nocorner > exp/gen_nocorner.log
$PY addrows.py om/s56_N26.cnf exp/s56_rows.cnf B1:15 > exp/gen_rows.log
for m in asc desc ascneg descneg ascP; do $PY prio.py om/s56_N26.cnf $m > exp/prio_$m.txt; done
: > exp/empty.txt
run_cad nosig exp/s56_nosig.cnf
run_cad nowit exp/s56_nowit.cnf
run_cad nocorner exp/s56_nocorner.cnf
run_occ base301 om/s56_N26.cnf exp/empty.txt
run_occ desc om/s56_N26.cnf exp/prio_desc.txt
run_occ ascneg om/s56_N26.cnf exp/prio_ascneg.txt
run_occ descneg om/s56_N26.cnf exp/prio_descneg.txt
run_occ ascP om/s56_N26.cnf exp/prio_ascP.txt
run_cad unsat om/s56_N26.cnf --unsat
run_cad noelim om/s56_N26.cnf --no-elim
run_occ nosig_asc exp/s56_nosig.cnf exp/prio_asc.txt
echo done >> $out
