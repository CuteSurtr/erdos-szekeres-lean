#!/bin/bash
# lrev launcher: gate (no YIELD, Tctl < 86 C; poll 60 s, at most 30 min), hash the worker's oleans, closure pre-check,
# the ONE unit esr-ag-lrev-axioms (Review.lean), hash the worker's oleans again, closure post-check.
set -u
R=/home/jay/research/data/formalize-20261122/comp-audit/review
W=/home/jay/research/data/formalize-20261122/comp-audit
cd $R
log() { echo "$(date '+%F %T %Z') $*" | tee -a $R/launch.log; }
tctl() { sensors 2>/dev/null | awk '/Tctl/{gsub(/[+°C]/,"",$2); print $2; exit}'; }
i=0
until [ ! -e /home/jay/research/data/agents-20261121/YIELD ] && awk -v t="$(tctl)" 'BEGIN{exit !(t+0 < 86)}'; do
  i=$((i+1)); [ $i -gt 30 ] && { log "gate unmet for 30 min; not started"; exit 3; }
  log "waiting: YIELD $( [ -e /home/jay/research/data/agents-20261121/YIELD ] && echo yes || echo no ), Tctl $(tctl)"; sleep 60
done
systemctl --user is-active --quiet esr-ag-lrev-axioms && { log "unit already active; refused"; exit 4; }
sha256sum $W/out/olean/*.olean > $R/worker_oleans_before.sha256
python3 -I -B $R/closure_check.py pre > $R/closure_pre.out 2>&1 || { log "closure pre-check failed; not started"; exit 5; }
LP=$(python3 -I -c "import json; print(json.load(open('$R/closure_pre.json'))['lean_path'])")
log "gate ok (Tctl $(tctl)); closure pre-check ok; starting esr-ag-lrev-axioms"
systemd-run --user --wait --collect --unit=esr-ag-lrev-axioms -p CPUQuota=100% -p MemoryMax=3500M \
  -p MemorySwapMax=0 -p RuntimeMaxSec=7200 --nice=10 --working-directory=$R \
  -E LEAN_PATH=$LP -E LEAN_NUM_THREADS=1 /bin/sh $R/unit_review.sh $R/review.log > $R/systemd_run.out 2>&1
rc=$?
log "unit finished: systemd-run rc $rc; $(grep -E '^lean_rc=' $R/review.log)"
sha256sum $W/out/olean/*.olean > $R/worker_oleans_after.sha256
cmp -s $R/worker_oleans_before.sha256 $R/worker_oleans_after.sha256 && log "worker oleans unchanged" || log "WORKER OLEANS CHANGED"
python3 -I -B $R/closure_check.py post > $R/closure_post.out 2>&1; log "closure post-check rc $? $(cat $R/closure_post.out)"
exit $rc
