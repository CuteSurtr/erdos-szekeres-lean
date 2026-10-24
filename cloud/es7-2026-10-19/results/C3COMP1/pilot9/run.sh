#!/bin/bash
# extra pilot (beyond the task): one H3/one six-bit cube that timed out at 1800 s, sigma-split on 3 more bits (third sigma level), 8 nine-bit cubes at cap 600
export PATH=/opt/bin:$PATH
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
echo "=== start $(date -u +%T)"
python3 close_tree.py /opt/work/base.cnf /opt/work/pilot9/out.jsonl 0s0_5__1s0-2s1-3s0-4s0-6s0-7s0 --jobs 3 --sigma-split 3 --sigma-levels 3 --caps 1,600 --cadopts=--sat --hours 0.1 2>&1
echo "=== end $(date -u +%T)"
