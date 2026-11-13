#!/bin/sh
# Unattended completion of ES(8) <= 311 (balanced budget 63). Never commits or pushes.
# Steps: wait for the search -> assemble + exact replay -> packed-lookup Lean export -> kernel check
# -> compile Final311 (Bridge63, Final) -> statement + axiom audit -> final-status.txt.
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"; cd "$REPO" || exit 1
export ELAN_HOME="$REPO/.elan"; export PATH="$ELAN_HOME/bin:$PATH"
E=.cache/es311; ST="$E/final-status.txt"; SRC=experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json
say() { echo "$(date '+%F %T') $*" | tee -a "$E/pipeline.log"; }
fail() { say "FAILED: $*"; echo "FAILED $(date '+%F %T'): $*" > "$ST"; exit 1; }
if [ ! -f "$E/lean-export/export.json" ]; then
say "waiting for search pid $(cat $E/bb63.pid)"
while kill -0 "$(cat $E/bb63.pid)" 2>/dev/null; do sleep 60; done
grep -q WITNESS "$E/bb63.log" && fail "search found a 63-hole assignment (see $E/bb63/WITNESS.json); needs new geometry"
grep -q '"DONE"' "$E/bb63.log" || fail "search ended without DONE"
say "search done; assembling and replaying"
.cache/solver-venv/bin/python .cache/es313/assemble.py "$E/bb63" "$E/tree-63.json.gz" "$SRC" > "$E/assemble.out" 2>&1 || fail "assemble"
python3 -c "import json,sys; r=json.loads(open('$E/assemble.out').read().strip().splitlines()[-1])['replay']; sys.exit(0 if r['complete'] and r['pending']==0 else 1)" || fail "replay incomplete: $(tail -1 $E/assemble.out)"
say "replay: $(tail -1 $E/assemble.out)"
rm -rf "$E/lean-export"
(cd scripts && python3 omission_fast_export.py "../$SRC" "../$E/tree-63.json.gz" --output "../$E/lean-export" \
  --namespace OmissionBalancedCover63 --module-prefix BalancedCover63Proof --leaf-limit 64) > "$E/export.out" 2>&1 || fail "export"
say "export: $(tail -1 $E/export.out)"
else say "resuming: export exists, continuing the kernel check"; fi
lake env python3 scripts/check_omission_lean.py "$E/lean-export" --resume --workers 10 --memory 6000 > "$E/lean-check.log" 2>&1
tail -1 "$E/lean-check.log" | grep -q '"complete": true' || fail "kernel check incomplete (see $E/lean-check.log)"
say "kernel check complete"
F=experiments/omission-final311-2026-10-14/Final311; OUT="$REPO/$E/final-build"; mkdir -p "$OUT/Final311"
if grep -rnwE "sorry|admit|native_decide|sorryAx" "$F" >/dev/null || LC_ALL=C grep -rlF -e sorry -e admit -e native_decide "$E/lean-export/BalancedCover63Proof" --include='*.lean' | head -1 | grep -q .; then fail "placeholder found"; fi
LP="$OUT:$REPO/$E/lean-export:$REPO/.cache/runtime/final-build:$REPO/.cache/es313/lean-export:$REPO/.cache/omission-residual32-bridge2650-2026-10-11:$(lake env printenv LEAN_PATH)"
for m in Bridge63 Final; do
  LEAN_PATH="$LP" lean -j1 -M 12000 "$F/$m.lean" -o "$OUT/Final311/$m.olean" > "$E/final-$m.out" 2>&1 || fail "compile $m (see $E/final-$m.out)"
done
printf 'import Final311.Final\n#check @ErdosSzekeres.Omission.forces_convex_octagon_311\n#print axioms ErdosSzekeres.Omission.forces_convex_octagon_311\n#print axioms ErdosSzekeres.Omission.convex_octagon_of_card_ge_311\n' > "$OUT/Audit.lean"
LEAN_PATH="$LP" lean -j1 "$OUT/Audit.lean" > "$E/final-audit.out" 2>&1 || fail "audit compile"
grep -q "forces_convex_octagon_311 : ErdosSzekeres.ForcesConvexNGon 311 8" "$E/final-audit.out" || fail "unexpected statement"
python3 - "$E/final-audit.out" <<'PY' || fail "unexpected axioms"
import re, sys
reps = re.findall(r"depends on axioms: \[([^]]*)\]", open(sys.argv[1]).read(), re.S)
assert len(reps) == 2 and all({a.strip() for a in r.split(',') if a.strip()} <= {'propext', 'Classical.choice', 'Quot.sound'} for r in reps)
PY
say "VERIFIED forces_convex_octagon_311 : ForcesConvexNGon 311 8 (standard axioms only)"
echo "VERIFIED $(date '+%F %T'): forces_convex_octagon_311 : ForcesConvexNGon 311 8 (standard axioms only)" > "$ST"
