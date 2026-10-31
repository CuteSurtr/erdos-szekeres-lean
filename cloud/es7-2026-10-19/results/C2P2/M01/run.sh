#!/bin/bash
# start epoch 1793429249 (2026-10-31 06:47:29 UTC), H=2.5 h, END = start + 2.5 h - 15 min = 1793437349
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793437349 > /opt/work/lane.stdout 2>&1 &
