#!/bin/bash
SCR=/sandbox
cd /path/to/repo
date -u +"start %FT%TZ" > $SCR/leancheck/out.txt
( /usr/bin/time -v lake env lean $SCR/leancheck/LayerLemmaAxioms.lean ) >> $SCR/leancheck/out.txt 2>&1
echo "exit $?" >> $SCR/leancheck/out.txt
date -u +"end %FT%TZ" >> $SCR/leancheck/out.txt
