#!/bin/bash
# verify each cube CNF == header + base body + chord_new + manifest units (byte-exact), header counts consistent
cd <rot45-work-dir>/
for d in cubes5 cubes4; do
  base=$(python3 -c "import json;print(json.load(open('$d/manifest.json'))['base'])")
  chord=$(python3 -c "import json;print(json.load(open('$d/manifest.json'))['chord'])")
  read nv nc < <(head -1 $base | awk '{print $3, $4}')
  nch=$(wc -l < $chord)
  python3 -c "
import json
man=json.load(open('$d/manifest.json'))
for c in man['cubes']: print(c['cube'], ' '.join(map(str,c['units'])))
" | while read name units; do
    f=$d/$name.cnf; nu=$(echo $units | wc -w)
    hdr=$(head -1 $f); exp="p cnf $nv $((nc+nch+nu))"
    if cmp -s <(tail -n +2 $f) <(tail -n +2 $base; cat $chord; for u in $units; do echo "$u 0"; done) && [ "$hdr" = "$exp" ]; then echo "$f OK"; else echo "$f MISMATCH ($hdr vs $exp)"; fi
  done
done
