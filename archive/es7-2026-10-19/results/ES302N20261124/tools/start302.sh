#!/bin/bash
# start302.sh (b69-prep, 22 Nov 2026): the steps that STATUS20261121_1930 section 6 ran by hand for 303, for the
# budget-69 tree. Run it as a small unit (README section 9); it may be started while the finder still runs.
#  1. waits until the finder unit is inactive; nothing under O is read or written before that;
#  2. requires the last finder entry of O/steps.log to be "occ (0 occupied) rc=0" and the last occ.out event DONE;
#  3. checks the pinned inputs (pins302.sha256);
#  4. writes the pre-registration O/prereg302.json (prereg302.py; files/nodes/leaves by the rule of ES303N section 5)
#     and logs it BEFORE any check runs; refuses if the HEURISTIC one_big projection exceeds 80 % of the assembly
#     unit's MemoryMax (the balcheck2 projection only withholds step 6, so check A still starts);
#  5. writes a fresh marker and starts the v5n54 assembly unit (as for 303: NW 10, NW_BIG 3, BIG_BYTES 10 MB,
#     SUB_NODES 30,000, MemoryMax 8G);
#  6. starts chain302.sh as its own unit (it waits for the assembly, checks it, runs balcheck2, logs the acceptance),
#     unless the balcheck2 projection exceeds 80 % of BC_MEM_MB at BC_T threads: then it logs the by-hand command with
#     the largest BC_T that fits.
# It pauses while agents-20261121/YIELD exists or Tctl >= 86 C before each start. The env overrides (B O WD FINDER_UNIT
# ASM_UNIT CHAIN_UNIT BC_UNIT ASM_Q ASM_MEM_MB NW NW_BIG ASM_CPUS ASM_RT BC_T BC_MEM_MB BC_CPUS BC_RT) exist for the
# dry run on the control tree and for a relaunch with other caps after a memory refusal.
set -u
P=/home/jay/research/data/bal186-20261119/b69prep; D=/home/jay/research/data/bal186-20261119/zrow
B=${B:-69}; O=${O:-$D/b69zs54}; L=$O/steps.log; M=$O/asm_v5n54_start.txt; WD=${WD:-$D}
FINDER_UNIT=${FINDER_UNIT:-esr-bal-zbs69}; ASM_UNIT=${ASM_UNIT:-esr-bal-zbs69asm}; CHAIN_UNIT=${CHAIN_UNIT:-esr-bal-chain302}
BC_UNIT=${BC_UNIT:-esr-bal-zbs69bc}; ASM_Q=${ASM_Q:-1000}; ASM_MEM_MB=${ASM_MEM_MB:-8192}; NW=${NW:-10}; NW_BIG=${NW_BIG:-3}
ASM_CPUS=${ASM_CPUS:-5-14}; ASM_RT=${ASM_RT:-43200}; BC_T=${BC_T:-4}; BC_MEM_MB=${BC_MEM_MB:-9000}; BC_CPUS=${BC_CPUS:-5-8}
BC_RT=${BC_RT:-14400}
gate() { while [ -e /home/jay/research/data/agents-20261121/YIELD ] || [ "$(sensors 2>/dev/null | awk '/^Tctl/ {gsub(/[^0-9.]/, "", $2); print int($2)}')" -ge 86 ] 2>/dev/null; do sleep 60; done; }
log() { echo "$(date '+%F %T') start302: $*" >> $L; }
until ! systemctl --user is-active -q $FINDER_UNIT; do sleep 60; done
last=$(grep -E 'start finder|occ \(0 occupied\) rc=' $L | tail -1)
case "$last" in *'occ (0 occupied) rc=0') ;; *) log "finder did not end with rc=0 (last entry: '$last'); nothing started"; exit 1;; esac
tail -1 $O/occ.out | grep -q '^{"event": "DONE"' || { log "last occ.out event is not DONE; nothing started"; exit 1; }
(cd / && sha256sum -c --quiet $P/pins302.sha256) >> $L 2>&1 || { log "pinned inputs changed (pins302.sha256); nothing started"; exit 1; }
python3 -I -B $P/prereg302.py $O/occ.out $O/occ/master.json $B > $O/prereg302.json; prc=$?
log "pre-registration rc=$prc sha256 $(sha256sum < $O/prereg302.json | cut -c1-64): $(python3 -I -B -c "import json; r=json.load(open('$O/prereg302.json')); print({k: r[k] for k in ('files', 'nodes', 'leaves', 'contexts', 'master_closed_leaves', 'largest_contexts', 'errors')})")"
[ $prc -eq 0 ] || { log "pre-registration found an inconsistency; nothing started"; exit 1; }
read a b sa sb t2 <<< "$(python3 -I -B -c "
import json; r = json.load(open('$O/prereg302.json')); n = [x[1] for x in r['largest_contexts']]
f = lambda t: round(6600 * sum(n[:t]) / 1646232)
a = round(2083 * sum(n[:$NW_BIG]) / 765389); b = f($BC_T)
t2 = max([t for t in range(1, $BC_T) if f(t) <= 0.8 * $BC_MEM_MB] or [0])
print(a, b, 'ok' if a <= 0.8 * $ASM_MEM_MB else 'over', 'ok' if b <= 0.8 * $BC_MEM_MB else 'over', t2)")"
log "HEURISTIC memory projection (b68-scaled): one_big top-$NW_BIG $a MB of ${ASM_MEM_MB}M: $sa; balcheck2 $BC_T threads $b MB of ${BC_MEM_MB}M: $sb"
[ "$sa" = ok ] || { log "one_big projection above 80 % of the assembly MemoryMax; nothing started (relaunch with a smaller NW_BIG)"; exit 1; }
gate
date '+%F %T' > $M
log "start assemble (v5n54 sha $(sha256sum < $P/balz_assemble_v5n54.py | cut -c1-12)..., NW=$NW NW_BIG=$NW_BIG BIG_BYTES=10000000 SUB_NODES=30000)"
systemd-run --user --unit=$ASM_UNIT -p CPUQuota=${ASM_Q}% -p MemoryMax=${ASM_MEM_MB}M -p MemorySwapMax=0 -p RuntimeMaxSec=$ASM_RT \
  --nice=10 --working-directory=$WD -E NW_BIG=$NW_BIG -E BIG_BYTES=10000000 -E SUB_NODES=30000 /usr/bin/taskset -c $ASM_CPUS \
  bash -c "python3 -I -B $P/balz_assemble_v5n54.py $B $O/occ - $O/files $NW > $O/assemble.out 2>&1; rc=\$?; echo \"\$(date '+%F %T') assemble+check_tree (v5n54) rc=\$rc \$(tail -c 700 $O/assemble.out)\" >> $L; exit \$rc"
log "assembly unit $ASM_UNIT started (rc $?)"
CH="systemd-run --user --unit=$CHAIN_UNIT -p CPUQuota=10% -p MemoryMax=200M -p MemorySwapMax=0 -p RuntimeMaxSec=86400 --nice=10 --working-directory=$WD -E B=$B -E O=$O -E WD=$WD -E ASM_UNIT=$ASM_UNIT -E BC_UNIT=$BC_UNIT -E BC_MEM=${BC_MEM_MB}M -E BC_CPUS=$BC_CPUS -E BC_RT=$BC_RT"
if [ "$sb" = ok ]; then
  $CH -E BC_T=$BC_T /bin/bash $P/chain302.sh
  log "chain unit $CHAIN_UNIT started (rc $?)"
else
  log "balcheck2 projection above 80 % of ${BC_MEM_MB}M at BC_T=$BC_T: chain302 NOT started (check A runs alone). By hand, during or after the assembly: $CH -E BC_T=$t2 /bin/bash $P/chain302.sh   (BC_T=$t2 is the largest that fits; 0 = none fits, and a larger MemoryMax needs the owner's OK)"
fi
