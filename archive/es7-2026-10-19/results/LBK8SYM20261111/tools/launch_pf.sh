#!/bin/bash
# usage: launch_pf.sh NAME MEM M TMAX [pfenc args...]   (one thread, in the capped lbk8sym slice)
D=/home/jay/research/data/lb-k8sym-20261111
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
NAME=$1; MEM=$2; M=$3; TMAX=$4; shift 4
systemd-run --user --unit=lb-k8sym-$NAME --slice=lbk8sym.slice -p CPUQuota=100% -p MemoryMax=$MEM -p Nice=10 \
  --working-directory=$D $PY -u $D/cegar/pfenc.py --m $M --out $D/cegar/$NAME --tag $NAME --tmax $TMAX "$@"
