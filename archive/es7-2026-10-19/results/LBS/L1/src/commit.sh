#!/bin/bash
# snapshot and push (only this directory)
cd "$(dirname "$0")/.." && ./src/snap.sh
git add -A . && git commit -qm "${1:-LBS L1: progress snapshot}"
for i in 1 2 3 4 5; do git pull -q --rebase --autostash origin es7-cloud && git push -q origin es7-cloud 2>/dev/null && { echo pushed; exit 0; }; sleep $((2**i)); done
git push -q origin HEAD:es7-fallback-lbs-l1 && echo pushed-fallback
