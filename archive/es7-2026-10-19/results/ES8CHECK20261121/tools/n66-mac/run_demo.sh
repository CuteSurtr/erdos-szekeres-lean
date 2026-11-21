#!/bin/sh
# n66-mac demo: one UP-refuted level-15 cube (hhhohh) through the Mac copy of p2_cert.sh (state path), single thread.
A=SCRATCH/agents/n66-mac
R36=SCRATCH/r36/bin
export P2_W=$A/w P2_PY=$A/bin/py CAKE=$R36/cake_lpr CADICAL=$R36/cadical ETV_A=4 ETV_B=4 P2_UNIT=none
cd $A/w
/usr/bin/time -l ./p2_cert.sh p2/c15mac/hhhohh/it1 p2/c15mac/hhhohh_state.json > $A/demo_run.out 2>&1
echo "p2_cert.sh exit $?" >> $A/demo_run.out
