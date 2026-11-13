#!/bin/bash
# start 1793451690 (2026-10-31 13:01:30Z), H=2.5, END = start + 2.5 h - 15 min = 1793459790 (Sat Oct 31 15:16:30 UTC 2026)
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793459790 > /opt/work/lane.stdout 2>&1 &
