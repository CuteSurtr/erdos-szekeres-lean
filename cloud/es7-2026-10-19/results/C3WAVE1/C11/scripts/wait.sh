#!/bin/bash
# wait up to $1 seconds, return early on SAT/rejection/runner end
D=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C11
end=$(( $(date +%s) + $1 ))
while [ $(date +%s) -lt $end ]; do
  grep -q "STOPPED\|RUNNER DONE" /opt/work/run.out && break
  sleep 20
done
cp /opt/work/out.jsonl $D/out.jsonl; cd /home/user/erdos-szekeres-lean && git add $D && git commit -qm "C11: progress $(date -u +%H:%M)" ; /opt/work/push.sh
date -u; free -g | head -2; tail -5 $D/driver.log; grep -c . $D/out.jsonl
