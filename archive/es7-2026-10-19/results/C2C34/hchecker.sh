#!/bin/bash
# cake_lpr lane for the hull cases: rebuild case CNF (base + cube), decompress the archived proof, run cake_lpr, record.
C=${C2C:?set C2C to the work directory}; B=${TOOLS:?set TOOLS to the directory with cadical, lrat-check, cake_lpr}; AR=${ARCHIVE:?set ARCHIVE}; STOP=$1; HEAP=${2:-16000}; BASE=$C/c34h_final.cnf
while [ "$(date +%s)" -lt $STOP ]; do
  name=$(python3 - $C <<'PY'
import json, sys, os
C = sys.argv[1]
done = set()
if os.path.exists(C + "/hc34/cake.jsonl"):
    done = {json.loads(l)["case"] for l in open(C + "/hc34/cake.jsonl") if l.strip()}
if os.path.exists(C + "/hc34/results.jsonl"):
    txt = open(C + "/hc34/results.jsonl").read().replace('"process\n', '"')
    for l in txt.splitlines():
        if not l.strip(): continue
        r = json.loads(l)
        if r.get("status") == "UNSATISFIABLE" and r.get("roundtrip") == "verified" and r["case"] not in done:
            print(r["case"]); break
PY
)
  if [ -z "$name" ]; then sleep 60; continue; fi
  F=$C/hc34/work/chk_$name.cnf; P=$C/hc34/work/chk_$name.lrat
  lits=$(grep "^$name " $C/hc34/cubes.txt | cut -d' ' -f2-); n=$(echo $lits | wc -w | tr -d ' ')
  awk -v n=$n '/^p cnf/ {print $1, $2, $3, $4 + n; next} {print}' $BASE > $F; for l in $lits; do echo "$l 0"; done >> $F
  zstd -q -d -f "$AR/$name.lrat.zst" -o $P
  t0=$(date +%s); out=$($B/cake_lpr --CML_HEAP_SIZE=$HEAP --CML_STACK_SIZE=4000 $F $P 2>&1); ec=$?; t1=$(date +%s)
  v=$(printf '%s\n' "$out" | grep -m1 -E 's VERIFIED|exhausted|rror|FAIL'); [ -z "$v" ] && v="no verdict line"
  echo "{\"case\": \"$name\", \"cake_lpr\": \"$v\", \"exit\": $ec, \"wall_s\": $((t1-t0)), \"heap_mb\": $HEAP}" >> $C/hc34/cake.jsonl
  rm -f $F $P
done
