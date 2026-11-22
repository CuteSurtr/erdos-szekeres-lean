#!/bin/bash
# combined: files newer than data/MARKER_START (21:10 KST, before this agent's first write) in the read-only olean
# stores this build reads (res-slices-fv/olean is excluded: its driver writes 3519 files; audit.py checks the mtime of
# every imported file instead). Output: data/readonly.txt (empty list = nothing written there since the marker).
W=/home/jay/research/data/formalize-20261122/combined
R=/home/jay/research/lean/erdos-szekeres-lean
S=("$R/.lake/build/lib/lean" $R/.lake/packages/*/.lake/build/lib/lean "$R/experiments/omission-compact-checker-2026-11-05/build/chain311/olean"
   "$R/experiments/omission-compact-checker-2026-11-05/build/CompactChecker" /home/jay/research/data/bal186-20261119/zrow/leanz/olean
   /home/jay/research/data/fv304-20261120/olean "$R/archive/es7-2026-10-19/results/ENCBLEAN/.lake/build/lib/lean"
   /home/jay/research/data/formalize-20261122/res118-rowblocks/build/olean /home/jay/research/data/formalize-20261122/res118/olean
   /home/jay/research/data/formalize-20261122/comp-audit/out/olean /home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/lib/lean)
{ echo "# stores checked:"; printf '#  %s\n' "${S[@]}"; echo "# files newer than $(stat -c %y $W/data/MARKER_START):"
  find "${S[@]}" -newer $W/data/MARKER_START -print; echo "# end"; } > $W/data/readonly.txt
