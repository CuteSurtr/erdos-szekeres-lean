#!/bin/bash
# start epoch 1793429214, END = start + 2.5 h - 15 min = 1793437314 (Sat Oct 31 09:01:54 UTC 2026)
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793437314 > /opt/work/lane.stdout 2>&1 &
