#!/bin/bash
# start 1793474753 (2026-10-31T19:25:53Z), H=4.5, END = start + 4.5 h - 15 min
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793490053 > /opt/work/lane.stdout 2>&1 &
