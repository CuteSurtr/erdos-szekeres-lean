#!/bin/bash
# Reviewer's own diff (slot lrv3): level-14 sources (n66enc, manifest-checked) with the renames applied by sed,
# against the level-15 sources. Output: own_diff_vs_level14.txt. Read-only on both trees; writes only under review/.
set -u
F=/home/jay/research/data/formalize-20261122
RV=$F/n66-level15/review
cd $F/n66enc && sha256sum -c logs/final_source_manifest.sha256 > $RV/own_l14_manifest_check.txt 2>&1
echo "level-14 manifest: $(grep -c ': OK$' $RV/own_l14_manifest_check.txt) OK, $(grep -vc ': OK$' $RV/own_l14_manifest_check.txt) not OK"
rm -rf $RV/l14ren; mkdir -p $RV/l14ren
cp -r $F/n66enc/lean/N66Enc $RV/l14ren/N66E15; cp -r $F/n66enc/lean/N66Geo $RV/l14ren/N66G15
rm -f $RV/l14ren/N66G15/ImportTest.lean
find $RV/l14ren -name '*.lean' -exec sed -i -e 's/N66Enc/N66E15/g' -e 's/N66Geo/N66G15/g' \
  -e 's/CubesUnsat132/CubesUnsat105/g' -e 's/leaves132/leaves105/g' -e 's/tree14/tree15/g' -e 's/\bR0\b/R0_15/g' \
  -e 's/n66_bound_55_/n66_bound_54_/g' -e 's/N66Bound 55/N66Bound 54/g' {} \;
cd $RV/l14ren && diff -r N66E15 $F/n66-level15/lean/N66E15 > $RV/own_diff_vs_level14.txt
diff -r N66G15 $F/n66-level15/lean/N66G15 >> $RV/own_diff_vs_level14.txt
echo "diff lines: $(wc -l < $RV/own_diff_vs_level14.txt)"
grep -E '^[<>]' $RV/own_diff_vs_level14.txt | grep -vE '^[<>] *(/-|--|\*|#|`|[A-Za-z].*[a-z]\.$)' | grep -vE '^[<>]\s*$' > $RV/own_diff_code_lines.txt
echo "non-comment changed lines: $(wc -l < $RV/own_diff_code_lines.txt)"
