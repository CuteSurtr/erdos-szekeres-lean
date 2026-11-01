#!/bin/bash
# Runs the project's own SYMMAX checkers (verifyg.py / verify5.py + brute.c) on COPIES of the example files.
cd "$(dirname "$0")"
while read -r G F K; do
  echo "## verifyg $G $F $K"; python3 -I code/verifyg.py "$G" "data/$F" "$K"; ./code/brute "$K" < "data/$F.orient"
done <<'LIST'
3 c3_27points.txt 7
3 c3_30points.txt 7
3 c3_31points.txt 7
4 c4_28points.txt 7
6 c6_30points.txt 7
M mirror_32points.txt 7
2 sym7_32points.txt 7
2 k6_c2_16points.txt 6
3 k6_c3_13points.txt 6
4 k6_c4_16points.txt 6
M k6_mirror_12points.txt 6
LIST
while read -r F K; do
  echo "## verify5 $F $K"; python3 -I code/verify5.py "data/$F" "$K"; ./code/brute "$K" < "data/$F.orient"
done <<'LIST'
c5_30points.txt 7
c5_31points.txt 7
c5_31minus_centre.txt 7
k6_c5_16points.txt 6
LIST
