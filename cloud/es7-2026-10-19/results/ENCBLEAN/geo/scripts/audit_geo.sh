#!/usr/bin/env bash
# audit_geo.sh: read-only checks of the ENCBLEAN geometric package (geo/, milestones M4-M8). Exit 0 iff all pass.
#   1. pinned files. (a) SOURCES.sha256 (Capstone2, KeyOrder, OrbitConsistency, Interface, Orbit) verifies with
#      exactly 5 OK lines and VENDOR.sha256 (the ten vendored ErdosSzekeres modules) with exactly 10; SOURCES.sha256
#      lists exactly the ES8Geo/*.lean files that are not M5-M8 unit files. (b) The PINNED list below (sha256 of
#      the build configuration geo/{lakefile.toml,lake-manifest.json,lean-toolchain}, ../{lakefile.toml,
#      lean-toolchain,lake-manifest.json}, of SOURCES.sha256 and VENDOR.sha256 themselves, and of the Std-only
#      package ../EncB.lean and ../EncB/*.lean, i.e. the definitions Model, encB, encode, cubes64, cubeCnf,
#      CubesUnsat64, cnfText, parseDimacs, DimacsSatisfiable that give the final theorems their meaning) verifies,
#      and ../EncB/ has no file outside it. (c) Neither lakefile sets Lean options (leanOptions, moreLeanArgs,
#      weakLeanArgs, server args, plugins, ...). (d) geo/lake-manifest.json pins Mathlib f897ebcf, every package of
#      the repository's lake-manifest.json at the same revision (when the repository is present), and each checkout
#      in geo/.lake/packages is at its manifest revision with no tracked change (skipped with AUDIT_SKIP_BUILD=1).
#   2. git cross-checks (skipped, with a note, outside a git checkout or with AUDIT_NO_GIT=1): every vendored
#      ErdosSzekeres/<p> and every PINNED file under ../ equals the repository file at the commit recorded in
#      VENDOR.sha256 (6a4e5c3c, the M9 commit; not the moving HEAD); once geo/ is committed, SOURCES.sha256 and
#      VENDOR.sha256 equal their committed versions at HEAD. No unlisted file under ErdosSzekeres/.
#   3. ES8Geo/{Capstone2,KeyOrder,OrbitConsistency}.lean equal results/LEANEXT/{capstone,keys,orbit}/<name> byte
#      for byte;
#   4. no forbidden token in the code of ES8Geo/*.lean, ES8Geo.lean and ErdosSzekeres/**/*.lean (comments and
#      docstrings stripped by a scanner that nests block comments and keeps string and char literals): sorry,
#      sorryAx, admit, native_decide, axiom declarations, opaque, implemented_by, extern, unsafe, maxHeartbeats 0,
#      debug.skipKernelTC, ofReduceBool, ofReduceNat, reduceBool, reduceNat;
#   5. no kernel evaluation of the (6,8,11) instance in the M5-M8 files. A "mention" is any of: encB/gen/genCoded/
#      numVars/allCodes/allCodesOf/encode/diagCoded/Model applied to 6 8 11, a named-argument instance
#      ((m := 6), (K := 8), (t := 11)), CubesUnsat64, cubesUnsat64*, cubes64, cubeVars64, cubeCnf, cnfText,
#      parseDimacs*, encB_unsat*, or any identifier containing 6811. (a) No risky token (decide, rfl, norm_num,
#      the simp family, omega, grind, trivial, aesop, Eq.refl, ..., #eval, #reduce) within 3 lines of a mention;
#      (b) a declaration (a column-0 command and its continuation lines) that mentions the instance is a term: it
#      contains no `by` (no tactic block at all) and no risky token; (c) the M5-M8 files define no macro, syntax,
#      elaborator or notation (which could hide a tactic behind a new name).
#      Check 5 is a text check and can be evaded by indirection (a local abbreviation for 6, say). The real
#      protection is the time limit of check 7: an evaluation of `encB 6 8 11` takes far longer than the limit.
#   6. ES8Geo.lean imports every ES8Geo/*.lean module;
#   7. build gate: `lake build --no-build` reports the build up to date (so every #guard_msgs on #print axioms and
#      #check in ES8Geo/Audit.lean passed when it was built), and the six M5-M8 files ES8Geo/{Labelling,ModelBasic,
#      ArcBridge,ModelOfLabelling,Main,Audit}.lean elaborate again, each within ${AUDIT_LEAN_TIMEOUT:-300} s, with no
#      error (`lake env lean` uses no package Lean options; check 1(c) makes that the same as `lake build`). The
#      axioms of the main theorems are printed and must be the three standard ones.
#      AUDIT_SKIP_BUILD=1 skips check 7 (and 1(d)); the run then ends AUDIT INCOMPLETE (exit 3), never AUDIT PASS.
# Nothing is written: no lake build, no lake update; `lake env lean` writes no .olean.
#
# audit_geo.sh --selftest: copies geo/ (without .lake), ../EncB*, the ../ build files and the three LEANEXT sources
# to a temporary directory, plants one violation per run (see selftest() below), runs the static checks there
# (AUDIT_SKIP_BUILD=1 AUDIT_NO_GIT=1) and expects exit 1 for each planted violation and exit 3 for the clean copy.
# Exit 0 iff every case behaves as expected. Nothing outside the temporary directory is written.
set -u -o pipefail
cd "$(dirname "$0")/.." || exit 2
GEO=$(pwd)
RESULTS=$(cd ../.. && pwd)           # cloud/es7-2026-10-19/results
export PATH="$HOME/.elan/bin:$PATH"

NEW_NAMES="Labelling ModelBasic ArcBridge ModelOfLabelling Main Audit"
NEW=""; for n in $NEW_NAMES; do NEW="$NEW ES8Geo/$n.lean"; done

# ---------------------------------------------------------------------------------------------------------------
# PINNED: recorded 2026-11-07 (M4-M8 fixer pass). The ../ entries equal the M9 commit 6a4e5c3c1249 (checked by
# check 2 when git is available); the geo/ entries are the M4 build configuration and the two frozen manifests.
PINNED=$(cat <<'EOF'
e96bed27ce6745176081d29f8bfa9b2c17d82ea812d54d745ffbcce2b318f576  lakefile.toml
9ed052f266fc14a4ef704c1e1aa7cbc92998b340ac007b47e782f846fcc56fd7  lake-manifest.json
42779d67b81608af8a12aa4328d2ab47ca201925b3b2bd68369587b5340bb434  lean-toolchain
52cf436dd8be4633a82d05de1450dd3671c0256f6bdeac45b98098639416a5e2  SOURCES.sha256
8060ed40c53094599a5c93e105b1374cafb32d9fc8f3fd500f3203e634225ca2  VENDOR.sha256
780b7d570523cc37606848d451a0aba686925a3ea0e9f647cbc161f6cf0b1842  ../lakefile.toml
42779d67b81608af8a12aa4328d2ab47ca201925b3b2bd68369587b5340bb434  ../lean-toolchain
b5add1d30739f96940dce83505ee98a93765a127a3f68854f312ac50fb0d1a41  ../lake-manifest.json
3ed1714e4cf6b8da2dfdab7c78aee8e710f67e4c404c8e6aa45e977e487d43d0  ../EncB.lean
2727e00bbd4ce9eab7f4af634c8ad3c056c1122cac1d9bd11f080e6265a69c5f  ../EncB/Coded.lean
fe9cf37e1c1577127bc33378fc737ab01eb83ce26b0ed7b1667ead3a02511b40  ../EncB/Compose.lean
c59425acb5ba5e1da652fbb8d2f77d0c78d8cfc522216f64015231f7ed765f98  ../EncB/Cover.lean
48cbeac96e085d2e3e90d3e7a44f40909b24e4fb985f545de2824c356f64f6a8  ../EncB/Dimacs.lean
38d3c2530629e1b33cd885fe36914c286ed95f545307cbce0fb1ea318a892b0b  ../EncB/EarlyWarning.lean
9a2087a4d116adec6793931986969fe01a01e4f520120389a5b2bbcb856f081f  ../EncB/Emit.lean
ec97b3355b9cfe39f85e9b011ae91c429b5e3764683b9d601cd25a2360a02adf  ../EncB/Gen.lean
a32673b8f5624f97326cd249109e8502f26a89f00d1ee03818b7b73ed354be2c  ../EncB/KernelCheckB.lean
6a141b39db41d7f35d408aeb2f9ba808c67138adcca651ca869c156b34e7cd22  ../EncB/KernelCheck.lean
42240829ba35fc9598285a15c8dcc92b1c749db4ae0f256ee537767375edca31  ../EncB/Model.lean
db0d368be4481a349deb4424b0426650e711d77086f95ac05b74dcdccb9e6844  ../EncB/ModelLemmas.lean
c8d6aed7e539db2c886230c80f891177de05a487e5041ad6f68f360b6d123e82  ../EncB/Render.lean
5c908151d342184a495a063de0f8c10acf55e6b7e3a94ab727dbbf870954b9b4  ../EncB/Satisfiable.lean
103f5bd10b8bde0788fc608ecf1018cd7452ccb303f2b60cd2ae990c4228ca4d  ../EncB/SortLemmas.lean
6fa1ad05bf38519fd62150ea1224098e63dcfbf9d8ad63d20589850dda5a55f7  ../EncB/SoundAng.lean
d2d5908189a9bf53af51074fef5e86eeb2dfe6aeda8f267dbc88f918b4f4ec2e  ../EncB/SoundChain.lean
48631ae6e2c94f88960c198563d0e924467ed32491da26a9ff02c95c7fc7606f  ../EncB/SoundOlit.lean
ce93c2011e6de4906788f2aee2a1e8aac2b73e0137117fc61ee96031a41c0ff2  ../EncB/SoundOrbit.lean
8cb4637efd3736a4ea589eb438c7095d5bc477ac2e20890b00ed4dcd6499268d  ../EncB/SoundRules.lean
c1bdb4175ee548b805154a62496bb8f7c5180cacfb9195c2b75b733e73a68807  ../EncB/SoundWord.lean
EOF
)
MATHLIB_REV=f897ebcf72cd16f89ab4577d0c826cd14afaafc7

# ---------------------------------------------------------------------------------------------------------------
selftest() {
  local tmp; tmp=$(mktemp -d "${TMPDIR:-/tmp}/audit_geo_selftest.XXXXXX") || exit 2
  trap 'rm -rf "$tmp"' EXIT
  local C="$tmp/c/results/ENCBLEAN/geo" nfail=0 ncase=0
  mk() {
    rm -rf "$tmp/c"
    mkdir -p "$C" "$tmp/c/results/LEANEXT/capstone" "$tmp/c/results/LEANEXT/keys" "$tmp/c/results/LEANEXT/orbit"
    (cd "$GEO" && tar cf - --exclude=./.lake .) | (cd "$C" && tar xf -)
    cp -r "$GEO/../EncB" "$GEO/../EncB.lean" "$GEO/../lakefile.toml" "$GEO/../lean-toolchain" \
      "$GEO/../lake-manifest.json" "$tmp/c/results/ENCBLEAN/"
    cp "$RESULTS/LEANEXT/capstone/Capstone2.lean" "$tmp/c/results/LEANEXT/capstone/"
    cp "$RESULTS/LEANEXT/keys/KeyOrder.lean" "$tmp/c/results/LEANEXT/keys/"
    cp "$RESULTS/LEANEXT/orbit/OrbitConsistency.lean" "$tmp/c/results/LEANEXT/orbit/"
  }
  case_() {  # name, expected exit code, shell mutation run inside the copy's geo/
    ncase=$((ncase + 1)); mk
    (cd "$C" && eval "$3") || { echo "  FAIL [$1] mutation did not apply"; nfail=$((nfail + 1)); return; }
    AUDIT_SKIP_BUILD=1 AUDIT_NO_GIT=1 bash "$C/scripts/audit_geo.sh" > "$tmp/out" 2>&1; local rc=$?
    local why; why=$(grep -m1 'FAIL' "$tmp/out" | sed 's/^ *//' | cut -c1-110)
    if [ "$rc" -eq "$2" ]; then echo "  ok   [$1] exit $rc ${why:+($why)}"
    else echo "  FAIL [$1] exit $rc, expected $2"; sed 's/^/       /' "$tmp/out" | tail -15; nfail=$((nfail + 1)); fi
  }
  echo "== audit_geo.sh --selftest $(date -Is) (scratch copy in $tmp)"
  case_ "clean copy (static checks only)" 3 'true'
  case_ "tactic in a declaration mentioning Model 6 8 11" 1 \
    'printf "\ntheorem st_a (h : EncB.Model 6 8 11) : True := by trivial\n" >> ES8Geo/Main.lean'
  case_ "tactic block without a listed tactic, instance named via CubesUnsat64" 1 \
    'printf "\ntheorem st_j (h : EncB.CubesUnsat64) : EncB.CubesUnsat64 := by\n  exact h\n" >> ES8Geo/Main.lean'
  case_ "decide next to encB 6 8 11" 1 \
    'printf "\nexample : EncB.encB 6 8 11 = EncB.encB 6 8 11 :=\n  of_decide_eq_true (by decide)\n" >> ES8Geo/Main.lean'
  case_ "named-argument instance with decide" 1 \
    'printf "\ntheorem st_b : EncB.Model (m := 6) (K := 8) (t := 11) → True := fun _ => by decide\n" >> ES8Geo/Main.lean'
  case_ "#eval on cubes64" 1 'printf "\n#eval EncB.cubes64.length\n" >> ES8Geo/Audit.lean'
  case_ "macro in a unit file" 1 'printf "\nmacro \"st_n\" : term => \`(True)\n" >> ES8Geo/ModelBasic.lean'
  case_ "axiom declaration" 1 'printf "\naxiom st_c : False\n" >> ES8Geo/Labelling.lean'
  case_ "maxHeartbeats 0" 1 'printf "\nset_option maxHeartbeats 0 in\ntheorem st_d : True := trivial\n" >> ES8Geo/ModelBasic.lean'
  case_ "sorryAx in code" 1 'printf "\ntheorem st_e : False := sorryAx False\n" >> ES8Geo/ArcBridge.lean'
  case_ "sorry hidden behind a string literal holding /-" 1 \
    'printf "\ndef st_f : String := \"/-\"\ntheorem st_g : False := sorry\ndef st_h : String := \"-/\"\n" >> ES8Geo/ArcBridge.lean'
  case_ "sorry after a nested block comment" 1 \
    'printf "\n/- a /- b -/ c -/ theorem st_i : False := sorry\n" >> ES8Geo/ArcBridge.lean'
  case_ "missing import in ES8Geo.lean" 1 'sed -i "/^import ES8Geo.Audit$/d" ES8Geo.lean'
  case_ "edited Interface.lean" 1 'printf "\n-- edit\n" >> ES8Geo/Interface.lean'
  case_ "Interface.lean dropped from SOURCES.sha256, then edited" 1 \
    'sed -i "/ES8Geo\/Interface.lean$/d" SOURCES.sha256; printf "\n-- edit\n" >> ES8Geo/Interface.lean'
  case_ "edited vendored module" 1 'printf "\n-- edit\n" >> ErdosSzekeres/Basic.lean'
  case_ "unlisted vendored module" 1 'printf "\n" > ErdosSzekeres/Extra.lean'
  case_ "leanOptions in geo/lakefile.toml" 1 \
    'printf "leanOptions = { debug.skipKernelTC = true }\n" >> lakefile.toml'
  case_ "moreLeanArgs in ../lakefile.toml" 1 \
    'printf "moreLeanArgs = [\"-Ddebug.skipKernelTC=true\"]\n" >> ../lakefile.toml'
  case_ "edited lean-toolchain" 1 'printf "leanprover/lean4:v4.25.0\n" > lean-toolchain'
  case_ "edited ../EncB/Model.lean" 1 'printf "\n-- edit\n" >> ../EncB/Model.lean'
  case_ "extra file in ../EncB" 1 'printf "\n" > ../EncB/Extra.lean'
  case_ "LEANEXT source differs" 1 'printf "\n" >> ../../LEANEXT/keys/KeyOrder.lean'
  echo "selftest: $((ncase - nfail))/$ncase cases as expected"
  [ $nfail -eq 0 ] && { echo "SELFTEST PASS"; exit 0; }
  echo "SELFTEST FAIL"; exit 1
}
[ "${1:-}" = "--selftest" ] && selftest

# ---------------------------------------------------------------------------------------------------------------
fail=0
ok()  { echo "  ok   $*"; }
bad() { echo "  FAIL $*"; fail=1; }
note() { echo "  note $*"; }

REPO=""
if [ "${AUDIT_NO_GIT:-0}" != 1 ]; then REPO=$(git rev-parse --show-toplevel 2>/dev/null || true); fi
VCOMMIT=$(grep -m1 -oE 'commit [0-9a-f]{40}' VENDOR.sha256 | cut -d' ' -f2)
echo "== audit_geo.sh $(date -Is) in $GEO"
if [ -n "$REPO" ]; then echo "   repository $REPO, HEAD $(git -C "$REPO" rev-parse --short HEAD), pinned commit ${VCOMMIT:0:12}"
else echo "   no git checkout (or AUDIT_NO_GIT=1): git cross-checks (check 2) skipped"; fi

echo "1. pinned files"
check_manifest() {  # file, expected number of OK lines
  local m=$1 want=$2 out n
  if out=$(grep -v '^#' "$m" | sha256sum -c 2>&1); then
    n=$(printf '%s\n' "$out" | grep -c ': OK$')
    if [ "$n" -eq "$want" ]; then ok "$m: $n files OK"; else bad "$m: $n OK lines, expected exactly $want"; fi
  else bad "$m:"; printf '%s\n' "$out" | grep -v ': OK$'; fi
}
check_manifest SOURCES.sha256 5
check_manifest VENDOR.sha256 10
want=$(for f in ES8Geo/*.lean; do case " $NEW " in *" $f "*) ;; *) echo "$f";; esac; done | LC_ALL=C sort)
have=$(grep -v '^#' SOURCES.sha256 | awk 'NF {print $2}' | LC_ALL=C sort)
[ "$want" = "$have" ] && ok "SOURCES.sha256 lists exactly the non-unit ES8Geo files" \
  || bad "SOURCES.sha256 lists [$(echo $have)], the non-unit ES8Geo files are [$(echo $want)]"
if out=$(printf '%s\n' "$PINNED" | sha256sum -c 2>&1); then
  ok "PINNED: $(printf '%s\n' "$out" | grep -c ': OK$') files OK (build configuration, manifests, ../EncB)"
else bad "PINNED:"; printf '%s\n' "$out" | grep -v ': OK$'; fi
extra=$(LC_ALL=C comm -23 <(ls ../EncB.lean ../EncB/*.lean | LC_ALL=C sort) \
  <(printf '%s\n' "$PINNED" | awk '{print $2}' | grep -E '^\.\./EncB' | LC_ALL=C sort))
[ -z "$extra" ] && ok "no unlisted file in ../EncB" || bad "unlisted files in ../EncB: $(echo $extra)"
opts=$(grep -nE 'leanOptions|LeanArgs|ServerArgs|ServerOptions|moreLinkArgs|plugins|loadDynlib|skipKernel|precompileModules' \
  lakefile.toml ../lakefile.toml || true)
[ -z "$opts" ] && ok "no Lean options in geo/lakefile.toml or ../lakefile.toml" || { bad "Lean options in a lakefile:"; printf '    %s\n' "$opts"; }
REPO_MANIFEST=""; [ -n "$REPO" ] && [ -f "$REPO/lake-manifest.json" ] && REPO_MANIFEST="$REPO/lake-manifest.json"
mout=$(python3 -I - lake-manifest.json "$MATHLIB_REV" "$REPO_MANIFEST" <<'PY'
import json, sys
geo = {p["name"]: p for p in json.load(open(sys.argv[1]))["packages"]}
bad = 0
if geo.get("mathlib", {}).get("rev") != sys.argv[2]:
    print("FAIL mathlib rev %s, expected %s" % (geo.get("mathlib", {}).get("rev"), sys.argv[2])); bad = 1
if geo.get("encblean", {}).get("type") != "path" or geo["encblean"].get("dir") != "..":
    print("FAIL encblean is not the path package ..");  bad = 1
if sys.argv[3]:
    for p in json.load(open(sys.argv[3]))["packages"]:
        if geo.get(p["name"], {}).get("rev") != p.get("rev"):
            print("FAIL %s: geo rev %s, repository rev %s" % (p["name"], geo.get(p["name"], {}).get("rev"), p.get("rev"))); bad = 1
    if not bad: print("ok geo manifest: Mathlib %s; every repository package at the repository's revision" % sys.argv[2][:8])
elif not bad: print("ok geo manifest: Mathlib %s (no repository manifest to compare)" % sys.argv[2][:8])
for n, p in geo.items():
    if p.get("type") == "git": print("PKG %s %s" % (n, p["rev"]))
sys.exit(bad)
PY
); rc=$?
printf '%s\n' "$mout" | grep -E '^(ok|FAIL)' | sed 's/^ok /  ok   /; s/^FAIL /  FAIL /'
[ $rc -eq 0 ] || fail=1
if [ "${AUDIT_SKIP_BUILD:-0}" = 1 ]; then
  note "package checkouts not inspected (AUDIT_SKIP_BUILD=1)"
else
  fpk=0; npk=0
  while read -r _ n rev; do
    npk=$((npk + 1)); d=.lake/packages/$n
    h=$(git -C "$d" rev-parse HEAD 2>/dev/null || echo none)
    st=$(git -C "$d" status --porcelain --untracked-files=no 2>/dev/null || echo error)
    if [ "$h" != "$rev" ] || [ -n "$st" ]; then fpk=1; bad "$d: HEAD $h, manifest $rev${st:+, tracked changes}"; fi
  done < <(printf '%s\n' "$mout" | grep '^PKG ')
  [ $fpk -eq 0 ] && ok "$npk package checkouts at their manifest revisions, no tracked changes"
fi

echo "2. git cross-checks against the pinned commit ${VCOMMIT:0:12} (not HEAD)"
extra=$(LC_ALL=C comm -23 <(find ErdosSzekeres -name '*.lean' | LC_ALL=C sort) <(grep -v '^#' VENDOR.sha256 | awk 'NF {print $2}' | LC_ALL=C sort))
[ -z "$extra" ] && ok "no unlisted file under ErdosSzekeres/" || bad "unlisted vendored files: $extra"
if [ -z "$REPO" ]; then
  note "skipped: not a git checkout (the PINNED hashes of check 1 still bind every file)"
elif [ -z "$VCOMMIT" ] || ! git -C "$REPO" cat-file -e "$VCOMMIT^{commit}" 2>/dev/null; then
  bad "commit '$VCOMMIT' from the VENDOR.sha256 header is not in the repository"
else
  REL=${GEO#"$REPO"/}; f2=0; n2=0
  cmp_commit() {  # local path, repository path, commit
    local lh ch; lh=$(sha256sum < "$1" | cut -d' ' -f1)
    if git -C "$REPO" cat-file -e "$3:$2" 2>/dev/null; then ch=$(git -C "$REPO" show "$3:$2" | sha256sum | cut -d' ' -f1)
    else ch=missing; fi
    n2=$((n2 + 1)); [ "$lh" = "$ch" ] || { f2=1; bad "$1 differs from $3:$2 (local $lh, commit $ch)"; }
  }
  while read -r _ p; do [ -n "$p" ] && cmp_commit "$p" "$p" "$VCOMMIT"; done < <(grep -v '^#' VENDOR.sha256)
  while read -r _ p; do
    case $p in ../*) cmp_commit "$p" "${REL%/geo}/${p#../}" "$VCOMMIT";; esac
  done < <(printf '%s\n' "$PINNED")
  [ $f2 -eq 0 ] && ok "$n2 files (10 vendored modules, ../EncB, ../ build files) equal commit ${VCOMMIT:0:12}"
  for m in SOURCES.sha256 VENDOR.sha256; do
    if git -C "$REPO" cat-file -e "HEAD:$REL/$m" 2>/dev/null; then
      cmp -s "$m" <(git -C "$REPO" show "HEAD:$REL/$m") && ok "$m equals its committed version" \
        || bad "$m differs from HEAD:$REL/$m"
    else note "$m not yet committed (bound by its PINNED hash)"; fi
  done
fi

echo "3. LEANEXT copies"
for pair in Capstone2.lean:capstone/Capstone2.lean KeyOrder.lean:keys/KeyOrder.lean \
            OrbitConsistency.lean:orbit/OrbitConsistency.lean; do
  f=ES8Geo/${pair%%:*}; s=$RESULTS/LEANEXT/${pair#*:}
  if cmp -s "$f" "$s"; then ok "$f = LEANEXT/${pair#*:}"; else bad "$f differs from $s"; fi
done

# Strip comments, keep the line count: block comments nest (/- /- -/ -/), `--` runs to the end of the line, and
# string literals "..." (with \ escapes) and char literals 'x' are kept verbatim, so "/-" in a string starts no
# comment. Raw strings r"..." are not recognized (none occur in these files).
strip() {
  perl -CSDA -0777 -ne '
    s{("(?:[^"\\]|\\.)*")|((?<![\w\x27.!?])\x27(?:[^\x27\\\n]|\\[^\n]{1,10}?)\x27)|(?<bc>/-(?:(?!/-|-/).|(?&bc))*-/)|(--[^\n]*)}{
      defined $1 ? $1 : defined $2 ? $2 : do { my $t = $&; $t =~ tr/\n//cd; $t }
    }gse;
    print;' "$1"
}

echo "4. forbidden tokens (code only)"
FORB='\b(sorry|sorryAx|admit|native_decide|opaque|implemented_by|extern|unsafe|skipKernelTC|ofReduceBool|ofReduceNat|reduceBool|reduceNat)\b|^\s*(@\[[^]]*\]\s*)?((private|protected|noncomputable)\s+)*axiom\b|maxHeartbeats\s+0\b'
nf=0; f4=0
while IFS= read -r f; do
  nf=$((nf + 1))
  hits=$(strip "$f" | grep -nE "$FORB" || true)
  [ -n "$hits" ] && { f4=1; bad "$f:"; printf '    %s\n' "$hits"; }
done < <(ls ES8Geo/*.lean ES8Geo.lean; find ErdosSzekeres -name '*.lean' | sort)
[ $f4 -eq 0 ] && ok "$nf files clean"
# report every bounded maxHeartbeats (allowed, must be documented)
mh=$(grep -rnE 'maxHeartbeats' ES8Geo ErdosSzekeres | grep -vE 'maxHeartbeats\s+0\b' || true)
[ -n "$mh" ] && { echo "  note bounded maxHeartbeats settings:"; printf '    %s\n' "$mh"; }

echo "5. no evaluation of the (6,8,11) instance in the M5-M8 files"
PAT='\b(encB|gen|genCoded|numVars|allCodes|allCodesOf|encode|diagCoded|Model)\s+6\s+8\s+11\b|\(\s*[mKt]\s*:=\s*(6|8|11)\s*\)|\b(CubesUnsat64|cubesUnsat64\w*|cubes64|cubeVars64|cubeCnf|cnfText|parseDimacs\w*|encB_unsat\w*|\w*6811\w*)\b'
RISK='(?<![\w#.])(decide|rfl|norm_num|simp|simp_all|simpa|dsimp|simp_arith|omega|grind|trivial|aesop|bv_decide|Eq\.refl|eq_self|Nat\.decEq|decide_eq_true|native_decide|of_decide_eq_true|run_cmd|run_tac|run_elab)(?![\w])|#eval\b|#reduce\b'
for f in $NEW; do
  [ -f "$f" ] || { bad "$f missing"; continue; }
  out=$(strip "$f" | PAT="$PAT" RISK="$RISK" F="$f" perl -CSDA -e '
    my ($pat, $risk, $f) = ($ENV{PAT}, $ENV{RISK}, $ENV{F});
    my $riskd = qr/(?<![\w#.\x27])by(?![\w\x27])|decreasing_by|$risk/;
    my @l = <STDIN>; my $bad = 0; my $n = 0; my $nd = 0;
    # (a) within 3 lines
    for my $i (0 .. $#l) {
      next unless $l[$i] =~ /$pat/; $n++;
      my ($lo, $hi) = ($i - 3 < 0 ? 0 : $i - 3, $i + 3 > $#l ? $#l : $i + 3);
      for my $j ($lo .. $hi) {
        if ($l[$j] =~ /$risk/) { printf "  FAIL %s:%d token \"%s\" within 3 lines of line %d\n", $f, $j+1, $&, $i+1; $bad = 1; }
      }
    }
    # (b) a declaration (a column-0 command and its continuation lines) that mentions the instance is a term
    my $kw = qr/^(?:@\[|#\w|theorem|lemma|def|abbrev|instance|example|structure|inductive|class|axiom|opaque|private|protected|noncomputable|partial|unsafe|namespace|end|section|open|set_option|attribute|variable|universe|import|mutual|macro|macro_rules|syntax|elab|elab_rules|notation|infix|infixl|infixr|prefix|postfix|local|scoped|deriving|initialize|run_cmd|run_tac|run_elab)\b/;
    my @blk; my ($s, $b) = (1, "");
    for my $i (0 .. $#l) {
      if ($l[$i] =~ $kw && $b =~ /\S/) { push @blk, [$s, $b]; ($s, $b) = ($i + 1, ""); }
      elsif ($l[$i] =~ $kw) { $s = $i + 1; }
      $b .= $l[$i];
    }
    push @blk, [$s, $b] if $b =~ /\S/;
    for my $x (@blk) { my ($s, $t) = @$x; next unless $t =~ /$pat/; $nd++;
      if ($t =~ /$riskd/) { print "  FAIL $f:$s declaration mentioning the instance contains \"$&\" (must be a term)\n"; $bad = 1; } }
    # (c) no macro, syntax, elaborator or notation
    for my $i (0 .. $#l) {
      if ($l[$i] =~ /^\s*(?:(?:local|scoped|private)\s+)*(macro|macro_rules|syntax|elab|elab_rules|notation|infix|infixl|infixr|prefix|postfix)\b/) {
        print "  FAIL $f:", $i+1, " defines a $1\n"; $bad = 1; }
    }
    print "  ok   $f: $n line(s) and $nd declaration(s) mention it; all terms, no risky token near\n" unless $bad;
    exit $bad;'); rc=$?
  printf '%s\n' "$out"
  [ $rc -eq 0 ] || fail=1
done

echo "6. module list"
f6=0
for f in ES8Geo/*.lean; do
  m=ES8Geo.$(basename "$f" .lean)
  grep -qx "import $m" ES8Geo.lean || { f6=1; bad "ES8Geo.lean does not import $m"; }
done
[ $f6 -eq 0 ] && ok "ES8Geo.lean imports all $(ls ES8Geo/*.lean | wc -l) modules"

echo "7. build gate (re-elaboration of the M5-M8 files; #guard_msgs on axioms and statements in ES8Geo/Audit.lean)"
gate=ran
if [ "${AUDIT_SKIP_BUILD:-0}" = 1 ]; then
  echo "  SKIPPED (AUDIT_SKIP_BUILD=1)"; gate=skipped
else
  if lake build --no-build > /dev/null 2>&1; then ok "lake build --no-build: up to date"
  else bad "lake build --no-build: build missing or stale (run lake build first)"; fi
  TO=${AUDIT_LEAN_TIMEOUT:-300}
  ERR='^[^:]+:[0-9]+:[0-9]+: error'
  for f in $NEW; do
    t0=$(date +%s.%N)
    out=$(timeout -k 5 "$TO" lake env lean "$f" 2>&1); rc=$?
    dt=$(printf '%.1f' "$(echo "$(date +%s.%N) - $t0" | bc)")
    if [ $rc -eq 0 ] && ! printf '%s\n' "$out" | grep -qE "$ERR"; then ok "$f elaborates (${dt} s)"
    else bad "$f: exit $rc after ${dt} s"; printf '%s\n' "$out" | grep -E "$ERR" | head -20; fi
    [ "$f" = ES8Geo/Main.lean ] && axo=$(printf '%s\n' "$out" | grep 'depends on axioms' || true)
  done
  printf '%s\n' "${axo:-}" | sed 's/^/    /'
  if [ -z "${axo:-}" ]; then bad "no axioms printed by ES8Geo/Main.lean"
  elif printf '%s\n' "$axo" | grep -v 'depends on axioms: \[propext, Classical.choice, Quot.sound\]$' | grep -q .
  then bad "a main theorem depends on a non-standard axiom"; fi
fi

if [ $fail -ne 0 ]; then echo "AUDIT FAIL"; exit 1; fi
if [ "$gate" = skipped ]; then echo "AUDIT INCOMPLETE (build gate skipped)"; exit 3; fi
if [ -z "$REPO" ]; then echo "AUDIT PASS (git cross-checks skipped: not a git checkout)"; exit 0; fi
echo "AUDIT PASS"; exit 0
