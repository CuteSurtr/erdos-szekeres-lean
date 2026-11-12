#!/bin/bash
# calibration of the template scans at 4-fold t = 13 (52 points, which exist)
D=/home/jay/research/data/lb-k8sym-20261111; cd $D
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
$PY -u cegar/template_scan.py 4 13 0 1 cegar/cal4t13 s13 30 21 150
$PY -u cegar/template_scan2.py 4 13 0 cegar/cal4t13 m13 30 22 300 3 3
