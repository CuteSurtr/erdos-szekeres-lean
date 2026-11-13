#!/bin/bash
# usage: launch_anneal.sh NAME M T CENTRE(0/1) HOURS SEED ANSATZ [extra args]
# runs one single-threaded annealer in the lb-k8sym slice (capped as a whole: CPUQuota 800%, MemoryMax 16G)
D=/home/jay/research/data/lb-k8sym-20261111
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
NAME=$1; M=$2; T=$3; C=$4; H=$5; SEED=$6; AN=$7; shift 7
CF=""; [ "$C" = "1" ] && CF="--centre"
systemd-run --user --unit=lb-k8sym-$NAME --slice=lbk8sym.slice -p CPUQuota=100% -p MemoryMax=2G -p Nice=10 \
  --working-directory=$D $PY -u $D/py/annealm.py --m $M --t $T $CF --out $D/runs/$NAME --seed $SEED --ansatz $AN --hours $H --tag $NAME "$@"
