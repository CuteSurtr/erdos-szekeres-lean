#!/bin/bash
# START=1793429258 END=1793437358 (START + 2.5 h - 15 min)
setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793437358 > /opt/work/lane.stdout 2>&1 &
