#!/bin/bash
# S4 orchestration: step (a) status, (b)+(c) whole-case attempts 4 at a time, then (d) the driver case by case.
cd /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19
S4=results/WAVE2/S4; END=$(date -u -d "2026-10-20 13:08:00" +%s); LOG=/opt/work/runner.log
export BIN=/opt/work/bin WORK=/opt/work/tmp
log(){ echo "$(date -u +%H:%M:%S) $*" | tee -a $LOG; }
pull(){ ( exec 9>/opt/work/git.lock; flock 9; git pull -q --rebase --autostash origin es7-cloud ); }
ORDER="U7_L14 U7_L9 U7_L2 U6_L11 U6_L7 U5_L14 U5_L8 U5_L2 U4_L13 U4_L8 U4_L2 U3_L13 U3_L9 U3_L5 U6-15_L U6-10_L U_L5-16 U_L5-14 U_L5-12 U_L5-10 U5-9_L U_L5-7 U5-6_L U_L4-14 U4-13_L U4-11_L U4-9_L U_L4-7 U4-6_L"
pull; FREE=""; LATER=""
for c in $ORDER; do s=$(python3 $S4/status.py $c); log "status $c: $s"
  case $s in CLOSED*) echo "$c $s" >> $S4/skipped.txt;; STARTED*) LATER="$LATER $c";; *) FREE="$FREE $c";; esac; done
log "free:$FREE later:$LATER"
# whole-case attempts, 4 in parallel
echo $FREE | tr ' ' '\n' | xargs -P4 -I{} sh -c 'r=$('$S4'/whole.sh {}); echo "$(date -u +%H:%M:%S) whole {}: $r" >> '$LOG
$S4/commit.sh "S4: whole-case attempts"
run_case(){ c=$1; pull; s=$(python3 $S4/status.py $c)
  case $s in CLOSED*) log "skip $c: $s"; echo "$c $s" >> $S4/skipped.txt; return;; esac
  [ -s $S4/$c/leaves.icnf ] && [ -e $S4/$c/open.icnf ] && ! grep -q '^a' $S4/$c/open.icnf && { log "$c already closed by S4"; return; }
  [ -f /opt/work/cases/$c.cnf ] || [ "$($S4/whole.sh $c)" = CLOSED ] && [ -s $S4/$c/leaves.icnf ] && return
  [ -e $S4/$c/SAT_whole.out ] && { log "SAT $c"; return; }; [ -f /opt/work/cases/$c.cnf ] || { log "no cnf $c"; return; }
  now=$(date +%s); H=$(echo "($END - $now)/3600" | bc -l); [ $now -ge $((END-600)) ] && { log "no time for $c"; echo $c >> $S4/notreached.txt; return; }
  log "driver $c hours=$H"
  python3 $S4/close_march.py /opt/work/cases/$c.cnf $S4/$c --name $c --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours $H >> $S4/$c.driver.log 2>&1
  log "driver $c exit: $(tail -1 $S4/$c.driver.log)"; mv $S4/$c.driver.log $S4/$c/driver.log
  $S4/commit.sh "S4: $c $(tail -1 $S4/$c/driver.log)"; }
for c in $FREE; do [ -s $S4/$c/leaves.icnf ] && ! grep -q '^a' $S4/$c/open.icnf && continue; run_case $c; done
for c in $LATER; do run_case $c; done
log "RUNNER DONE"
