#!/bin/bash
# usage: launch.sh job cpu% mem mode pts K seed ncand  -> systemd user unit esr-sat-<job>, ends by 12:00 KST
W=/home/jay/research/data/roadmap-20261115/pm1115/sat3
BIN=${BIN:-sat3ls}; job=$1 cpu=$2 mem=$3 mode=$4 pts=$5 k=$6 seed=$7 nc=${8:-8}
end=$(date -d '2026-11-18 12:00' +%s); secs=$(( end - $(date +%s) ))
mkdir -p $W/runs/$job
systemd-run --user --unit=esr-sat-$job -p CPUQuota=$cpu% -p MemoryMax=$mem -p MemorySwapMax=0 -p RuntimeMaxSec=$((secs + 60)) \
  --nice=10 --working-directory=$W -E OPENBLAS_NUM_THREADS=1 -E OMP_NUM_THREADS=1 -E MKL_NUM_THREADS=1 -E NCAND=$nc -E STALL=${STALL:-1500} -E KICKP=${KICKP:-0.5} -E SYMG=${SYMG:-4} -E OVER=${OVER:-3} \
  $W/$BIN $mode $pts $k runs/$job $seed $secs ${@:9}
