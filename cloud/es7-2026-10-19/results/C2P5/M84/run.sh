#!/bin/bash
# start epoch 1793459472, H=5.25, END=start+H-15min
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793477472 > /opt/work/lane.stdout 2>&1 &
