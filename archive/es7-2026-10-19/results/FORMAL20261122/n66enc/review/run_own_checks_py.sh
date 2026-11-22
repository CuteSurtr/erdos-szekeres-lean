#!/bin/bash
# Re-run of the own_checks.py step only (the first run stopped at a missing justification file of an UP-refuted cube).
RV=/home/jay/research/data/formalize-20261122/n66enc/review
cd $RV
/usr/bin/time -v /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -I $RV/own_checks.py 7 3000 > $RV/own_checks.out 2> $RV/own_checks.time
echo "own_checks rc=$?"
