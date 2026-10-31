#!/bin/bash
# start epoch 1793459590 (2026-10-31 15:13:10 UTC), H = 5.25, END = start + 5.25 h - 15 min = 1793477590
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793477590 > /opt/work/lane.stdout 2>&1 &
