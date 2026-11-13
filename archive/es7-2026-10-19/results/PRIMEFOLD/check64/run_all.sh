#!/bin/sh
# Exact check of the 7-fold 64-point files in ../sets/k8 (scripts written from scratch by an independent check).
# For each file: distinctness, 7-fold invariance, exact orientation table (no zero), a 110-digit decimal
# cross-check of every sign, convex k-gon counts by an anchor DP, and the same counts by a separate C enumerator.
# Output: check64.log.  Takes about a minute.
set -e
D=$(cd "$(dirname "$0")" && pwd)
cd "$D"
${CC:-cc} -O2 ${CFLAGS:-} -o cvxenum cvxenum.c
{
for f in c7_64pts_small c7_64pts_9layers_centre c7_64_own_s1000 c7_64pts_9layers_centre_own \
         p7_compound_64 p7_two_orbit_64 rule_p7_64pts m7_x2_G9s_centre; do
  echo "######## $f"
  python3 -I verify64.py ../sets/k8/$f.pts $f.signs | sed "s#^file .*/sets/#file sets/#"
  ./cvxenum $f.signs
  python3 -I modules.py ../sets/k8/$f.pts 20 | sed -n 2p
done
echo "######## p7_compound_64 and p7_two_orbit_64: identical orientation tables under the row labelling?"
cmp p7_compound_64.signs p7_two_orbit_64.signs && echo IDENTICAL
echo "######## DP vs brute force on 300 random 13-point subsets of p7_compound_64"
python3 -I dp_bruteforce_test.py ../sets/k8/p7_compound_64.pts 300 13
echo "######## line-module enumerator vs brute force"
python3 -I modules.py ../sets/k8/p7_compound_64.pts 20 --selftest | head -1
} > check64.log 2>&1
rm -f ./*.signs
cat check64.log
