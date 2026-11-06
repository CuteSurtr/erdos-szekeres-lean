#!/bin/bash
# Re-run of the recorded lower-bound checkers on copies (6 Nov 2026, for the P1 draft).
SCR=/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad
R=/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results
cd $SCR/rerun
date -u +"start %FT%TZ" > timing.txt
( time sh check64/run_all.sh > /dev/null ) 2>> timing.txt
gcc -O2 -o six60/dfs_convex $R/SIX60/verify/dfs_convex.c
for f in A B C C2 D; do
  python3 -I $R/SIX60/verify/verify60.py $R/SIX60/sets/c6_60pts_$f.pts > six60/verify60_$f.log 2>&1
  python3 -I -c "import sys
for l in open(sys.argv[1]):
    l=l.split('#')[0].split()
    if l: w=list(map(int,l)); print(w[0]-w[2]-w[3]+w[5], w[1]+w[2]-w[4]-w[5])" $R/SIX60/sets/c6_60pts_$f.pts > six60/${f}_ab.txt
  ( time ./six60/dfs_convex six60/${f}_ab.txt > six60/dfs_$f.log ) 2>> timing.txt
done
date -u +"end %FT%TZ" >> timing.txt
