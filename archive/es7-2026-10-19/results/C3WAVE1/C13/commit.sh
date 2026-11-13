#!/bin/bash
# commit from a separate clone so the live files in the primary repo are never rewritten by git
S=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C13; T=/opt/push/cloud/es7-2026-10-19/results/C3WAVE1/C13
cd /opt/push && git pull -q --rebase --autostash origin es7-cloud; mkdir -p $T; cp -p $S/* $T/ && git add $T && git commit -qm "C13: progress $(date -u +%H:%M)"; for i in 1 2 3 4 5 6; do git pull -q --rebase --autostash origin es7-cloud && git push -q origin es7-cloud && { echo pushed; break; }; sleep $((2*i)); done; git log --oneline -1
