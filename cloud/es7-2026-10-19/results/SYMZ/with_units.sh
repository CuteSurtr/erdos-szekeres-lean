#!/bin/bash
# usage: with_units.sh CNF UNITS OUT  -- CNF plus the unit clauses in UNITS (header adjusted)
n=$(wc -l < "$2" | tr -d ' ')
awk -v n=$n '/^p cnf/ {print $1, $2, $3, $4 + n; next} {print}' "$1" > "$3"; cat "$2" >> "$3"
