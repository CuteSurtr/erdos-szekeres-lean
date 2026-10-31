#!/bin/bash
# usage: push.sh "message"
cd /home/user/erdos-szekeres-lean || exit 1
git add cloud/es7-2026-10-19/results/Mi-0/
git commit -qm "$1" || true
for i in 1 2 3 4 5 6; do
  git pull -q --rebase --autostash origin es7-cloud && git push -q -u origin es7-cloud 2>/dev/null && { echo pushed; exit 0; }
  sleep $((2**i))
done
git push -q -u origin HEAD:claude/es7-mi-0 && echo "pushed to claude/es7-mi-0"
