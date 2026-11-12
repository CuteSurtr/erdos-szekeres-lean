#!/bin/sh
# usage: withunits.sh BASE.cnf UNITS OUT.cnf   (BASE + unit clauses, header adjusted)
set -e
read -r p c nv ncl < "$1"
nu=$(wc -l < "$2")
{ echo "p cnf $nv $((ncl + nu))"; tail -n +2 "$1"; cat "$2"; } > "$3"
