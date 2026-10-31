#!/bin/bash
# start 1793439761 (Sat Oct 31 09:42:41 UTC 2026), H=2.5, END = start + 2.5 h - 15 min = 1793447861 (Sat Oct 31 11:57:41 UTC 2026)
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793447861 > /opt/work/lane.stdout 2>&1 &
