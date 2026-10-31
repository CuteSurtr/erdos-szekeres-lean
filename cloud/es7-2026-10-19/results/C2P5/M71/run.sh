#!/bin/bash
# start epoch 1793459370, H=5.25, END=start+H*3600-900
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793477370 > /opt/work/lane.stdout 2>&1 &
