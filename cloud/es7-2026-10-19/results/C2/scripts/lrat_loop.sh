#!/bin/bash
# Periodic LRAT spot checks of cubes closed in this session (C2), at nice 5.
# Every round: for each run, take the closed.txt lines added since the previous round (the
# first round starts after the lines inherited from the local run), check up to NS of them (NS large = all)
# with lrat_spot.py (fresh CaDiCaL solve with --lrat, then lrat-check), append JSON lines.
# usage: lrat_loop.sh <C-scripts-dir> <workdir> <bindir> <stop-epoch> <NS> <timeout> run:cnf:inherited ...
S="$1"; W="$2"; B="$3"; STOP="$4"; NS="$5"; TL="$6"; shift 6
declare -A done_; round=0
for spec in "$@"; do IFS=: read r cnf inh <<< "$spec"; done_[$r]=$inh; done
while [ "$(date +%s)" -lt "$STOP" ]; do
  sleep 300; round=$((round+1))
  for spec in "$@"; do
    IFS=: read r cnf inh <<< "$spec"
    tot=$(wc -l < "$W/runs/$r/closed.txt")
    tail -n +"$((done_[$r]+1))" "$W/runs/$r/closed.txt" | head -n "$((tot-done_[$r]))" > "$W/lrat_new_$r.txt"
    done_[$r]=$tot
    [ -s "$W/lrat_new_$r.txt" ] || continue
    nice -n 5 python3 "$S/lrat_spot.py" "$cnf" "$W/lrat_new_$r.txt" "$B" "$W/lratwd" "$NS" "$TL" "$round" -1 >> "$W/runs/lrat_$r.jsonl"
  done
done
