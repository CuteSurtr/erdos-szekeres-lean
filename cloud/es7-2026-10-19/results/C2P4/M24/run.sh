#!/bin/bash
# start 1793451682 (Sat Oct 31 13:01:22 UTC 2026), H=2.5, END = start + 2.5 h - 15 min
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793459782 > /opt/work/lane.stdout 2>&1 &
