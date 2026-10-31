#!/bin/bash
# start 2026-10-31 03:22:44 UTC (epoch 1793416964), H = 3.0, END = start + 3 h - 15 min = 1793426864 (06:07:44 UTC)
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793426864 > /opt/work/lane.stdout 2>&1 &
