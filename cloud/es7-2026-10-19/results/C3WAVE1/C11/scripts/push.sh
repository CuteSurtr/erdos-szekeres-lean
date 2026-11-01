#!/bin/bash
cd /home/user/erdos-szekeres-lean
for i in 1 2 3 4 5 6; do git pull --rebase --autostash -q && git push -q origin es7-cloud 2>/dev/null && { echo pushed; exit 0; }; sleep $((i*3)); done
echo "PUSH FAILED -> claude/es7-c3w1-c11"; git push -q origin HEAD:claude/es7-c3w1-c11
