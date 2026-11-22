#!/bin/bash
# s3520-gate (22 Nov 2026): compile the chunk modules of one exported unit, one at a time, inside this unit.
# Usage: compile_loop.sh <export dir> <tag> <unit> <slot i> <of n>     (modules j with (j-1) % n == i; skips an existing
# olean). Before each compile: stop cleanly if the YIELD file exists; wait (60 s polls, up to 90 min) while Tctl >= 86 C.
# A module that Lean does not accept stops the loop (exit 1). Per module: logs/RS<tag>_<stem>.log (compile.sh, with
# /usr/bin/time -v) and logs/RS<tag>_<stem>.mem (sampled.sh: anon + shmem of this unit's cgroup, sampled every 0.5 s).
set -u
G=/home/jay/research/data/formalize-20261122/s3520-gate
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
ex=$1; tag=$2; u=$3; i=$4; n=$5
OL=${GATE_OLEAN:-$G/olean}
stems=$($PY -I -B -c "import json,sys; print(' '.join(m['module'].split('.')[-1] for m in json.load(open(sys.argv[1]))['modules']))" "$(printf '%s/ctx/ctx-%04d.json' "$ex" "$u")") || exit 2
j=0
for s in $stems; do
  j=$((j + 1)); [ $(((j - 1) % n)) -ne "$i" ] && continue
  ol=$OL/RS$tag/$s.olean
  [ -e "$ol" ] && continue
  for ((w = 0; ; w++)); do
    [ -e /home/jay/research/data/agents-20261121/YIELD ] && { echo "$(date -Is) YIELD file: stop before $s"; exit 0; }
    t=$(sensors | awk '/Tctl/ {gsub(/[^0-9.]/, "", $2); print $2}')
    awk -v t="$t" 'BEGIN {exit !(t < 86)}' && break
    [ $w -ge 90 ] && { echo "$(date -Is) Tctl $t C for 90 min: stop before $s"; exit 3; }
    echo "$(date -Is) Tctl $t C >= 86: waiting before $s"; sleep 60
  done
  $G/tools/sampled.sh $G/logs/RS${tag}_$s.mem $G/tools/compile.sh "$ex/src/RS$tag/$s.lean" "$ol" "$G/logs/RS${tag}_$s.log" "$ex/src"; rc=$?
  echo "$(date -Is) $s rc=$rc $(cat $G/logs/RS${tag}_$s.mem | cut -d' ' -f1-3) $(grep -E 'Elapsed|Maximum resident' $G/logs/RS${tag}_$s.log | tr -s ' ' | tr '\n' ' ')"
  [ $rc -ne 0 ] && { echo "$(date -Is) $s: lean_rc=$rc, loop stopped"; exit 1; }
done
echo "$(date -Is) slot $i of $n done"
