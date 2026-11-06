#!/usr/bin/env bash
# Tests of coverage_es310.py (6 November 2026). Python only: nothing is compiled, no Lean runs.
# ES(8) <= 310 is NOT proved; these tests only exercise the coverage bookkeeping.
#
#   test_coverage_es310.sh            (writes only under build/es310/test-cov and logs/es310)
#
# Inputs: ctx 2406 and 2407 of the running campaign C (read only, opened by export_es310.py and
# coverage_es310.py) and a fake campaign of 4,096 synthetic contexts (make_cov_fixture_es310.py).
#  A. real data: export_es310.py --ctx 2406,2407 --chunk-leaves 500 (several SRs per context, an internal
#     skeleton in both, 8 modules), merge_es310.py --subtree 11:1203; coverage --partial, --subtree 11:1203,
#     --tree63-shape and the --cache path must PASS;
#  B. fake campaign: fixture export of all 4,096 contexts (1-3 leaves each, 1,365 internal skeletons, some
#     K = 2^18), merge_es310.py --complete; coverage --complete must PASS;
#  C. negative tests, each on a fresh copy, each must FAIL (exit 1) with the named check failing. Where a
#     file with a recorded sha256 is mutated, the sha256 is re-recorded (context manifest, merged manifest,
#     and merge's ctx_manifests pin), so that the semantic check, not the hash check, has to catch it.
#  Fixer additions (6 Nov): --exporter-sha256 is exact (a prefix, the export_es311 hash and the text
#  "export_es310" are refused); a held OUT/.export.lock gives exit 4; a changed run_context.py is a warning only.
set -u
D=$(cd "$(dirname "$0")" && pwd)
C=/home/jay/research/data/es8-b64-pilot-20261105
SRC=$D/../omission-cover-certificates-2026-10-10/balanced-v2-source.json
T=$D/build/es310/test-cov
SHAPE63=$D/build/es311/shape-a79a9dd5792cf849.json.gz
mkdir -p "$D/logs/es310"
LOG=$D/logs/es310/test_coverage_es310-$(date +%Y%m%d-%H%M%S).log
exec > >(tee "$LOG") 2>&1
case "$T" in "$D"/build/es310/test-cov) ;; *) echo "bad T $T"; exit 2 ;; esac
rm -rf "$T"
mkdir -p "$T"
NPASS=0; NFAIL=0
ok()  { NPASS=$((NPASS + 1)); echo "  PASS  $*"; }
bad() { NFAIL=$((NFAIL + 1)); echo "  FAIL  $*"; }
cov() { nice -n 10 python3 "$D/coverage_es310.py" "$@" 2>/dev/null; }
failing() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(" ".join(k for k,v in d["checks"].items() if not v["ok"]))' "$1"; }

expect_pass() {  # name, coverage args...
  local name=$1; shift
  local out=$T/r-$name.json
  cov "$@" > "$out"; local rc=$?
  if [ $rc -eq 0 ]; then ok "$name (exit 0, $(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d["contexts_checked"], "contexts,", d["leaves"], "leaves,", len(d["checks"]), "checks,", d["seconds"], "s")' "$out"))"
  else bad "$name: exit $rc, failing checks: $(failing "$out" 2>/dev/null)"; fi
}
expect_fail() {  # name, expected failing check, coverage args...
  local name=$1 want=$2; shift 2
  local out=$T/r-$name.json
  cov "$@" > "$out"; local rc=$?
  local f; f=$(failing "$out" 2>/dev/null)
  if [ $rc -eq 1 ] && [[ " $f " == *" $want "* ]]; then ok "$name -> FAIL as required [$f]"
  else bad "$name: exit $rc (want 1), failing checks [$f], wanted '$want'"; fi
  python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); w=sys.argv[2]; c=d["checks"].get(w,{}); print("        e.g.", (c.get("first") or ["-"])[0][:220])' "$out" "$want" 2>/dev/null
}

# mutation helper: python3 -c "$MUT" DIR PREFIX ACTION ARGS...
read -r -d '' MUT <<'EOF'
import hashlib, json, re, sys
from pathlib import Path
out, prefix, action, *a = sys.argv[1:]
out = Path(out)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
mf = out / f"manifest-{prefix}.json"
def rerecord(files):
    """re-record the sha256 of mutated module / Root files and of the context manifests that list them"""
    merged = json.loads(mf.read_text()) if mf.exists() else None
    for f in files:
        rel = str(f.relative_to(out))
        if f.name == "Root.lean":
            if merged: merged["root"]["sha256"] = sha(f)
            continue
        k = int(f.name[1:5])
        cm = out / "ctx" / f"ctx-{k:04d}.json"
        man = json.loads(cm.read_text())
        for mm in man["modules"]:
            if mm["file"] == rel: mm["sha256"] = sha(f)
        cm.write_text(json.dumps(man, indent=1) + "\n")
        if merged:
            for mm in merged["modules"]:
                if mm["file"] == rel: mm["sha256"] = sha(f)
            for e in merged.get("ctx_manifests") or []:
                if e["ctx"] == k: e["sha256"] = sha(cm)
    if merged: mf.write_text(json.dumps(merged, indent=1) + "\n")
def edit_line(f, pred, fn, count=1):
    lines = f.read_text().split("\n"); n = 0
    for i, ln in enumerate(lines):
        if n < count and pred(ln):
            new = fn(ln); assert new != ln, ln[:80]; lines[i] = new; n += 1
    assert n == count, (f, n)
    f.write_text("\n".join(lines))
def flip_last(pathlist):  # flip the decision of the last pair of a path literal
    return re.sub(r"\((\d+), ([12])\)\]$", lambda m: f"({m.group(1)}, {3 - int(m.group(2))})]", pathlist)
def flip_first(pathlist):
    return re.sub(r"^\[\((\d+), ([12])\)", lambda m: f"[({m.group(1)}, {3 - int(m.group(2))})", pathlist)
src = out / "src" / prefix
root = src / "Root.lean"
if action == "split_vertex_block":      # a split vertex inside a block term of module a[0]
    f = src / f"{a[0]}.lean"
    edit_line(f, lambda l: l.startswith("noncomputable def") and "(.split " in l,
              lambda l: re.sub(r"\(\.split (\d+) ", lambda m: f"(.split {(int(m.group(1)) + 1) % 252} ", l, count=1))
    if a[1:] != ["nohash"]: rerecord([f])
elif action == "split_vertex_comb":     # the vertex of a split_pm combination inside module a[0]
    f = src / f"{a[0]}.lean"
    edit_line(f, lambda l: l.startswith("  split_pm "),
              lambda l: re.sub(r"\] (\d+) ex", lambda m: f"] {(int(m.group(1)) + 1) % 252} ex", l, count=1))
    rerecord([f])
elif action == "flip_block_path":       # one decision of one block's chk and ex statements (consistently)
    f = src / f"{a[0]}.lean"
    lines = f.read_text().split("\n")
    i = next(i for i, l in enumerate(lines) if l.startswith("theorem chk"))
    for j in (i, i + 1):
        lines[j] = re.sub(r"\(pmask \(zerosF 252\) (\[[^\]]*\])\)", lambda m: f"(pmask (zerosF 252) {flip_first(m.group(1))})", lines[j])
    f.write_text("\n".join(lines)); rerecord([f])
elif action == "swap_block_path":       # swap two decisions of one block's statements (same mask: crit1 item 3)
    f = src / f"{a[0]}.lean"
    lines = f.read_text().split("\n")
    i = next(i for i, l in enumerate(lines) if l.startswith("theorem chk"))
    def sw(m):
        pairs = re.findall(r"\(\d+, [12]\)", m.group(1)); pairs[0], pairs[1] = pairs[1], pairs[0]
        return "(pmask (zerosF 252) [" + ", ".join(pairs) + "])"
    for j in (i, i + 1):
        lines[j] = re.sub(r"\(pmask \(zerosF 252\) (\[[^\]]*\])\)", sw, lines[j])
    f.write_text("\n".join(lines)); rerecord([f])
elif action == "flip_base_ctx":         # flip one base-path decision of context a[0] in all its statements
    k = int(a[0]); man = json.loads((out / "ctx" / f"ctx-{k:04d}.json").read_text())
    v, x = man["base_path"][0]; old, new = f"({v}, {x}), ", f"({v}, {3 - x}), "
    files = [out / mm["file"] for mm in man["modules"]] + [root]
    for f in files:
        t = f.read_text()
        if f.name == "Root.lean":   # only the theorems of this context's internal skeleton
            t = "\n".join(l.replace(old, new) if re.match(rf"(theorem ex{k + 1}\d{{5}} |  split_pm .*\] \d+ (?:{prefix}\.C{k:04d}|ex{k + 1}\d{{5}}))", l) else l for l in t.split("\n"))
        else:
            t = t.replace(old, new)
        f.write_text(t)
    rerecord(files)
elif action == "budget_ex":             # budget literal 64 -> 63 in one combination/block ex statement
    f = src / f"{a[0]}.lean"
    edit_line(f, lambda l: l.startswith("theorem ex"), lambda l: l.replace("FFeas fcat62 3131 252 64 ", "FFeas fcat62 3131 252 63 "))
    rerecord([f])
elif action == "leaf_word":             # one packed word of one leaf decremented
    f = src / f"{a[0]}.lean"
    edit_line(f, lambda l: l.startswith("noncomputable def") and "natlits% [" in l,
              lambda l: re.sub(r"natlits% \[(\d+)", lambda m: f"natlits% [{int(m.group(1)) - 1}", l, count=1))
    rerecord([f])
elif action == "root_dup_ctx":          # in the Root, the one child of the depth-11 node a[0] := its zero child
    edit_line(root, lambda l: l.startswith("  split_pm ") and l.endswith(f" {a[1]} {a[2]}"), lambda l: l[: -len(a[2])] + a[1])
    rerecord([root])
elif action == "root_wrong_module":     # a context SR referenced from another module of the same context
    edit_line(root, lambda l: f" {a[0]}" in l, lambda l: l.replace(f" {a[0]}", f" {a[1]}", 1))
    rerecord([root])
elif action == "root_flip":             # flip one decision of Root theorem ex<a[0]> (statement and split_pm path)
    lines = root.read_text().split("\n")
    i = next(i for i, l in enumerate(lines) if l.startswith(f"theorem ex{a[0]} "))
    lines[i] = re.sub(r"\(pmask \(zerosF 252\) (\[[^\]]*\])\)", lambda m: f"(pmask (zerosF 252) {flip_first(m.group(1))})", lines[i])
    lines[i + 1] = re.sub(r"\(zerosF 252\) (\[[^\]]*\])", lambda m: f"(zerosF 252) {flip_first(m.group(1))}", lines[i + 1])
    root.write_text("\n".join(lines)); rerecord([root])
elif action == "root_vertex":           # the vertex of Root theorem ex<a[0]>
    lines = root.read_text().split("\n")
    i = next(i for i, l in enumerate(lines) if l.startswith(f"theorem ex{a[0]} "))
    lines[i + 1] = re.sub(r"\] (\d+) ", lambda m: f"] {(int(m.group(1)) + 1) % 252} ", lines[i + 1], count=1)
    root.write_text("\n".join(lines)); rerecord([root])
elif action == "root_budget":           # theorem root at budget 63
    edit_line(root, lambda l: l.startswith("theorem root"), lambda l: l.replace(" 252 64 ", " 252 63 "))
    rerecord([root])
elif action == "root_drop_import":
    edit_line(root, lambda l: l == f"import {a[0]}", lambda l: "")
    t = root.read_text().replace("\n\n", "\n", 1); root.write_text(t); rerecord([root])
elif action == "manifest_tree_sha":     # the recorded tree gz sha256 of context a[0] (as if the campaign file changed)
    k = int(a[0]); cm = out / "ctx" / f"ctx-{k:04d}.json"; man = json.loads(cm.read_text())
    man["inputs"]["tree_gz"]["sha256"] = "0" * 64; cm.write_text(json.dumps(man, indent=1) + "\n")
elif action == "manifest_drop_sr":      # drop the last SR of the last module of context a[0] from its manifest
    k = int(a[0]); cm = out / "ctx" / f"ctx-{k:04d}.json"; man = json.loads(cm.read_text())
    s, c = man["modules"][-1]["subtree_roots"].pop(); man["modules"][-1]["leaves"] -= c
    cm.write_text(json.dumps(man, indent=1) + "\n")
elif action == "module_touch":          # change a module comment without re-recording its sha256
    f = src / f"{a[0]}.lean"
    edit_line(f, lambda l: l.startswith("-- "), lambda l: l + " x")
else:
    sys.exit(f"unknown action {action}")
EOF
mut() { python3 -c "$MUT" "$@" || { echo "  mutation $* raised"; NFAIL=$((NFAIL + 1)); }; }
fresh() { rm -rf "$T/$2"; cp -a "$T/$1" "$T/$2"; }

echo "== test_coverage_es310.sh $(date '+%F %T %Z'); coverage_es310.py sha256 $(sha256sum "$D/coverage_es310.py" | cut -c1-64)"
echo "== A. real data: ctx 2406, 2407 (export_es310.py, merge_es310.py --subtree 11:1203)"
for f in export_es310.py merge_es310.py; do [ -f "$D/$f" ] || { echo "missing $D/$f"; exit 2; }; done
nice -n 10 python3 "$D/export_es310.py" --campaign "$C" --source "$SRC" --out "$T/sub" --ctx 2406,2407 \
  --chunk-leaves 500 --block-leaves 64 --per-word 8 --prefix E310BT > "$T/export-sub.json" 2> "$T/export-sub.err" \
  || { echo "export_es310.py failed: $(tail -2 "$T/export-sub.err")"; exit 2; }
python3 "$D/merge_es310.py" "$T/sub" --subtree 11:1203 --prefix E310BT > "$T/merge-sub.json" 2>&1 \
  || { echo "merge_es310.py failed: $(cat "$T/merge-sub.json")"; exit 2; }
echo "  export: $(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print([(e["ctx"], e["leaves"], e["modules"], e["skeleton"]) for e in d["exported"]])' "$T/export-sub.json") (ctx, leaves, modules, internal skeleton)"
expect_pass sub-partial "$T/sub" --partial --prefix E310BT
expect_pass sub-subtree "$T/sub" --subtree 11:1203 --prefix E310BT
if [ -f "$SHAPE63" ]; then expect_pass sub-tree63 "$T/sub" --subtree 11:1203 --prefix E310BT --tree63-shape "$SHAPE63"; fi
expect_pass sub-jobs2 "$T/sub" --subtree 11:1203 --prefix E310BT --jobs 2
expect_fail sub-subtree-wrong-node ctx_manifests_present "$T/sub" --subtree 11:1202 --prefix E310BT
fresh sub pm
python3 "$D/merge_es310.py" "$T/pm" --partial --prefix E310BT > /dev/null 2>&1 || bad "merge --partial"
expect_pass partial-merge "$T/pm" --partial --prefix E310BT --report "$T/pm/coverage-report.json"
[ -s "$T/pm/coverage-report.json" ] && ok "--report written" || bad "--report not written"
EXSHA=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["exporter_sha256"]["export_es310"])' "$T/sub/ctx/ctx-2406.json")
expect_pass exporter-pinned "$T/sub" --partial --prefix E310BT --exporter-sha256 "$EXSHA"
expect_fail exporter-pin-wrong exporter_pinned "$T/sub" --partial --prefix E310BT --exporter-sha256 "$(printf '%064d' 0)"
EX311=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["exporter_sha256"]["export_es311"])' "$T/sub/ctx/ctx-2406.json")
expect_fail exporter-pin-is-the-311-hash exporter_pinned "$T/sub" --partial --prefix E310BT --exporter-sha256 "$EX311"
for p in "${EXSHA:0:4}" "${EXSHA:0:63}" export_es310 "${EXSHA^^}"; do  # a prefix, 63 digits, the key text, upper case
  cov "$T/sub" --partial --prefix E310BT --exporter-sha256 "$p" > "$T/r-pin-usage.json"; rc=$?
  if [ $rc -eq 2 ] && grep -q 'is not 64 hex digits' "$T/r-pin-usage.json"; then ok "exporter pin '${p:0:16}...' refused as usage (exit 2)"
  else bad "exporter pin '$p': exit $rc (want 2)"; fi
done
flock -x -n "$T/sub/.export.lock" sleep 8 &
LKP=$!; sleep 0.5
cov "$T/sub" --partial --prefix E310BT > "$T/r-locked.json"; rc=$?
if [ $rc -eq 4 ] && grep -q 'is held' "$T/r-locked.json"; then ok "lock held by an exporter/merge: exit 4"; else bad "lock held: exit $rc (want 4)"; fi
wait $LKP
expect_pass after-lock-released "$T/sub" --partial --prefix E310BT
# cache: second run skips the deep check; a changed module with its sha re-recorded is deep-checked again
fresh sub cache
expect_pass cache-run1 "$T/cache" --partial --prefix E310BT --cache "$T/cache/cov-cache.json"
expect_pass cache-run2 "$T/cache" --partial --prefix E310BT --cache "$T/cache/cov-cache.json"
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); assert d["contexts_deep_checked"] == 0, d["contexts_deep_checked"]' "$T/r-cache-run2.json" \
  && ok "cache-run2 deep-checked 0 contexts" || bad "cache-run2 did not use the cache"
mut "$T/cache" E310BT split_vertex_block C240702
expect_fail cache-after-change block_terms "$T/cache" --partial --prefix E310BT --cache "$T/cache/cov-cache.json"
fresh sub cache2
cov "$T/cache2" --partial --prefix E310BT --cache "$T/cache2/cov-cache.json" > /dev/null
mut "$T/cache2" E310BT module_touch C240601
expect_fail cache-hit-module-changed module_sha256 "$T/cache2" --partial --prefix E310BT --cache "$T/cache2/cov-cache.json"

echo "== B. fake campaign: 4,096 synthetic contexts, merge_es310.py --complete"
nice -n 10 python3 "$D/make_cov_fixture_es310.py" fake-campaign "$T/fake-campaign" --from "$C" > /dev/null || exit 2
nice -n 10 python3 "$D/make_cov_fixture_es310.py" export "$T/complete" --campaign "$T/fake-campaign" --prefix E310BK > /dev/null || exit 2
python3 "$D/merge_es310.py" "$T/complete" --complete --prefix E310BK --no-profile > "$T/merge-complete.json" 2>&1 \
  || { echo "merge --complete failed: $(cat "$T/merge-complete.json")"; exit 2; }
FK="--prefix E310BK --campaign $T/fake-campaign"
expect_pass complete "$T/complete" --complete $FK
expect_pass complete-partial "$T/complete" --partial $FK --jobs 2
fresh complete sub35
python3 "$D/merge_es310.py" "$T/sub35" --subtree 3:5 --prefix E310BK --no-profile > /dev/null 2>&1 || bad "merge --subtree 3:5"
expect_pass fake-subtree-3:5 "$T/sub35" --subtree 3:5 $FK
expect_fail complete-root-as-subtree-3:5 root_statement "$T/complete" --subtree 3:5 $FK

echo "== C. negative tests (each must FAIL)"
# 1. drop a context
fresh sub n1; rm "$T/n1/ctx/ctx-2407.json"
expect_fail drop-context-subtree ctx_manifests_present "$T/n1" --subtree 11:1203 --prefix E310BT
expect_fail drop-context-partial ctx_manifests_present "$T/n1" --partial --ctx 2406,2407 --prefix E310BT
fresh complete f1; rm "$T/f1/ctx/ctx-1234.json"
expect_fail drop-context-complete ctx_manifests_present "$T/f1" --complete $FK
# 2. change a split vertex in a module (block term; split_pm combination), and in the Root
fresh sub n2; mut "$T/n2" E310BT split_vertex_block C240701
expect_fail split-vertex-block block_terms "$T/n2" --subtree 11:1203 --prefix E310BT
fresh sub n2h; mut "$T/n2h" E310BT split_vertex_block C240701 nohash
expect_fail split-vertex-block-sha-not-rerecorded module_sha256 "$T/n2h" --subtree 11:1203 --prefix E310BT
fresh sub n2b; mut "$T/n2b" E310BT split_vertex_comb C240703
expect_fail split-vertex-combination split_vertex_children "$T/n2b" --subtree 11:1203 --prefix E310BT
fresh sub n2c; mut "$T/n2c" E310BT root_vertex 1000003251
expect_fail split-vertex-root root_vertices "$T/n2c" --subtree 11:1203 --prefix E310BT
fresh complete f2; mut "$T/f2" E310BK split_vertex_comb C000201
expect_fail split-vertex-complete-module split_vertex_children "$T/f2" --complete $FK
fresh complete f2b; mut "$T/f2b" E310BK root_vertex 1000000777
expect_fail split-vertex-complete-root root_vertices "$T/f2b" --complete $FK
# 3. flip one path decision (module statements; base path of one context everywhere; Root), and a swap
fresh sub n3; mut "$T/n3" E310BT flip_block_path C240602
expect_fail flip-path-block statement_paths "$T/n3" --subtree 11:1203 --prefix E310BT
fresh sub n3b; mut "$T/n3b" E310BT flip_base_ctx 2407
expect_fail flip-base-path-ctx2407 statement_paths "$T/n3b" --subtree 11:1203 --prefix E310BT
fresh sub n3c; mut "$T/n3c" E310BT root_flip 1000003251
expect_fail flip-path-root root_paths "$T/n3c" --subtree 11:1203 --prefix E310BT
fresh sub n3d; mut "$T/n3d" E310BT swap_block_path C240701
expect_fail swap-two-decisions statement_paths "$T/n3d" --subtree 11:1203 --prefix E310BT
fresh complete f3; mut "$T/f3" E310BK root_flip 1000000005
expect_fail flip-path-complete-root root_paths "$T/f3" --complete $FK
# 4. duplicate a context reference (the depth-11 node's one child := its zero child)
fresh sub n4; mut "$T/n4" E310BT root_dup_ctx 1000003251 ex240700000 ex240800000
expect_fail duplicate-context-ref root_references "$T/n4" --subtree 11:1203 --prefix E310BT
fresh sub n4b; mut "$T/n4b" E310BT root_wrong_module E310BT.C240702.ex852 E310BT.C240703.ex852
expect_fail ref-from-wrong-module root_references "$T/n4b" --subtree 11:1203 --prefix E310BT
DUP=$(python3 - "$T/complete/src/E310BK/Root.lean" <<'EOF'
import re, sys
for l in open(sys.argv[1]):
    m = re.match(r"  split_pm .*\] \d+ (E310BK\.C\d{6}\.ex0|ex\d{9}) (E310BK\.C\d{6}\.ex0|ex\d{9})$", l)
    if m:
        print(m.group(1), m.group(2)); break
EOF
)
fresh complete f4; mut "$T/f4" E310BK root_dup_ctx X $DUP
expect_fail duplicate-context-ref-complete root_references "$T/f4" --complete $FK
# 5. wrong budget literal in one ex (module), in theorem root
fresh sub n5; mut "$T/n5" E310BT budget_ex C240704
expect_fail budget-63-in-one-ex budget_literal "$T/n5" --subtree 11:1203 --prefix E310BT
fresh sub n5b; mut "$T/n5b" E310BT root_budget
expect_fail budget-63-theorem-root root_statement "$T/n5b" --subtree 11:1203 --prefix E310BT
fresh complete f5; mut "$T/f5" E310BK root_budget
expect_fail budget-63-complete-root root_statement "$T/f5" --complete $FK
# 6. further: a leaf word, a recorded input hash, a dropped SR, a dropped Root import
fresh sub n6; mut "$T/n6" E310BT leaf_word C240601
expect_fail leaf-word-changed block_terms "$T/n6" --subtree 11:1203 --prefix E310BT
fresh sub n7; mut "$T/n7" E310BT manifest_tree_sha 2406
expect_fail input-hash-changed inputs_rehash "$T/n7" --partial --prefix E310BT
fresh sub n8; mut "$T/n8" E310BT manifest_drop_sr 2407
expect_fail sr-dropped subtree_roots_cover "$T/n8" --partial --prefix E310BT
fresh sub n9; mut "$T/n9" E310BT root_drop_import E310BT.C240705
expect_fail root-import-dropped root_imports "$T/n9" --subtree 11:1203 --prefix E310BT

echo "== D. campaign-side negatives (a second fake campaign, mutated in place; never C)"
F2=$T/fake2
nice -n 10 python3 "$D/make_cov_fixture_es310.py" fake-campaign "$F2" --from "$C" > /dev/null || exit 2
nice -n 10 python3 "$D/make_cov_fixture_es310.py" export "$T/f2x" --campaign "$F2" --prefix E310BK --ctx 0,1,2 > /dev/null || exit 2
F2K="--prefix E310BK --campaign $F2"
expect_pass fake2-baseline "$T/f2x" --partial $F2K
touch "$F2/campaign/WITNESS-ALERT.txt"
expect_fail witness-alert witness_absent "$T/f2x" --partial $F2K
rm "$F2/campaign/WITNESS-ALERT.txt"
touch "$F2/runs/ctx-1-b64.WITNESS.json"
expect_fail witness-file witness_absent "$T/f2x" --partial $F2K
rm "$F2/runs/ctx-1-b64.WITNESS.json"
cp -p "$F2/run_context.py" "$T/run_context.py.bak"; echo "# changed" >> "$F2/run_context.py"
expect_pass run-context-changed-is-a-warning "$T/f2x" --partial $F2K
grep -q 'campaign code: run_context.py sha256 recorded' "$T/r-run-context-changed-is-a-warning.json" \
  && ok "run_context.py changed: PASS with the campaign-code warning" || bad "run_context.py changed: no warning"
cp -p "$T/run_context.py.bak" "$F2/run_context.py"
for st in capped:status replay:replay; do
  name=${st%%:*}; what=${st##*:}
  cp -p "$F2/runs/ctx-2-b64.result.json" "$T/res2.bak"; cp -p "$T/f2x/ctx/ctx-0002.json" "$T/man2.bak"
  python3 - "$F2/runs/ctx-2-b64.result.json" "$T/f2x/ctx/ctx-0002.json" "$what" <<'EOF'
import hashlib, json, os, sys
rp, cm, what = sys.argv[1:]
r = json.load(open(rp))
if what == "status":
    r["status"] = "capped"
else:
    r["replay"]["ok"] = False
open(rp, "w").write(json.dumps(r, indent=1))
raw = open(rp, "rb").read(); st = os.stat(rp)
m = json.load(open(cm))   # re-record the result file, so that only the result's content can fail
m["inputs"]["result"].update(sha256=hashlib.sha256(raw).hexdigest(), size=len(raw), mtime_ns=st.st_mtime_ns)
open(cm, "w").write(json.dumps(m, indent=1) + "\n")
EOF
  expect_fail "result-$name" result_closed "$T/f2x" --partial $F2K
  cp -p "$T/res2.bak" "$F2/runs/ctx-2-b64.result.json"; cp -p "$T/man2.bak" "$T/f2x/ctx/ctx-0002.json"
done
expect_pass fake2-restored "$T/f2x" --partial $F2K
python3 - "$F2/contexts.jsonl" <<'EOF'
import json, sys
p = sys.argv[1]
lines = open(p).read().split("\n")
c = json.loads(lines[1]); c["path"][5][0] = (c["path"][5][0] + 1) % 252   # ctx 1: another vertex at depth 5
lines[1] = json.dumps(c, separators=(",", ":")); open(p, "w").write("\n".join(lines))
EOF
expect_fail contexts-jsonl-prefix-vertex contexts_jsonl "$T/f2x" --partial $F2K

echo "== result: $NPASS passed, $NFAIL failed (log $LOG)"
[ $NFAIL -eq 0 ]
