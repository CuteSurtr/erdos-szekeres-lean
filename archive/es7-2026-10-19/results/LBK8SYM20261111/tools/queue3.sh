#!/bin/bash
# queue3.sh NAME TMAX FILE... : one unit that runs the phase-fixed CEGAR (pair cuts) on the given live phase vectors in turn
D=/home/jay/research/data/lb-k8sym-20261111
NAME=$1; TMAX=$2; shift 2
cd $D && ./launch_pf.sh $NAME 8G 3 $TMAX --pairs 1 --stop-at $(date -d "2026-11-12 04:00" +%s) "$@"
