#!/bin/bash
# Hexagonal-hull lane with proofs: base c34h_final.cnf (angular + hull-vertex normal form) + the hull cube of a case;
# CaDiCaL --lrat (limit LIMIT), lrat-check, zstd archive with verified round trip, JSON line in hc34/results.jsonl.
C=${C2C:?set C2C to the work directory}; B=${TOOLS:?set TOOLS to the directory with cadical, lrat-check, cake_lpr}; AR=${ARCHIVE:?set ARCHIVE}; LIMIT=$1; NOCLAIM=$2; BASE=$C/c34h_final.cnf
while read -r name; do
  [ "$(date +%s)" -lt $NOCLAIM ] || exit 0
  mkdir $C/hc34/claimsL/$name 2>/dev/null || continue
  F=$C/hc34/work/$name.cnf; P=$C/hc34/work/$name.lrat; O=$C/hc34/$name.L.out
  lits=$(grep "^$name " $C/hc34/cubes.txt | cut -d' ' -f2-); n=$(echo $lits | wc -w | tr -d ' ')
  awk -v n=$n '/^p cnf/ {print $1, $2, $3, $4 + n; next} {print}' $BASE > $F; for l in $lits; do echo "$l 0"; done >> $F
  cnfsha=$(shasum -a 256 $F | cut -d' ' -f1)
  t0=$(date +%s); $B/cadical -t $LIMIT --lrat --binary=false $F $P > $O 2>&1; t1=$(date +%s)
  st=$(grep -m1 '^s ' $O | cut -c3-); [ -z "$st" ] && st=UNKNOWN
  ts=$(grep 'total process time' $O | awk '{print $(NF-1)}')
  rec="\"case\": \"$name\", \"status\": \"$st\", \"solve_s\": \"$ts\", \"wall_s\": $((t1-t0)), \"cube_literals\": $n, \"cnf_sha256\": \"$cnfsha\""
  if [ "$st" = "UNSATISFIABLE" ]; then
    lc=$($B/lrat-check $F $P 2>&1 | grep -m1 -E 'VERIFIED|FAIL|rror'); psha=$(shasum -a 256 $P | cut -d' ' -f1); pb=$(stat -f %z $P)
    zstd -q -T2 -10 -f $P -o "$AR/$name.lrat.zst"; asha=$(shasum -a 256 "$AR/$name.lrat.zst" | cut -d' ' -f1)
    rt=$(zstd -q -d -c "$AR/$name.lrat.zst" | shasum -a 256 | cut -d' ' -f1); [ "$rt" = "$psha" ] && rv=verified || rv=MISMATCH
    rec="$rec, \"lrat_check\": \"$lc\", \"proof_bytes\": $pb, \"proof_sha256\": \"$psha\", \"archive_sha256\": \"$asha\", \"roundtrip\": \"$rv\""
    [ "$rv" = verified ] && rm -f $P
  elif [ "$st" = "SATISFIABLE" ]; then cp $O $C/hc34/SAT_$name.out; rm -f $P
  else rm -f $P; fi
  rm -f $F
  echo "{$rec}" >> $C/hc34/results.jsonl
done < $C/hc34/hex_order.txt
