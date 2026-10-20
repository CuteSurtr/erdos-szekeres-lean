#!/bin/bash
# F5 manager: runs the driver, checkpoints every 30 min (copy, commit, pull, drop cubes others closed).
R=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19
D=$R/results/WAVE2/F5; O=/opt/work/U4_L; END=$(date -u -d '12:22' +%s)
export BIN=/opt/work/bin SCRATCH=/opt/work/scratch
mkdir -p $O; [ -f $O/top.icnf ] || cp $D/U4_L/share.icnf $O/top.icnf
start() {
  H=$(python3 -c "print(max(0,($END-$(date +%s))/3600))")
  setsid python3 $D/close_march.py /opt/work/U4_L.cnf $O --top $D/U4_L/share.icnf --timeout 300 --split-depth 6 --jobs 4 --hours $H >> $O/driver.log 2>&1 &
  PID=$!; echo "$(date -u +%T) start pid $PID hours $H" >> $D/U4_L/manager.log
}
sync_out() {
  for f in leaves.jsonl leaves.icnf open.icnf; do [ -f $O/$f ] && cp $O/$f $D/U4_L/$f; done
  cp $O/top.icnf $D/U4_L/queue.icnf; ls $O/SAT_* >/dev/null 2>&1 && cp $O/SAT_* $D/U4_L/
}
commit() {
  cd $R; git add results/WAVE2/F5; git commit -qm "WAVE2 F5: U4_L progress $(date -u +%H:%M)"
  git pull -q --rebase --autostash; for i in 1 2 3; do git push -q origin es7-cloud && return; sleep $((2*i)); git pull -q --rebase --autostash; done
  git push -q origin HEAD:claude/es7-w2-f5 && echo "$(date -u +%T) pushed to claude/es7-w2-f5" >> $D/U4_L/manager.log
}
start
while true; do
  for i in $(seq 180); do kill -0 $PID 2>/dev/null || break; sleep 10; done
  sync_out
  if ! kill -0 $PID 2>/dev/null; then echo "$(date -u +%T) driver exited" >> $D/U4_L/manager.log; commit; break; fi
  commit
  cd $R; others=$(ls -d results/WAVE1/W29/U4_L results/WAVE2/*/U4_L | grep -v WAVE2/F5)
  python3 $D/drop.py $O/open.icnf /opt/work/newq.icnf $D/U4_L/dropped.jsonl $O/leaves.jsonl $others > /opt/work/drop.out
  echo "$(date -u +%T) $(cat /opt/work/drop.out)" >> $D/U4_L/manager.log
  if ! grep -q 'dropped 0$' /opt/work/drop.out && [ $(( END - $(date +%s) )) -gt 900 ]; then
    kill -TERM -$PID; sleep 3; kill -KILL -$PID 2>/dev/null; wait $PID 2>/dev/null
    cp $O/open.icnf $D/U4_L/open_before_restart.icnf 2>/dev/null
    cp /opt/work/newq.icnf $O/top.icnf; rm -rf $SCRATCH/*; start
  fi
done
echo "$(date -u +%T) manager done" >> $D/U4_L/manager.log
