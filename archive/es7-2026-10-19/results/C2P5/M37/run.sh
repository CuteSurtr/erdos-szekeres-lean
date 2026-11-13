#!/bin/bash
# C2P5 M37 lane, started Sat Oct 31 20:08:57 UTC 2026 (start epoch 1793477195, H=4.5)
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793492495 > /opt/work/lane.stdout 2>&1 &
