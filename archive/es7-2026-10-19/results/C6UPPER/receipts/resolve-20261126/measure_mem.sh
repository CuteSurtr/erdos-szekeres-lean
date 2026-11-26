#!/bin/bash
# measure_mem.sh (26 Nov 2026): every 5 s, anon MB (memory.stat anon) of each esr-n66-d1-* unit and its phase
# (cadical / cake_lpr / other, by the process names in the unit's cgroup). Output: mem_samples.tsv; read-only.
U=$(id -u); APP=/sys/fs/cgroup/user.slice/user-$U.slice/user@$U.service/app.slice
OUT=/home/jay/research/data/resolve-queue-20261126/d1/mem_samples.tsv
[ -s $OUT ] || echo -e "time\tunit\tphase\tanon_mb" > $OUT
end=$(( $(date +%s) + ${1:-4500} ))
while [ "$(date +%s)" -lt $end ]; do
  t=$(date '+%T')
  for d in $APP/esr-n66-d1-*.service; do
    [ -f "$d/memory.stat" ] || continue
    a=$(awk '/^anon /{print int($2/1048576)}' "$d/memory.stat")
    ph=other
    for p in $(cat "$d/cgroup.procs" 2>/dev/null); do
      c=$(cat /proc/$p/comm 2>/dev/null); case "$c" in cadical*) ph=cadical;; cake_lpr*) ph=cake_lpr;; esac
    done
    echo -e "$t\t$(basename $d .service)\t$ph\t$a" >> $OUT
  done
  sleep 5
done
