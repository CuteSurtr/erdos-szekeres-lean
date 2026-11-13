#!/bin/bash
# exact B&B (budget 33): 2,650 rows + main thread's cake_lpr-certified coupled rows + capacity row
cd /home/jay/research/lean/erdos-szekeres-lean
for c in 58 59 60 61 62; do
  r=$((84-c)); out=/home/jay/research/data/theory310-20261113/pbbcombo_c${c}_b33
  mkdir -p $out
  timeout 900 /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -u experiments/omission-final313-2026-10-11/search/pbb_strong.py 33 2 16 $out /home/jay/research/data/theory310-20261113/extra_cert_F${r}.json > $out.log 2>&1
  echo "c=$c: $(tail -1 $out.log | cut -c1-200)"
done
