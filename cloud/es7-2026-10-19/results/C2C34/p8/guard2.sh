#!/bin/bash
# Memory guard (vm_stat based). used = active + wired + compressed pages. Above 30 GB used: create p8/STOP (solver lanes
# stop claiming); below 26 GB: remove it. Above 38 GB: kill the newest P8 solver CaDiCaL, then the newest cube solver.
P8=${WORK:?set WORK to the work directory}/c2c/p8; END=$1
while [ "$(date +%s)" -lt $END ]; do
  used=$(vm_stat | awk '/Pages (active|wired down|occupied by compressor)/ {gsub("\\.","",$NF); s+=$NF} END {printf "%d", s*16384/1e9}')
  if [ $used -gt 30 ] && [ ! -e $P8/STOP ]; then touch $P8/STOP; echo "$(date -u +%H:%M:%S) used ${used}GB: STOP" >> $P8/guard.log; fi
  if [ $used -lt 26 ] && [ -e $P8/STOP ]; then rm -f $P8/STOP; echo "$(date -u +%H:%M:%S) used ${used}GB: resume" >> $P8/guard.log; fi
  if [ $used -gt 38 ]; then
    pid=$(ps -axo pid=,command= | awk '/local\/bin\/cadical/ && /p8\/work/ && !/awk/ {print $1}' | sort -n | tail -1)
    [ -z "$pid" ] && pid=$(ps -axo pid=,command= | awk '/local\/bin\/cadical/ && /cs\/cube_/ && !/awk/ {print $1}' | sort -n | tail -1)
    [ -n "$pid" ] && kill $pid && echo "$(date -u +%H:%M:%S) used ${used}GB: killed $pid" >> $P8/guard.log
  fi
  sleep 15
done
