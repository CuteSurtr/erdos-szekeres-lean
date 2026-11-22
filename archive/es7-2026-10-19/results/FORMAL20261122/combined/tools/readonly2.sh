#!/bin/bash
# combined part 2 (copy of readonly.sh: + the two N66 stores, MARKER_START2, readonly2.txt): files newer than data/MARKER_START2 (23:48 KST) in the read-only olean
# stores this build reads (res-slices-fv/olean is excluded: its driver writes 3519 files; audit.py checks the mtime of
# every imported file instead). Output: data/readonly2.txt (empty list = nothing written there since the marker).
W=/home/jay/research/data/formalize-20261122/combined
R=/home/jay/research/lean/erdos-szekeres-lean
S=("$R/.lake/build/lib/lean" $R/.lake/packages/*/.lake/build/lib/lean "$R/experiments/omission-compact-checker-2026-11-05/build/chain311/olean"
   "$R/experiments/omission-compact-checker-2026-11-05/build/CompactChecker" /home/jay/research/data/bal186-20261119/zrow/leanz/olean
   /home/jay/research/data/fv304-20261120/olean "$R/archive/es7-2026-10-19/results/ENCBLEAN/.lake/build/lib/lean"
   /home/jay/research/data/formalize-20261122/res118-rowblocks/build/olean /home/jay/research/data/formalize-20261122/res118/olean
   /home/jay/research/data/formalize-20261122/comp-audit/out/olean /home/jay/research/data/formalize-20261122/n66-level15/build/olean
   /home/jay/research/data/formalize-20261122/n66-l15-rows/build/olean /home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/lib/lean)
{ echo "# stores checked:"; printf '#  %s\n' "${S[@]}"; echo "# files newer than $(stat -c %y $W/data/MARKER_START2):"
  find "${S[@]}" -newer $W/data/MARKER_START2 -print; echo "# end"; } > $W/data/readonly2.txt
