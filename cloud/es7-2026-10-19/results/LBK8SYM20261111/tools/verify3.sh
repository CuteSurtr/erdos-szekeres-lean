#!/bin/bash
# verify3.sh PTS DIR : full exact verification of a threefold .pts set (rows w0 w1 w2, point w0 + w1 w + w2 w^2).
# (1) ES8SYM pipeline (verify_cfg exact Z[w] + interval signs, cvx2 two DPs, cvxcheck DFS, crosscheck_decimal); the
#     nested-layer flag of verify_cfg does not apply to threefold sets (no layer lemma), all other flags must hold;
# (2) lattice coordinates a = w0 - w2, b = w1 - w2: ES8SYM verify_set.py (big-integer DP, C3 symmetry) and enum_convex.c
#     (__int128 DFS listing); (3) verify_indep.py (stdlib, two anchored DPs); (4) SIX60 dfs_convex.c (exhaustive).
D=/home/jay/research/data/lb-k8sym-20261111; T=/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/ES8SYM/tools
P=$(readlink -f $1); mkdir -p $2; cd $2
$D/tools/verify_mf.sh $P 3 $(head -1 $P | sed -E 's/.*C=([01]).*/\1/') . > /dev/null 2>&1
grep -E "verify_cfg|'m'|PASS|FAIL|8-gons|8-subsets|largest" verify.log
awk '!/^#/ && NF==3 {print $1-$3, $2-$3}' $P > lattice.txt
python3 -B $T/verify_set.py lattice.txt 8 C3 > verify_set.log 2>&1; tail -n 4 verify_set.log
$D/src/enum_convex lattice.txt - none > enum_convex.log 2>&1; tail -n 4 enum_convex.log
python3 -B $D/tools/verify_indep.py 3 $P 8 > verify_indep.log 2>&1; tail -n 3 verify_indep.log
$D/src/dfs_convex lattice.txt > dfs_convex.log 2>&1; tail -n 3 dfs_convex.log
