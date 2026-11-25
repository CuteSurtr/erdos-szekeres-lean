#!/bin/bash
# control: controls/Geo5/Bad5.lean claims the heptagon for 31 points with the centre allowed; it must NOT compile
set -u
. /home/jay/research/data/formalize-20261122/sevenfold/tools/env.sh
F=/home/jay/research/data/formalize-20261122/fivefold
export LEAN_PATH="$LP_SELF:$F/olean"
cd "$F/controls" && "$LEAN" -j1 -R "$F/controls" Geo5/Bad5.lean > "$F/logs/bad5.out" 2>&1
echo "lean_rc=$?" >> "$F/logs/bad5.out"
