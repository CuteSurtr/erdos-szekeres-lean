#!/bin/bash
# F3: rebuild the skip file from W25 and all other WAVE2 U3_L logs
cd /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results
python3 WAVE2/F3/mkskip.py 7ab00d97d5047e0003bd8d254560dc8464d880d7165c6d7f0e01fab79ee0f823 \
  WAVE2/F3/U3_L/share.icnf /opt/work/skip.icnf.new WAVE1/W25/U3_L/leaves.jsonl \
  $(ls WAVE2/*/U3_L/leaves.jsonl | grep -v '^WAVE2/F3/') && mv /opt/work/skip.icnf.new /opt/work/skip.icnf
cp /opt/work/skip.icnf WAVE2/F3/U3_L/skip.icnf
