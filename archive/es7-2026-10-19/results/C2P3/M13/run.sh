#!/bin/bash
# start 1793439782 (2026-10-31T09:43:02Z), H=2.5, END=start+H h-15 min=1793447882
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793447882 > /opt/work/lane.stdout 2>&1 &
