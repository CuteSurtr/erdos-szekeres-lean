#!/bin/sh
# Sequential (one process at a time) saturation runs over a queue file.
# Queue lines:  sat <id>      -> bin/sat sat sets/<id>.txt 8 ...
#               verify <id>   -> bin/verify sets/<id>.txt 8 out/<id>.cert out/<id>.unc
# Stops starting new jobs after DEADLINE (epoch seconds) if set.
HERE=$(cd "$(dirname "$0")" && pwd)
Q=${1:-"$HERE/queue.txt"}
OUT="$HERE/out"
mkdir -p "$OUT"
while read -r kind id; do
  [ -z "$kind" ] && continue
  if [ -n "$DEADLINE" ] && [ "$(date +%s)" -ge "$DEADLINE" ]; then
    echo "deadline reached before $kind $id" >> "$OUT/queue.log"; break
  fi
  t0=$(date +%s)
  if [ "$kind" = sat ]; then
    [ -s "$OUT/$id.sat.json" ] && continue
    "$HERE/bin/sat" sat "$HERE/sets/$id.txt" 8 "$OUT/$id.bad" "$OUT/$id.cert" > "$OUT/$id.sat.json.tmp" 2> "$OUT/$id.sat.log"
    rc=$?
    mv "$OUT/$id.sat.json.tmp" "$OUT/$id.sat.json"
  else
    [ -s "$OUT/$id.verify.json" ] && continue
    "$HERE/bin/verify" "$HERE/sets/$id.txt" 8 "$OUT/$id.cert" "$OUT/$id.unc" > "$OUT/$id.verify.json.tmp" 2> "$OUT/$id.verify.log"
    rc=$?
    mv "$OUT/$id.verify.json.tmp" "$OUT/$id.verify.json"
  fi
  t1=$(date +%s)
  echo "$kind $id rc=$rc wall=$((t1 - t0))s $(cat "$OUT/$id.$kind.json")" >> "$OUT/queue.log"
  if [ "$kind" = sat ] && ! grep -q '"bad_candidates": 0,' "$OUT/$id.sat.json"; then
    echo "ALERT $id: nonzero bad_candidates or failed run" >> "$OUT/ALERT.txt"
  fi
done < "$Q"
echo "queue finished $(date)" >> "$OUT/queue.log"
