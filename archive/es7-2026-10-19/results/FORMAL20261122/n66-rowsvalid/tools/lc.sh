#!/bin/bash
# Compile one module of this work dir with the bare lean (inside a unit). usage: lc.sh <Pkg/Mod> [extra lean args]
# Writes build/olean/<Pkg/Mod>.olean (+ .ilean) and logs/<Pkg_Mod>.log; prints time -v summary into the log.
set -u
D=/home/jay/research/data/formalize-20261122/n66-rowsvalid
source $D/tools/env.sh
m=$1; shift
mkdir -p $D/build/olean/$(dirname $m) $D/logs
log=$D/logs/$(echo $m | tr / _).log
cd $D/lean
{ echo "== $(date '+%F %T') lean $m $*"; /usr/bin/time -v $TC/bin/lean -j1 -R . -o $D/build/olean/$m.olean -i $D/build/olean/$m.ilean "$@" $m.lean; echo "rc=$?"; } > $log 2>&1
tail -1 $log
