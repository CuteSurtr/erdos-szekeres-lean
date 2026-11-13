#!/bin/sh
# usage: sh cert.sh CFG SCALE OUTNAME   (exact certificate: verify_cfg.py methods A/B/C + cvx2 two DPs)

mkdir -p cert
grep -v '^#' "$1" | sort -k1,1 -g -r > cert/$3.cfg
python3 -I verify_cfg.py cert/$3.cfg 8 0 9 $2 cert/$3 > cert/$3.log 2>&1
./cvx2 cert/$3 9 >> cert/$3.log 2>&1
python3 -I verify_cfg.py --pts cert/$3.pts 8 0 9 cert/$3.re >> cert/$3.log 2>&1
cmp cert/$3.otab cert/$3.re.otab && echo "OTAB-RECHECK IDENTICAL" >> cert/$3.log
shasum -a 256 cert/$3.pts cert/$3.otab >> cert/$3.log
tail -14 cert/$3.log
