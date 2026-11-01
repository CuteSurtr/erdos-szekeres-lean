#!/bin/bash
# wait up to $1 seconds, or until some run reports a zero count
cd "$(dirname "$0")/.."; end=$((SECONDS+$1))
while [ $SECONDS -lt $end ]; do ./src/snap.sh; if grep -l ZERO snap/*.runs.txt 2>/dev/null || grep -l '^# c7 0 ' snap/*.best.txt 2>/dev/null; then echo ZERO; exit 0; fi; pgrep -x 'lbs2?' >/dev/null || { echo nojobs; exit 0; }; sleep 20; done
