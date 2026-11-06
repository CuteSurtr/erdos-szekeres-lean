#!/bin/bash
SCR=/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad
cd /home/jay/research/lean/erdos-szekeres-lean
date -u +"start %FT%TZ" > $SCR/leancheck/out.txt
( /usr/bin/time -v lake env lean $SCR/leancheck/LayerLemmaAxioms.lean ) >> $SCR/leancheck/out.txt 2>&1
echo "exit $?" >> $SCR/leancheck/out.txt
date -u +"end %FT%TZ" >> $SCR/leancheck/out.txt
