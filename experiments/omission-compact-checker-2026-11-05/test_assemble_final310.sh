#!/bin/bash
# Tests of assemble_final310.sh (6 November 2026; a port of test_assemble_final311.sh). ES(8) <= 310 is NOT
# proved, and none of these tests needs or makes an E310 build. Everything is written under
# build/es310/test-assemble; build/es311/full, build/chain311, build/CompactChecker and build/ext are only read;
# the summary goes to logs/es310/assemble-tests.txt.
#
#  0. Static: Final310Compact.lean has the pinned sha256; drive_es310.FINAL_TEMPLATE equals design section D
#     outside comments; template variants (budget 63, an E311.Final import, a line hidden by a "-- /-" trick)
#     are rejected by the comparison.
#  1. A stub E310.Final: drive_es310.FINAL_TEMPLATE without the two Root imports, its two theorems with the
#     template's exact statements but proved by `sorry`. Compiled against the chain (Lean).
#  2. assemble_final310.sh --test-stub: Final310Compact.lean against the stub (Lean, two compiles). Expected:
#     Lean exits 0, the statement reads ForcesConvexNGon 310 8, sorryAx is among the axioms (main log and
#     audit), and the script reports "not verified" for exactly those two axiom problems and nothing else.
#  3. Run checks on a synthetic export (no Lean; 4,096 context manifests, 4,097 fake chunk .oleans, run.tsv
#     rows with the current dependency stamps; the E311R side is the real build/es311/full, read only):
#     consistent: accepted; then each of 14 perturbations refused. The gates (shapes / coverage outputs) on
#     synthetic outputs. The whole script in --dry-run on the synthetic export, on the real (absent) export,
#     and with a process named like the driver: refused, with the reasons.
#  4. --test-stub with an extra LEAN_PATH root holding a copy of BalancedBudgets.olean: refused (shadowing).
#  5. --test-stub with build/ext as an extra root: refused.
#  6. The audit file's `#check @` / `#print axioms` / `#eval` lines on a module that exists (Lean).
#  7. The report step on synthetic logs (no Lean): clean; killed by a signal; OOM kill; statement 311;
#     a second (fake) axiom line for the theorem; an extra axiom line for another name; two statement lines;
#     an E311B module in the environment; no axiom line in the audit.
#  8. Test switches outside the test modes and the cap guard: A310_EXTRA_ROOT, A310_E311, A310_MEM=45G refused;
#     A310_MEM=44G passes the guard.
#  9. The pins of check-chain on a fake tree (no Lean): unchanged it passes (route same, the 13 pinned
#     inputs, the .lake freeze); refused when a library.json hash or closure.json's toolchain sha256 differs,
#     when an input is newer than the run, when an input has other bytes but the same mtime (the sha256 pin),
#     and when a catalog's October record differs (route rebuilt is refused).
# 10. The .lake freeze on a synthetic root: an old .olean passes, a fresh one is refused; the real roots pass.
# 11. A fake `#print axioms` line printed by #eval: (a) added to Final310Compact.lean and compiled against the
#     stub (Lean): the report rejects the log (two axiom lines for the theorem); (b) replacing the genuine
#     `#print axioms`: a byte-identical copy of the script refuses the source at step 0 (pin).
# 12. Statement 311: a variant proving `ForcesConvexNGon 311 8` (from 310 by monotonicity), compiled against
#     the stub and audited exactly as the script audits (Lean, two compiles): the report rejects the statement.
# Fixer additions (6 November 2026, after the soundness and operations reviews):
#  2. also: the compiled source is the pinned copy WORK/final-src/Final310Compact.lean; the report says
#     test_only, checks_passed false, verified false; the script's last line is not "VERIFIED".
#  3. also: the script pins (merge, driver, coverage, shapes) and the merged manifest's merger_sha256 and the
#     coverage gate's checker_sha256: each wrong one refused.
#  7. also: 7j a clean report in a test mode: exit 0 but verified false, test_only true ("TEST ONLY");
#     7k a non-library .olean (CompactChecker.Path) that differs from its pin; 7l a non-library module with no
#     record; 7m the compiled source is not the pinned file.
# 13. the Lean-job count of cool(): lean processes with --server / --worker are not counted.
# 14. freeze_es310.sh on a copy of the script: fills the four pins once, then refuses.
# Every lean or lake process runs in a scope with MemoryMax=12G, MemorySwapMax=0, nice -n 10, one at a time,
# started only when Tctl < 85 C and fewer than 2 lean processes run.
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(cd "$HERE/../.." && pwd)
T=$HERE/build/es310/test-assemble
OUT=$HERE/logs/es310/assemble-tests.txt
THM=ErdosSzekeres.Omission.Compact310.forces_convex_octagon_310
rm -rf "$T"; mkdir -p "$T/src/E310" "$T/path/CompactChecker" "$T/E310" "$T/shadow" "$HERE/logs/es310"
exec 3>&1
log() { echo "$*" | sed "s#$REPO#<repo>#g; s#$HOME#<home>#g" | tee -a "$T/summary.txt" >&3; }
: > "$T/summary.txt"
log "assemble_final310.sh tests, $(date -u +%FT%TZ); assemble_final310.sh sha256 $(sha256sum < "$HERE/assemble_final310.sh" | cut -c1-64);" \
  "test script sha256 $(sha256sum < "$0" | cut -c1-64); drive_es310.py sha256 $(sha256sum < "$HERE/drive_es310.py" | cut -c1-64)"
PYH=$(python3 -I -c "import sys; t = open(sys.argv[1]).read(); print(t.split(\"<<'PYEOF'\\n\", 1)[1].split('\\nPYEOF\\n', 1)[0])" "$HERE/assemble_final310.sh")
ph() { python3 -I -c "$PYH" "$1" "$HERE" "${@:2}"; }   # the assembly's helper (env A310_* as given)
gate() {  # the workflow's limits before every Lean job: Tctl < 85 C and fewer than 2 lean processes
  local t n i
  for i in $(seq 360); do
    t=$(sensors 2>/dev/null | awk '/^Tctl:/ {gsub(/[^0-9.]/, "", $2); print $2; exit}'); n=$(pgrep -xc lean)
    [ -n "$t" ] && awk -v t="$t" 'BEGIN { exit !(t < 85) }' && [ "$n" -lt 2 ] && { echo "Tctl $t C, $n lean"; return 0; }
    sleep 10
  done
  echo "Tctl ${t:-?} C / $n lean processes for an hour"; return 1
}
leanc() {  # leanc LOG ROOT FILE [OLEAN]: one capped Lean job with LEAN_PATH=$LPT; LOG gets time -v and cgroup lines
  local log=$1 root=$2 file=$3 o=() g
  [ -n "${4:-}" ] && o=(-o "$4")
  g=$(gate) || { log "FAIL: no Lean slot: $g"; cp "$T/summary.txt" "$OUT"; exit 1; }
  (cd "$REPO" && LEAN_PATH="$LPT" LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 \
    systemd-run --user --scope --quiet -p MemoryMax=12G -p MemorySwapMax=0 -p CPUQuota=100% nice -n 10 \
    sh -c 'cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup); "$@"; rc=$?
      echo "cgroup memory.peak: $(cat $cg/memory.peak 2>/dev/null)"
      echo "cgroup memory.swap.peak: $(cat $cg/memory.swap.peak 2>/dev/null)"
      echo "cgroup oom_kill: $(sed -n "s/^oom_kill //p" $cg/memory.events 2>/dev/null)"; exit $rc' \
    sh /usr/bin/time -v lean -j1 -R "$root" "${o[@]}" "$file") > "$log" 2>&1
  local rc=$?
  echo "($g at start)" >> "$log"
  return $rc
}
costs() { echo "wall $(sed -n 's/.*Elapsed (wall clock) time (h:mm:ss or m:ss): //p' "$1"), RSS $(sed -n 's/.*Maximum resident set size (kbytes): //p' "$1") kB, cgroup peak $(sed -n 's/^cgroup memory.peak: //p' "$1") B, oom_kill $(sed -n 's/^cgroup oom_kill: //p' "$1")"; }

# 0. Static checks.
pin=$(sed -n 's/^FINAL_SRC_SHA=\([0-9a-f]\{64\}\).*/\1/p' "$HERE/assemble_final310.sh")
log "0. Final310Compact.lean sha256 $(sha256sum < "$HERE/assembly/Final310Compact.lean" | cut -c1-64); pinned $pin;" \
  "$( [ "$(sha256sum < "$HERE/assembly/Final310Compact.lean" | cut -c1-64)" = "$pin" ] && echo equal || echo DIFFERENT)"
ph template > "$T/template.lean" 2> "$T/template.err"
log "0. drive_es310.FINAL_TEMPLATE vs design section D (outside comments): exit $? (0 expected) $(cat "$T/template.err")"
sed 's/(\(∑ i, holes i\)) ≤ 64 :=/(\1) ≤ 63 :=/' "$T/template.lean" > "$T/tv-63.lean"
sed 's/^import E311R.Root$/import E311R.Root\nimport E311.Final/' "$T/template.lean" > "$T/tv-import.lean"
sed 's/^namespace E310$/namespace E310\n-- see \/-\naxiom cheat : False\n-- -\//' "$T/template.lean" > "$T/tv-hidden.lean"
for v in 63 import hidden; do
  r=$(ph template-errors "$T/tv-$v.lean" 2>&1); log "0. template variant '$v': exit $? (1 expected): $(echo "$r" | cut -c1-200)"
done

# 1. The stub.
python3 -I - "$T/template.lean" > "$T/src/E310/Final.lean" <<'PY' || { log "FAIL: stub generation"; exit 1; }
import re, sys
t = open(sys.argv[1]).read()
s = t.replace("import E310B.Root\n", "").replace("import E311R.Root\n", "")
s = s.replace("  CompactChecker.Bridge311Bal.balanced_of_root E310B.root\n", "  sorry\n")
s = s.replace("  CompactChecker.Bridge311Res.residual_of_root E311R.root\n", "  sorry\n")
stm = lambda x: re.findall(r"(theorem \w+ :.*?):=", x, re.S)
assert len(stm(t)) == 2 and stm(s) == stm(t), "statements differ from the template"
assert s.count("sorry") == 2 and not re.search(r"^import E31", s, re.M) and "E310B.root" not in s and "E311R.root" not in s
sys.stdout.write(s)
PY
log "1. stub source: $(sha256sum < "$T/src/E310/Final.lean" | cut -c1-64); statements byte-identical to drive_es310.FINAL_TEMPLATE's"
for m in $(ph cc-closure Bridge311Bal Bridge311Res); do ln -s "$HERE/build/CompactChecker/$m.olean" "$T/path/CompactChecker/$m.olean"; done
LAKE_LP=$(cd "$REPO" && systemd-run --user --scope --quiet -p MemoryMax=2G -p MemorySwapMax=0 nice -n 10 \
  lake env printenv LEAN_PATH)
LPT="$LAKE_LP:$HERE/build/chain311/olean:$T/path"
leanc "$T/stub-final.log" "$T/src" "$T/src/E310/Final.lean" "$T/E310/Final.olean"
rc=$?
log "1. stub E310.Final: lean exit $rc; $(grep -c "declaration uses 'sorry'" "$T/stub-final.log") sorry warnings;" \
  "$(grep -E "^'E310\." "$T/stub-final.log" | tr '\n' ' ')"
[ $rc -eq 0 ] || { log "FAIL: the stub does not compile"; cp "$T/summary.txt" "$OUT"; exit 1; }

# 2. The composition against the stub.
g=$(gate) || { log "FAIL: no Lean slot: $g"; cp "$T/summary.txt" "$OUT"; exit 1; }
A310_MEM=12G "$HERE/assemble_final310.sh" --test-stub "$T" > "$T/assemble-stub.out" 2>&1
rc=$?
log "2. --test-stub: exit $rc (1 expected); $(tail -1 "$T/assemble-stub.out")"
python3 -I - "$T/out/final310-compact.json" "$THM" "$pin" <<'PY' | while read -r l; do log "   $l"; done
import json, sys
d, thm = json.load(open(sys.argv[1])), sys.argv[2]
for k in ("main_compile", "audit_compile"):
    c = d[k]
    print(f"{k}: scope exit {c['scope_exit']}, wall {c['wall']}, cgroup peak {int(c['cgroup_memory_peak'] or 0) / 2**30:.2f} GB, "
          f"RSS {int(c['max_rss_kb'] or 0) / 2**20:.2f} GB, oom_kill {c['cgroup_oom_kill']}")
print(f"statement: {d['statement']}")
print(f"axioms: [{d['axioms']}]; audit axioms: [{d['audit_axioms']}]")
print(f"verified: {d['verified']}; problems: {d['problems']}")
print(f"route {d['route']}; inputs equal to the 311 pins: {d['chain']['inputs_equal_to_311_pins']}; "
      f".lake .olean files under the freeze: {d['chain']['lake_oleans_checked']} (newest {d['chain']['lake_newest_utc']})")
print(f"imported modules: {d['imported_modules']} (library {d['library_modules']}); top-level: "
      + ", ".join(f"{k} {v[:12]}" for k, v in sorted(d['top_level_oleans'].items())))
ax = d["axioms"] or ""
import hashlib
pin = sys.argv[3]
src_ok = (d["final_source"].endswith("/out/final-src/Final310Compact.lean") and d["final_source_sha256"] == pin
          and d["final_source_pin"] == pin)
print(f"compiled source: {d['final_source']} (sha256 {d['final_source_sha256'][:12]}, pin {pin[:12]}): "
      f"{'the pinned copy' if src_ok else 'NOT the pinned copy'}; test_only {d['test_only']}, checks_passed {d['checks_passed']}")
ok = (src_ok and d["test_only"] is True and d["checks_passed"] is False
      and not d["verified"] and "sorryAx" in ax and d["audit_axioms"] == ax
      and d["statement"] == f"{thm} : ErdosSzekeres.ForcesConvexNGon 310 8"
      and d["main_compile"]["scope_exit"] == "0" and d["audit_compile"]["scope_exit"] == "0"
      and d["problems"] == [f"nonstandard axioms for {thm}: [{ax}]", f"audit: nonstandard axioms for {thm}: [{ax}]"])
print("RESULT " + ("as expected: Lean exit 0 (both compiles), ForcesConvexNGon 310 8, sorryAx, rejected only for its axioms"
                   if ok else "UNEXPECTED"))
PY
grep -q 'Exit status: 0' "$T/out/final310-compact.main.log" && log "   main compile log: Exit status 0" \
  || log "   UNEXPECTED: main compile did not exit 0"
grep -q 'VERIFIED' "$T/assemble-stub.out" && log "   UNEXPECTED: the stub run printed VERIFIED" \
  || log "   the stub run printed no VERIFIED line (its last line: $(tail -1 "$T/assemble-stub.out" | cut -c1-120))"
cp "$T/summary.txt" "$OUT"

# 3. Run checks on a synthetic export.
F=$T/fake-export; FP=$(printf 'a%.0s' $(seq 64)):$(sed -n 's/^EXPORTER311_SHA256=\([0-9a-f]\{64\}\).*/\1/p' "$HERE/assemble_final310.sh")
for f in merge_es310.py drive_es310.py coverage_es310.py shapes_es311.py; do FP=$FP:$(sha256sum < "$HERE/$f" | cut -c1-64); done
pinset() { echo "$FP" | awk -F: -v i="$1" -v v="$2" 'BEGIN { OFS = ":" } { $i = v; print }'; }  # pinset FIELD VALUE
python3 -I - "$HERE" "$F" "$FP" <<'PY' || { log "FAIL: synthetic export"; exit 1; }
import hashlib, json, sys, datetime
from pathlib import Path
here, F, (p310, p311, pmerge) = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3].split(":")[:3]
sys.path.insert(0, str(here))
import drive_es310 as d10
STAMPED = ["Bridge311Bal", "Bridge311Res", "Fcat2650", "Fcat62", "Path"]
st = {n: (here / "build/CompactChecker" / f"{n}.stamp").read_text().strip() for n in STAMPED}
cols = d10.COLUMNS
h = lambda b: hashlib.sha256(b).hexdigest()
for d in ("ctx", "olean/E310B", "olean/E310"):
    (F / d).mkdir(parents=True, exist_ok=True)
STD = "[propext, Classical.choice, Quot.sound]"
rows, mods, total = [], [], 0
def row(utc, phase, mod, leaves, src, olean_bytes, axioms, wall="1.00"):
    o = F / "olean" / (mod.replace(".", "/") + ".olean")
    o.write_bytes(olean_bytes)
    r = {"utc": utc, "phase": phase, "module": mod, "leaves": leaves, "src_sha256": src,
         "deps_stamp": d10.deps_stamp_of(phase, None if phase == "final" else "Fcat62", st), "verdict": "ok", "exit": 0,
         "kernel_s": "0.5", "elab_s": "0.5", "wall_s": wall, "user_s": wall, "peak_rss_kb": 1, "olean_bytes": len(olean_bytes),
         "olean_sha256": h(olean_bytes), "axioms": axioms, "expected": 1, "load1": "1.0", "host": "synthetic",
         "log": "logs/none", "cg_peak_kb": 1}
    rows.append("\t".join(str(r.get(c, "")) for c in cols))
for k in range(4096):
    cm = []
    for j in range(1, (2 if k == 7 else 1) + 1):
        name, leaves = f"E310B.C{k:04d}{j:02d}", 10 + j
        src = h(name.encode())
        cm.append({"module": name, "file": f"src/E310B/C{k:04d}{j:02d}.lean", "sha256": src, "leaves": leaves,
                   "subtree_roots": [[0, leaves]], "blocks": 1, "entries": 1, "words": 1, "min_margin": 1,
                   "max_base": 4194304, "corrupted": False})
        row("2026-11-07T00:10:00Z", "chunk", name, leaves, src, (name + " olean").encode(), f"{name}.ex0={STD}")
    s = sum(m["leaves"] for m in cm)
    total += s
    man = {"ctx": k, "prefix": "E310B", "params": {"budget": 64, "K": 131072, "J": 131072 << 12, "per_word": 8,
           "chunk_leaves": 12000, "block_leaves": 64, "catalog_base": 4194304}, "base_path": [],
           "exporter_sha256": {"export_es310": p310, "export_es311": p311}, "modules": cm, "skeleton": [],
           "stats": {"leaves": s, "nodes": 2 * s - 1, "over_budget": 0, "min_margin": 1}}
    (F / "ctx" / f"ctx-{k:04d}.json").write_text(json.dumps(man))
    mods += [{x: m[x] for x in ("module", "file", "sha256", "leaves", "subtree_roots", "corrupted")} for m in cm]
rsha = h(b"synthetic Root")
row("2026-11-07T01:00:00Z", "root", "E310B.Root", total, rsha, b"Root olean", f"E310B.root={STD}", "10.00")
row("2026-11-07T01:10:00Z", "final", "E310.Final", total + 437579, h(d10.FINAL_TEMPLATE.encode()), b"Final olean",
    f"E310.balanced_excludes_64={STD};E310.residual_excludes_32={STD}", "10.00")
(F / "run.tsv").write_text("\t".join(cols) + "\n" + "\n".join(rows) + "\n")
(F / "manifest-E310B.json").write_text(json.dumps({
    "side": "balanced", "prefix": "E310B", "catalog": "CompactChecker.Fcat62", "rows": 3131, "states": 252,
    "budget": 64, "catalog_base": 4194304, "complete": True, "total_leaves": total, "export_root": 0, "base_path": [],
    "root": {"module": "E310B.Root", "file": "src/E310B/Root.lean", "sha256": rsha}, "modules": mods,
    "merger_sha256": pmerge}))
print(len(mods), total)
PY
log "3. synthetic export: $(python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1])); print(len(d["modules"]), "chunk modules,", d["total_leaves"], "leaves, 4096 context manifests")' "$F/manifest-E310B.json")"
case_dir() {  # case_dir NAME: a case directory whose entries are symlinks to the synthetic export's
  local c=$T/case-$1; rm -rf "$c"; mkdir -p "$c"
  for e in ctx olean manifest-E310B.json run.tsv; do ln -s "$F/$e" "$c/$e"; done; echo "$c"
}
runcheck() {  # runcheck LABEL DIR [EXPECTED-EXIT] [env...]: the helper's check-run on DIR
  local lab=$1 dir=$2 want=$3; shift 3
  env A310_EXPORT="$dir" A310_PINS="$FP" "$@" python3 -I -c "$PYH" check-run "$HERE" > "$T/check-$lab.out" 2>&1
  local rc=$?
  log "3. $lab: exit $rc ($want expected): $(cut -c1-330 "$T/check-$lab.out")"
}
tsvedit() {  # tsvedit DIR AWK-PROGRAM: DIR/run.tsv becomes an edited copy of the synthetic one
  rm "$1/run.tsv"; awk -F'\t' 'BEGIN { OFS = "\t" } '"$2"' { print }' "$F/run.tsv" > "$1/run.tsv"
}
runcheck consistent "$F" 0
c=$(case_dir stamp); tsvedit "$c" '$3 == "E310B.C001201" { $6 = "0000" substr($6, 5) }'; runcheck chunk-stamp "$c" 1
c=$(case_dir oleansha); tsvedit "$c" '$3 == "E310B.C204801" { $15 = "0000" substr($15, 5) }'; runcheck chunk-olean "$c" 1
c=$(case_dir order); tsvedit "$c" '$3 == "E310B.C409501" { $1 = "2026-11-07T01:05:00Z" }'; runcheck chunk-after-root "$c" 1
c=$(case_dir final); tsvedit "$c" '$3 == "E310.Final" { $5 = "0000" substr($5, 5) }'; runcheck final-template-sha "$c" 1
c=$(case_dir finalax); tsvedit "$c" '$3 == "E310.Final" { sub(/E310.balanced_excludes_64=\[propext,/, "E310.balanced_excludes_64=[propext, sorryAx,", $16) }'
runcheck final-sorryAx "$c" 1
c=$(case_dir failrow); tsvedit "$c" '$3 == "E310B.Root" { $7 = "fail" }'; runcheck root-fail "$c" 1
c=$(case_dir dropmod); rm "$c/manifest-E310B.json"
python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1])); d["modules"]=[m for m in d["modules"] if m["module"]!="E310B.C000702"]; d["total_leaves"]-=12; json.dump(d,open(sys.argv[2],"w"))' "$F/manifest-E310B.json" "$c/manifest-E310B.json"
runcheck manifest-misses-a-ctx-module "$c" 1
c=$(case_dir dropctx); rm "$c/ctx" "$c/manifest-E310B.json"; mkdir "$c/ctx"
for f in "$F"/ctx/ctx-*.json; do [ "$(basename "$f")" = ctx-3000.json ] || ln -s "$f" "$c/ctx/"; done
python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1])); d["modules"]=[m for m in d["modules"] if not m["module"].startswith("E310B.C3000")]; d["total_leaves"]-=11; json.dump(d,open(sys.argv[2],"w"))' "$F/manifest-E310B.json" "$c/manifest-E310B.json"
runcheck 4095-contexts "$c" 1
c=$(case_dir budget); rm "$c/manifest-E310B.json"
python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1])); d["budget"]=63; json.dump(d,open(sys.argv[2],"w"))' "$F/manifest-E310B.json" "$c/manifest-E310B.json"
runcheck manifest-budget-63 "$c" 1
c=$(case_dir extraman); ln -s "$HERE/build/es311/full/manifest-E311R.json" "$c/manifest-E311R.json"; runcheck extra-manifest "$c" 1
runcheck exporter-pin "$F" 1 A310_PINS="$(printf 'b%.0s' $(seq 64)):${FP#*:}"
runcheck no-pin "$F" 1 A310_PINS=":"
Z64=$(printf '0%.0s' $(seq 64))
runcheck merge-pin-wrong "$F" 1 A310_PINS="$(pinset 3 "$Z64")"
runcheck driver-pin-wrong "$F" 1 A310_PINS="$(pinset 4 "$Z64")"
runcheck coverage-pin-empty "$F" 1 A310_PINS="$(pinset 5 "")"
runcheck shapes-pin-wrong "$F" 1 A310_PINS="$(pinset 6 "$Z64")"
c=$(case_dir merger); rm "$c/manifest-E310B.json"
python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1])); d["merger_sha256"]="0"*64; json.dump(d,open(sys.argv[2],"w"))' "$F/manifest-E310B.json" "$c/manifest-E310B.json"
runcheck manifest-merger-sha "$c" 1
c=$(case_dir reuse); mkdir -p "$c/reuse/E311R"; cp "$F/olean/E310B/C000001.olean" "$c/reuse/E311R/C00001.olean"; runcheck reuse-olean "$c" 1
E2=$T/e311-copy; mkdir -p "$E2"; cp "$HERE/build/es311/full/manifest-E311B.json" "$HERE/build/es311/full/manifest-E311R.json" "$E2/"
ln -s "$HERE/build/es311/full/olean" "$E2/olean"
awk -F'\t' 'BEGIN { OFS = "\t" } NR > 1 && $3 == "E311R.C00005" { $6 = "0000" substr($6, 5) } { print }' "$HERE/build/es311/full/run.tsv" > "$E2/run.tsv"
runcheck e311r-stamp "$F" 1 A310_E311="$E2"
#  Gates on synthetic shapes / coverage outputs (the real tools need a real export).
RJ=$(A310_EXPORT="$F" A310_PINS="$FP" python3 -I -c "$PYH" check-run "$HERE" 2>/dev/null)
MS=$(sha256sum < "$F/manifest-E310B.json" | cut -c1-64)
PCOV=$(echo "$FP" | cut -d: -f5)
mkg() {  # mkg NAME SHAPES-PASS COV-PASS MODE CONTEXTS MERGED-SHA EXPORTER [CHECKER-SHA]
  printf '{"export": "x", "manifests": {"manifest-E310B.json": {"files": 4098, "failing": 0}}, "PASS": %s}\n' "$2" > "$T/g-$1-shapes.json"
  printf '{"mode": "%s", "contexts_checked": %s, "merged_manifest_sha256": "%s", "exporter_sha256": {"export_es310": "%s"}, "checker_sha256": "%s", "PASS": %s}\n' \
    "$4" "$5" "$6" "$7" "${8:-$PCOV}" "$3" > "$T/g-$1-cov.json"
}
gates() {  # gates LABEL COV-EXIT EXPECTED
  A310_EXPORT="$F" A310_PINS="$FP" python3 -I -c "$PYH" gates "$HERE" "$T/g-$1-shapes.json" "$T/g-$1-cov.json" "$2" "$MS" "$RJ" > "$T/g-$1.out" 2>&1
  log "3. gates $1: exit $? ($3 expected): $(cut -c1-260 "$T/g-$1.out")"
}
P10=${FP%%:*}
mkg pass true true complete 4096 "$MS" "$P10"; gates pass 0 0
mkg covfail true false complete 4096 "$MS" "$P10"; gates covfail 1 1
mkg partial true true partial 4096 "$MS" "$P10"; gates partial 0 1
mkg n4095 true true complete 4095 "$MS" "$P10"; gates n4095 0 1
mkg other-manifest-sha true true complete 4096 "$(printf 'c%.0s' $(seq 64))" "$P10"; gates other-manifest-sha 0 1
mkg shapesfail false true complete 4096 "$MS" "$P10"; gates shapesfail 0 1
mkg cov-exit-1 true true complete 4096 "$MS" "$P10"; gates cov-exit-1 1 1
mkg cov-exporter true true complete 4096 "$MS" "$(printf 'd%.0s' $(seq 64))"; gates cov-exporter 0 1
mkg cov-checker-sha true true complete 4096 "$MS" "$P10" "$(printf 'e%.0s' $(seq 64))"; gates cov-checker-sha 0 1
#  The whole script, --dry-run.
A310_EXPORT="$F" "$HERE/assemble_final310.sh" --dry-run > "$T/dry-synthetic.out" 2>&1
log "3. --dry-run on the synthetic export (the script's own pins; the campaign runs): exit $? (1 expected): $(tail -1 "$T/dry-synthetic.out" | cut -c1-600)"
bash -c 'exec -a "python3 drive_es310.py build/es310/full --reuse build/es311/full:E311R --jobs 2" sleep 60' &
dummy=$!; sleep 1  # killed right after the dry run
"$HERE/assemble_final310.sh" --dry-run > "$T/dry-driver.out" 2>&1
r=$?; grep -q 'a drive_es310 runs\|a drive_es310.py runs' "$T/dry-driver.out" && w=listed || w="NOT listed"
log "3. a process named like the driver: exit $r (1 expected); the driver reason is $w"
kill $dummy 2>/dev/null; wait $dummy 2>/dev/null
"$HERE/assemble_final310.sh" --dry-run > "$T/dry-real.out" 2>&1
log "3. --dry-run on the real export (absent: nothing exported yet): exit $? (1 expected): $(tail -1 "$T/dry-real.out" | cut -c1-600)"
cp "$T/summary.txt" "$OUT"

# 4. A shadowed module.
cp "$HERE/build/chain311/olean/BalancedBudgets.olean" "$T/shadow/BalancedBudgets.olean"
A310_MEM=12G A310_EXTRA_ROOT="$T/shadow" "$HERE/assemble_final310.sh" --test-stub "$T" > "$T/assemble-shadow.out" 2>&1
log "4. extra root with a copy of BalancedBudgets.olean: exit $? (1 expected): $(tail -1 "$T/assemble-shadow.out" | cut -c1-400)"

# 5. build/ext on LEAN_PATH.
A310_MEM=12G A310_EXTRA_ROOT="$HERE/build/ext" "$HERE/assemble_final310.sh" --test-stub "$T" > "$T/assemble-ext.out" 2>&1
log "5. build/ext as an extra root: exit $? (1 expected): $(tail -1 "$T/assemble-ext.out" | cut -c1-400)"

# 6. The audit file's Lean on a module that exists now.
mkdir -p "$T/audit"
cat > "$T/audit/AuditProbe.lean" <<'LEAN'
import BalancedBudgets
#check @OmissionBalanced.balanced_bound_of_hole_budget
#print axioms OmissionBalanced.balanced_bound_of_hole_budget
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"module {m}"
LEAN
LPT="$LAKE_LP:$HERE/build/chain311/olean" leanc "$T/audit.log" "$T/audit" "$T/audit/AuditProbe.lean"
log "6. audit probe: lean exit $?; $(grep -c '^module ' "$T/audit.log") module lines (BalancedBudgets listed: $(grep -cx 'module BalancedBudgets' "$T/audit.log")); #check prints: $(grep -m1 '^@\?OmissionBalanced.balanced_bound_of_hole_budget' "$T/audit.log" | cut -c1-100); axiom line: $(grep -m1 "^'OmissionBalanced" "$T/audit.log" | cut -c1-140)"
cp "$T/summary.txt" "$OUT"

# 7. The report step on synthetic logs (no Lean). Final310Compact is on no LEAN_PATH root here, so a clean
#    pair of logs gives exactly one problem: that module not found.
cg0=$(printf 'cgroup memory.peak: 1\ncgroup memory.swap.peak: 0\ncgroup oom_kill: 0')
AX="'$THM' depends on axioms: [propext, Classical.choice, Quot.sound]"
printf "%s\n\tExit status: 0\n%s\n" "$AX" "$cg0" > "$T/syn-main.log"
mkaudit() {  # mkaudit FILE STATEMENT-NUMBER [extra lines]
  { echo "$THM : ErdosSzekeres.ForcesConvexNGon $2 8"; echo "$AX"; grep '^module ' "$T/audit.log"; echo "module Final310Compact"
    [ -n "${3:-}" ] && printf '%s\n' "$3"; printf '\tExit status: 0\n%s\n' "$cg0"; } > "$1"
}
mkaudit "$T/syn-audit.log" 310
CJ=$(ph check-chain "$LAKE_LP" "" 2>&1)
synth() {  # synth TAG MAINLOG MAINRC AUDITLOG
  A310_FINAL_PIN="$pin" python3 -I -c "$PYH" report "$HERE" "$2" "$3" "$4" 0 "$LAKE_LP:$HERE/build/chain311/olean" \
    "$T/syn-$1.json" "$T/syn-$1-imports.tsv.gz" synthetic same "" "$CJ" 12G \
    "$HERE/assembly/Final310Compact.lean" "$LAKE_LP" "$T/E310/Final.olean" "" > "$T/syn-$1.out" 2>&1
  log "$1: exit $? (1 expected): $(cut -c1-420 "$T/syn-$1.out")"
}
synth 7a-clean "$T/syn-main.log" 0 "$T/syn-audit.log"
{ echo "Command terminated by signal 9"; cat "$T/syn-main.log"; } > "$T/syn-main-signal.log"
synth 7b-signal "$T/syn-main-signal.log" 137 "$T/syn-audit.log"
sed 's/^cgroup oom_kill: 0$/cgroup oom_kill: 1/' "$T/syn-main.log" > "$T/syn-main-oom.log"
synth 7c-oom "$T/syn-main-oom.log" 0 "$T/syn-audit.log"
mkaudit "$T/syn-audit-311.log" 311
synth 7d-statement-311 "$T/syn-main.log" 0 "$T/syn-audit-311.log"
{ echo "'$THM' depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]"; cat "$T/syn-main.log"; } > "$T/syn-main-fake.log"
synth 7e-fake-second-axiom-line "$T/syn-main-fake.log" 0 "$T/syn-audit.log"
{ echo "'ErdosSzekeres.Omission.Compact310.balanced_population_187' depends on axioms: [propext]"; cat "$T/syn-main.log"; } > "$T/syn-main-other.log"
synth 7f-axiom-line-of-another-name "$T/syn-main-other.log" 0 "$T/syn-audit.log"
mkaudit "$T/syn-audit-2stmt.log" 310 "$THM : ErdosSzekeres.ForcesConvexNGon 310 8"
synth 7g-two-statement-lines "$T/syn-main.log" 0 "$T/syn-audit-2stmt.log"
mkaudit "$T/syn-audit-e311b.log" 310 "module E311B.C00001"
synth 7h-E311B-module "$T/syn-main.log" 0 "$T/syn-audit-e311b.log"
grep -v "^'" "$T/syn-audit.log" > "$T/syn-audit-noax.log"
synth 7i-audit-without-axiom-line "$T/syn-main.log" 0 "$T/syn-audit-noax.log"
#  7j-m (fixer): a fake root that provides Final310Compact (any bytes: the report compares it with the .olean
#  argument), and fake roots for CompactChecker.Path and an unknown module.
CR=$T/clean-root; rm -rf "$CR"; mkdir -p "$CR/CompactChecker" "$CR/Foo"
cp "$T/E310/Final.olean" "$CR/Final310Compact.olean"
rep7() {  # rep7 TAG AUDITLOG SRC EXPECTED-EXIT: the report with Final310Compact found on $CR, test mode "synthetic"
  A310_FINAL_PIN="$pin" python3 -I -c "$PYH" report "$HERE" "$T/syn-main.log" 0 "$2" 0 \
    "$LAKE_LP:$HERE/build/chain311/olean:$CR" "$T/syn-$1.json" "$T/syn-$1-imports.tsv.gz" synthetic same "" "$CJ" 12G \
    "$3" "$LAKE_LP" "$CR/Final310Compact.olean" "" > "$T/syn-$1.out" 2>&1
  log "$1: exit $? ($4 expected): $(cut -c1-420 "$T/syn-$1.out")"
}
rep7 7j-clean-in-a-test-mode "$T/syn-audit.log" "$HERE/assembly/Final310Compact.lean" 0
log "   7j record: $(python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1])); print("verified", d["verified"], "| checks_passed", d["checks_passed"], "| test_only", d["test_only"], "| non-library oleans compared", len(d["non_library_oleans"]))' "$T/syn-7j-clean-in-a-test-mode.json")"
printf 'not the real Path.olean\n' > "$CR/CompactChecker/Path.olean"
{ cat "$T/syn-audit.log"; echo "module CompactChecker.Path"; } > "$T/syn-audit-ccpath.log"
rep7 7k-CompactChecker.Path-differs-from-its-pin "$T/syn-audit-ccpath.log" "$HERE/assembly/Final310Compact.lean" 1
rm "$CR/CompactChecker/Path.olean"; printf 'x\n' > "$CR/Foo/Bar.olean"
{ cat "$T/syn-audit.log"; echo "module Foo.Bar"; } > "$T/syn-audit-foo.log"
rep7 7l-unrecorded-non-library-module "$T/syn-audit-foo.log" "$HERE/assembly/Final310Compact.lean" 1
rm "$CR/Foo/Bar.olean"
cp "$HERE/assembly/Final310Compact.lean" "$T/edited-final.lean"; echo "-- edited after step 0" >> "$T/edited-final.lean"
rep7 7m-compiled-source-not-the-pinned-one "$T/syn-audit.log" "$T/edited-final.lean" 1
cp "$T/summary.txt" "$OUT"

# 8. Test switches outside the test modes, and the cap guard.
A310_EXTRA_ROOT="$T/shadow" "$HERE/assemble_final310.sh" --dry-run > "$T/sw-extra.out" 2>&1
log "8a. A310_EXTRA_ROOT without --test-stub or A310_EXPORT: exit $? (1 expected): $(tail -1 "$T/sw-extra.out" | cut -c1-200)"
A310_E311="$T/e311-copy" "$HERE/assemble_final310.sh" --dry-run > "$T/sw-e311.out" 2>&1
log "8b. A310_E311 without A310_EXPORT: exit $? (1 expected): $(tail -1 "$T/sw-e311.out" | cut -c1-200)"
A310_MEM=45G "$HERE/assemble_final310.sh" --dry-run > "$T/sw-45.out" 2>&1
log "8c. A310_MEM=45G: exit $? (1 expected): $(tail -1 "$T/sw-45.out" | cut -c1-200)"
A310_MEM=44G "$HERE/assemble_final310.sh" --dry-run > "$T/sw-44.out" 2>&1
r=$?; grep -q 'A310_MEM must be' "$T/sw-44.out" && w="REFUSED BY THE CAP GUARD" || w="passes the cap guard"
log "8d. A310_MEM=44G: $w (the dry run then stops for another reason, exit $r)"

# 9. The pins of check-chain on a fake tree: FR/experiments/x stands for HERE, with symlinks to the real files
#    except the ones a case changes (copies). FR/.lake, lean-toolchain and lake-manifest.json are symlinks.
FR=$T/fake/repo; FH=$FR/experiments/x
mkdir -p "$FH/build/chain311" "$FH/build/CompactChecker" "$FH/logs/es311"
for f in .lake lean-toolchain lake-manifest.json; do ln -s "$REPO/$f" "$FR/$f"; done
ln -s "$HERE/CompactChecker" "$FH/CompactChecker"; ln -s "$HERE/build/ext" "$FH/build/ext"
ln -s "$HERE/logs/es311/hardcap-rebuild.tsv" "$FH/logs/es311/hardcap-rebuild.tsv"
for f in build.tsv olean; do ln -s "$HERE/build/chain311/$f" "$FH/build/chain311/$f"; done
for f in "$HERE"/build/CompactChecker/*.olean; do ln -s "$f" "$FH/build/CompactChecker/$(basename "$f")"; done
FLP=$(echo "$LAKE_LP" | sed "s#$REPO/#$FR/#g")
RS=$(echo "$RJ" | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["first_compile_start_utc"])')
log "9. run start used: $RS (the synthetic export's check-run: the minimum over its run.tsv and build/es311/full/run.tsv)"
pins() { cp "$HERE/build/chain311/closure.json" "$HERE/build/chain311/library.json" "$FH/build/chain311/"; }
chk() { python3 -I -c "$PYH" check-chain "$FH" "$FLP" "$RS" > "$T/pins-$1.out" 2>&1; }
edit_json() {  # edit_json FILE PYTHON-STATEMENT (d is the loaded JSON)
  python3 -I -c 'import json, sys; f = sys.argv[1]; d = json.load(open(f)); exec(sys.argv[2]); json.dump(d, open(f, "w"))' "$1" "$2"; }
relink() { rm -f "$FH/build/CompactChecker/$1.olean"; ln -s "$HERE/build/CompactChecker/$1.olean" "$FH/build/CompactChecker/$1.olean"; }
pins; chk 0; r=$?
log "9a. fake tree, unchanged: exit $r (0 expected); $(python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1])); print("route", d["route"], "| library verified", d["library_pinned_verified"], "| inputs equal to the 311 pins", d["inputs_equal_to_311_pins"], "older than", d["run_first_compile_utc"], "| .lake .olean", d["lake_oleans_checked"], "newest", d["lake_newest_utc"])' "$T/pins-0.out" 2>&1 | cut -c1-400)"
pins; edit_json "$FH/build/chain311/library.json" 'd["modules"]["ErdosSzekeres.Omission.PopulationBounds"][1] = "0" * 64'
chk 1; log "9b. library.json hash of PopulationBounds changed: exit $? (1 expected): $(tail -1 "$T/pins-1.out" | cut -c1-300)"
pins; edit_json "$FH/build/chain311/closure.json" 'd["lean_toolchain_sha256"] = "0" * 64'
chk 2; log "9c. closure.json toolchain sha256 changed: exit $? (1 expected): $(tail -1 "$T/pins-2.out" | cut -c1-300)"
pins; rm "$FH/build/CompactChecker/Fcat62.olean"; cp "$HERE/build/CompactChecker/Fcat62.olean" "$FH/build/CompactChecker/"
chk 3; log "9d. a copy of Fcat62.olean written now (same bytes, newer mtime): exit $? (1 expected): $(tail -1 "$T/pins-3.out" | cut -c1-300)"
relink Fcat62
pins; rm "$FH/build/CompactChecker/Split.olean"; cp "$HERE/build/CompactChecker/Split.olean" "$FH/build/CompactChecker/"
python3 -I -c 'import sys; f = open(sys.argv[1], "r+b"); f.seek(-1, 2); b = f.read(1); f.seek(-1, 2); f.write(bytes([b[0] ^ 1])); f.close()' "$FH/build/CompactChecker/Split.olean"
touch -r "$HERE/build/CompactChecker/Split.olean" "$FH/build/CompactChecker/Split.olean"
chk 4; log "9e. Split.olean with its last byte changed and the original mtime: exit $? (1 expected): $(tail -1 "$T/pins-4.out" | cut -c1-300)"
relink Split
pins; edit_json "$FH/build/chain311/closure.json" 'd["modules"]["BalancedCoverCutsV2"]["recorded_olean_sha256"] = "0" * 64'
chk 5; log "9f. October record of BalancedCoverCutsV2 changed (route rebuilt): exit $? (1 expected): $(tail -1 "$T/pins-5.out" | cut -c1-300)"
cp "$T/summary.txt" "$OUT"

# 10. The .lake freeze.
L=$T/lake; mkdir -p "$L/old/lib/lean/A" "$L/new/lib/lean/B"
: > "$L/old/lib/lean/A/X.olean"; touch -d 2026-11-01T00:00:00Z "$L/old/lib/lean/A/X.olean"
: > "$L/new/lib/lean/B/Y.olean"; cp -p "$L/old/lib/lean/A/X.olean" "$L/new/lib/lean/B/X.olean"
ph check-lake "$L/old" > "$T/lake-old.out" 2>&1; log "10a. a root with one .olean of 1 Nov: exit $? (0 expected): $(cut -c1-200 "$T/lake-old.out")"
ph check-lake "$L/new" > "$T/lake-new.out" 2>&1; log "10b. a root with an .olean written now: exit $? (1 expected): $(cut -c1-300 "$T/lake-new.out")"
ph check-lake > "$T/lake-real.out" 2>&1; log "10c. the real .lake/build/lib and .lake/packages/*/.lake/build/lib: exit $? (0 expected): $(cut -c1-200 "$T/lake-real.out")"

# 11. A fake `#print axioms` line printed by #eval.
#  a. Added to Final310Compact.lean, compiled against the stub: the genuine line (with sorryAx) and the fake one.
mkdir -p "$T/fake-eval/src" "$T/fake-eval/olean" "$T/fake-eval/path/E310"
ln -s "$T/E310/Final.olean" "$T/fake-eval/path/E310/Final.olean"
sed "s|^#print axioms forces_convex_octagon_310\$|#print axioms forces_convex_octagon_310\n#eval IO.println \"'$THM' depends on axioms: [propext, Classical.choice, Quot.sound]\"|" \
  "$HERE/assembly/Final310Compact.lean" > "$T/fake-eval/src/Final310Compact.lean"
LPT="$LAKE_LP:$HERE/build/chain311/olean:$T/path:$T/fake-eval/path" leanc "$T/fake-eval/main.log" "$T/fake-eval/src" \
  "$T/fake-eval/src/Final310Compact.lean" "$T/fake-eval/olean/Final310Compact.olean"
rc=$?
log "11a. Final310Compact.lean + a fake axiom line by #eval, against the stub: lean exit $rc; $(costs "$T/fake-eval/main.log"); axiom lines in the log:"
grep "^'" "$T/fake-eval/main.log" | while read -r l; do log "      $l"; done
synth 11a-report-on-that-log "$T/fake-eval/main.log" "$rc" "$T/syn-audit.log"
#  b. The genuine `#print axioms` replaced by the fake one: the source pin refuses it before anything else.
FH2=$T/fake2/repo/experiments/x; mkdir -p "$FH2/assembly"; cp "$HERE/assemble_final310.sh" "$FH2/"
sed "s|^#print axioms forces_convex_octagon_310\$|#eval IO.println \"'$THM' depends on axioms: [propext, Classical.choice, Quot.sound]\"|" \
  "$HERE/assembly/Final310Compact.lean" > "$FH2/assembly/Final310Compact.lean"
cmp -s "$HERE/assemble_final310.sh" "$FH2/assemble_final310.sh" && same="byte-identical copy" || same="NOT IDENTICAL"
"$FH2/assemble_final310.sh" --test-stub "$T" > "$T/fake2.out" 2>&1
log "11b. $same of the script, with the genuine #print axioms replaced by the #eval: exit $? (1 expected): $(tail -1 "$T/fake2.out" | sed "s#$T#<T>#g" | cut -c1-300)"
cp "$T/summary.txt" "$OUT"

# 12. Statement 311, from 310 by monotonicity, compiled against the stub and audited as the script audits.
W=$T/wrong311; mkdir -p "$W/src" "$W/olean" "$W/audit"
python3 -I - "$HERE/assembly/Final310Compact.lean" > "$W/src/Final310Compact.lean" <<'PY'
import sys
s = open(sys.argv[1]).read()
old = ("theorem forces_convex_octagon_310 : ForcesConvexNGon 310 8 :=\n"
       "  Partition.forces_of_population_bounds (by omega) balanced_population_187 residual_population_121\n")
new = ("theorem forces_convex_octagon_310 : ForcesConvexNGon 311 8 :=\n"
       "  fun s gp h => (Partition.forces_of_population_bounds (by omega) balanced_population_187\n"
       "    residual_population_121) s gp (by omega)\n")
assert s.count(old) == 1
sys.stdout.write(s.replace(old, new))
PY
LPT="$LAKE_LP:$HERE/build/chain311/olean:$T/path:$T/fake-eval/path" leanc "$W/main.log" "$W/src" "$W/src/Final310Compact.lean" \
  "$W/olean/Final310Compact.olean"
rc=$?
log "12. variant 'forces_convex_octagon_310 : ForcesConvexNGon 311 8' against the stub: lean exit $rc; $(costs "$W/main.log"); $(grep "^'" "$W/main.log" | head -1)"
sed -n '/^cat > "\$AUD\/Audit310.lean" <<EOF$/,/^EOF$/p' "$HERE/assemble_final310.sh" | sed '1d;$d' | sed "s|\$THEOREM|$THM|g" > "$W/audit/Audit310.lean"
LPT="$LAKE_LP:$HERE/build/chain311/olean:$T/path:$T/fake-eval/path:$W/olean" leanc "$W/audit.log" "$W/audit" "$W/audit/Audit310.lean"
arc=$?
log "12. its audit (Audit310.lean as the script writes it): lean exit $arc; statement line: $(grep -m1 "^@\?$THM :" "$W/audit.log")"
A310_FINAL_PIN="$pin" python3 -I -c "$PYH" report "$HERE" "$W/main.log" "$rc" "$W/audit.log" "$arc" \
  "$LAKE_LP:$HERE/build/chain311/olean:$T/path:$T/fake-eval/path:$W/olean" "$W/report.json" "$W/imports.tsv.gz" \
  synthetic same "" "$CJ" 12G "$W/src/Final310Compact.lean" "$LAKE_LP" "$W/olean/Final310Compact.olean" "" > "$W/report.out" 2>&1
log "12. report on these two logs: exit $? (1 expected): $(cut -c1-500 "$W/report.out")"
grep -q 'is not the pinned Final310Compact.lean' "$W/report.out" && log "12. ... and the compiled (edited) source is flagged as not the pinned one" \
  || log "12. UNEXPECTED: the edited source was not flagged"
cp "$T/summary.txt" "$OUT"

# 13. cool()'s Lean-job count ignores editor / lean-lsp servers (fake processes named lean; no Lean runs).
FL=$T/fakelean; rm -rf "$FL"; mkdir -p "$FL"; printf '#!/bin/sh\nsleep 30\n' > "$FL/lean"; chmod +x "$FL/lean"
a0=$(pgrep -xc lean); j0=$(ph lean-jobs)
"$FL/lean" --server & f1=$!; "$FL/lean" --worker file:///x.lean & f2=$!; "$FL/lean" -j1 -R /x -o /x.olean /x.lean & f3=$!
sleep 1; a1=$(pgrep -xc lean); j1=$(ph lean-jobs)
kill $f1 $f2 $f3 2>/dev/null; wait $f1 $f2 $f3 2>/dev/null
log "13. three fake processes named lean (--server, --worker, a compile): pgrep -xc lean $a0 -> $a1; lean-jobs $j0 -> $j1" \
  "($( [ $((a1 - a0)) -eq 3 ] && [ $((j1 - j0)) -eq 1 ] && echo 'as expected: only the compile counts' || echo UNEXPECTED))"
grep -q 'n=$(py lean-jobs' "$HERE/assemble_final310.sh" && ! grep -q 'pgrep -xc lean' "$HERE/assemble_final310.sh" \
  && log "13. cool() uses lean-jobs, not pgrep -xc lean" || log "13. UNEXPECTED: cool() still counts every lean process"

# 14. freeze_es310.sh on a copy of the script (never on the real one here).
FZ=$T/freeze; rm -rf "$FZ"; mkdir -p "$FZ"; cp "$HERE/assemble_final310.sh" "$FZ/assemble_final310.sh"
"$HERE/freeze_es310.sh" 16 --target "$FZ/assemble_final310.sh" --record "$FZ/frozen-shas.txt" > "$FZ/freeze1.out" 2>&1
r1=$?
ok14=$(python3 -I - "$HERE" "$FZ/assemble_final310.sh" <<'PY'
import hashlib, re, sys
from pathlib import Path
here, t = Path(sys.argv[1]), Path(sys.argv[2]).read_text()
want = {"EXPORTER_SHA256": "export_es310.py", "MERGE_SHA256": "merge_es310.py", "DRIVER_SHA256": "drive_es310.py",
        "COVERAGE_SHA256": "coverage_es310.py"}
got = {v: re.search(rf"^{v}=(\S*)$", t, re.M).group(1) for v in want}
print("pins equal the current files" if all(got[v] == hashlib.sha256((here / f).read_bytes()).hexdigest()
      for v, f in want.items()) else f"UNEXPECTED {got}")
PY
)
"$HERE/freeze_es310.sh" 16 --target "$FZ/assemble_final310.sh" --record "$FZ/frozen-shas-2.txt" > "$FZ/freeze2.out" 2>&1
r2=$?
log "14. freeze_es310.sh 16 on a copy: exit $r1 (0 expected), $ok14; a second run: exit $r2 (1 expected): $(tail -1 "$FZ/freeze2.out" | cut -c1-160)"
cmp -s "$HERE/assemble_final310.sh" "$FZ/assemble_final310.sh" && log "14. UNEXPECTED: the copy is unchanged" \
  || log "14. the real assemble_final310.sh is untouched (its pins still empty: $(grep -c '^\(EXPORTER\|MERGE\|DRIVER\|COVERAGE\)_SHA256=""$' "$HERE/assemble_final310.sh") of 4)"
cp "$T/summary.txt" "$OUT"
log "done $(date -u +%FT%TZ)"
cp "$T/summary.txt" "$OUT"
