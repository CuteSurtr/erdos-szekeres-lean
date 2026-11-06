#!/bin/bash
# Python-only tests of export_es310.py and merge_es310.py (6 November 2026; route to ES(8) <= 310, which is
# NOT proved). Usage: test_export_es310.sh   (log: logs/es310/test_export_es310.log)
#
# Everything runs on a FAKE campaign, build/es310/test-fake/camp, reset before each case from
# build/es310/test-fake/pristine (copies, made once with cp -p, of the real campaign's contexts.jsonl,
# run_context.py and the ctx 2406 / 2407 result and tree files). Nothing is written under the real campaign;
# the only fake run_context.py processes have their working directory in the test area, never the campaign
# directory (campaign.py:37 counts only processes whose cwd is the campaign). Outputs: build/es310/test-export-*.
# No Lean, no systemd unit, no signal to any process but the test's own sleepers.
#
# Cases: every refusal of design E1 and of the critiques (status capped / witness / error, replay not ok,
# truncated result, live process in any cwd, young files, gz EOF / CRC / missing, WITNESS files, source and
# catalog hashes, --out inside the campaign, mismatched tree / contexts / counts, a non-tree, a bad leaf,
# parameters, lock), the ALERT case (one gz byte changed after export: exit 2, old export byte-identical, then
# latched), determinism (two exports and a re-export byte-identical), per-context K (a leaf scaled by 16),
# --corrupt (exactly one Lean-test failure), merge (partial / subtree / complete refusals, tampered module,
# merge-side ALERT), a Python simulation of split_pm's literal-path requirement over the merged sub-Root
# (with a negative control), and a synthetic --complete merge (4,096 fake one-leaf modules, never compiled)
# that exercises all 12 Root levels, the root at [] := ex1000000001 and the complete-mode refusals.
# Fixer additions (6 Nov, after the soundness and operations reviews): a broken / missing tree gz is "not ready"
# only while result.json is <= 600 s old and refused after that (2b); a refusal of one context does not stop
# the others (2c, exit 1 at the end); a stale exporter exits 5 (3); a changed run_context.py / pbb_strong.py
# is a recorded warning, not an ALERT, in the exporter and the merge (5b).
set -u -o pipefail
D=$(cd "$(dirname "$0")" && pwd)
C=/home/jay/research/data/es8-b64-pilot-20261105
SRC=$(cd "$D/.." && pwd)/omission-cover-certificates-2026-10-10/balanced-v2-source.json
T=$D/build/es310
TF=$T/test-fake
PRISTINE=$TF/pristine
FAKE=$TF/camp
LOGD=$D/logs/es310
mkdir -p "$LOGD" "$TF"
exec > >(tee "$LOGD/test_export_es310.log") 2>&1
OLD='2026-11-05 12:00:00'
PASS=0; FAIL=0; FAILED=()
LIVEPIDS=()
cleanup() { for p in "${LIVEPIDS[@]:-}"; do [ -n "$p" ] && kill "$p" 2>/dev/null; done; }
trap cleanup EXIT
say() { echo "== $(date -u +%FT%TZ) $*"; }
ok() { PASS=$((PASS + 1)); echo "PASS  $*"; }
bad() { FAIL=$((FAIL + 1)); FAILED+=("$1"); echo "FAIL  $*"; }

guard() { case "$1" in "$T"/test-*) ;; *) echo "refusing to touch $1"; exit 99 ;; esac; }
reset_fake() {
  guard "$FAKE"; rm -rf "$FAKE"; mkdir -p "$FAKE/runs" "$FAKE/campaign"
  cp -p "$PRISTINE/contexts.jsonl" "$PRISTINE/run_context.py" "$FAKE/"
  cp -p "$PRISTINE"/runs/* "$FAKE/runs/"
}
fresh_out() { guard "$1"; rm -rf "$1"; }
nothing_written() {  # OUT absent, or holding only .export.lock
  [ ! -e "$1" ] || [ -z "$(find "$1" -mindepth 1 ! -name .export.lock -print -quit)" ]
}
X() { nice -n 10 python3 "$D/export_es310.py" --campaign "$FAKE" --source "$SRC" --per-word 8 --block-leaves 64 \
        --prefix E310BT "$@"; }
M() { nice -n 10 python3 "$D/merge_es310.py" "$@"; }
LAST=""
# run NAME WANT_EXIT NOTHING_DIR|- CMD...: the exit code must be WANT_EXIT; with a dir, nothing may be written there
run() {
  local name=$1 want=$2 chk=$3; shift 3
  LAST=$("$@" 2> "$TF/last.err"); local got=$?
  local why
  why=$(printf '%s' "$LAST" | python3 -c 'import json,sys
try:
  d=json.loads(sys.stdin.read().strip().splitlines()[-1])
  print({k: d[k] for k in ("refused","refused_ctx","alert","not_ready","not_closed","skipped_same","stale_exporter","code_changed") if d.get(k)})
except Exception as e: print("no summary", e)')
  if [ "$got" != "$want" ]; then bad "$name" "(exit $got, want $want) $why"; tail -3 "$TF/last.err"; return 1; fi
  if [ "$chk" != - ] && ! nothing_written "$chk"; then bad "$name" "(something was written in $chk)"; return 1; fi
  ok "$name (exit $got) $why"
}
jset() {  # FILE PYTHON: edit a JSON file (d), then give it an old mtime
  python3 - "$1" "$2" <<'EOF'
import json, sys
p = sys.argv[1]; d = json.load(open(p)); exec(sys.argv[2]); open(p, "w").write(json.dumps(d, indent=1))
EOF
  touch -d "$OLD" "$1"
}
tset() {  # GZ PYTHON: edit a tree (t), rewrite the gz, then give it an old mtime
  python3 - "$1" "$2" <<'EOF'
import gzip, json, sys
p = sys.argv[1]; t = json.loads(gzip.decompress(open(p, "rb").read())); exec(sys.argv[2])
open(p, "wb").write(gzip.compress(json.dumps(t, separators=(",", ":")).encode(), mtime=0))
EOF
  touch -d "$OLD" "$1"
}
flipbyte() {  # FILE OFFSET: xor one byte, keep the mtime
  python3 - "$1" "$2" <<'EOF'
import os, sys
p, off = sys.argv[1], int(sys.argv[2]); st = os.stat(p)
b = bytearray(open(p, "rb").read()); b[off] ^= 0x5A; open(p, "wb").write(bytes(b))
os.utime(p, ns=(st.st_atime_ns, st.st_mtime_ns))
EOF
}
snap() { (cd "$1" && find . -type f ! -name .export.lock ! -name 'ALERT-*' -print0 | sort -z | xargs -0 sha256sum); }

say "setup: pristine copies of the campaign's contexts.jsonl, run_context.py and ctx 2406/2407 files (read only)"
guard "$PRISTINE"; rm -rf "$PRISTINE"; mkdir -p "$PRISTINE/runs"
cp -p "$C/contexts.jsonl" "$C/run_context.py" "$PRISTINE/"
cp -p "$C"/runs/ctx-2406-b64.json.gz "$C"/runs/ctx-2406-b64.result.json \
      "$C"/runs/ctx-2407-b64.json.gz "$C"/runs/ctx-2407-b64.result.json "$PRISTINE/runs/"
(cd "$PRISTINE" && sha256sum contexts.jsonl run_context.py runs/*)
echo "exporter sha256: $(sha256sum "$D/export_es310.py" | cut -c1-64); merge sha256: $(sha256sum "$D/merge_es310.py" | cut -c1-64)"
R=$T/test-export-refuse
mkdir -p "$R"

say "1. refusals (exit 1, nothing written)"
for st in capped witness error; do
  reset_fake; jset "$FAKE/runs/ctx-2406-b64.result.json" "d['status'] = '$st'"
  fresh_out "$R/status-$st"; run "status $st" 1 "$R/status-$st" X --out "$R/status-$st" --ctx 2406
done
reset_fake; jset "$FAKE/runs/ctx-2406-b64.result.json" "d['replay']['ok'] = False"
fresh_out "$R/replay-ok"; run "replay.ok false" 1 "$R/replay-ok" X --out "$R/replay-ok" --ctx 2406
reset_fake; jset "$FAKE/runs/ctx-2406-b64.result.json" "del d['replay']"
fresh_out "$R/replay-gone"; run "replay missing" 1 "$R/replay-gone" X --out "$R/replay-gone" --ctx 2406
reset_fake; jset "$FAKE/runs/ctx-2406-b64.result.json" "d['replay']['pending'] = 11"
fresh_out "$R/replay-pending"; run "replay.pending 11" 1 "$R/replay-pending" X --out "$R/replay-pending" --ctx 2406
reset_fake; jset "$FAKE/runs/ctx-2406-b64.result.json" "d['replay']['leaves_checked'] = 920"
fresh_out "$R/lchecked"; run "replay.leaves_checked != leaves" 1 "$R/lchecked" X --out "$R/lchecked" --ctx 2406
reset_fake; jset "$FAKE/runs/ctx-2406-b64.result.json" "d['pending'] = 1"
fresh_out "$R/pending"; run "pending 1" 1 "$R/pending" X --out "$R/pending" --ctx 2406
reset_fake; jset "$FAKE/runs/ctx-2406-b64.result.json" "d['budget'] = 63"
fresh_out "$R/budget"; run "result budget 63" 1 "$R/budget" X --out "$R/budget" --ctx 2406
reset_fake; jset "$FAKE/runs/ctx-2406-b64.result.json" "d['rules']['catalog_sha256'] = '0' * 64"
fresh_out "$R/rules"; run "rules.catalog_sha256 changed" 1 "$R/rules" X --out "$R/rules" --ctx 2406
reset_fake; cp "$SRC" "$TF/source-modified.json"; printf ' ' >> "$TF/source-modified.json"
fresh_out "$R/source"
run "source file with another sha256 (read_source)" 1 "$R/source" \
  nice -n 10 python3 "$D/export_es310.py" --campaign "$FAKE" --source "$TF/source-modified.json" --per-word 8 \
  --prefix E310BT --out "$R/source" --ctx 2406
[ ! -e "$R/source" ] && ok "source refusal created no OUT" || bad "source refusal created OUT"
reset_fake; echo '{}' > "$FAKE/runs/ctx-2406-b64.WITNESS.json"
fresh_out "$R/wit1"; run "WITNESS file of the context" 1 "$R/wit1" X --out "$R/wit1" --ctx 2406
reset_fake; echo '{}' > "$FAKE/runs/ctx-17-b64.WITNESS.json"
fresh_out "$R/wit2"; run "WITNESS file of another context (--all-closed)" 1 "$R/wit2" X --out "$R/wit2" --all-closed
reset_fake; echo 'alert' > "$FAKE/campaign/WITNESS-ALERT.txt"
fresh_out "$R/wit3"; run "campaign/WITNESS-ALERT.txt" 1 "$R/wit3" X --out "$R/wit3" --ctx 2406
reset_fake
run "--out inside the campaign" 1 "$FAKE/out" X --out "$FAKE/out" --ctx 2406
[ ! -e "$FAKE/out" ] && ok "--out inside the campaign: not created" || bad "--out inside the campaign was created"
guard "$T/test-export-link"; rm -f "$T/test-export-link"; ln -s "$FAKE/runs" "$T/test-export-link"
run "--out through a symlink into the campaign" 1 - X --out "$T/test-export-link/out" --ctx 2406
[ ! -e "$FAKE/runs/out" ] && ok "symlinked --out: not created" || bad "symlinked --out was created"
rm -f "$T/test-export-link"
if python3 - "$D" "$C" <<'EOF'
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import export_es310 as E
D, C = Path(sys.argv[1]), Path(sys.argv[2])
bad = [C / "x", C / "runs" / "y", D / "build" / "es311" / "full" / "z", D / "build" / "CompactChecker" / "q",
       D / "build" / "ext" / "q", D / "build" / "chain311" / "q", C.parent, D.parent.parent / ".lake" / "x"]
for o in bad:   # check_out only computes paths; it creates nothing
    try:
        E.check_out(o, D / "build" / "es310" / "test-fake" / "camp")
        print("NOT refused:", o); sys.exit(1)
    except E.Refuse as e:
        print("refused:", o)
E.check_out(D / "build" / "es310" / "test-export-ok", D / "build" / "es310" / "test-fake" / "camp")
print("accepted:", D / "build" / "es310" / "test-export-ok")
EOF
then ok "check_out refuses the real campaign, its parent and the 311 build dirs (function call only)"
else bad "check_out"; fi
reset_fake; cp -p "$FAKE/runs/ctx-2407-b64.json.gz" "$FAKE/runs/ctx-2406-b64.json.gz"
fresh_out "$R/ctxmix"; run "tree of ctx 2407 under the name of ctx 2406" 1 "$R/ctxmix" X --out "$R/ctxmix" --ctx 2406
reset_fake
python3 - "$FAKE/contexts.jsonl" <<'EOF'
import json, sys
p = sys.argv[1]; lines = open(p).read().split("\n")
for i, l in enumerate(lines):
    if l.startswith('{"ctx":2406,'):
        c = json.loads(l); c["path"][11][1] ^= 1; lines[i] = json.dumps(c, separators=(",", ":"))
open(p, "w").write("\n".join(lines))
EOF
touch -d "$OLD" "$FAKE/contexts.jsonl"
fresh_out "$R/ctxline"; run "contexts.jsonl: one decision of ctx 2406 flipped" 1 "$R/ctxline" X --out "$R/ctxline" --ctx 2406
reset_fake; jset "$FAKE/runs/ctx-2406-b64.result.json" "d['leaves'] = 920; d['replay']['leaves_checked'] = 920"
fresh_out "$R/count"; run "result leaf count differs from the tree" 1 "$R/count" X --out "$R/count" --ctx 2406
reset_fake; tset "$FAKE/runs/ctx-2406-b64.json.gz" "
i = next(j for j, nd in enumerate(t['nodes']) if nd['type'] == 'weighted'); t['nodes'][i] = {'type': 'pending'}"
fresh_out "$R/pend"; run "tree with a pending node" 1 "$R/pend" X --out "$R/pend" --ctx 2406
reset_fake; tset "$FAKE/runs/ctx-2406-b64.json.gz" "
i = next(j for j, nd in enumerate(t['nodes']) if nd['type'] == 'weighted'); t['nodes'][i]['weights'] = [[r, 0] for r, w in t['nodes'][i]['weights']]"
fresh_out "$R/margin"; run "tree with a leaf of margin < 1 (weights zeroed)" 1 "$R/margin" X --out "$R/margin" --ctx 2406
reset_fake; tset "$FAKE/runs/ctx-2406-b64.json.gz" "
b = [nd for nd in t['nodes'] if nd['type'] == 'branch']; b[5]['one'] = b[3]['zero']"
fresh_out "$R/dag"; run "tree with a node reached twice" 1 "$R/dag" X --out "$R/dag" --ctx 2406
reset_fake; tset "$FAKE/runs/ctx-2406-b64.json.gz" "
i = next(j for j, nd in enumerate(t['nodes']) if nd['type'] == 'weighted'); t['nodes'][i]['weights'][0][0] = -1"
fresh_out "$R/negrow"; run "tree with a negative row index" 1 "$R/negrow" X --out "$R/negrow" --ctx 2406
reset_fake; tset "$FAKE/runs/ctx-2406-b64.json.gz" "t['budget'] = 63"
fresh_out "$R/tbudget"; run "tree budget 63" 1 "$R/tbudget" X --out "$R/tbudget" --ctx 2406
reset_fake
fresh_out "$R/corrupt-default"
run "--corrupt with the default prefix E310B" 1 "$R/corrupt-default" \
  nice -n 10 python3 "$D/export_es310.py" --campaign "$FAKE" --source "$SRC" --per-word 8 --out "$R/corrupt-default" \
  --ctx 2406 --corrupt 1

say "2. not ready (exit 3 with --ctx, nothing written)"
reset_fake; rm "$FAKE/runs/ctx-2406-b64.result.json"
fresh_out "$R/nr-missing"; run "result missing" 3 "$R/nr-missing" X --out "$R/nr-missing" --ctx 2406
reset_fake; head -c 300 "$PRISTINE/runs/ctx-2406-b64.result.json" > "$FAKE/runs/ctx-2406-b64.result.json"
touch -d "$OLD" "$FAKE/runs/ctx-2406-b64.result.json"
fresh_out "$R/nr-trunc"; run "truncated result.json" 3 "$R/nr-trunc" X --out "$R/nr-trunc" --ctx 2406
reset_fake; touch "$FAKE/runs/ctx-2406-b64.result.json"
fresh_out "$R/nr-young"; run "result younger than 120 s" 3 "$R/nr-young" X --out "$R/nr-young" --ctx 2406
reset_fake; touch "$FAKE/runs/ctx-2406-b64.json.gz"
fresh_out "$R/nr-younggz"; run "tree gz younger than 120 s" 3 "$R/nr-younggz" X --out "$R/nr-younggz" --ctx 2406
RES300() { touch -d '300 seconds ago' "$FAKE/runs/ctx-2406-b64.result.json"; }  # older than 120 s, younger than 600 s
reset_fake; head -c 100000 "$PRISTINE/runs/ctx-2406-b64.json.gz" > "$FAKE/runs/ctx-2406-b64.json.gz"
touch -d "$OLD" "$FAKE/runs/ctx-2406-b64.json.gz"; RES300
fresh_out "$R/nr-gzeof"; run "truncated tree gz (EOFError), result.json 300 s old" 3 "$R/nr-gzeof" X --out "$R/nr-gzeof" --ctx 2406
reset_fake; flipbyte "$FAKE/runs/ctx-2406-b64.json.gz" 300000; RES300
fresh_out "$R/nr-gzcrc"; run "tree gz with one byte changed (CRC / inflate / JSON error), result.json 300 s old" 3 "$R/nr-gzcrc" \
  X --out "$R/nr-gzcrc" --ctx 2406
reset_fake; rm "$FAKE/runs/ctx-2406-b64.json.gz"; RES300
fresh_out "$R/nr-gzgone"; run "tree gz missing, result.json 300 s old" 3 "$R/nr-gzgone" X --out "$R/nr-gzgone" --ctx 2406
say "2b. the same tree-file faults behind a result.json older than 600 s: damage, refused (exit 1, nothing written)"
reset_fake; head -c 100000 "$PRISTINE/runs/ctx-2406-b64.json.gz" > "$FAKE/runs/ctx-2406-b64.json.gz"
touch -d "$OLD" "$FAKE/runs/ctx-2406-b64.json.gz"
fresh_out "$R/dmg-gzeof"; run "truncated tree gz, result.json old: refused" 1 "$R/dmg-gzeof" X --out "$R/dmg-gzeof" --ctx 2406
printf '%s' "$LAST" | grep -q 'the tree file is damaged' && ok "  ... the refusal says the tree file is damaged" || bad "damage message"
reset_fake; flipbyte "$FAKE/runs/ctx-2406-b64.json.gz" 300000
fresh_out "$R/dmg-gzcrc"; run "tree gz with one byte changed, result.json old: refused" 1 "$R/dmg-gzcrc" X --out "$R/dmg-gzcrc" --ctx 2406
reset_fake; rm "$FAKE/runs/ctx-2406-b64.json.gz"
fresh_out "$R/dmg-gzgone"; run "tree gz missing, result.json old: refused" 1 "$R/dmg-gzgone" X --out "$R/dmg-gzgone" --ctx 2406
say "2c. one refused context does not stop the others"
reset_fake; jset "$FAKE/runs/ctx-2406-b64.result.json" "d['replay']['ok'] = False"
fresh_out "$R/perctx"; run "--ctx 2406,2407 with ctx 2406 refused (replay.ok false): exit 1" 1 - X --out "$R/perctx" --ctx 2406,2407
[ -f "$R/perctx/ctx/ctx-2407.json" ] && [ ! -e "$R/perctx/ctx/ctx-2406.json" ] && [ -z "$(ls "$R/perctx/src/E310BT" | grep '^C2406')" ] \
  && ok "  ... ctx 2407 exported, nothing of ctx 2406 written" || bad "per-context refusal: manifests"
printf '%s' "$LAST" | grep -q '"refused_ctx": {"2406": ' && printf '%s' "$LAST" | grep -q '"refused": null' \
  && ok "  ... summary: refused_ctx {2406: ...}, refused null" || bad "per-context refusal: summary"
reset_fake; flipbyte "$FAKE/runs/ctx-2407-b64.json.gz" 300000
fresh_out "$R/perctx2"; run "--all-closed with ctx 2407's tree damaged: exit 1" 1 - X --out "$R/perctx2" --all-closed
[ -f "$R/perctx2/ctx/ctx-2406.json" ] && [ ! -e "$R/perctx2/ctx/ctx-2407.json" ] \
  && ok "  ... ctx 2406 exported, ctx 2407 refused" || bad "per-context refusal (--all-closed): manifests"
fresh_out "$R/perctx"; fresh_out "$R/perctx2"
reset_fake
(cd "$FAKE" && exec python3 -c 'import time; time.sleep(60)' run_context.py --budget 64 --ctx 2406) &
LP=$!; LIVEPIDS+=("$LP"); sleep 0.5
fresh_out "$R/nr-live1"; run "live run_context.py --budget 64 --ctx 2406 (cwd = fake campaign)" 3 "$R/nr-live1" \
  X --out "$R/nr-live1" --ctx 2406
kill "$LP"; wait "$LP" 2>/dev/null
(cd "$T" && exec python3 -c 'import time; time.sleep(60)' /elsewhere/run_context.py --budget=64 --ctx=2406) &
LP=$!; LIVEPIDS+=("$LP"); sleep 0.5
fresh_out "$R/nr-live2"; run "live run_context.py --budget=64 --ctx=2406 (cwd = build/es310, another path)" 3 \
  "$R/nr-live2" X --out "$R/nr-live2" --ctx 2406
kill "$LP"; wait "$LP" 2>/dev/null
(cd "$T" && exec python3 -c 'import time; time.sleep(60)' run_context.py --budget 63 --ctx 2406) &
LP=$!; LIVEPIDS+=("$LP"); sleep 0.5
fresh_out "$R/live63"; run "a live budget-63 run of ctx 2406 does not block (exported)" 0 - X --out "$R/live63" --ctx 2406
kill "$LP"; wait "$LP" 2>/dev/null
reset_fake; touch "$FAKE/runs/ctx-2407-b64.result.json"
fresh_out "$R/allc-young"; run "--all-closed: ctx 2407 young, ctx 2406 exported" 0 - X --out "$R/allc-young" --all-closed
[ -f "$R/allc-young/ctx/ctx-2406.json" ] && [ ! -e "$R/allc-young/ctx/ctx-2407.json" ] \
  && ok "--all-closed young: only ctx 2406 has a manifest" || bad "--all-closed young: manifests"
reset_fake; jset "$FAKE/runs/ctx-2407-b64.result.json" "d['status'] = 'capped'"
fresh_out "$R/allc-capped"; run "--all-closed: ctx 2407 capped is skipped as not closed" 0 - X --out "$R/allc-capped" --all-closed
[ -f "$R/allc-capped/ctx/ctx-2406.json" ] && [ ! -e "$R/allc-capped/ctx/ctx-2407.json" ] \
  && ok "--all-closed capped: only ctx 2406 has a manifest" || bad "--all-closed capped: manifests"
reset_fake; jset "$FAKE/runs/ctx-2407-b64.result.json" "d['status'] = 'witness'"
fresh_out "$R/allc-wit"; run "--all-closed: a result with status witness refuses the run" 1 "$R/allc-wit" \
  X --out "$R/allc-wit" --all-closed

say "3. determinism (chunk limit 500: several subtree roots and an internal skeleton in both contexts)"
reset_fake
A=$T/test-export-detA; B=$T/test-export-detB
fresh_out "$A"; fresh_out "$B"
run "export 2406,2407 into detA" 0 - X --out "$A" --ctx 2406,2407 --chunk-leaves 500
run "export 2406,2407 into detB" 0 - X --out "$B" --ctx 2406,2407 --chunk-leaves 500
diff -r --exclude=.export.lock "$A" "$B" > "$TF/det.diff" && ok "detA and detB byte-identical ($(find "$A/src" -name '*.lean' | wc -l) modules, 2 manifests)" \
  || bad "detA and detB differ (see $TF/det.diff)"
snap "$A" > "$TF/detA.before"
run "re-export into detA: both skipped as same" 0 - X --out "$A" --ctx 2406,2407 --chunk-leaves 500
printf '%s' "$LAST" | grep -q '"skipped_same": \[2406, 2407\]' && ok "skipped_same [2406, 2407]" || bad "skipped_same"
snap "$A" | diff - "$TF/detA.before" > /dev/null && ok "detA unchanged by the skip run" || bad "detA changed by the skip run"
rm "$A/ctx/ctx-2407.json"
run "re-export of ctx 2407 after its manifest was removed" 0 - X --out "$A" --all-closed --chunk-leaves 500
snap "$A" | diff - "$TF/detA.before" > /dev/null && ok "re-export byte-identical (modules and manifest)" || bad "re-export differs"
run "per-word 4 into an OUT exported at 8" 1 - nice -n 10 python3 "$D/export_es310.py" --campaign "$FAKE" --source "$SRC" \
  --per-word 4 --prefix E310BT --out "$A" --ctx 2406 --chunk-leaves 500
run "another prefix into the same OUT" 1 - nice -n 10 python3 "$D/export_es310.py" --campaign "$FAKE" --source "$SRC" \
  --per-word 8 --prefix E310BK --out "$A" --ctx 2406 --chunk-leaves 500
python3 - "$A/ctx/ctx-2406.json" <<'EOF'
import json, sys
p = sys.argv[1]; d = json.load(open(p)); d["exporter_sha256"]["export_es310"] = "0" * 64
open(p, "w").write(json.dumps(d, indent=1) + "\n")
EOF
run "a context by another exporter sha256 is reported (exit 5)" 5 - X --out "$A" --ctx 2406,2407 --chunk-leaves 500
printf '%s' "$LAST" | grep -q '"stale_exporter": \[2406\]' && ok "stale_exporter [2406]" || bad "stale_exporter"
run "--refresh-exporter re-exports it" 0 - X --out "$A" --ctx 2406,2407 --chunk-leaves 500 --refresh-exporter
snap "$A" | diff - "$TF/detA.before" > /dev/null && ok "refreshed export byte-identical to the original" || bad "refresh differs"
flock -n "$A/.export.lock" sleep 6 &
FP=$!; sleep 0.5
run "exporter while the lock is held" 4 - X --out "$A" --ctx 2406 --chunk-leaves 500
run "merge while the lock is held" 4 - M "$A" --prefix E310BT --partial
wait "$FP"

say "4. merge"
run "merge --complete with 2 of 4096 contexts" 1 - M "$A" --prefix E310BT --complete
run "merge --partial" 0 - M "$A" --prefix E310BT --partial
python3 - "$A/manifest-E310BT.json" <<'EOF' && ok "partial manifest: 311 schema keys, complete false, root null, 8 modules, 2702 leaves" || bad "partial manifest"
import json, sys
m = json.load(open(sys.argv[1]))
need = ["side", "prefix", "catalog", "rows", "states", "budget", "catalog_base", "complete", "total_leaves",
        "export_root", "base_path", "root", "modules"]
assert all(k in m for k in need), [k for k in need if k not in m]
assert m["complete"] is False and m["root"] is None and m["budget"] == 64 and m["catalog_base"] == 4194304
assert m["catalog"] == "CompactChecker.Fcat62" and m["rows"] == 3131 and m["states"] == 252 and m["side"] == "balanced"
assert len(m["modules"]) == 8 and m["total_leaves"] == 2702
for mm in m["modules"]:
    assert all(k in mm for k in ("module", "file", "sha256", "leaves", "subtree_roots", "corrupted"))
EOF
run "merge --subtree 11:1203" 0 - M "$A" --prefix E310BT --subtree 11:1203
run "merge --subtree 11:1203 (detB)" 0 - M "$B" --prefix E310BT --subtree 11:1203
cmp -s "$A/src/E310BT/Root.lean" "$B/src/E310BT/Root.lean" && cmp -s "$A/manifest-E310BT.json" "$B/manifest-E310BT.json" \
  && ok "sub-Root and manifest of detA and detB byte-identical" || bad "sub-Root or manifest differ between detA and detB"
SH=$(python3 "$D/shapes_es311.py" "$A"); echo "$SH" | grep -q '"PASS": true' && ok "shapes_es311.py on detA: PASS" \
  || { bad "shapes_es311.py on detA"; echo "$SH" | head -30; }
python3 - "$A/manifest-E310BT.json" <<'EOF' && ok "subtree manifest: complete, export_root 1000003251, base path of the depth-11 node" || bad "subtree manifest"
import json, sys
m = json.load(open(sys.argv[1]))
assert m["complete"] is True and m["export_root"] == 1000000000 + 2048 + 1203 and m["root"]["module"] == "E310BT.Root"
assert m["base_path"] == [[87, 1], [71, 1], [19, 2], [70, 2], [84, 1], [166, 1], [181, 2], [232, 1], [41, 2], [38, 2], [214, 1]]
EOF
cat > "$TF/simulate.py" <<'EOF'
"""Python simulation of what Lean requires of the literal paths (written for this test; imports nothing from the
exporter): every split_pm proof cites children stated at exactly (v, 2) :: P and (v, 1) :: P, where P is the
path of its own statement (Path.lean:51-56); every checkF2_feas cites a chk at its own path; every reference
is to a theorem defined earlier (module files in manifest order, then the Root); the root is at the expected
path; every subtree root of the manifest is cited exactly once."""
import json, re, sys
from pathlib import Path
out, prefix, want_root = Path(sys.argv[1]), sys.argv[2], json.loads(sys.argv[3])
man = json.load(open(out / f"manifest-{prefix}.json"))
files = [(mm["module"], out / mm["file"]) for mm in man["modules"]] + [(prefix, out / man["root"]["file"])]
PAIR = re.compile(r"\((\d+), (\d+)\)")
THM = re.compile(r"^theorem (ex\d+|chk\d+|root) : .*?\(pmask \(zerosF 252\) (\[[^\]]*\])\)")
SPLIT = re.compile(r"^  split_pm fcat62 3131 252 64 \(zerosF 252\) (\[[^\]]*\]) (\d+) (\S+) (\S+)$")
FEAS = re.compile(r"^  checkF2_feas fcat62 3131 252 64 4194304 \d+ \d+ \d+ \d+ fcat62_wf b(\d+) _ chk(\d+)$")
stmt, errs, cites = {}, [], {}
P = lambda s: [[int(a), int(b)] for a, b in PAIR.findall(s)]
def res(ns, r):
    return r if "." in r else f"{ns}.{r}"
for ns, f in files:
    L = f.read_text().split("\n")
    for i, ln in enumerate(L):
        m = THM.match(ln)
        if not m:
            continue
        name, path = m.group(1), P(m.group(2))
        full = f"{ns}.{name}"
        if full in stmt:
            errs.append(f"{full} defined twice")
        if name == "root":
            r = res(ns, ln.rsplit(":= ", 1)[1])
            cites[r] = cites.get(r, 0) + 1
            if stmt.get(r) != path or path != want_root:
                errs.append(f"root: path {path}, cites {r} at {stmt.get(r)}, want {want_root}")
        elif name.startswith("ex"):
            s, fz = SPLIT.match(L[i + 1]), FEAS.match(L[i + 1])
            if s:
                p0, v, a, b = P(s.group(1)), int(s.group(2)), res(ns, s.group(3)), res(ns, s.group(4))
                for c in (a, b):
                    cites[c] = cites.get(c, 0) + 1
                if p0 != path or stmt.get(a) != [[v, 2]] + path or stmt.get(b) != [[v, 1]] + path:
                    errs.append(f"{full}: split_pm at {p0} (statement {path}) v {v}: {a} at {stmt.get(a)}, {b} at {stmt.get(b)}")
            elif fz:
                if stmt.get(f"{ns}.chk{fz.group(2)}") != path or not (fz.group(1) == fz.group(2) == name[2:]):
                    errs.append(f"{full}: chk path differs")
            else:
                errs.append(f"{full}: unknown proof line")
        stmt[full] = path
for mm in man["modules"]:
    for s, _ in mm["subtree_roots"]:
        if cites.get(f"{mm['module']}.ex{s}") != 1:
            errs.append(f"{mm['module']}.ex{s} cited {cites.get(mm['module'] + '.ex' + str(s), 0)} times")
print(json.dumps({"theorems": len(stmt), "errors": errs[:5], "n_errors": len(errs)}))
sys.exit(1 if errs else 0)
EOF
ROOTP='[[87, 1], [71, 1], [19, 2], [70, 2], [84, 1], [166, 1], [181, 2], [232, 1], [41, 2], [38, 2], [214, 1]]'
python3 "$TF/simulate.py" "$A" E310BT "$ROOTP" && ok "split_pm literal-path simulation over detA's modules and sub-Root" \
  || bad "split_pm simulation on detA"
NEG=$T/test-export-simneg; fresh_out "$NEG"; mkdir -p "$NEG"; cp -r "$A/src" "$A/manifest-E310BT.json" "$NEG/"
sed -i '/^theorem ex240800000 /,+1 s/(144, 1)/(144, 2)/' "$NEG/src/E310BT/Root.lean"
python3 "$TF/simulate.py" "$NEG" E310BT "$ROOTP" && bad "negative control: the simulation accepted a flipped decision" \
  || ok "negative control: one decision of ctx 2407's base path flipped in the sub-Root is caught"
fresh_out "$NEG"
run "merge --subtree 12:2406 (one context)" 0 - M "$A" --prefix E310BT --subtree 12:2406
python3 "$TF/simulate.py" "$A" E310BT "$(python3 -c "
import json; print(json.dumps([[144, 2]] + json.loads('$ROOTP')))")" && ok "split_pm simulation, single-context sub-Root" \
  || bad "split_pm simulation, single-context sub-Root"
rm "$A/ctx/ctx-2407.json"
run "merge --subtree 11:1203 with ctx 2407 missing" 1 - M "$A" --prefix E310BT --subtree 11:1203
run "merge --subtree 0:0 (use --complete)" 1 - M "$A" --prefix E310BT --subtree 0:0
run "re-export ctx 2407" 0 - X --out "$A" --ctx 2407 --chunk-leaves 500
cp -p "$A/src/E310BT/C240702.lean" "$TF/C240702.keep"; echo "-- tampered" >> "$A/src/E310BT/C240702.lean"
run "merge with a tampered module source" 1 - M "$A" --prefix E310BT --subtree 11:1203
cp -p "$TF/C240702.keep" "$A/src/E310BT/C240702.lean"
run "merge after restoring it" 0 - M "$A" --prefix E310BT --subtree 11:1203
snap "$A" > "$TF/detA.merged"
flipbyte "$FAKE/runs/ctx-2407-b64.json.gz" 1000
run "merge after one byte of ctx 2407's gz changed: ALERT" 2 - M "$A" --prefix E310BT --subtree 11:1203
[ -f "$A/ALERT-changed-inputs.txt" ] && ok "merge wrote ALERT-changed-inputs.txt" || bad "merge wrote no ALERT file"
snap "$A" | diff - "$TF/detA.merged" > /dev/null && ok "merge ALERT: nothing else changed" || bad "merge ALERT changed files"
rm "$A/ALERT-changed-inputs.txt"; reset_fake

say "5. ALERT: inputs of an exported context changed"
AL=$T/test-export-alert; fresh_out "$AL"
run "export ctx 2406" 0 - X --out "$AL" --ctx 2406
snap "$AL" > "$TF/alert.before"
flipbyte "$FAKE/runs/ctx-2406-b64.json.gz" 1000
run "one byte of the gz changed (mtime kept): ALERT" 2 - X --out "$AL" --ctx 2406
[ -f "$AL/ALERT-changed-inputs.txt" ] && ok "ALERT-changed-inputs.txt written: $(sed -n 2p "$AL/ALERT-changed-inputs.txt" | cut -c1-120)" \
  || bad "no ALERT file"
snap "$AL" | diff - "$TF/alert.before" > /dev/null && ok "old export byte-identical after the ALERT" || bad "old export changed"
reset_fake
run "ALERT latch: exit 2 while the ALERT file exists, even with the inputs restored" 2 - X --out "$AL" --all-closed
run "merge refuses while the ALERT file exists" 2 - M "$AL" --prefix E310BT --partial
rm "$AL/ALERT-changed-inputs.txt"
run "after the ALERT file is removed: skipped as same" 0 - X --out "$AL" --all-closed
printf '%s' "$LAST" | grep -q '"skipped_same": \[2406\]' && ok "skipped_same [2406], ctx 2407 exported" || bad "skip after ALERT"
jset "$FAKE/runs/ctx-2406-b64.result.json" "d['host'] = 'elsewhere'"
run "result.json of an exported context changed: ALERT" 2 - X --out "$AL" --all-closed
rm -f "$AL/ALERT-changed-inputs.txt"; reset_fake
cp "$FAKE/contexts.jsonl" "$TF/ctx.keep"; printf '\n' >> "$FAKE/contexts.jsonl"; touch -d "$OLD" "$FAKE/contexts.jsonl"
run "contexts.jsonl changed (one blank line added): ALERT" 2 - X --out "$AL" --all-closed
rm -f "$AL/ALERT-changed-inputs.txt"; reset_fake

say "5b. campaign code changed after the export: a recorded warning, not an ALERT"
snap "$AL" > "$TF/code.before"
echo "# edited by test_export_es310.sh (fake campaign)" >> "$FAKE/run_context.py"
run "run_context.py changed: exit 0, no ALERT" 0 - X --out "$AL" --all-closed
[ ! -e "$AL/ALERT-changed-inputs.txt" ] && printf '%s' "$LAST" | grep -q '"code_changed": \["run_context differs from the one recorded' \
  && ok "  ... code_changed warning recorded, no ALERT file" || bad "code change: $(printf '%s' "$LAST" | cut -c1-300)"
snap "$AL" | diff - "$TF/code.before" > /dev/null && ok "  ... the export is unchanged (both contexts skipped as same)" || bad "code change rewrote the export"
run "merge --partial with the changed run_context.py: exit 0" 0 - M "$AL" --prefix E310BT --partial
printf '%s' "$LAST" | grep -q '"code_changed": \["run_context: recorded' && ok "  ... merge records the code_changed warning" \
  || bad "merge code_changed: $(printf '%s' "$LAST" | cut -c1-300)"
rm "$AL/ctx/ctx-2407.json"
run "re-export of ctx 2407 with the new run_context.py: exit 0" 0 - X --out "$AL" --all-closed
run "merge --subtree 11:1203 over two run_context.py sha256s: exit 0" 0 - M "$AL" --prefix E310BT --subtree 11:1203
python3 -c 'import json,sys; m=json.load(open(sys.argv[1])); s=m["inputs"]["run_context"]["sha256"]; assert isinstance(s, list) and len(s) == 2, s; assert m["code_changed"], m["code_changed"]' \
  "$AL/manifest-E310BT.json" && ok "  ... merged manifest records both run_context.py sha256s and the warning" || bad "merged manifest code record"
reset_fake

say "6. per-context K: one leaf of ctx 2406 with capacity and weights scaled by 16 (margin scales too)"
reset_fake; tset "$FAKE/runs/ctx-2406-b64.json.gz" "
W = [nd for nd in t['nodes'] if nd['type'] == 'weighted']
x = max(W, key=lambda nd: max(w for r, w in nd['weights']))
x['capacity'] *= 16; x['weights'] = [[r, 16 * w] for r, w in x['weights']]"
KO=$T/test-export-K; fresh_out "$KO"
run "export of the scaled tree" 0 - X --out "$KO" --ctx 2406
python3 - "$KO/ctx/ctx-2406.json" <<'EOF' && ok "per-context K = least power of 2 above the largest weight (>= 2^20), J = K << 12, no Lean-test failure" || bad "per-context K"
import json, sys
m = json.load(open(sys.argv[1]))
K, J, w = m["params"]["K"], m["params"]["J"], m["stats"]["max_weight"]
print("K", K, "J", J, "max_weight", w)
assert K == 1 << max(17, w.bit_length()) and K >= 1 << 20 and w < K and J == K << 12
assert m["stats"]["lean_test_failures"] == 0
EOF
SH=$(python3 - "$KO" <<'EOF'
import json, sys
from pathlib import Path
sys.path.insert(0, "/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-compact-checker-2026-11-05")
import shapes_es311
out = Path(sys.argv[1]); m = json.load(open(out / "ctx/ctx-2406.json"))
sp = shapes_es311.side_params({"catalog": "CompactChecker.Fcat62", "rows": 3131, "states": 252, "budget": 64,
                               "catalog_base": 4194304, "prefix": "E310BT"})
errs = [e for mm in m["modules"] for e in shapes_es311.check_text((out / mm["file"]).read_text(), "chunk", mm["module"], sp)]
print("shape errors", errs)
EOF
); echo "$SH" | grep -q 'shape errors \[\]' && ok "scaled-K module passes the line-shape check" || bad "scaled-K shapes: $SH"
fresh_out "$KO"; reset_fake

say "7. --corrupt (Python side of the rejection test E2)"
XO=$T/test-export-corrupt; fresh_out "$XO"
run "--corrupt 1 --ctx 2406 --prefix E310BX" 0 - nice -n 10 python3 "$D/export_es310.py" --campaign "$FAKE" --source "$SRC" \
  --per-word 8 --prefix E310BX --out "$XO" --ctx 2406 --chunk-leaves 500 --corrupt 1
python3 - "$XO" "$A" <<'EOF' && ok "exactly one Lean-test failure, at the corrupted leaf of module 1; modules 2 and 3 equal detA's (prefix aside); module 1 differs in one block def" || bad "--corrupt"
import json, sys
from pathlib import Path
xo, ao = Path(sys.argv[1]), Path(sys.argv[2])
x, a = json.load(open(xo / "ctx/ctx-2406.json")), json.load(open(ao / "ctx/ctx-2406.json"))
c = x["corruption"]; print("corruption", c)
assert x["stats"]["lean_test_failures"] == 1 and c["module"] == "E310BX.C240601" and c["new_margin"] <= 0
assert [mm["corrupted"] for mm in x["modules"]] == [True, False, False]
assert [mm["subtree_roots"] for mm in x["modules"]] == [mm["subtree_roots"] for mm in a["modules"]]
tx = [(xo / mm["file"]).read_text().replace("E310BX", "E310BT") for mm in x["modules"]]
ta = [(ao / mm["file"]).read_text() for mm in a["modules"]]
assert tx[1:] == ta[1:] and tx[0] != ta[0]
dl = [i for i, (l1, l2) in enumerate(zip(tx[0].split("\n"), ta[0].split("\n"))) if l1 != l2]
print("module 1: differing lines", dl, "(the def of the block holding the corrupted leaf)")
assert len(dl) == 1 and tx[0].split("\n")[dl[0]].startswith("noncomputable def b")
EOF
run "--corrupt into an OUT that already holds the context" 1 - nice -n 10 python3 "$D/export_es310.py" --campaign "$FAKE" \
  --source "$SRC" --per-word 8 --prefix E310BX --out "$XO" --ctx 2406 --chunk-leaves 500 --corrupt 1
X2=$T/test-export-corrupt9; fresh_out "$X2"
run "--corrupt 9 (no such module)" 1 "$X2" nice -n 10 python3 "$D/export_es310.py" --campaign "$FAKE" --source "$SRC" \
  --per-word 8 --prefix E310BX --out "$X2" --ctx 2406 --chunk-leaves 500 --corrupt 9
run "merge --subtree 12:2406 of the corrupted export (flagged)" 0 - M "$XO" --prefix E310BX --subtree 12:2406
grep -q '"corrupted": true' "$XO/manifest-E310BX.json" && ok "merged manifest flags the corrupted module" || bad "corrupted flag"
fresh_out "$X2"

say "8. synthetic --complete merge: 4,096 fake one-leaf modules (never compiled; shape-valid), three contexts with an internal skeleton"
reset_fake; printf 'x' > "$FAKE/runs/syn-dummy"; touch -d "$OLD" "$FAKE/runs/syn-dummy"
SY=$T/test-export-syncomplete; fresh_out "$SY"
python3 - "$SY" "$FAKE" "$SRC" <<'PYEOF' && ok "wrote 4,096 synthetic context manifests and modules (prefix E310BK)" || bad "synthetic setup"
import hashlib, json, os, sys
from pathlib import Path
out, fake, src = Path(sys.argv[1]), Path(os.path.realpath(sys.argv[2])), sys.argv[3]
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    st = os.stat(p); return {"path": str(p), "size": st.st_size, "mtime_ns": st.st_mtime_ns, "sha256": sha(p)}
pbb = "/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-final311-2026-10-14/search/pbb_strong.py"
glob_in = {"contexts_jsonl": {"path": str(fake / "contexts.jsonl"), "sha256": sha(fake / "contexts.jsonl")},
           "source": {"path": src, "sha256": sha(src)},
           "run_context": {"path": str(fake / "run_context.py"), "sha256": sha(fake / "run_context.py")},
           "pbb_strong": {"path": pbb, "sha256": sha(pbb)}}
dummy = rec(fake / "runs" / "syn-dummy")
(out / "ctx").mkdir(parents=True); (out / "src" / "E310BK").mkdir(parents=True)
lp = lambda p: "[" + ", ".join(f"({v}, {x})" for v, x in p) + "]"
F = "fcat62 3131 252 64"
def block(j, p):
    return [f"noncomputable def b{j} : PTree := .overBudget",
            f"theorem chk{j} : checkF2 {F} 2 131072 536870912 8 b{j} (pmask (zerosF 252) {lp(p)}) = true := by decide +kernel",
            f"theorem ex{j} : ¬ ∃ holes : Fin 252 → ℕ, FFeas {F} (pmask (zerosF 252) {lp(p)}) holes :=",
            f"  checkF2_feas {F} 4194304 2 131072 536870912 8 fcat62_wf b{j} _ chk{j}"]
for line in open(fake / "contexts.jsonl"):
    c = json.loads(line); k = c["ctx"]
    base = [(v, 2 if b == 0 else 1) for v, b in reversed(c["path"])]
    name = f"E310BK.C{k:04d}01"
    L = ["import CompactChecker.Fcat62", "import CompactChecker.Path", "open CompactChecker",
         "set_option maxRecDepth 100000", "set_option Elab.async false", "set_option linter.all false",
         f"namespace {name}", "-- synthetic module for a merge test (never compiled)"]
    if k in (0, 2406, 4095):
        v = min(set(range(252)) - {x for x, _ in base})
        L += block(1, [(v, 2)] + base) + block(2, [(v, 1)] + base) + ["#print axioms ex1", "#print axioms ex2"]
        srs, skel = [[1, 1], [2, 1]], [{"u": 0, "vertex": v, "zero": 1, "one": 2}]
    else:
        L += block(0, base) + ["#print axioms ex0"]
        srs, skel = [[0, 1]], []
    L.append(f"end {name}")
    data = ("\n".join(L) + "\n").encode()
    f = out / "src" / "E310BK" / f"C{k:04d}01.lean"; f.write_bytes(data)
    nl = sum(c2 for _, c2 in srs)
    man = {"ctx": k, "prefix": "E310BK", "campaign": str(fake),
           "params": {"budget": 64, "K": 131072, "J": 536870912, "per_word": 8, "chunk_leaves": 12000,
                      "block_leaves": 64, "catalog_base": 4194304, "catalog": "CompactChecker.Fcat62",
                      "rows": 3131, "states": 252, "profile": False},
           "ctx_path": c["path"], "base_path": [list(x) for x in base],
           "inputs": {"result": dummy, "tree_gz": dummy, "tree_json_sha256": "", **glob_in},
           "exporter_sha256": {"export_es310": "synthetic", "export_es311": "synthetic"},
           "modules": [{"module": name, "file": f"src/E310BK/C{k:04d}01.lean", "sha256": hashlib.sha256(data).hexdigest(),
                        "leaves": nl, "subtree_roots": srs, "blocks": len(srs), "entries": 0, "words": 0,
                        "min_margin": None, "max_base": 2, "corrupted": False}],
           "subtree_roots": srs, "skeleton": skel,
           "stats": {"leaves": nl, "nodes": 2 * nl - 1, "over_budget": nl, "min_margin": None},
           "result": {"leaves": nl, "nodes": 2 * nl - 1}, "corruption": None}
    (out / "ctx" / f"ctx-{k:04d}.json").write_text(json.dumps(man) + "\n")
PYEOF
run "merge --complete of the synthetic export" 0 - M "$SY" --prefix E310BK --complete --no-profile
python3 - "$SY" <<'PYEOF' && ok "complete manifest: export_root 0, base_path [], 4,099 leaves, 4,095 + 3 skeleton theorems, root := ex1000000001 at []" || bad "synthetic complete manifest / Root"
import json, sys
from pathlib import Path
out = Path(sys.argv[1]); m = json.load(open(out / "manifest-E310BK.json"))
assert m["complete"] is True and m["export_root"] == 0 and m["base_path"] == [] and m["total_leaves"] == 4099
assert m["skeleton_theorems"] == 4098 and len(m["modules"]) == 4096 and m["root"]["module"] == "E310BK.Root"
R = (out / m["root"]["file"]).read_text().split("\n")
want = "theorem root : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcat62 3131 252 64 (pmask (zerosF 252) []) holes := ex1000000001"
assert R.count(want) == 1, [l for l in R if l.startswith("theorem root")]
import re
top = [l for l in R if re.match(r"theorem ex1\d{9} : ", l)]          # 10^9 + 2^d + p (10 digits)
inner = [l for l in R if re.match(r"theorem ex\d{6,9} : ", l)]       # (k+1)*100000 + u
assert len(top) == 4095 and len(inner) == 3 and sum(l.startswith("import E310BK.C") for l in R) == 4096
assert sorted(int(re.match(r"theorem ex(\d+)", l).group(1)) for l in top) == [10**9 + (1 << d) + p for d in range(12) for p in range(1 << d)]
assert sorted(int(re.match(r"theorem ex(\d+)", l).group(1)) for l in inner) == [100000, 240700000, 409600000]
assert "  split_pm fcat62 3131 252 64 (zerosF 252) [] 214 ex1000000002 ex1000000003" in R
print("Root lines", len(R), "first top theorem:", top[0][:60], "... last:", top[-1][:40])
PYEOF
SH=$(python3 "$D/shapes_es311.py" "$SY"); echo "$SH" | grep -q '"PASS": true' && ok "shapes_es311.py on the synthetic complete export: PASS (4,096 modules and the Root)" \
  || { bad "shapes_es311.py on the synthetic export"; echo "$SH" | head -20; }
python3 "$TF/simulate.py" "$SY" E310BK '[]' && ok "split_pm literal-path simulation over all 12 levels of the complete Root" \
  || bad "split_pm simulation, complete Root"
mv "$SY/ctx/ctx-1234.json" "$TF/ctx-1234.keep"
run "merge --complete with one context missing" 1 - M "$SY" --prefix E310BK --complete --no-profile
mv "$TF/ctx-1234.keep" "$SY/ctx/ctx-1234.json"
cp "$SY/ctx/ctx-0777.json" "$TF/ctx-0777.keep"
jset "$SY/ctx/ctx-0777.json" "d['modules'][0]['corrupted'] = True"
run "merge --complete with a corrupted module" 1 - M "$SY" --prefix E310BK --complete --no-profile
cp "$TF/ctx-0777.keep" "$SY/ctx/ctx-0777.json"
jset "$SY/ctx/ctx-0777.json" "d['exporter_sha256']['export_es310'] = 'other'"
run "merge --complete with two exporter sha256s" 1 - M "$SY" --prefix E310BK --complete --no-profile
cp "$TF/ctx-0777.keep" "$SY/ctx/ctx-0777.json"
jset "$SY/ctx/ctx-0777.json" "d['base_path'][0][1] = 3 - d['base_path'][0][1]"
run "merge --complete with a context base path that differs from contexts.jsonl" 1 - M "$SY" --prefix E310BK --complete --no-profile
cp "$TF/ctx-0777.keep" "$SY/ctx/ctx-0777.json"
cp "$SY/ctx/ctx-2406.json" "$TF/ctx-2406.keep"
jset "$SY/ctx/ctx-2406.json" "d['skeleton'][0]['one'] = 3"
run "merge --complete with a skeleton child that is no subtree root" 1 - M "$SY" --prefix E310BK --complete --no-profile
cp "$TF/ctx-2406.keep" "$SY/ctx/ctx-2406.json"
run "merge --complete again after every edit was undone" 0 - M "$SY" --prefix E310BK --complete --no-profile
fresh_out "$SY"; reset_fake

say "9. the real campaign was only read"
python3 - "$C" <<'EOF' && ok "no file under the campaign directory mentions the test area, and no test path exists there" || bad "campaign check"
import os, sys
C = sys.argv[1]
hits = [os.path.join(dp, f) for dp, dn, fn in os.walk(C) for f in fn if "test-export" in f or f.startswith(".") and f.endswith(".tmp")]
assert not os.path.exists(os.path.join(C, "out")) and not hits, hits
EOF

echo
say "summary: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || { printf 'failed: %s\n' "${FAILED[@]}"; exit 1; }
