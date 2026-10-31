#!/bin/bash
# generate control (b) and main-run CNFs sequentially (one core)
cd "$(dirname "$0")"
for args in "18 6 2" "18 6 3" "18 6 6" "18 6 9" "33 7 11" "32 7 2" "33 7 3"; do
  set -- $args; tag="n$1k$2m$3"
  echo "== $tag $(date)"
  /usr/bin/time -p python3 symcnf.py $args -o cnf/$tag.cnf --map cnf/$tag.json 2>&1
done
echo "== done $(date)"
