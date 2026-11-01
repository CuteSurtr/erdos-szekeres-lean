#!/bin/bash
# start Sat Oct 31 03:23:15 UTC 2026 (epoch 1793416995), END = start + 3.0 h - 15 min
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793426895 > /opt/work/lane.stdout 2>&1 &
