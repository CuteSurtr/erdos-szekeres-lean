#!/bin/bash
# C2P5 M02: start 1793470351 (2026-10-31T18:12:31Z), H = 4.5, END = start + 4.5 h - 15 min
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793485651 > /opt/work/lane.stdout 2>&1 &
