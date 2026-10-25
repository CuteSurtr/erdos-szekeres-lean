#!/bin/bash
export PATH=/opt/bin:$PATH
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
echo "=== NODE 0s0_5__1s0-2s1-3s0-4s0-6s0-7s0 start $(date -u +%T)"
python3 close_tree.py /opt/work/base.cnf /opt/work/out0.jsonl 0s0_5__1s0-2s1-3s0-4s0-6s0-7s0 --jobs 3 --sigma-split 3 --sigma-levels 3 --caps 1,3600 --cadopts=--sat --hours 0.05 2>&1
echo "=== NODE end $(date -u +%T)"
