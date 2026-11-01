#!/bin/bash
# F4 manager (adapted from F5's): drop cubes closed elsewhere, run the driver, checkpoint every 30 min
# (copy, commit, pull, drop again; restart the driver on the pruned frontier if anything was dropped).
R=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19
D=$R/results/WAVE2/F4; O=/opt/work/F4/U4_L; END=$(date -u -d '13:08' +%s)
export BIN=/opt/work/bin SCRATCH=/opt/work/scratch
mkdir -p $O; touch $D/U4_L/dropped.jsonl
others() { cd $R; ls -d results/WAVE1/W29/U4_L results/WAVE2/*/U4_L | grep -v WAVE2/F4; }
dropq() {  # $1 = queue in, writes /opt/work/F4/newq.icnf
  cd $R; python3 $D/drop.py $1 /opt/work/F4/newq.icnf $D/U4_L/dropped.jsonl $O/leaves.jsonl $(others) > /opt/work/F4/drop.out
  echo "$(date -u +%T) $(cat /opt/work/F4/drop.out)" >> $D/U4_L/manager.log
}
start() {
  H=$(python3 -c "print(max(0,($END-$(date +%s))/3600))")
  setsid python3 $D/close_march.py /opt/work/U4_L.cnf $O --top $O/queue.icnf --timeout 300 --split-depth 6 --jobs 4 --hours $H >> $O/driver.log 2>&1 &
  PID=$!; echo "$(date -u +%T) start pid $PID hours $H queue $(wc -l < $O/top.icnf)" >> $D/U4_L/manager.log
}
sync_out() {
  for f in leaves.jsonl leaves.icnf open.icnf; do [ -f $O/$f ] && cp $O/$f $D/U4_L/$f; done
  cp $O/top.icnf $D/U4_L/queue.icnf; ls $O/SAT_* >/dev/null 2>&1 && cp $O/SAT_* $D/U4_L/
}
commit() {
  cd $R; git add results/WAVE2/F4; git commit -qm "WAVE2 F4: U4_L progress $(date -u +%H:%M)"
  git pull -q --rebase --autostash; for i in 1 2 3 4; do git push -q origin es7-cloud && return; sleep $((2**i)); git pull -q --rebase --autostash; done
  git push -q origin HEAD:claude/es7-w2-f4 && echo "$(date -u +%T) pushed to claude/es7-w2-f4" >> $D/U4_L/manager.log
}
cd $R; git pull -q --rebase --autostash
dropq $D/U4_L/share.icnf; cp /opt/work/F4/newq.icnf $O/queue.icnf; cp $O/queue.icnf $O/top.icnf
start; sync_out; commit
while true; do
  for i in $(seq 180); do kill -0 $PID 2>/dev/null || break; sleep 10; done
  sync_out
  if ! kill -0 $PID 2>/dev/null; then echo "$(date -u +%T) driver exited: $(tail -1 $O/driver.log)" >> $D/U4_L/manager.log; commit; break; fi
  commit
  dropq $O/open.icnf
  if ! grep -q 'dropped 0$' /opt/work/F4/drop.out && [ $(( END - $(date +%s) )) -gt 900 ]; then
    kill -TERM -$PID; sleep 3; kill -KILL -$PID 2>/dev/null; wait $PID 2>/dev/null
    cp $O/open.icnf $D/U4_L/open_before_restart.icnf 2>/dev/null
    cp /opt/work/F4/newq.icnf $O/queue.icnf; cp $O/queue.icnf $O/top.icnf; rm -rf $SCRATCH/*; start
  fi
done
echo "$(date -u +%T) manager done" >> $D/U4_L/manager.log
touch /opt/work/F4/MANAGER_DONE
