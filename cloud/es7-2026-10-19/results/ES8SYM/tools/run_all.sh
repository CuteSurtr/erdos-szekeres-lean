#!/bin/sh
# Re-runs every check of ES8SYM. Run from cloud/es7-2026-10-19/results:
#   sh ES8SYM/tools/run_all.sh ES8SYM OUTDIR
# Needs Python 3 (standard library only) and a C compiler. Set PYTHON, CC or CFLAGS if needed (on some macOS installs:
# CFLAGS="-O2 -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX26.sdk"). Takes about one minute.
set -e
D=$1; O=$2; T=$D/tools; X=$D/structure
CC=${CC:-cc}; CFLAGS=${CFLAGS:--O2}; PY="${PYTHON:-python3} -B"
mkdir -p $O
for p in cvx2 cvxcheck enum_convex enum_table; do $CC $CFLAGS -o $O/$p $T/$p.c; done
for p in inv modules; do $CC $CFLAGS -o $O/$p $X/$p.c; done

echo "== 1. sets in Z[zeta_m] (name m centre)"
for spec in c4_52pts_13layers:4:0 c5_51pts_10layers_centre:5:1 c6_54pts_9layers:6:0 c7_63pts_9layers:7:0 \
            c7_64pts_small:7:1 c7_64pts_9layers_centre:7:1 c7_64pts_9layers_centre_own:7:1 rule_p7_64pts:7:1 \
            p7_compound_64:7:1; do
  n=${spec%%:*}; r=${spec#*:}; m=${r%%:*}; c=${r#*:}
  echo "-- $n  m=$m centre=$c"
  shasum -a 256 $D/sets/$n.pts
  $PY $T/layer_order.py $D/sets/$n.pts $m $O/$n.L.pts
  $PY $T/verify_cfg.py --pts $O/$n.L.pts $m $c 8 $O/$n
  $O/cvx2 $O/$n 8
  $PY $T/otab2txt.py $O/$n $O/$n.orient
  $O/cvxcheck $O/$n.orient 8
  $PY $T/crosscheck_decimal.py $O/$n $m
done

echo "== 2. sets with integer (or Eisenstein) coordinates (name symmetry)"
# mirror46_A_S has its axis on y = 0; the checked copy has x and y swapped (a reflection), so the axis becomes x = 0.
for spec in c2_64points_k8:C2 c2_64points_k8_bb:C2 c3_55points_k8:C3 mirror_46points_k8:M mirror46_A_S:MX deep42:C2; do
  n=${spec%%:*}; s=${spec#*:}; e=$s; [ "$s" = C3 ] && e=none
  echo "-- $n  $s"
  shasum -a 256 $D/sets/$n.txt
  if [ "$s" = MX ]; then
    awk '/^#/ {print; next} NF == 2 {print $2, $1}' $D/sets/$n.txt > $O/$n.txt; s=M; e=M
  else
    cp $D/sets/$n.txt $O/$n.txt
  fi
  $PY $T/verify_set.py $O/$n.txt 8 $s
  $O/enum_convex $O/$n.txt $O/$n.txt.orient $e
done
echo "-- control_wide_middle_k8 (same construction with a wide middle cluster; must contain octagons)"
cp $D/sets/control_wide_middle_k8.txt $O/control.txt
$O/enum_convex $O/control.txt - C2 || true

echo "== 3. refuted lemmas"
echo "-- rotation-chain lemma as first written: 6-fold and 4-fold chains (rows a c1 c2 c3 Qa, 1-based)"
$PY $T/rotation_chain_cex.py $D/sets/c6_54pts_9layers.pts 6 1 7 8 12 4
$PY $T/rotation_chain_cex.py $D/sets/c4_52pts_13layers.pts 4 1 2 9 7 3
echo "-- needle of c7_64pts_small (rows 7 15 23 31 36 44 49 60, 0-based)"
$PY $T/subset_convex.py $O/c7_64pts_small.orient 7 15 23 31 36 44 49 60
echo "-- central chains and the projective image of c2_64points_k8"
$PY $T/projective_check.py $O/c2_64points_k8.txt $O/k8proj
$O/enum_table $O/k8proj_T.bin $O/k8proj_T_sides.txt 8
echo "-- deep halves"
$PY $T/deep_halves_check.py $O/c2_64points_k8.txt
$PY $T/deep_halves_check.py $O/deep42.txt

echo "== 4. mirror: regenerate both CNFs for 23 points"
$PY $D/mirror/enc_rmax.py 23 $O/r23.cnf
$PY $D/mirror/encode.py 23 8 $O/es_n23_K8.cnf full
shasum -a 256 $O/r23.cnf $O/es_n23_K8.cnf

echo "== 5. order-type invariants and line-modules of the 64-point sets"
for n in c7_64pts_small c7_64pts_9layers_centre c7_64pts_9layers_centre_own rule_p7_64pts p7_compound_64; do
  $PY $X/orient.py zeta 7 $D/sets/$n.pts $O/$n.ot
done
$PY $X/orient.py int $D/sets/c2_64points_k8.txt $O/c2_64points_k8.ot
$PY $X/orient.py int $X/es_64points.txt $O/es_64.ot
for n in c7_64pts_small c7_64pts_9layers_centre c7_64pts_9layers_centre_own rule_p7_64pts p7_compound_64 \
         c2_64points_k8 es_64; do
  echo "-- $n"
  $O/inv $O/$n.ot
  $O/modules $O/$n.ot | grep -v '^module '
done
echo "-- hull vertices of the first two 7-fold sets are not deep (exact certificates)"
$PY $X/deep_check.py $D/sets/c7_64pts_small.pts 7
$PY $X/deep_check.py $D/sets/c7_64pts_9layers_centre.pts 7
echo "== done"
