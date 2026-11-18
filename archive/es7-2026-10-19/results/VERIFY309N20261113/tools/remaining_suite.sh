#!/bin/bash
set -eu
R=/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/VERIFY309N20261113
V=/home/jay/research/data/verify309-codex-20261113
while systemctl --user is-active --quiet nov13c-vfy-codex-cert57; do sleep 5; done
if ! test -f "$V/VERIFIED57"; then
  # Larger checker heap only after the other large verifier jobs have finished.
  while systemctl --user is-active --quiet nov13c-vfy-E2-n37 || systemctl --user is-active --quiet p2-watch-d1b || systemctl --user is-active --quiet nov13c-vfy-D1b-m16; do sleep 5; done
  test "$(cat "$V/cadical57.exit")" = 20
  /home/jay/.local/bin/cake_lpr --CML_HEAP_SIZE=2000 --CML_STACK_SIZE=100 /home/jay/research/data/n66-20261113/p2/b12/it1/trim.cnf "$V/fresh57.lrat" > "$V/cake57-retry.log" 2>&1
  grep -Fx 's VERIFIED UNSAT' "$V/cake57-retry.log"
  touch "$V/VERIFIED57"
fi
/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -u "$R/tools/certify_new_rows.py" > "$R/logs/row-certificates.jsonl" 2>&1
/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -u "$R/tools/recert_residual.py" > "$R/logs/residual-certificates.jsonl" 2>&1
