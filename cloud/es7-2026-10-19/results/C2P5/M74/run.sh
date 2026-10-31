#!/bin/bash
# start 1793459418 (epoch), H=5.25, END = start + 5.25 h - 15 min
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793477418 > /opt/work/lane.stdout 2>&1 &
