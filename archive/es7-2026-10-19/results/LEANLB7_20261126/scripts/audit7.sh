#!/usr/bin/env bash
# audit7.sh: read-only checks of LEANLB7_20261126 (adapted from LEANLB20261111/scripts/audit.sh). Exit 0 iff all pass.
#  1. VENDOR.sha256 verifies, and each vendored module equals the repository file of the same path.
#  2. The shared modules are byte-identical to LEANLB20261111 (checker, soundness, k = 8 statement file and its
#     data, bridge, geometry, G/*, toolchain, manifest; the lakefile differs only in its comment line).
#  3. scripts/gen_data7.py --check: the six LeanLB/Data files regenerate byte for byte from the repository's set
#     files; each set file is tracked by git and unmodified against HEAD (no hash list exists for them).
#  4. No forbidden token in the Lean sources (comments stripped); the only set_option is maxRecDepth.
#  5. logs/build_final.log (clean `lake build`): the #guard_msgs axiom audit of LeanLB/Audit7.lean printed the
#     standard axioms for the six theorems and the two ES(7) >= 33 corollaries, and the log has no error; logs/reject7.log has exactly 4 errors.
set -u
cd "$(dirname "$0")/.."
K8=../LEANLB20261111
REPO=$(cd ../../../.. && pwd)
fail=0
echo "== 1. vendored modules"
sha256sum -c --quiet VENDOR.sha256 && echo "VENDOR.sha256 OK" || fail=1
for f in $(awk '!/^#/{print $2}' VENDOR.sha256); do
  cmp -s "$f" "$REPO/$f" || { echo "DIFFERS from repository: $f"; fail=1; }
done
echo "vendored files equal the repository files: $(awk '!/^#/' VENDOR.sha256 | wc -l) checked"
echo "== 2. shared modules equal LEANLB20261111"
n=0
for f in LeanLB/Checker.lean LeanLB/CheckerSound.lean LeanLB/Statement.lean LeanLB/Bridge.lean LeanLB/Geometry.lean \
         LeanLB/G/*.lean $(cd $K8 && ls LeanLB/Data/*.lean) lean-toolchain lake-manifest.json scripts/gen_data.py VENDOR.sha256; do
  cmp -s "$f" "$K8/$f" && n=$((n + 1)) || { echo "DIFFERS from LEANLB20261111: $f"; fail=1; }
done
d=$(diff lakefile.toml $K8/lakefile.toml | grep -c '^[<>]')
[ "$d" = 2 ] && echo "lakefile.toml: only the comment line differs" || { echo "lakefile.toml differs in $d lines"; fail=1; }
echo "$n shared files identical"
echo "== 3. data files"
python3 -B scripts/gen_data7.py --check || fail=1
for s in SYMMAX/c3_31points.txt SYMMAX/c6_30points.txt SYMMAX/c4_28points.txt SYM2/sym7_32points.txt \
         SYMMAX/mirror_32points.txt SYMMAX/c5_31points.txt; do
  p=archive/es7-2026-10-19/results/$s
  if git -C "$REPO" ls-files --error-unmatch "$p" >/dev/null 2>&1 && git -C "$REPO" diff --quiet HEAD -- "$p"; then
    echo "OK   $s tracked, unmodified (last change $(git -C "$REPO" log -1 --format='%h %cs' -- "$p"))"
  else echo "FAIL $s untracked or modified"; fail=1; fi
done
echo "== 4. forbidden tokens"
python3 -I - <<'PY' || fail=1
import re, glob, sys
bad = re.compile(r"\b(sorry|admit|native_decide|axiom|opaque|implemented_by|extern|unsafe|ofReduceBool|ofReduceNat|skipKernelTC|maxHeartbeats)\b")
def strip(src):
    out, i, depth = [], 0, 0
    while i < len(src):
        if src.startswith("/-", i): depth += 1; i += 2; continue
        if depth and src.startswith("-/", i): depth -= 1; i += 2; continue
        if depth: i += 1; continue
        if src.startswith("--", i):
            j = src.find("\n", i); i = len(src) if j < 0 else j; continue
        out.append(src[i]); i += 1
    return "".join(out)
n, ok = 0, True
for f in sorted(glob.glob("LeanLB/**/*.lean", recursive=True) + ["LeanLB.lean"] + glob.glob("ErdosSzekeres/**/*.lean", recursive=True)):
    code = strip(open(f).read()); n += 1
    for m in bad.finditer(code):
        line = code[:m.start()].count("\n") + 1
        if m.group(1) == "axiom" and code[max(0, m.start()-7):m.start()] == "#print ":
            continue
        print(f"{f}:{line}: {m.group(1)}"); ok = False
    for m in re.finditer(r"set_option\s+([\w.]+)", code):
        if m.group(1) != "maxRecDepth":
            print(f"{f}: set_option {m.group(1)}"); ok = False
print(f"scanned {n} files: {'OK' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
PY
echo "== 5. axiom audit and controls"
for t in threefold31 sixfold30 fourfold28 halfturn32 mirror32 fivefold31 not_forcesConvexNGon_32_7 heptagon_lower_bound; do
  grep -q "'LeanLB.$t' depends on axioms: \[propext, Classical.choice, Quot.sound\]" logs/build_final.log \
    && echo "OK   LeanLB.$t" || { echo "FAIL LeanLB.$t"; fail=1; }
done
grep -q "Build completed successfully" logs/build_final.log || { echo "FAIL: build did not complete"; fail=1; }
grep -qi "error" logs/build_final.log && { echo "FAIL: error in build log"; fail=1; }
r=$(grep -cE '^tests/Reject7.lean:[0-9]+:[0-9]+: error' logs/reject7.log)
[ "$r" = 4 ] && echo "OK   tests/Reject7.lean: 4 of 4 controls rejected" || { echo "FAIL reject7: $r errors"; fail=1; }
[ $fail = 0 ] && echo "AUDIT PASS" || echo "AUDIT FAIL"
exit $fail
