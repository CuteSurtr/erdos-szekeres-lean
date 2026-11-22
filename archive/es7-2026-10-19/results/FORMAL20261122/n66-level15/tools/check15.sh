#!/bin/bash
# Compile check/Check15.lean against this directory's oleans (no olean written).
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/n66-level15
source $D/tools/geo_env.sh
cd $D/check
/usr/bin/time -f "Check15 lean wall=%e s maxrss=%M KB" /home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean -j1 Check15.lean
