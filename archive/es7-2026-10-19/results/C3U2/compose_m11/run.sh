#!/bin/bash
# The official composition (C3U2 step 3): C3U2 compose.py and C3AUDIT3 mycompose.py (fixed) on the 127 record files
# of files.txt, with and without --mirror-h6, via tests/frontier_cmp.py; also the old C3U compose.py (95cafa93).
# Base: /opt/work/base.cnf = gen_case.py 11 7 none (p cnf 168399 4154921, sha256 bf0e502e...dd6da). sha checks on.
mkdir -p /opt/work/snap && cd /home/user/erdos-szekeres-lean && git archive 3fd8a4d8 $(for d in C3WAVE1 C3WAVE2 C3S0 C3W3 C3W3S C3SIG C3SIG2 C3W4; do echo cloud/es7-2026-10-19/results/$d; done) | tar -x -C /opt/work/snap
cd /opt/work/snap/cloud/es7-2026-10-19/results; T=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results
F=$(grep -v '^#' $T/C3U2/compose_m11/files.txt | tr '\n' ' ')
for v in C3U2 C3U; do for mh in "" "--mirror-h6"; do tag=nomirror; [ -n "$mh" ] && tag=mirrorh6
  python3 $T/C3U2/tests/frontier_cmp.py $T/$v/tools 11 7 /opt/work/base.cnf /opt/work/m11/${v}_$tag $F $mh > /opt/work/m11/${v}_$tag.log 2>&1
done; done
python3 $T/C3U2/tests/make_open_roots.py /opt/work/m11/C3U2_mirrorh6_roots.tsv $T/C3U2/open_roots.tsv $T/C3W4/lists/*.tsv
