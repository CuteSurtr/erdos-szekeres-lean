#!/bin/bash
# Spec comparison (spec.py) on small CNFs written by the unmodified encoder copy zcnf_orig.py.
E=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$E/cnf"
cd "$E/cnf"
for tk in "4 5" "4 6" "5 5" "5 6" "6 6" "6 7" "7 7" "8 7"; do
  set -- $tk
  for hf in "" "--hull"; do
    nm=orig_t$1k$2${hf:+h}
    python3 -I "$E/zcnf_orig.py" rot $1 $2 --m 2 $hf -o $nm.cnf --map $nm.json > /dev/null
    echo "== $nm"
    python3 -I "$E/spec.py" $nm.cnf $nm.json $hf | grep -E "SPEC|DIFFER|extra"
  done
done
