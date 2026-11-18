#!/bin/bash
# LP-polish realizer on every cex file that is still abstract
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
for f in cex/*.json; do
  if grep -q '"realized": false' "$f"; then timeout 240 $PY realize2.py "$f" 25 >> realize2.log 2>&1; fi
done
