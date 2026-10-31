#!/bin/bash
# start Sat Oct 31 19:25:48 UTC 2026 (epoch 1793474748), H=4.5, END = start + 4.5 h - 15 min
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793490048 > /opt/work/lane.stdout 2>&1 &
