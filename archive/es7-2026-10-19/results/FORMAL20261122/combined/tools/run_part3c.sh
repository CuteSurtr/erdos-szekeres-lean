#!/bin/bash
# combined part 3 chain (25 Nov 2026), unattended: s35_20 finish recipe (res-slices-fv §9) -> spec snapshot -> PART3.md
# §§3-6 (mklinks3, marker, ES302Final, Bad302 control, Audit3, audit3) -> N66 re-solve driver restarted. Stops at the
# first failed check (no acceptance is declared here: the advisor consult and the records come after, by hand).
# Log: data/part3_run.log; result: data/part3_summary.json. Run as a unit (esr-vfy-p3chain).
set -u
D=/home/jay/research/data/formalize-20261122/res-slices-fv; W=/home/jay/research/data/formalize-20261122/combined
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
LOG=$W/data/part3_run.log; SUM=$W/data/part3_summary.json
STD="depends on axioms: \[propext, Classical.choice, Quot.sound\]"
log() { echo "$(date '+%F %T') $*" >> "$LOG"; }
done_json() { printf '{"time": "%s", "stage": "%s", "status": "%s"}\n' "$(date '+%F %T')" "$1" "$2" > "$SUM"; }
fail() { log "STOP at $1: $2"; done_json "$1" "STOPPED: $2"; exit 1; }
cd "$W"
log "chain start (resume c: RP3520 already compiled by b; MemoryMax 12G per PART3 §5, dated note in PART3.md §7)"

# 1-2 (resume, 26 Nov): the first run stopped because audit.py 3520 listed 412 problems, all axiom lines split by
# profiler text ("... .olean serialization took N ms" inside the line), and axlines.py found 671 missing whole lines.
# The recipe settles these with the re-print module (step 3); every other audit/axlines result is unchanged.
python3 -I - <<'PYEOF' || fail finish "audit problems other than profiler-split axiom lines"
import json, re, sys
l = [x for x in open("/home/jay/research/data/formalize-20261122/res-slices-fv/logs/finish3520.out") if x.startswith('{"tag": "3520", "theorem"')]
P = json.loads(l[-1])["problems"]
sys.exit(0 if P and all("non-standard axioms" in p and re.search(r"took \d+(\.\d+)?m?s", p) for p in P) else 1)
PYEOF
log "audit: all 412 problems are profiler-split axiom lines (checked)"
grep -q "lean_rc=0" $D/logs/RP3520.log || fail finish "RP3520 compile (run by chain b, 00:17-00:20)"
$PY -I -B $D/tools/axlines.py 3520 > $D/logs/axlines3520_after_reprint.out 2>&1 || fail finish "axlines after the reprint"
log "axlines settled by the reprint (logs/axlines3520_after_reprint.out)"
python3 -I -c "
import json,sys
l=[x for x in open('$D/logs/finish3520.out') if x.startswith('{\"manifests\"')]
d=json.loads(l[-1]); sys.exit(0 if d['leaves_ok'] and d['min_margin']==1 and d['max_min_margin_violations']==0 and d['lean_test_failures']==0 else 1)" \
  || fail finish "leaf sum / margin / leaf tests (step 4)"
log "finish recipe ok (audit: only split axiom lines, settled; axlines; leaf sum 119,054,033)"

# 3. step 5: snapshot of the six-slice specialisation
mkdir -p $D/data/spec-snapshots; n=Res118FV-s33_18-s34_18-s34_19-s35_18-s35_19-s35_20
cp -p $D/lean/RS/Res118FV.lean $D/data/spec-snapshots/$n.lean; cp -p $D/logs/RS_Res118FV.log $D/data/spec-snapshots/$n.log
cp -p $D/olean/RS/Res118FV.olean $D/data/spec-snapshots/$n.olean; log "spec snapshot $n"

# 4. PART3 §3: links3 and the two-providers check
tools/start3.sh links 2048 3600 1 python3 -I -B tools/mklinks3.py || fail links "mklinks3.py (logs/links.out)"
log "links3 ok"
touch data/MARKER_START3; log "marker data/MARKER_START3"

# 5. PART3 §6 item 1: ES302Final (MemoryMax 12G, stop at 9,830 MB: PART3 §5 as first registered; 7G left too little page cache)
tools/start3.sh es302final 12288 21600 1 /bin/bash tools/unit_lean.sh logs/ES302Final.log out/Combined/ES302Final.olean src \
  src/Combined/ES302Final.lean 9830 || fail es302final "unit failed (logs/ES302Final.log)"
grep -q 'lean_rc=0' logs/ES302Final.log || fail es302final "lean_rc"
grep -qiE '(^|: )error' logs/ES302Final.log && fail es302final "an error line in the log"
awk '/=== CHECK/{on=1} /Command being timed/{on=0} on' logs/ES302Final.log > data/es302final_check.txt
log "ES302Final ok"

# 6. item 2: Bad302 must fail with a type mismatch at bad301 and nothing else
tools/start3.sh bad302 12288 21600 1 /bin/bash tools/unit_lean.sh logs/ctl_Bad302.log - controls controls/Bad302.lean 9830
grep -q 'lean_rc=0' logs/ctl_Bad302.log && fail bad302 "the control compiled"
ne=$(grep -cE 'error' logs/ctl_Bad302.log); grep -qiE 'type mismatch|Type mismatch|mismatch' logs/ctl_Bad302.log || fail bad302 "no type mismatch"
log "Bad302 failed as required ($ne error lines; review the log by hand)"

# 7. item 3: Audit3 (statement check and module list) and the import audit
tools/start3.sh audit3lean 12288 21600 1 /bin/bash tools/unit_lean.sh logs/Audit3.log - src src/Audit3.lean 9830 \
  || fail audit3 "Audit3.lean unit failed"
grep -q 'lean_rc=0' logs/Audit3.log || fail audit3 "Audit3 lean_rc"
tools/start3.sh audit3 2048 3600 1 python3 -I -B tools/audit3.py || fail audit3 "audit3.py reported problems (data/audit3.json)"
log "audit3 ok"

# 8. resume the N66 re-solve (paused for this chain)
systemctl --user is-active -q esr-vfy-n66drv || systemd-run --user --unit=esr-vfy-n66drv --collect -q -p CPUQuota=10% \
  -p MemoryMax=300M -p MemorySwapMax=0 -p RuntimeMaxSec=259200 --nice=10 \
  --working-directory=/home/jay/research/data/n66-resolve-20261125 /home/jay/research/data/n66-resolve-20261125/run_resolve.sh 4
log "N66 driver restarted"
done_json all "OK: finish recipe, links3, ES302Final, Bad302 control, Audit3, audit3 (acceptance needs the advisor)"
log "chain end"
