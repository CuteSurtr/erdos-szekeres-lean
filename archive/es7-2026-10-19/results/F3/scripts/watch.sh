#!/bin/bash
# Sequentially process every realized 26-set as it appears: grow_guided .pts files, arm F records
# with "points", realize_models records with "points" (extracted to .pts first).
# usage: watch.sh BIN RUNDIR END
BIN=$1; RUN=$2; END=$3; H=$(cd "$(dirname "$0")" && pwd); P=/usr/bin/python3
mkdir -p $RUN/found $RUN/proc
while [ $(date +%s) -lt $END ]; do
  cp -n $RUN/gg/gg*.pts $RUN/found/ 2>/dev/null
  $P - "$RUN" <<'PY'
import json, glob, os, sys
run = sys.argv[1]
for f in glob.glob(f"{run}/armF_*.jsonl") + glob.glob(f"{run}/kph/real_*.jsonl"):
    for l in open(f):
        r = json.loads(l)
        if "points" not in r: continue
        if "exact_ok" in r and not r["exact_ok"]: continue
        if "exact_check" in r and not r["exact_check"]: continue
        nm = r.get("id") or "K" + os.path.basename(f)[5:-6] + "_" + str(r["model"])
        out = f"{run}/found/{nm}.pts"
        if not os.path.exists(out):
            open(out, "w").write("".join(f"{x} {y}\n" for x, y in r["points"]))
PY
  for f in $RUN/found/*.pts; do
    [ -e "$f" ] || continue; n=$(basename $f .pts)
    [ -d $RUN/proc/$n ] && continue   # started (status.json is written at the end)
    echo "$(date -u +%T) start $n"; $H/process_set.sh $BIN $f $RUN/proc $RUN/known_fp.jsonl; echo "$(date -u +%T) done $n $(cat $RUN/proc/$n/status.json)"
  done
  sleep 30
done
