#!/bin/bash
# n66-resolve-20261125 (PLAN.md): re-solve the 105 level-15 N66 cube leaves with the house certify script, one unit per
# leaf (esr-n66-* since 26 Nov 00:1x, track n66; before: esr-vfy-n66-*; 1 thread, MemoryMax 6G), at most JOBS at once. Each trim.cnf is re-hashed against the receipt
# first; a mismatch skips the leaf and is logged. Results: out/<dir>/certify.jsonl; tally with tally.py.
set -u
O=/home/jay/research/data/n66-resolve-20261125; N=/home/jay/research/data/n66-20261113; JOBS=${1:-4}
CERT=/home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/certify_cnf.sh
log() { echo "$(date '+%F %T') $*" >> "$O/run.log"; }
active() { systemctl --user list-units 'esr-vfy-n66-*' 'esr-n66-*' --state=active,activating --no-legend --plain | wc -l; }
log "start JOBS=$JOBS; cadical $(cadical --version 2>&1 | head -1); cake_lpr $(sha256sum ~/.local/bin/cake_lpr | cut -c1-16)"
while IFS=$'\t' read -r dir want bytes; do
  id=$(echo "$dir" | sed -E 's#^p2/##; s#/it1$##; s#/#_#g'); out=$O/out/$id
  grep -qs '"verdict":"s VERIFIED UNSAT"' "$out/certify.jsonl" && continue
  # a leaf whose unit (old or new name) is still active is running: never launch it twice (26 Nov 00:1x incident)
  systemctl --user is-active -q esr-n66-$id esr-vfy-n66-$id && continue
  got=$(sha256sum "$N/$dir/trim.cnf" | cut -d' ' -f1)
  [ "$got" = "$want" ] || { log "HASH MISMATCH $dir $got"; continue; }
  while [ "$(active)" -ge "$JOBS" ]; do sleep 30; done
  systemd-run --user --unit=esr-n66-$id --collect -q -p CPUQuota=100% -p MemoryMax=6G -p MemorySwapMax=0 \
    -p RuntimeMaxSec=21600 --nice=10 --working-directory=$O bash "$CERT" "$N/$dir/trim.cnf" "$out" 4000 --keep
  log "launched $id (old proof $bytes B)"; sleep 5
done < "$O/leaves.tsv"
while [ "$(active)" -gt 0 ]; do sleep 60; done
log "all launched leaves finished"
