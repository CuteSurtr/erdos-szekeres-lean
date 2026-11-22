#!/bin/bash
# The one review unit: R2 (compile_review.sh, measured with /usr/bin/time -v) then R3 (hashcheck.py on the frozen exe).
RV=/home/jay/research/data/formalize-20261122/v182-lean/review
cd $RV
/usr/bin/time -v $RV/tools/compile_review.sh > $RV/logs/compile_review.log 2>&1
echo "COMPILE_RC $?" >> $RV/logs/compile_review.log
rm -rf $RV/tmp_hb
/usr/bin/time -v /usr/bin/python3 -I -B $RV/tools/hashcheck.py $RV/logs $RV/tmp_hb > $RV/logs/hashcheck.log 2>&1
echo "HASHCHECK_RC $?" >> $RV/logs/hashcheck.log
