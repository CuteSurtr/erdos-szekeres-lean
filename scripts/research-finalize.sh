#!/bin/sh
# Completion procedure for ES(8) <= 313. Run automatically by research-monitor.sh once every
# certificate module is verified, or by hand. Never pushes or commits.
#   research-finalize.sh --preflight   check toolchain, inputs and imports only (no Root needed)
# Writes .cache/runtime/final-report.json, final-report.txt and final-status.txt.
. "$(dirname "$0")/research-common.sh"
cd "$REPO" || exit 1
OUT="$RT/final-build"; BRIDGE=".cache/omission-residual32-bridge2650-2026-10-11"
FINAL="experiments/omission-final313-2026-10-11/Final313"
fail() { echo "FAILED: $*" | tee "$RT/final-status.txt"; exit 1; }
LP="$OUT:$REPO/$EXPORT:$REPO/$BRIDGE:$(lake env printenv LEAN_PATH)"
echo "== toolchain"; lean --version
# 1. Certificate inputs must match the checkpoint manifest.
python3 - "$RT" <<'PY' || fail "input checksum mismatch"
import json, hashlib, sys
rt = sys.argv[1]; m = json.load(open(rt + '/checkpoint-manifest.json'))
paths = {'source-2650.json': '.cache/es313/source-2650.json', 'tree-2650-32.json.gz': '.cache/es313/tree-2650-32.json.gz',
         'export.json': '.cache/es313/lean-export/export.json'}
for k, p in paths.items():
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    assert h == m['inputs'][k], (k, h)
print('inputs match checkpoint manifest')
PY
# 2. No placeholders or bypasses in the Lean sources of the final chain.
if grep -rnwE "sorry|admit|native_decide|sorryAx" "$FINAL" experiments/omission-residual32-bridge2650-2026-10-11/Residual32Bridge2650 >/dev/null; then fail "placeholder or native_decide found"; fi
if LC_ALL=C grep -rlF -e sorry -e admit -e native_decide "$EXPORT/Residual2650ZeroProof" --include='*.lean' | head -1 | grep -q . \
   || LC_ALL=C grep -rlE '^(axiom|unsafe|noncomputable axiom|private axiom) ' "$EXPORT/Residual2650ZeroProof" --include='*.lean' | head -1 | grep -q .; then
  fail "placeholder in exported certificate"; fi
echo "no placeholders, axioms, unsafe or native_decide in the final chain sources"
mkdir -p "$OUT/Final313"
if [ "$1" = "--preflight" ]; then
  printf 'import Residual32Bridge2650.Final\nimport Residual2650ZeroProof.Catalog\n#check @OmissionResidual32Bridge2650.forces_convex_octagon_313_of_node\n' > "$OUT/Preflight.lean"
  LEAN_PATH="$LP" lean -j1 "$OUT/Preflight.lean" || fail "preflight imports"
  echo "preflight ok"; exit 0
fi
# 3. Every module verified, every recorded .olean unchanged, completion flag set.
python3 "$RT/state.py" --verify-oleans --json "$RT/final-state.json" > /dev/null
python3 - "$RT" <<'PY' || fail "certificate check incomplete or inconsistent"
import json, sys
s = json.load(open(sys.argv[1] + '/final-state.json'))
assert s['verified'] == s['expected_modules'] and not s['failed'] and s['olean_mismatch'] == [] and s['complete_flag'] is True, s
print('all', s['verified'], 'modules verified; oleans rehashed; complete flag set')
PY
# 4. Compile the catalog match and the final assembly afresh.
for m in Match Final; do
  LEAN_PATH="$LP" lean -j1 -M 12000 "$FINAL/$m.lean" -o "$OUT/Final313/$m.olean" > "$RT/final-$m.out" 2>&1 || fail "compile $m (see final-$m.out)"
done
# 5. Statement and axiom audit.
printf 'import Final313.Final\n#check @ErdosSzekeres.Omission.forces_convex_octagon_313\n#print axioms ErdosSzekeres.Omission.forces_convex_octagon_313\n#print axioms ErdosSzekeres.Omission.convex_octagon_of_card_ge_313\n' > "$OUT/Audit.lean"
LEAN_PATH="$LP" lean -j1 "$OUT/Audit.lean" > "$RT/final-audit.out" 2>&1 || fail "audit compile"
grep -q "forces_convex_octagon_313 : ErdosSzekeres.ForcesConvexNGon 313 8" "$RT/final-audit.out" || fail "unexpected theorem statement"
python3 - "$RT" <<'PY' || fail "unexpected axioms"
import re, sys
out = open(sys.argv[1] + '/final-audit.out').read()
reps = re.findall(r"depends on axioms: \[([^]]*)\]", out, re.S)
assert len(reps) == 2, out
for r in reps:
    ax = {a.strip() for a in r.split(',') if a.strip()}
    assert ax <= {'propext', 'Classical.choice', 'Quot.sound'}, ax
print('axioms: only propext, Classical.choice, Quot.sound')
PY
# 6. Report.
python3 - "$RT" <<'PY'
import json, hashlib, subprocess, sys, time
rt = sys.argv[1]; m = json.load(open(rt + '/checkpoint-manifest.json'))
files = ['experiments/omission-final313-2026-10-11/Final313/Match.lean', 'experiments/omission-final313-2026-10-11/Final313/Final.lean']
rep = {'result': 'ES(8) <= 313: ErdosSzekeres.Omission.forces_convex_octagon_313 : ForcesConvexNGon 313 8',
       'time': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'lean': subprocess.run(['lean', '--version'], capture_output=True, text=True).stdout.strip(),
       'mathlib_rev': m['mathlib_rev'], 'git_head': subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip(),
       'certificate_inputs': m['inputs'], 'final_sources': {f: hashlib.sha256(open(f, 'rb').read()).hexdigest() for f in files},
       'audit': open(rt + '/final-audit.out').read(), 'scope': 'Kernel-checked end to end on this machine; not yet committed or pushed.'}
json.dump(rep, open(rt + '/final-report.json', 'w'), indent=1)
open(rt + '/final-report.txt', 'w').write(rep['result'] + '\n' + rep['audit'])
PY
echo "VERIFIED $(date '+%F %T'): forces_convex_octagon_313 : ForcesConvexNGon 313 8 (standard axioms only)" | tee "$RT/final-status.txt"
