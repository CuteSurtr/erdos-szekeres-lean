#!/bin/bash
# Mutation controls: copy the sources, apply one mutation, rebuild Std + Mathlib-side modules into mut/<name>/olean
# (LEAN_PATH without the main build/olean); a mutant is KILLED if some module fails to compile.
D=/home/jay/research/data/formalize-20261122/ae33-lean
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
R=/home/jay/research/lean/erdos-szekeres-lean
P=$R/.lake/packages
ENCB=$R/archive/es7-2026-10-19/results/ENCBLEAN
run_mutant() {  # name file python-replace-old python-replace-new
  local name=$1 file=$2 old=$3 new=$4
  local M=$D/mut/$name
  rm -rf $M; mkdir -p $M/olean/AE33Enc $M/olean/AE33Geo
  cp -r $D/lean $M/lean
  python3 -I - "$M/lean/$file" "$old" "$new" <<'PY' || { echo "$name: MUTATION NOT APPLIED"; return; }
import sys
p, old, new = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(p).read()
assert s.count(old) == 1, 'pattern count %d' % s.count(old)
open(p, 'w').write(s.replace(old, new))
PY
  local LP_STD="$TC/lib/lean:$ENCB/.lake/build/lib/lean:$M/olean"
  local LP_GEO="$P/Cli/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean:$P/mathlib/.lake/build/lib/lean:$R/.lake/build/lib/lean:$TC/lib/lean:$ENCB/.lake/build/lib/lean:$M/olean"
  cd $M/lean
  local failed=""
  for m in Basic Clause Gen Data Bridge; do
    LEAN_PATH=$LP_STD $TC/bin/lean -j1 -R . -o $M/olean/AE33Enc/$m.olean AE33Enc/$m.lean > $M/$m.log 2>&1 || { failed="AE33Enc.$m"; break; }
  done
  if [ -z "$failed" ]; then
    for m in Slot Sem Sound Pair; do
      LEAN_PATH=$LP_GEO $TC/bin/lean -j1 -R . -o $M/olean/AE33Geo/$m.olean AE33Geo/$m.lean > $M/$m.log 2>&1 || { failed="AE33Geo.$m"; break; }
    done
  fi
  if [ -n "$failed" ]; then
    echo "$name: KILLED at $failed ($(grep -m1 -o 'error: .*' $M/${failed#*.}.log | cut -c1-110))"
  else
    echo "$name: SURVIVED (all modules compiled)"
  fi
  rm -rf $M/olean
}
run_mutant oct_sign AE33Enc/Clause.lean "let cl := [l1, -l2, -l3]" "let cl := [l1, l2, -l3]"
run_mutant r2_sign AE33Enc/Clause.lean "else [-(ex * lx), ey * ly, -(ez * lz)]" "else [-(ex * lx), ey * ly, ez * lz]"
run_mutant jk_slot AE33Enc/Clause.lean "let Q1 := Q.take (i + 1) ++ [n] ++ Q.drop (i + 1)" "let Q1 := Q.take i ++ [n] ++ Q.drop i"
run_mutant gp_pred AE33Enc/Clause.lean "s0 * s1 == -s2 * s3 && -s2 * s3 == s4 * s5" "s0 * s1 == s2 * s3 && s2 * s3 == s4 * s5"
run_mutant rad_pred AE33Enc/Clause.lean "s0 == -s1 && -s1 == s2 && s2 == -s3" "s0 == -s1 && -s1 == s2 && s2 == s3"
run_mutant chi_w AE33Enc/Basic.lean "else .lit (s.2.2.2 * ((2 * n2 n + 1 + s.1 : Nat) : Int))" "else .lit (-s.2.2.2 * ((2 * n2 n + 1 + s.1 : Nat) : Int))"
run_mutant ac_sign AE33Enc/Clause.lean "let cl := [s * l1, s * l2, s * l3]" "let cl := [s * l1, s * l2, -(s * l3)]"
run_mutant control_doc AE33Enc/Clause.lean "def isUnit (e : Int) : Bool := e == 1 || e == -1" "/-- doc-only change -/
def isUnit (e : Int) : Bool := e == 1 || e == -1"
