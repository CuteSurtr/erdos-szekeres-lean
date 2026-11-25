#!/bin/bash
# run Lean core's verified LRAT checker on CNF LRAT (see LeanLrat.lean); prints its s-line
exec /home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean --run /home/jay/research/data/lrat-lean-20261125/LeanLrat.lean "$1" "$2"
