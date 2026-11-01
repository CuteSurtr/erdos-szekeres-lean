#!/bin/bash
cd "$(dirname "$0")"
V=${PY:-python3}
R=${ES7_RESULTS:-$(cd ../.. && pwd)}
/usr/bin/time -l $V test_real.py 4 $R/SYMMAX/c4_28points.txt 24 28 > logs/real_c4_28.log 2>&1
/usr/bin/time -l $V test_real.py 5 $R/SYMMAX/c5_30points.txt 25 30 > logs/real_c5_30.log 2>&1
/usr/bin/time -l $V test_real.py 5 $R/SYMMAX/c5_31points.txt 25 30 > logs/real_c5_31.log 2>&1
echo REAL DONE
