#!/bin/bash
# start 1793460281 (2026-10-31 15:24:41 UTC); END = start + 5.25 h - 15 min = 1793478281
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793478281 > /opt/work/lane.stdout 2>&1 &
