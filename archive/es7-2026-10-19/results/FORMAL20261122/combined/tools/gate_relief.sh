#!/bin/bash
# gate_relief.sh (26 Nov 2026): while the part-3 chain (esr-vfy-p3chain) runs, if one of its gated launches has
# waited 10 or more polls at start3.sh's gate (logs/gates3.log, "gate wait N for JOB"), freeze the exploratory
# budget-70 finder (esr-bal-zbs70, 16 threads; systemd freezer, no work lost) so that Tctl can fall below the
# gate's 86 C; thaw it as soon as the gate reports "gate ok". Never touches the gate, the YIELD file or the chain.
# Log: logs/gate_relief.log. Ends (thawing first) when the chain unit is inactive.
W=/home/jay/research/data/formalize-20261122/combined; G=$W/logs/gates3.log; L=$W/logs/gate_relief.log; U=esr-bal-zbs70
log() { echo "$(date '+%F %T') $*" >> $L; }
frozen() { [ "$(systemctl --user show $U -p FreezerState --value)" = frozen ]; }
log "start (chain active: $(systemctl --user is-active esr-vfy-p3chain))"
while systemctl --user is-active -q esr-vfy-p3chain; do
  last=$(tail -1 $G)
  n=$(sed -n 's/.* gate wait \([0-9]*\) for .*/\1/p' <<< "$last")
  if [ -n "$n" ] && [ "$n" -ge 10 ] && ! frozen && systemctl --user is-active -q $U; then
    systemctl --user freeze $U && log "froze $U ($last)"
  elif [[ "$last" == *"gate ok"* ]] && frozen; then
    systemctl --user thaw $U && log "thawed $U ($last)"
  fi
  sleep 30
done
frozen && systemctl --user thaw $U && log "thawed $U (chain ended)"
log "end"
