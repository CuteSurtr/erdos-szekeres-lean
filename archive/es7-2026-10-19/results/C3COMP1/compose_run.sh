#!/bin/bash
# C3COMP1 part 1: C3U2 compose.py (cad4e050) and C3AUDIT3 mycompose.py (fixed, 5336f631, unchanged at 5392150c) via
# C3U2/tests/frontier_cmp.py, on the record files of files.txt at commit 5392150c (snapshot by git archive), sha checks on.
cd /opt/work/snap/cloud/es7-2026-10-19/results
F=$(cat /opt/work/m11/files.txt | tr '\n' ' ')
T=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
echo "start $(date -u +%T)"
for mh in "--mirror-h6" ""; do tag=nomirror; [ -n "$mh" ] && tag=mirrorh6
  python3 /opt/work/snap/cloud/es7-2026-10-19/results/C3U2/tests/frontier_cmp.py $T 11 7 /opt/work/base.cnf /opt/work/m11/C3U2_$tag $F $mh > /opt/work/m11/C3U2_$tag.log 2>&1
  echo "done $tag $(date -u +%T)"
done
