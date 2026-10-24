#!/bin/bash
cd /home/user/erdos-szekeres-lean
D=cloud/es7-2026-10-19/results/C3WAVE1/C09
pushit() {
  for i in 1 2 3 4 5; do
    git pull -q --rebase --autostash origin es7-cloud && git push -q origin es7-cloud && { echo "pushed $(date -u +%T)"; return 0; }
    sleep $((2**i))
  done
  git push -q origin HEAD:claude/es7-c3w1-c09 && echo "PUSHED TO claude/es7-c3w1-c09 $(date -u +%T)"
}
while true; do
  sleep ${PERIOD:-1500}
  cp /opt/work/out.jsonl $D/out.jsonl; cat /opt/work/driver_part1.log /opt/work/driver.log > $D/driver.log
  git add $D/out.jsonl $D/driver.log
  git commit -qm "C09: progress $(date -u +%H:%M)" && pushit
done
