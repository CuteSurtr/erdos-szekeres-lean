#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
rm -f conj8_certs.jsonl conj7_certs.jsonl
$PY conj_certs.py 7 conj8_certs.jsonl etv858.json pool_main.jsonl maxpiece.jsonl maxpiece_dr.jsonl maxpiece_r7.jsonl > conj8_certs.log 2>&1
$PY conj_certs.py 6 conj7_certs.jsonl etv757.json pool_hept.jsonl > conj7_certs.log 2>&1
