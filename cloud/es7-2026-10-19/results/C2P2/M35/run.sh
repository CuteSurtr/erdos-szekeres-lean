#!/bin/bash
# start epoch 1793429261, H=2.5, END=start+H*3600-900
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793437361 > /opt/work/lane.stdout 2>&1 &
