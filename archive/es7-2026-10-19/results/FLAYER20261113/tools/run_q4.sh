#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
$PY compose.py > compose.log 2>&1
$PY lemma_check.py pool_etv.jsonl pool_compose.jsonl pool_sub64.jsonl pool_size.jsonl sets_pE.jsonl sets_pX.jsonl sets_pEuA.jsonl sets_pZ.jsonl sets_psize.jsonl sets_etvwalk.jsonl > lemma_check.log 2>&1
$PY realize_small.py singles.jsonl singles_real.jsonl > singles_real.log 2>&1
$PY an3.py > an3.log 2>&1
# verified abstract witnesses for the refuted level-set candidates (signotopes saved)
$PY sample_fl.py 38 1 samples_lvl.jsonl E 30 > samples_lvl.log 2>&1
$PY sample_fl.py 40 1 samples_lvl.jsonl E 33 >> samples_lvl.log 2>&1
$PY sample_fl.py 40 1 samples_lvl.jsonl EuA 36 >> samples_lvl.log 2>&1
$PY sample_fl.py 44 1 samples_lvl.jsonl EuA 40 >> samples_lvl.log 2>&1
$PY sample_fl.py 40 1 samples_lvl.jsonl EnA 20 >> samples_lvl.log 2>&1
$PY split.py samples 6 6 samples_E26.jsonl samples_lvl.jsonl > split_abs.log 2>&1
# abstract 50-point configurations
$PY sample_fl.py 50 1,2 samples_50.jsonl > samples_50.log 2>&1
$PY split.py samples 6 6 samples_50.jsonl >> split_abs.log 2>&1
$PY cert.py 4 8 23 plain 400 > q4b.log 2>&1
