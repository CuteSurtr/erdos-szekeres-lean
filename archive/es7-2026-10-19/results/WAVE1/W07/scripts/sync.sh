#!/bin/bash
# copy run records into the results dir, commit and push
cd /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19
cp /sandbox/058c295a-3faa-5b75-9cfa-a2ae73282e6d/scratchpad/run_U_L2/leaves.jsonl results/WAVE1/W07/U_L2/ 2>/dev/null
for f in leaves.icnf open.icnf; do [ -f /sandbox/058c295a-3faa-5b75-9cfa-a2ae73282e6d/scratchpad/run_U_L2/$f ] && cp /sandbox/058c295a-3faa-5b75-9cfa-a2ae73282e6d/scratchpad/run_U_L2/$f results/WAVE1/W07/U_L2/; done
ls /sandbox/058c295a-3faa-5b75-9cfa-a2ae73282e6d/scratchpad/run_U_L2/SAT_* >/dev/null 2>&1 && cp /sandbox/058c295a-3faa-5b75-9cfa-a2ae73282e6d/scratchpad/run_U_L2/SAT_*.model results/WAVE1/W07/U_L2/ 2>/dev/null
git add $D 2>/dev/null; git add results/WAVE1/W07 && git commit -qm "W07: ${1:-progress}"
for i in 1 2 3 4 5; do git pull -q --rebase --autostash origin es7-cloud && git push -q origin es7-cloud && exit 0; sleep $((i*3)); done
git push -q origin HEAD:cloud-fallback/es7-wave1-w07; echo "pushed to cloud-fallback/es7-wave1-w07"
