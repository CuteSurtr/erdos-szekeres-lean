#!/bin/bash
set -eu
V=/home/jay/research/data/verify309-codex-20261113
D=/home/jay/research/data/n66-20261113/p2/b12/it1
mkdir -p "$V"
sha256sum "$D/trim.cnf" "$D/trim.lrat" > "$V/original.sha256"
/usr/bin/cadical --version > "$V/cadical.version"
set +e
/usr/bin/cadical --lrat=true --binary=false "$D/trim.cnf" "$V/fresh57.lrat" > "$V/cadical57.log" 2>&1
rc=$?
set -e
echo "$rc" > "$V/cadical57.exit"
test "$rc" = 20
sha256sum "$V/fresh57.lrat" > "$V/fresh57.lrat.sha256"
/home/jay/.local/bin/cake_lpr --CML_HEAP_SIZE=1000 --CML_STACK_SIZE=100 "$D/trim.cnf" "$V/fresh57.lrat" > "$V/cake57.log" 2>&1
grep -Fx 's VERIFIED UNSAT' "$V/cake57.log"
touch "$V/VERIFIED57"
