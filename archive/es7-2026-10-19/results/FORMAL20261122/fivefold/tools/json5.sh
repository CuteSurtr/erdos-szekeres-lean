#!/bin/bash
# print the messages of src/Geo5/Main5.lean as JSON lines (for writing the #guard_msgs pins); no olean is written
set -u
. /home/jay/research/data/formalize-20261122/sevenfold/tools/env.sh
F=/home/jay/research/data/formalize-20261122/fivefold
export LEAN_PATH="$LP_SELF:$F/olean"
cd "$F/src" && "$LEAN" -j1 --json -R "$F/src" Geo5/Main5.lean > "$F/logs/msgs.jsonl" 2>&1
echo "rc=$?" >> "$F/logs/msgs.jsonl"
