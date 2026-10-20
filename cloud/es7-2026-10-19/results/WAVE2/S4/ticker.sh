#!/bin/bash
# periodic progress commit every 20 min
while true; do sleep 1200; /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/WAVE2/S4/commit.sh "S4: progress $(date -u +%H:%M)"; done
