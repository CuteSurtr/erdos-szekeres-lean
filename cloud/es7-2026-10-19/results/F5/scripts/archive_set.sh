#!/bin/bash
# copy one processed set (without work/) into data/sets/NAME, plus 32-set order-type fingerprints
S=$1; N=$(basename $S); D=$(dirname "$0")/../data/sets/$N
mkdir -p $D && cp -r $S/*.pts $S/*.json $S/*.jsonl $S/*.log $S/*.txt $S/sets32 $D/ 2>/dev/null
/usr/bin/python3 $(dirname "$0")/fingerprint.py $S/sets32/*.pts > $D/fingerprints32.txt
echo "$N: $(ls $S/sets32 | wc -l) files, $(ls $S/sets32 | grep -vc small) exact, $(awk '{print $2}' $D/fingerprints32.txt | sort -u | wc -l) distinct order types"
