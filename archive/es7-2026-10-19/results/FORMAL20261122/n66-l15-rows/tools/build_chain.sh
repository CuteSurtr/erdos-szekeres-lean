#!/bin/bash
# Compile the theorem-side chain in order (inside a unit; one lean process per module; stop at the first failure).
# usage: build_chain.sh [first-module]   (resume from that module)
D=/home/jay/research/data/formalize-20261122/n66-l15-rows
MODS="N66R15Geo/Bound N66R15Chk/Tables N66R15Chk/Look N66R15Chk/TabPs"
for i in $(seq 0 13); do MODS="$MODS N66R15Chk/TabTt$i"; done
MODS="$MODS N66R15Chk/TabTt N66R15Chk/TabDr0 N66R15Chk/TabDr1 N66R15Chk/TabDr N66R15Chk/TabCan N66R15Chk/Check"
for i in 0 1 2 3; do MODS="$MODS N66R15Chk/certsOkTF$i"; done
for i in 0 1 2 3; do MODS="$MODS N66R15Chk/certsOkCF$i"; done
MODS="$MODS N66R15Chk/CertsOk N66R15Chk/IsCore"
for i in $(seq 0 27); do MODS="$MODS N66R15Chk/Rows$i"; done
MODS="$MODS N66R15Chk/RowsAll N66R15Geo/Assembly N66R15Geo/End N66R15Geo/Final"
if [ -n "${1:-}" ]; then MODS=$(echo $MODS | tr ' ' '\n' | sed -n "/^${1//\//\\/}\$/,\$p" | tr '\n' ' '); fi
$D/tools/lc.sh $MODS
