#!/bin/bash
# memory-aware scheduler: start pending cubes (5-fold first) while lanes < MAX and MemAvailable > MINGB
cd <rot45-work-dir>
MAX=20; MINGB=12; dl=$(cat deadline)
while [ $(date +%s) -lt $((dl-600)) ]; do
  running=$(ps -eo args | awk '$1=="cadical"' | wc -l)
  avail=$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)
  if [ $running -lt $MAX ] && [ $avail -gt $MINGB ]; then
    next=""
    for f in cubes5/*.cnf cubes4/*.cnf; do b=${f%.cnf}; [ -e $b.lock ] && continue; next=$f; break; done
    [ -z "$next" ] && { echo "$(date +%H:%M) all cubes started"; break; }
    touch ${next%.cnf}.lock; setsid nohup ./lane.sh $next > /dev/null 2>&1 &
    echo "$(date +%H:%M) started $next (running $running, avail ${avail}G)"
    sleep 20; continue
  fi
  sleep 60
done
