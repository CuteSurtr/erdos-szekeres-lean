#!/bin/bash
# start Sat Oct 31 13:01:34 UTC 2026 (epoch 1793451694), END = start + 2.5 h - 15 min
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793459794 > /opt/work/lane.stdout 2>&1 &
