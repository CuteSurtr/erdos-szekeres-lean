#!/bin/bash
cd /home/user/erdos-szekeres-lean || exit 1
D=cloud/es7-2026-10-19/results/C3WAVE1/C08
cp /opt/work/out.jsonl /opt/work/driver.log /opt/work/roots_done.txt $D/ 2>/dev/null
find $D -size +50M -print | grep . && { echo "file over 50MB, not committing"; exit 1; }
git add $D && git commit -qm "C3WAVE1 C08: ${1:-progress $(date -u +%H:%M)}" -- $D || true
for i in 1 2 3 4 5; do
  git pull -q --rebase --autostash origin es7-cloud && git push -q origin es7-cloud && { echo pushed; exit 0; }
  sleep $((2**i))
done
git push -q origin HEAD:claude/es7-c3w1-c08 && echo "pushed to claude/es7-c3w1-c08"
