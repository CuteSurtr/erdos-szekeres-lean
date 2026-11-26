#!/bin/bash
# resolve-queue-20261126: generic re-solve driver. usage: run_queue.sh SETDIR JOBS UNIT_MEM_GB
# SETDIR/jobs.tsv rows: id <TAB> cnf path <TAB> recorded cnf sha256 <TAB> cake heap MB. One unit per job
# (esr-n66-<set>-<id>: the re-solve budget, guard track n66), at most JOBS at once counted over ALL re-solve units
# (esr-n66-*, esr-vfy-n66-*), so it never adds to a running N66 re-solve beyond JOBS. Skips a job whose certify.jsonl
# already has the exact verdict or whose unit is active; a hash mismatch skips the job (logged). Proofs kept (.lrat.zst).
set -u
S=$1; J=$2; M=$3; set_=$(basename $S)
CERT=/home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/certify_cnf.sh
log() { echo "$(date '+%F %T') $*" >> "$S/run.log"; }
active() { systemctl --user list-units 'esr-n66-*' 'esr-vfy-n66-*' --state=active,activating --no-legend --plain | wc -l; }
log "start JOBS=$J MEM=${M}G; cadical $(cadical --version 2>&1 | head -1); cake_lpr $(sha256sum ~/.local/bin/cake_lpr | cut -c1-16)"
while IFS=$'\t' read -r id cnf want heap; do
  out=$S/out/$id; u=esr-n66-$set_-$id
  grep -qs '"verdict":"s VERIFIED UNSAT"' "$out/certify.jsonl" && continue
  systemctl --user is-active -q $u && continue
  got=$(sha256sum "$cnf" | cut -d' ' -f1)
  [ "$got" = "$want" ] || { log "HASH MISMATCH $id $got"; continue; }
  while [ "$(active)" -ge "$J" ]; do sleep 60; done
  systemd-run --user --unit=$u --collect -q -p CPUQuota=100% -p MemoryMax=${M}G -p MemorySwapMax=0 \
    -p RuntimeMaxSec=43200 --nice=10 --working-directory=$S bash "$CERT" "$cnf" "$out" "$heap" --keep
  log "launched $id"; sleep 5
done < "$S/jobs.tsv"
while [ "$(systemctl --user list-units "esr-n66-$set_-*" --state=active --no-legend --plain | wc -l)" -gt 0 ]; do sleep 60; done
log "all launched jobs finished"
