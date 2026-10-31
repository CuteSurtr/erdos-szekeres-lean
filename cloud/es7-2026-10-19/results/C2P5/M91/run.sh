#!/bin/bash
# START = 1793459507 (2026-10-31 15:11:47 UTC); END = START + 5.25 h - 15 min = 1793477507 (20:11:47 UTC)
# Note: a first launch at 15:14:32 accidentally started two lane instances; both were killed within a minute
# (no record written), unit.cnf/unit.lrat/lane.log removed, base.cnf re-verified, and the single lane below was
# started at 15:15:05 UTC.
cd /opt/work && setsid nohup python3 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl 1793477507 > /opt/work/lane.stdout 2>&1 &
