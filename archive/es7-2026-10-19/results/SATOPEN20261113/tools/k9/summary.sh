#!/bin/sh
# one line per cube: name | solved line | verdict (VERIFIED_LINES / noproof / heapfail) | conflicts
cd /home/jay/research/data/satopen-20261113/k9/cubes
for d in *; do
  [ -f $d/solved ] || continue
  v=$(grep -h -o "VERIFIED_LINES [0-9]*\|noproof probe" $d/result.txt 2>/dev/null | head -1)
  [ -f $d/heapfail ] && v="$v heapfail:$(wc -l < $d/heapfail)"
  c=$(grep -E "^c conflicts:" $d/cadical.out 2>/dev/null | awk '{print $3}')
  echo "$d | $(cut -c1-60 $d/solved) | ${v:-pending} | conflicts ${c:-?}"
done
