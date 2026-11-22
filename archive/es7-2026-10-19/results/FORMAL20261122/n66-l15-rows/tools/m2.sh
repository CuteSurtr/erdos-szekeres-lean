#!/bin/bash
# M2 in one unit: freeze check, M1 controls (tools/m1.sh), then M9 (tools/hash_binding.py), then freeze check again.
D=/home/jay/research/data/formalize-20261122/n66-l15-rows
cd $D
tools/freeze.sh check || { echo FREEZE_BROKEN; exit 3; }
tools/m1.sh > logs/m1.log 2>&1; echo "m1 exit $?"
python3 -I tools/hash_binding.py logs/m9_hash_binding.tsv > logs/m9.log 2>&1; echo "hash_binding exit $?"
tools/freeze.sh check || { echo FREEZE_BROKEN_AFTER; exit 3; }
