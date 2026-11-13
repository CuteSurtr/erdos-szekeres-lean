#!/bin/bash
# start 1793416997 (2026-10-31T03:23:17Z), H = 3.0, END = start + 3 h - 15 min
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793426897 > /opt/work/lane.stdout 2>&1 &
