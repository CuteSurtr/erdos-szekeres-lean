#!/usr/bin/env bash
# audit.sh: read-only checks of LEANLB20261111. Exit 0 iff all pass.
#  1. VENDOR.sha256: the vendored repository modules verify, and each equals the repository file of the
#     same path (when the repository is present).
#  2. scripts/gen_data.py --check: every LeanLB/Data/*.lean regenerates byte for byte from the
#     repository's set file; the source hashes equal the repository's SHA256SUMS entries.
#  3. No forbidden token in the Lean sources (comments stripped): sorry, admit, native_decide, axiom,
#     opaque, implemented_by, extern, unsafe, ofReduceBool, ofReduceNat, debug.skipKernelTC,
#     maxHeartbeats; the only set_option is maxRecDepth.
#  4. The axiom audit of LeanLB/Audit.lean (#guard_msgs; built by `lake build`) is present in
#     logs/build_final.log with the expected output for the seven theorems.
set -u
cd "$(dirname "$0")/.."
REPO=$(cd ../../../.. && pwd)
fail=0
echo "== 1. vendored modules"
sha256sum -c --quiet VENDOR.sha256 && echo "VENDOR.sha256 OK" || fail=1
if [ -d "$REPO/ErdosSzekeres" ]; then
  for f in $(awk '!/^#/{print $2}' VENDOR.sha256); do
    cmp -s "$f" "$REPO/$f" || { echo "DIFFERS from repository: $f"; fail=1; }
  done
  echo "vendored files equal the repository files: $(awk '!/^#/' VENDOR.sha256 | wc -l) checked"
fi
echo "== 2. data files"
python3 -I scripts/gen_data.py --check || fail=1
for pair in "ES8SYM/sets/SHA256SUMS.txt c4_52pts_13layers.pts" "ES8SYM/sets/SHA256SUMS.txt c2_64points_k8.txt" \
            "ES8SYM/sets/SHA256SUMS.txt mirror_46points_k8.txt" "ES8SYM/sets/SHA256SUMS.txt c7_64pts_small.pts" \
            "SIX60/sets/SHA256SUMS.txt c6_60pts_D.pts" "ES8SYM/sets3/SHA256SUMS c5_56pts_11layers_centre.pts" \
            "ES8SYM/sets4/SHA256SUMS c3_61pts_centre.txt"; do
  set -- $pair
  rec=$(grep "[ /]$2\$" "../$1" | awk '{print $1}')
  src=$(grep -rl "$2" LeanLB/Data/*.lean | head -1)
  got=$(grep -o 'SHA-256 `[0-9a-f]*`' "$src" | head -1 | tr -d '`' | awk '{print $2}')
  if [ -n "$rec" ] && [ "$rec" = "$got" ]; then echo "OK   $2 matches $1"; else echo "FAIL $2 recorded=$rec data=$got"; fail=1; fi
done
echo "== 3. forbidden tokens"
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
        # `#print axioms` is the audit command itself
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
echo "== 4. axiom audit (from the last full build)"
if [ -f logs/build_final.log ]; then
  for t in sixfold60 fourfold52 halfturn64 mirror46 threefold61 sevenfold64 fivefold56; do
    grep -q "'LeanLB.$t' depends on axioms: \[propext, Classical.choice, Quot.sound\]" logs/build_final.log \
      && echo "OK   LeanLB.$t" || { echo "FAIL LeanLB.$t"; fail=1; }
  done
  grep -q "error" logs/build_final.log && { echo "FAIL: error in build log"; fail=1; }
else
  echo "logs/build_final.log missing"; fail=1
fi
[ $fail = 0 ] && echo "AUDIT PASS" || echo "AUDIT FAIL"
exit $fail
