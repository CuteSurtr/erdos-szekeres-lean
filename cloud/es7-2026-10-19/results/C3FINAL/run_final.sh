#!/bin/bash
# Final double composition of the 3-fold class (m = 11, k = 7): C3U2 compose.py (cad4e050, unmodified) and C3AUDIT3
# mycompose.py (fixed version) via C3U2/tests/frontier_cmp.py, --mirror-h6 (the reduced cut, 910 depth-2 roots),
# sha checks on, over every record file of the results tree at f788780c5623e39b8fe0a45eba98058a2774a9b4 (git archive snapshot).
cd /private/tmp/claude-501/-Users-jiho-Desktop-lean-4-/3d74306a-3b6f-4edb-85db-abd21cbf81c6/scratchpad/c3/final/snap/cloud/es7-2026-10-19/results || exit 1
echo "start $(date -u +%FT%TZ)"
python3 C3U2/tests/frontier_cmp.py /private/tmp/claude-501/-Users-jiho-Desktop-lean-4-/3d74306a-3b6f-4edb-85db-abd21cbf81c6/scratchpad/local/c3u2/cloud/es7-2026-10-19/results/C3U2/tools 11 7 /private/tmp/claude-501/-Users-jiho-Desktop-lean-4-/3d74306a-3b6f-4edb-85db-abd21cbf81c6/scratchpad/local/work/base.cnf /private/tmp/claude-501/-Users-jiho-Desktop-lean-4-/3d74306a-3b6f-4edb-85db-abd21cbf81c6/scratchpad/c3/final/C3FINAL_mirrorh6 $(cat /private/tmp/claude-501/-Users-jiho-Desktop-lean-4-/3d74306a-3b6f-4edb-85db-abd21cbf81c6/scratchpad/c3/final/compose_files.txt) --mirror-h6
echo "exit $? end $(date -u +%FT%TZ)"
