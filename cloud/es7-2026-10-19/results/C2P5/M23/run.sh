#!/bin/bash
# start 1793473868 (2026-10-31T19:11:08Z), END = start + 4.5 h - 15 min = 1793489168 (2026-10-31T23:26:08Z)
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793489168 > /opt/work/lane.stdout 2>&1 &
