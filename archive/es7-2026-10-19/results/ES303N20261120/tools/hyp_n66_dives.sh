#!/bin/bash
# HEURISTIC: production-option dives with HYPOTHETICAL capacity rows h(Z), h(Z*) >= 16 (N66 <= 54) or 17 (N66 <= 53).
# Neither bound is proved; this only prices the N66 lever after the Z*-row.
cd /home/jay/research/data/bal186-20261119/zrow/hyp54
FB=/home/jay/research/data/bal186-20261119/fastbb256
PO="--ktop=16 --klow=4 --dtop=0 --dmid=0"
for B in 69 70 71; do $FB dive hyp_rhs16.rows $B 200 1 d16_b$B.json $PO > d16_b$B.log 2>&1; done
for B in 71 72 73; do $FB dive hyp_rhs17.rows $B 200 1 d17_b$B.json $PO > d17_b$B.log 2>&1; done
echo DONE
