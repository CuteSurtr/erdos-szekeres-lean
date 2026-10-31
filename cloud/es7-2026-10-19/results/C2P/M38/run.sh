#!/bin/bash
# start 1793416961 (Sat Oct 31 03:22:41 UTC 2026), H=3.0, END = start + 3h - 15min
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793426861 > /opt/work/lane.stdout 2>&1 &
