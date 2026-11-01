#!/bin/bash
# smallpipe.sh BUDGET files... : compress then sat.c-check the small realizations
cd /tmp/claude-0/-home-user-erdos-szekeres-lean/7d9c6ca0-022c-5e66-8370-d636a42cff9f/scratchpad
S=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/F2/scripts
B=$1; shift
python3 $S/compress32.py $B "$@" >> compress.log
for f in "$@"; do s=${f%.pts}_small.pts; [ -f $s ] && python3 $S/check32.py ./satc ./ext_solve ./brute_kgon base33.cnf new32swd $s >> small_check.jsonl; done
