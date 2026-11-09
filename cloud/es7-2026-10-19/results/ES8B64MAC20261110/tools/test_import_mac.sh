#!/bin/sh
# Test of the Mac -> Linux import path (ES8B64MAC20261110), run on the Mac.
#   sh test_import_mac.sh MACDIR REPO TESTDIR PY
# MACDIR: the Mac budget-64 work directory (runs/, contexts.jsonl, tools/run_context.py)
# REPO:   a checkout holding the frozen ES(8) <= 310 scripts
# TESTDIR: an empty scratch directory;  PY: a python with the campaign's packages
# 1. bundle three Mac contexts; 2. import them into a stand-in campaign directory with import_mac_runs.py
# (dry run, run, rerun = no-clobber); 3. run the FROZEN export_es310.py (sha256 29854a37...) and merge_es310.py
# --partial on them; 4. negative control: an unrewritten result whose pbb_strong path does not exist must be refused.
# macOS has no /proc: the exporter's live-job scan is given an empty /proc (there are no live jobs for these
# contexts), and the files are dated 300 s back to pass its 120 s age check. Nothing under MACDIR is written.
set -u
M=$1; W=$2; T=$3; PY=$4
E=$W/experiments/omission-compact-checker-2026-11-05
SRC=$W/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json
IMP=$W/cloud/es7-2026-10-19/results/ES8B64MAC20261110/tools/import_mac_runs.py
mkdir -p "$T/bundle/runs" "$T/C/runs" "$T/C/campaign" "$T/lin/search"
for k in 3850 768 4068; do cp -p "$M/runs/ctx-$k-b64.result.json" "$M/runs/ctx-$k-b64.json.gz" "$T/bundle/runs/"; done
(cd "$T/bundle" && shasum -a 256 runs/ctx-* > SHA256SUMS)
cp "$M/contexts.jsonl" "$T/C/"; cp "$M/tools/run_context.py" "$T/C/run_context.py"
cp "$W/experiments/omission-final311-2026-10-14/search/pbb_strong.py" "$T/lin/search/"
echo "== sha256 (first 12): frozen exporter, merge; run_context.py, pbb_strong.py, contexts.jsonl"
shasum -a 256 "$E/export_es310.py" "$E/merge_es310.py" "$T/C/run_context.py" "$T/lin/search/pbb_strong.py" \
  "$T/C/contexts.jsonl" | cut -c1-12
cat > "$T/noproc.py" <<'EOF'
import os, runpy, sys
_l = os.listdir
os.listdir = lambda p='.': [] if p == '/proc' else _l(p)
script = sys.argv[1]; sys.argv = sys.argv[1:]
runpy.run_path(script, run_name='__main__')
EOF
backdate() { python3 -c "import os,sys,time; [os.utime(os.path.join(sys.argv[1],n),(time.time()-300,)*2) for n in os.listdir(sys.argv[1])]" "$1"; }
summ() { python3 -c "import json,sys; d=json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); print(json.dumps({k:d.get(k) for k in sys.argv[2:]}))" "$@"; }

echo "== import, dry run"; python3 -I "$IMP" --bundle "$T/bundle" --campaign "$T/C" --pbb "$T/lin/search/pbb_strong.py" --dry-run > "$T/i0.json"; echo "exit $?"; summ "$T/i0.json" dry_run imported linux_has
echo "files written by the dry run: $(ls "$T/C/runs" | wc -l | tr -d ' ')"
echo "== import"; python3 -I "$IMP" --bundle "$T/bundle" --campaign "$T/C" --pbb "$T/lin/search/pbb_strong.py" > "$T/i1.json"; echo "exit $?"; summ "$T/i1.json" imported linux_has closed_in_campaign_runs
echo "== import again, path taken from the results already there"; python3 -I "$IMP" --bundle "$T/bundle" --campaign "$T/C" > "$T/i2.json"; echo "exit $?"; summ "$T/i2.json" imported linux_has
echo "== differences between a Mac result and its imported copy (lines)"; diff "$T/bundle/runs/ctx-4068-b64.result.json" "$T/C/runs/ctx-4068-b64.result.json" | grep -c '^[<>]'
diff "$T/bundle/runs/ctx-4068-b64.result.json" "$T/C/runs/ctx-4068-b64.result.json" | grep '^[<>]' | sed 's/: ".*\//: "<path>\//'
for k in 3850 768 4068; do cmp -s "$T/bundle/runs/ctx-$k-b64.json.gz" "$T/C/runs/ctx-$k-b64.json.gz" && echo "ctx $k tree identical"; done

backdate "$T/C/runs"
echo "== frozen exporter on the imported contexts"
"$PY" -I "$T/noproc.py" "$E/export_es310.py" --campaign "$T/C" --source "$SRC" --out "$T/out" --ctx 768,3850,4068 \
  --per-word 16 --chunk-leaves 12000 --block-leaves 64 > "$T/export.json" 2> "$T/export.err"; echo "exit $?"
summ "$T/export.json" exported refused refused_ctx not_ready code_changed
echo "== frozen merge, partial"
"$PY" -I "$T/noproc.py" "$E/merge_es310.py" "$T/out" --partial > "$T/merge.json" 2> "$T/merge.err"; echo "exit $?"
summ "$T/merge.json" refused alert code_changed contexts modules total_leaves

echo "== negative control: unrewritten result, Mac path absent"
N=$T/Cneg; mkdir -p "$N/runs" "$N/campaign"; cp "$T/C/contexts.jsonl" "$T/C/run_context.py" "$N/"
cp "$M/runs/ctx-3850-b64.json.gz" "$N/runs/"
sed 's#"pbb_strong": "[^"]*"#"pbb_strong": "/absent/lean 4 /.cache/es7/wt-b64-5aa5b31f2/experiments/omission-final311-2026-10-14/search/pbb_strong.py"#' \
  "$M/runs/ctx-3850-b64.result.json" > "$N/runs/ctx-3850-b64.result.json"
backdate "$N/runs"
"$PY" -I "$T/noproc.py" "$E/export_es310.py" --campaign "$N" --source "$SRC" --out "$T/outneg" --ctx 3850 \
  --per-word 16 --chunk-leaves 12000 --block-leaves 64 > "$T/neg.json" 2> "$T/neg.err"; echo "exit $? (1 expected)"
summ "$T/neg.json" refused exported
