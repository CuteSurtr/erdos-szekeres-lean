#!/bin/sh
# F6: copy the driver's output (/opt/work/U_L8, outside the repo) into U_L8/, refresh the skip file, commit, push
R=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/WAVE2/F6; O=/opt/work/U_L8
cd /home/user/erdos-szekeres-lean || exit 1
git pull -q --rebase --autostash
$R/refresh_skip.sh
python3 - "$O/leaves.jsonl" "$R/U_L8/leaves.jsonl" <<'PY'
import sys; d = open(sys.argv[1]).read(); open(sys.argv[2], "w").write(d[:d.rfind("\n") + 1])
PY
for f in leaves.icnf open.icnf top.icnf; do [ -f $O/$f ] && cp $O/$f $R/U_L8/$f; done
git add $R && git commit -qm "F6: U_L8 progress $(date -u +%H:%M)" || true
git pull -q --rebase --autostash
git push -q origin es7-cloud || git push -q origin HEAD:claude/es7-w2-f6
git log --oneline -1
