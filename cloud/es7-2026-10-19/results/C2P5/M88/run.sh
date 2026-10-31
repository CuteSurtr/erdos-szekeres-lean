#!/bin/bash
# start 1793459426 (2026-10-31T15:10:26Z), H=5.25, END = start + 5.25h - 15min
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793477426 > /opt/work/lane.stdout 2>&1 &
