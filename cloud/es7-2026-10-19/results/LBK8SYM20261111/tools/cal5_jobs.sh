#!/bin/bash
# 5-fold: template scans at t = 11 + centre (56 points exist; calibration) and t = 12 + centre (target 61)
D=/home/jay/research/data/lb-k8sym-20261111; cd $D
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
$PY -u cegar/template_scan.py 5 11 1 0 cegar/cal5t11 s11 30 31 100
$PY -u cegar/template_scan2.py 5 11 1 cegar/cal5t11 m11 30 32 200 2 3
$PY -u cegar/template_scan2.py 5 12 1 cegar/tplB5 m12 30 33 600 2 3
