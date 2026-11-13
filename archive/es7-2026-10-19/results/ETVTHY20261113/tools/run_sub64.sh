#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
$PY sub5cap.py
$PY conj_certs.py 7 conj8_sub64_certs.jsonl pool_sub64.jsonl > conj8_sub64.log 2>&1
