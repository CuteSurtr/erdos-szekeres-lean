#!/bin/bash
# start Sat Oct 31 15:10:14 UTC 2026 (epoch 1793459414), H=5.25, END=1793477414 (Sat Oct 31 20:10:14 UTC 2026)
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793477414 > /opt/work/lane.stdout 2>&1 &
