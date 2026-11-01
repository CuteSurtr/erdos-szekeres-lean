#!/bin/bash
# start 1793416994 (Sat Oct 31 03:23:14 UTC 2026), END = start + 3.0 h - 15 min = 1793426894 (Sat Oct 31 06:08:14 UTC 2026)
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793426894 > /opt/work/lane.stdout 2>&1 &
