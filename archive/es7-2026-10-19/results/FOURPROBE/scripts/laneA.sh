#!/bin/bash
D="<repo>/.cache/es7/final-2026-11-04/four_probe"
"<repo>/.cache/es7/final-2026-11-04/four_probe/scripts/lane.sh" t15 "$D/m4K8t15.cnf" "$D/t15.lrat" 1793753820 600
"<repo>/.cache/es7/final-2026-11-04/four_probe/scripts/lane.sh" t16 "$D/m4K8t16.cnf" "$D/t16.lrat" 1793753820 600
"<repo>/.cache/es7/final-2026-11-04/four_probe/scripts/lane.sh" c11100 "$D/cubes17/c11100.cnf" "$D/cubes17/c11100.lrat" 1793753820
echo "$(date +%H:%M:%S) laneA done" >> "$D/logs/lanes.txt"
