#!/bin/bash
# start 1793416995 (Sat Oct 31 03:23:15 UTC 2026), END = start + 3 h - 15 min = 1793426895 (Sat Oct 31 06:08:15 UTC 2026)
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793426895 > /opt/work/lane.stdout 2>&1 &
