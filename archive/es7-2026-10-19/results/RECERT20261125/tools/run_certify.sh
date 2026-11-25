#!/bin/bash
# resolve-sym-20261125 step 2 (PLAN.md): certify C5, C4 and D2 one after another with the house script
# (CaDiCaL 2.1.3 --lrat, then cake_lpr; the verdict counts only on the exact line "s VERIFIED UNSAT"; proofs kept as
# .lrat.zst). Each CNF is re-hashed against the record first. Heap per formula: C5 8000 (its own script's value),
# C4 4500 (default 4,096 MiB sufficed on the Mac), D2 4000 (the replay's value). Results in out/certify.jsonl.
set -u
O=/home/jay/research/data/resolve-sym-20261125; C=$O/cnf; OUT=$O/out; mkdir -p "$OUT"
CERT=/home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/certify_cnf.sh
log() { echo "$(date '+%F %T') $*" | tee -a "$OUT/run.log"; }
run() { f=$1 want=$2 heap=$3
  got=$(sha256sum "$C/$f" | cut -d' ' -f1)
  [ "$got" = "$want" ] || { log "HASH MISMATCH $f $got"; return 1; }
  log "start $f heap $heap"
  bash "$CERT" "$C/$f" "$OUT" "$heap" --keep; rc=$?
  log "end $f rc=$rc; cake: $(grep -m1 -E 's VERIFIED|exhausted|rror|FAIL' "$OUT/${f%.cnf}.cake.out" 2>/dev/null)"
}
log "cadical $(cadical --version 2>&1 | head -1); cake_lpr $(sha256sum ~/.local/bin/cake_lpr | cut -c1-16)"
run c4_n32L_cuts.cnf 2aa18f1e89152959c13adec575d3fda4a01b0dedaef2388984ba6fe6bfdb78d1 8000
run c5_n35L.cnf 90dea1cf87d3d8500dffff9d9741e84abc9babe4e1ac4e32035448ce7c0668a8 4500
run B_m7K8t10.cnf b4d290176cb675c61ecbcf70380cc520aabf093d00e2572328a0975ae2d296e2 4000
log "all done"
