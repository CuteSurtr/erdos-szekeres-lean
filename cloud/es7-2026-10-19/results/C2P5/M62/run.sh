#!/bin/bash
# start 1793460268, H=5.25, END=1793478268 (Sat Oct 31 20:24:28 UTC 2026)
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793478268 > /opt/work/lane.stdout 2>&1 &
