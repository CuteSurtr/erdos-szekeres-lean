#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
$PY bfp_verify.py split_counterexample_5_5_14_bfp.jsonl nosplit_more_bfp.jsonl nosplit_sample_bfp.jsonl > bfp_verify.log 2>&1
$PY verify_nosplit_many.py nosplit_check40.jsonl > verify_nosplit_many.log 2>&1
$PY sample56.py 25 1 61 > sample56.log 2>&1
$PY gen2.py 41 900000 pE init_E25.json "f[0]==4" 0.3 > ns12_pE.log 2>&1
