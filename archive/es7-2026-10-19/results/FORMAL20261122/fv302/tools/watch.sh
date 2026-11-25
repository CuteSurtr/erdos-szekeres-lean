#!/bin/bash
# Watcher (24 Nov): exits (= wakes the main session) on a real problem only. Axiom ALERT lines of drive302 are checked
# with axiom_audit.py (profiler text inside axiom lines is a known false alarm); a failing audit, a STOP file, an
# inactive driver or guard, or the time limit ends the watch. Usage: watch.sh SECONDS
W=/home/jay/research/data/fv302-20261124; D=/home/jay/research/data/formalize-20261122/res-slices-fv
t0=$(date +%s); seen=$(grep -c ALERT $W/logs/driver.log)
while [ $(( $(date +%s) - t0 )) -lt $1 ]; do
  [ -e $W/STOP ] && { echo "STOP file in FV302: $(cat $W/STOP)"; exit 0; }
  [ -e $D/STOP ] && { echo "STOP file in s35_20: $(cat $D/STOP)"; exit 0; }
  for u in esr-fv2-drv esr-fvr-drv esr-ygd-guard esr-memguard-1125a esv-memguard-1122c; do
    systemctl --user is-active -q $u || { echo "unit $u is not active"; exit 0; }
  done
  n=$(grep -c ALERT $W/logs/driver.log)
  if [ $n -gt $seen ]; then
    while read -r line; do
      m=$(echo "$line" | sed -n 's/.*ALERT \(C[0-9]*\): [0-9]* axiom lines are not the standard three.*/\1/p')
      if [ -n "$m" ] && python3 -I $W/tools/axiom_audit.py $W/logs/lean/$m.log > /dev/null; then
        echo "$(date '+%F %T') $m: axiom ALERT is profiler interleaving (audit passes)" >> $W/logs/false_alerts.log
      else
        echo "REAL ALERT: $line"; exit 0
      fi
    done < <(grep ALERT $W/logs/driver.log | tail -n $((n - seen)))
    seen=$n
  fi
  sleep 60
done
echo "watch limit reached"
