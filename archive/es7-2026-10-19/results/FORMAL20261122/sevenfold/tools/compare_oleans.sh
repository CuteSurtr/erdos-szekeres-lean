#!/bin/bash
# compare_oleans.sh: the 32 reused modules built here (olean/) against ENCBLEAN's prebuilt oleans, byte for byte.
W=/home/jay/research/data/formalize-20261122/sevenfold
R=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN
{
echo "# compare_oleans.sh $(date -Is) (olean store built $(stat -c %y $W/olean/Geo7/Main7.olean))"
same=0; diff=0
for m in Gen Dimacs Coded Cover Model ModelLemmas SortLemmas SoundOlit SoundOrbit SoundChain SoundAng SoundRules SoundWord Satisfiable Render Compose; do
  a=$(sha256sum $W/olean/EncB/$m.olean | cut -d' ' -f1); b=$(sha256sum $R/.lake/build/lib/lean/EncB/$m.olean | cut -d' ' -f1)
  if [ "$a" = "$b" ]; then same=$((same+1)); else diff=$((diff+1)); echo "DIFF EncB/$m"; fi; done
for f in ErdosSzekeres/Basic ErdosSzekeres/Definitions ErdosSzekeres/Orientation ErdosSzekeres/OrientationGeometry ErdosSzekeres/Suk/BaseChart ErdosSzekeres/Suk/BaseOrder ErdosSzekeres/Suk/FourPoint ErdosSzekeres/Suk/OrientationClique ErdosSzekeres/Suk/SupportingLines ErdosSzekeres/Suk/TriangleOrder ES8Geo/Capstone2 ES8Geo/KeyOrder ES8Geo/Orbit ES8Geo/OrbitConsistency ES8Geo/Interface ES8Geo/Labelling; do
  a=$(sha256sum $W/olean/$f.olean | cut -d' ' -f1); b=$(sha256sum $R/geo/.lake/build/lib/lean/$f.olean | cut -d' ' -f1)
  if [ "$a" = "$b" ]; then same=$((same+1)); else diff=$((diff+1)); echo "DIFF $f"; fi; done
echo "reused oleans: same=$same diff=$diff (of 32)"
} | tee $W/logs/olean_compare.log
