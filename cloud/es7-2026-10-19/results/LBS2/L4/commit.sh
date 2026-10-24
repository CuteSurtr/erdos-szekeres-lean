#!/bin/bash
# Sync live/ into data/ chunks, summarize, commit and push (only this directory).
cd "$(dirname "$0")"
python3 sync.py && python3 analyze.py > /dev/null
cd /home/user/erdos-szekeres-lean
git add cloud/es7-2026-10-19/results/LBS2/L4
git commit -qm "LBS2 L4: progress $(date -u +%H:%M)"
for i in 1 2 3 4; do git pull -q --rebase --autostash origin es7-cloud && git push -q origin es7-cloud && break; sleep $((2 ** i)); done
git log --oneline -1
