#!/bin/bash
# Reviewer rv5 driver (a waiter, no compute): after e1c ends, run e1r (gated unit), then cake (gated unit).
# Bounded: each wait at most 100 min. Log: review/driver.log.
V=/home/jay/research/data/formalize-20261122/n66-l15-rows/review
log() { echo "$(date '+%F %T') $*" >> $V/driver.log; }
waitu() { for i in $(seq 1 600); do systemctl --user is-active -q esr-ag-rv5-$1 || return 0; sleep 10; done; log "timeout waiting for $1"; exit 3; }
waitu e1c; log "e1c ended: $(cat $V/peak_e1c.txt 2>/dev/null)"
$V/unit.sh e1r 5G 3600 3300 /usr/bin/python3 -I $V/own_e1r.py >> $V/driver.log 2>&1 || { log "e1r launch failed"; exit 1; }
sleep 5; waitu e1r; log "e1r ended: $(cat $V/peak_e1r.txt 2>/dev/null)"
$V/unit.sh cake 4G 3600 2600 $V/own_cake.sh >> $V/driver.log 2>&1 || { log "cake launch failed"; exit 1; }
sleep 5; waitu cake; log "cake ended: $(cat $V/peak_cake.txt 2>/dev/null)"
log "driver done"
