#!/bin/bash
# copy run records into the results dir, commit and push
cd /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19
cp /tmp/claude-0/-home-user-erdos-szekeres-lean/058c295a-3faa-5b75-9cfa-a2ae73282e6d/scratchpad/run_U_L2/leaves.jsonl results/WAVE1/W07/U_L2/ 2>/dev/null
for f in leaves.icnf open.icnf; do [ -f /tmp/claude-0/-home-user-erdos-szekeres-lean/058c295a-3faa-5b75-9cfa-a2ae73282e6d/scratchpad/run_U_L2/$f ] && cp /tmp/claude-0/-home-user-erdos-szekeres-lean/058c295a-3faa-5b75-9cfa-a2ae73282e6d/scratchpad/run_U_L2/$f results/WAVE1/W07/U_L2/; done
ls /tmp/claude-0/-home-user-erdos-szekeres-lean/058c295a-3faa-5b75-9cfa-a2ae73282e6d/scratchpad/run_U_L2/SAT_* >/dev/null 2>&1 && cp /tmp/claude-0/-home-user-erdos-szekeres-lean/058c295a-3faa-5b75-9cfa-a2ae73282e6d/scratchpad/run_U_L2/SAT_*.model results/WAVE1/W07/U_L2/ 2>/dev/null
git add results/WAVE1/W07 && git commit -qm "W07: ${1:-progress}" && git pull -q --rebase --autostash origin es7-cloud && (git push -q origin es7-cloud || git push -q origin HEAD:claude/es7-wave1-w07)
