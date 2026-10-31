#!/bin/bash
# start 1793460251 (Sat Oct 31 15:24:11 UTC 2026), H=5.25, END = start + 5.25 h - 15 min
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793478251 > /opt/work/lane.stdout 2>&1 &
