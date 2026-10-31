#!/bin/bash
# start epoch 1793439773 (Sat Oct 31 09:42:53 UTC 2026), H=2.5, END = start + 2.5 h - 15 min
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793447873 > /opt/work/lane.stdout 2>&1 &
