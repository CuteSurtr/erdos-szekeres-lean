#!/bin/bash
# Layer-profile lane for the central 34-point case: claim the next profile (lay/profiles17.txt), build base + layer units,
# solve with CaDiCaL --lrat (limit LIMIT s), check UNSAT proofs with lrat-check, archive them (zstd, verified round trip),
# record one JSON line in lay/results.jsonl. SAT outputs are kept in full. No new profile after NOCLAIM (epoch s).
C=${C2C:?set C2C to the work directory}; B=${TOOLS:?set TOOLS to the directory with cadical, lrat-check, cake_lpr}; AR=${ARCHIVE:?set ARCHIVE}; LIMIT=$1; NOCLAIM=$2
BASE=$C/lay/r2_t17k7_nosb.cnf; MAP=$C/lay/r2_t17k7_nosb.json
while read -r prof; do
  [ "$(date +%s)" -lt $NOCLAIM ] || exit 0
  name=L$(echo $prof | tr ',' '_')
  mkdir $C/lay/claims/$name 2>/dev/null || continue
  U=$C/lay/units/$name.txt; F=$C/lay/work/$name.cnf; P=$C/lay/work/$name.lrat; O=$C/lay/$name.out
  python3 $C/zlayers.py $MAP $prof $U > /dev/null || { echo "{\"profile\": \"$prof\", \"status\": \"units-error\"}" >> $C/lay/results.jsonl; continue; }
  n=$(wc -l < $U | tr -d ' ')
  awk -v n=$n '/^p cnf/ {print $1, $2, $3, $4 + n; next} {print}' $BASE > $F; cat $U >> $F
  cnfsha=$(shasum -a 256 $F | cut -d' ' -f1); usha=$(shasum -a 256 $U | cut -d' ' -f1)
  t0=$(date +%s); $B/cadical -t $LIMIT --lrat --binary=false $F $P > $O 2>&1; t1=$(date +%s)
  st=$(grep -m1 '^s ' $O | cut -c3-); [ -z "$st" ] && st=UNKNOWN
  rec="\"profile\": \"$prof\", \"status\": \"$st\", \"wall_s\": $((t1-t0)), \"units\": $n, \"units_sha256\": \"$usha\", \"cnf_sha256\": \"$cnfsha\""
  if [ "$st" = "UNSATISFIABLE" ]; then
    lc=$($B/lrat-check $F $P 2>&1 | grep -m1 -E 'VERIFIED|FAIL|rror'); psha=$(shasum -a 256 $P | cut -d' ' -f1); pb=$(stat -f %z $P)
    zstd -q -T2 -10 -f $P -o "$AR/$name.lrat.zst"; asha=$(shasum -a 256 "$AR/$name.lrat.zst" | cut -d' ' -f1)
    rt=$(zstd -q -d -c "$AR/$name.lrat.zst" | shasum -a 256 | cut -d' ' -f1); [ "$rt" = "$psha" ] && rv=verified || rv=MISMATCH
    rec="$rec, \"lrat_check\": \"$lc\", \"proof_bytes\": $pb, \"proof_sha256\": \"$psha\", \"archive_sha256\": \"$asha\", \"roundtrip\": \"$rv\""
    [ "$rv" = verified ] && rm -f $P
  elif [ "$st" = "SATISFIABLE" ]; then
    cp $O $C/lay/SAT_$name.out; rm -f $P
  else
    rm -f $P
  fi
  rm -f $F
  echo "{$rec}" >> $C/lay/results.jsonl
done < $C/lay/profiles17.txt
