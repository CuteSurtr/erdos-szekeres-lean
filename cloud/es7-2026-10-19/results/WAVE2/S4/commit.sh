#!/bin/bash
# commit and push S4 results; usage: commit.sh MSG
cd /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19
exec 9>/opt/work/git.lock; flock 9
git add results/WAVE2/S4 && git commit -qm "$1" 
for i in 1 2 3 4; do git pull -q --rebase --autostash origin es7-cloud && git push -q -u origin es7-cloud && exit 0; sleep $((2**i)); done
git push -q -u origin HEAD:claude/es7-w2-s4 && echo "PUSHED TO claude/es7-w2-s4" >> /opt/work/runner.log
