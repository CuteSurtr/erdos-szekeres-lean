#!/bin/bash
# watch_verify.sh : every 30 s, exact-verify any new float N8 = 0 configuration (found_*.json of the annealers,
# cand_*.json of the LP-CEGAR runs, *_N8_0.json of altproj2) at scales 2^30, 2^40, 2^50 with the ES8SYM pipeline.
D=/home/jay/research/data/lb-k8sym-20261111
cd $D
STOP=$(date -d '2026-11-12 04:25' +%s)
mkdir -p exact; touch exact/VERIFIED.tsv exact/seen.txt
while [ $(date +%s) -lt $STOP ]; do
  for f in runs/*/found_*.json cegar/*/cand_*.json runs/*/*_N8_0.json; do
    [ -f "$f" ] || continue; grep -qx "$f" exact/seen.txt && continue; echo "$f" >> exact/seen.txt
    n=$(echo $f | tr '/' '_' | sed 's/.json$//')
    M=$(python3 -c "import json;print(json.load(open('$f')).get('m') or 4)")
    N8=$(python3 -c "import json;d=json.load(open('$f'));print((d.get('counts') or {}).get('8','?'))")
    [ "$N8" != "0" ] && [ "$N8" != "?" ] && continue
    for S in 30 40 50; do
      d=exact/${n}_S${S}; mkdir -p $d
      python3 tools/to_pts.py $M $f $S $d/cand.pts > /dev/null
      C=$(head -1 $d/cand.pts | sed -E 's/.*C=([01]).*/\1/')
      tools/verify_mf.sh $d/cand.pts $M $C $d > $d/summary.txt 2>&1
      ok=$(grep -c "PASS" $d/verify.log); e8=$(grep -c "convex  8-gons: DP1 0  DP2 0" $d/verify.log); s8=$(grep -c "convex 8-subsets: 0" $d/verify.log)
      echo -e "$(date +%H:%M:%S)\t$f\tm=$M\tS=$S\tC=$C\tPASS_lines=$ok\tcvx2_8gons0=$e8\tcvxcheck_8subsets0=$s8\t$(sha256sum $d/cand.pts | cut -c1-64)" >> exact/VERIFIED.tsv
    done
  done
  sleep 30
done
