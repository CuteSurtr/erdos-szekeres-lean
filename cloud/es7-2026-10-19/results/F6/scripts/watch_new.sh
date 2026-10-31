#!/bin/bash
# Launch handle26.sh for every new realized 26-set (grow_guided gg*.pts, arm F records with points,
# realizer successes with exact_check true). usage: watch_new.sh SCRATCH
S=$1; H=$(cd "$(dirname "$0")" && pwd)/handle26.sh; mkdir -p $S/newpts $S/handled
while true; do
  cp -n $S/run/gg/*.pts $S/newpts/ 2>/dev/null
  /usr/bin/python3 - $S <<'PY'
import json, glob, os, sys
S = sys.argv[1]
for f in glob.glob(S + "/run/armF_*.jsonl"):
    for l in open(f):
        r = json.loads(l)
        if "points" in r and r.get("exact_ok"):
            p = f"{S}/newpts/{r['id']}.pts"
            if not os.path.exists(p): open(p, "w").write("".join(f"{x} {y}\n" for x, y in r["points"]))
for f in glob.glob(S + "/run/real_*.jsonl"):
    for l in open(f):
        r = json.loads(l)
        if r.get("realized") and r.get("exact_check"):
            p = f"{S}/newpts/kph{r['model']}.pts"
            if not os.path.exists(p): open(p, "w").write("".join(f"{x} {y}\n" for x, y in r["points"]))
PY
  for p in $S/newpts/*.pts; do n=$(basename $p .pts)
    [ -e $S/handled/$n ] && continue; touch $S/handled/$n; echo "NEW $n"
    nohup $H $S $p > $S/handle_$n.log 2>&1 &
  done
  sleep 20
done
