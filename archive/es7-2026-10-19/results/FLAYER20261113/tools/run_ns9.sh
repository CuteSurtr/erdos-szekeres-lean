#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
$PY bfp.py nosplit_sample.jsonl > bfp_sample.log 2>&1
$PY realize_uncert.py nosplit_sample_bfp.jsonl 2 250000 nosplit_sample_real.jsonl > realize_uncert.log 2>&1
