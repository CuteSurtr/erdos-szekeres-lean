#!/bin/bash
cd /home/user/erdos-szekeres-lean
D=cloud/es7-2026-10-19/results/C3WAVE1/C03
while true; do
  sleep 1500
  cp /opt/work/out.jsonl /opt/work/driver.log $D/; git add $D/out.jsonl $D/driver.log
  git commit -qm "C03: progress $(date -u +%H:%M)" && git pull -q --rebase --autostash && (git push -q origin es7-cloud || git push -q origin HEAD:claude/es7-c3w1-c03) >> /opt/work/push.log 2>&1
  grep -q "ALL DONE" /opt/work/driver.log && break
done
