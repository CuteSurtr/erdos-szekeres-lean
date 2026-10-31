#!/bin/bash
# start 1793451686, H=2.5, END=start+2.5h-15min=1793459786
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793459786 > /opt/work/lane.stdout 2>&1 &
