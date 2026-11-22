#!/bin/bash
# M9 hash binding (tools/hash_binding15.py, Python hashlib) and the final checks, in one unit.
D=/home/jay/research/data/formalize-20261122/n66-level15
cd $D
echo "== statement check $(date '+%F %T')"
tools/check15.sh > logs/check15.log 2>&1; echo "check15 exit $?"
echo "== m9 $(date '+%F %T')"
python3 -I tools/hash_binding15.py logs/m9_hash_binding.tsv; echo "hash_binding15 exit $?"
echo "== final checks $(date '+%F %T')"
tools/final_checks15.sh
echo "== done $(date '+%F %T')"
