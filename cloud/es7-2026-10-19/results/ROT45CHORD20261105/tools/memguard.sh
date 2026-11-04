#!/bin/bash
# kill the youngest cadical lane if MemAvailable < 3 GB (prevents the kernel OOM killer from choosing at random)
cd <rot45-work-dir>; dl=$(cat deadline)
while [ $(date +%s) -lt $dl ]; do
  avail=$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)
  if [ $avail -lt 3 ]; then
    p=$(ps -eo pid,etimes,args --sort=etimes | awk '$3=="cadical"{print $1; exit}')
    a=$(ps -o args= -p $p)
    kill $p; echo "$(date +%H:%M:%S) MemAvailable ${avail}G: killed youngest lane $p ($a)" >> memguard.log
    printf "%s\tKILLED-FOR-MEMORY\t-\t-\t-\n" "$(basename $(echo $a | awk '{print $NF}') .lrat)" >> results.tsv
    sleep 30
  fi
  sleep 15
done
