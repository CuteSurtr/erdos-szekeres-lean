#!/bin/bash
# driver.sh -- reviewer rv4: prep (once) -> run.sh (resumable) -> post. Runs inside unit esr-ag-rv4-<job>.
set -u
V=/home/jay/research/data/formalize-20261122/n66enc-recheck/verify
cd "$V" || exit 1
if ! [ -s out/expected.json ] || ! [ -s out/plan.tsv ]; then
  /usr/bin/python3 -I tools/prep.py > logs/prep.log 2>&1 || { echo "$(date '+%F %T') prep failed" >> logs/run.log; exit 2; }
fi
bash tools/run.sh; rc=$?
/usr/bin/python3 -I tools/post.py > logs/post.log 2>&1
exit $rc
