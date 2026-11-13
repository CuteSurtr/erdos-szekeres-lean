#!/bin/bash
# start 1793439766 (epoch, session start), H=2.5, END=start+2.5h-15min
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793447866 > /opt/work/lane.stdout 2>&1 &
