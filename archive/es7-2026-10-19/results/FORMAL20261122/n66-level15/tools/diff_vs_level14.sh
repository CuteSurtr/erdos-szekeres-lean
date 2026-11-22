#!/bin/bash
# Apply the identifier renames of DESIGN.md §0 to the level-14 sources (copy in scratch/l14renamed) and diff them
# against this directory's sources: the output is exactly the hand edits (level-dependent items, DESIGN.md §2).
set -e
D=/home/jay/research/data/formalize-20261122/n66-level15
S=/home/jay/research/data/formalize-20261122/n66enc
T=$D/scratch/l14renamed
rm -rf $T; mkdir -p $T/N66E15 $T/N66G15
for f in $D/lean/N66E15/*.lean; do cp $S/lean/N66Enc/$(basename $f) $T/N66E15/; done
for f in $D/lean/N66G15/*.lean; do cp $S/lean/N66Geo/$(basename $f) $T/N66G15/; done
sed -i -E 's/N66Enc/N66E15/g; s/N66Geo/N66G15/g; s/CubesUnsat132/CubesUnsat105/g; s/leaves132/leaves105/g; s/tree14/tree15/g; s/\bR0\b/R0_15/g; s/n66_bound_55_/n66_bound_54_/g; s/N66Bound 55/N66Bound 54/g; s/\b132\b/105/g; s/level-14/level-15/g' $T/N66E15/*.lean $T/N66G15/*.lean
cd $T && diff -r . $D/lean --exclude=data || true
