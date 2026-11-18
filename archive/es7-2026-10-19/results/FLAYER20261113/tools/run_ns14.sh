#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
$PY gen2.py 51 900000 pEuA init_E31.json "f[0]==4 or f[3]>=1" 0.3 > ns14.log 2>&1
$PY gen2.py 52 900000 pE init_E31.json "f[0]==4" 0.3 >> ns14.log 2>&1
