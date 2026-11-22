#!/usr/bin/env python3
"""fv304-audit driver (22 Nov 2026): closing import audit of FV304 and the combined 304 theorem. Resumable.
Run as a unit (README §9):  python3 -I -B tools/fv4a.py.  Writes only under its work directory; never runs lake; no
git writes (git show only). Each step writes data/step_<name>.json; a step with "ok": true is skipped on a rerun, a
step with problems stops the driver (status.json state FAILED). Child compiles: one unit esr-ag-fv4a-<job> at a time
(1 thread, MemoryMax 4000M, MemorySwapMax 0) running tools/unit_lean.sh; gates and the memory rule: README §4.
Steps:
 pins      check_pins_es304z.py (read only, python3 -I -B) + comp-audit's pin checks (lake roots = library.json,
           no lake .olean newer than the 4 Nov freeze, 196 chain311 .olean = build.tsv) + LemmaZ/BalancedBudgetsZ
           pins + FV304 scripts and record sources = git HEAD
 shadow    no module file provided by two roots on FV304's LEAN_PATH, also with olean/ appended; negative control:
           appending res118/olean must be refused (BalancedBudgetsZ + six CompactChecker symlinks)
 support   CompactChecker.FcatZ / BridgeZ rebuilt off-path (recompile/) from git-tracked copies; byte comparison
 res118    Res118 Rows, LemmaA, Glue, Final, Compose304 rebuilt into olean/ (sources = res118 README §7 sha256)
 audit     src/Audit.lean (import E304Z.Final only): statements, axioms, definitions, module list; no olean
 combined  src/FV4A/Combined.lean -> olean/FV4A/Combined.olean: the combined theorem, its axioms, module list
 records   FV304 records: 8,192 context manifests vs export/src (sha256), structural scan of every E304Z source,
           per-module logs and run.tsv, olean mtime order (every import older than the importer's compile start)
 closure   import closures of audit and combined: providing root, resolved file, sha256, pin class and status
 readonly  files newer than MARKER_START in the repo and in the read-only olean stores
then result.json (verdict, problems, findings)."""
import ast, collections, datetime, hashlib, json, os, re, shutil, subprocess, sys, time
from pathlib import Path

W = Path(__file__).resolve().parent.parent
REPO = Path("/home/jay/research/lean/erdos-szekeres-lean")
EXP = REPO / "experiments/omission-compact-checker-2026-11-05"
CHAIN = EXP / "build/chain311"
FV = Path("/home/jay/research/data/fv304-20261120")
RES = Path("/home/jay/research/data/formalize-20261122/res118")
LEANZ = Path("/home/jay/research/data/bal186-20261119/zrow/leanz/olean")
LEAN = Path("/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean")
SKILL = REPO / ".claude/skills/es-research/scripts"
YIELD = Path("/home/jay/research/data/agents-20261121/YIELD")
APP = Path(f"/sys/fs/cgroup/user.slice/user-{os.getuid()}.slice/user@{os.getuid()}.service/app.slice")
DATA, LOGS, SRC, OUT, RECOMP = W / "data", W / "logs", W / "src", W / "olean", W / "recompile"
MARKER = W / "MARKER_START"
STD = {"propext", "Classical.choice", "Quot.sound"}
MB = 2 ** 20
ANON_STOP_MB = 3200                       # 80 % of MemoryMax=4000M (pre-registered, README §4)
FREEZE = datetime.datetime(2026, 11, 4, 14, 46, tzinfo=datetime.timezone.utc).timestamp()  # assemble_final310.sh
LEMMAZ_PIN = "ef249ba167372ac31f995027299efa1eeddac251ff73e4ef093a990ab02c353c"   # ES305 §7; comp-audit rebuild
BBZ_PIN = "38d8f8aed92e5e2fefbd86bf46607f920eea28dc5b757a5a30e26734b0cbe71a"      # comp-audit rebuild
RES_SRC = {  # res118 README §7, in build order
    "Rows": "d19bbdbd252441324d36e60bd34801a2d7f4b52025a831b802790b01a34e41a8",
    "LemmaA": "dea2773271e556bbfbbf5d1cf27c2ab0dbf7b8f2e98dfd24a163cfc6bd083a85",
    "Glue": "50f9d6c10691f8376edea80f67b1e2ac0e5384718ec4c5017e2e6f7c3ab13a29",
    "Final": "7f9198b7660c2ff6329fe5ac3a640b1efa0e09d68f60b65c263cb3cc2713d83b",
    "Compose304": "e8040287f5be312858f6a625f9b9685627ba0e366c1cb9abbab7161f2b87b699"}
GIT_FILES = {  # repo path -> record pin (None: git HEAD only)
    "experiments/omission-compact-checker-2026-11-05/CompactChecker/FcatZ.lean": None,
    "experiments/omission-compact-checker-2026-11-05/CompactChecker/BridgeZ.lean": None,
    "experiments/omission-compact-checker-2026-11-05/drive_es304z.py": None,
    "experiments/omission-compact-checker-2026-11-05/export_es304z.py": None,
    "experiments/omission-compact-checker-2026-11-05/root_es304z.py": None,
    "experiments/omission-compact-checker-2026-11-05/lean_es304z.sh": None,
    "experiments/omission-compact-checker-2026-11-05/mk_ctx_es304z.py": None,
    "experiments/omission-compact-checker-2026-11-05/check_pins_es304z.py": None,
    "experiments/omission-compact-checker-2026-11-05/drive_es310.py": None,
    "experiments/omission-compact-checker-2026-11-05/export_es310.py": None,
    "archive/es7-2026-10-19/results/ES305N20261119/LemmaZ.lean":
        "e6b28efaa80cb2158180daf12dd4ce76cf2b86cc833ae9d79b1c08ffca005d65",
    "archive/es7-2026-10-19/results/ES305N20261119/BalancedBudgetsZ.lean":
        "3e0651a023a58df5a9a0fff4c7d0fc1c5859dfe40b67e9a4e17cdc313224ab1a"}
FV_ROOTS = (FV / "lean_path.txt").read_text().strip().split(":")
LAKE_ROOTS = FV_ROOTS[:FV_ROOTS.index(str(CHAIN / "olean"))]
CMB_ROOTS = FV_ROOTS + [str(OUT)]
EXPECT = {  # the printed statements must contain these pieces in this order
    "E304Z.Final.excludes_67": ["E304Z.Final.excludes_67 : OmissionBalancedZ.ExcludesHoleBudgetZ 67"],
    "E304Z.Final.forces_304_of_n66_res": ["E304Z.Final.forces_304_of_n66_res", "OmissionZRow.N66Bound 55",
                                          "ErdosSzekeres.Omission.Partition.ResidualBound 118",
                                          ": ErdosSzekeres.ForcesConvexNGon 304 8"],
    "FV4A.forces_304_of_slices_rows_n66": [
        "FV4A.forces_304_of_slices_rows_n66", "OmissionZRow.N66Bound 55", "Res118.BlockValid Res118.rowsP",
        "Res118.BlockValid Res118.rowsQ", "Res118.BlockValid Res118.rowsU", "Res118.BlockValid Res118.rowsA",
        "Res118.ResSliceExcludes [] 33 18", "Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 34 18",
        "Res118.ResSliceExcludes Res118.rowsP 34 19", "Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 35 18",
        "Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19",
        "Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20",
        ": ErdosSzekeres.ForcesConvexNGon 304 8"]}
INFO_EXPECT = {"E304Z.root": ["E304Z.root", "CompactChecker.FFeas CompactChecker.fcatZ 3132 252 67",
                              "(CompactChecker.pmask (CompactChecker.zerosF 252) [])"]}
AXRE = re.compile(r"^'([^'\n]+)' (?:depends on axioms: \[([^\]\n]*)\]|does not depend on any axioms)[ \t]*$", re.M)
TOKENS = [b"sorry", b"admit", b"native_decide", b"ofReduceBool", b"skipKernelTC", b"implemented_by", b"extern",
          b"unsafe", b"axiom ", b"debug.", b"run_cmd", b"run_elab", b"run_meta", b"#eval", b"elab ", b"macro",
          b"syntax", b"@[", b"attribute", b"instance", b"opaque", b"partial"]
FIRST_OK = {b"theorem", b"noncomputable", b"checkF2_feas", b"split_pm", b"set_option", b"--", b"import", b"open",
            b"namespace", b"end", b"#print", b""}
_shacache = {}


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def kst():
    return time.strftime("%F %T")


def say(msg):
    print(f"fv4a {kst()} {msg}", flush=True)
    with open(W / "driver.log", "a") as f:
        f.write(f"{kst()} {msg}\n")


def status(step, state, detail=None):
    (W / "status.json").write_text(json.dumps({"time": kst(), "step": step, "state": state, "detail": detail},
                                              indent=1) + "\n")


def sha(p, cache=True):
    p = str(p)
    if cache and p in _shacache:
        return _shacache[p]
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    if cache:
        _shacache[p] = h.hexdigest()
    return h.hexdigest()


def unanon(s):
    return s.replace("<repo>", str(REPO)).replace("<home>", str(Path.home()))


def mpath(m):
    return Path(*m.split(".")).with_suffix(".olean")


def shadowed(roots):
    """{file: [roots]} for every module file (.olean, .olean.server, .olean.private) that two roots provide
    (comp-audit/comp_audit.py shadowed, = drive_es310.shadowed_modules widened to the v4.24.0 companions)."""
    seen, dup = {}, {}
    for r in roots:
        for dirpath, _, files in os.walk(r):
            for fn in files:
                if fn.endswith((".olean", ".olean.server", ".olean.private")):
                    rel = os.path.relpath(os.path.join(dirpath, fn), r)
                    if rel in seen:
                        dup.setdefault(rel, [seen[rel]]).append(r)
                    else:
                        seen[rel] = r
    return dup


def axioms(text):
    """[(name, set)] of the #print axioms lines; None when a line mentioning axioms does not parse."""
    found = [(m.group(1), {a.strip() for a in (m.group(2) or "").split(",") if a.strip()}) for m in AXRE.finditer(text)]
    return found if len(found) == len(re.findall(r"depends? on (?:any )?axioms", text)) else None


def sections(text):
    """{marker: text} of the Lean output between '=== X' lines (Audit.lean, Combined.lean)."""
    parts, cur = {}, None
    for line in text.split("\tCommand being timed:")[0].splitlines():
        m = re.fullmatch(r"=== (\w+)", line.strip())
        if m:
            cur = m.group(1)
            parts[cur] = []
        elif cur:
            parts[cur].append(line)
    return {k: "\n".join(v) for k, v in parts.items()}


def in_order(s, pieces):
    i = 0
    for p in pieces:
        j = s.find(p, i)
        if j < 0:
            return False
        i = j + len(p)
    return True


def wall_s(text):
    m = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): (\S+)", text)
    if not m:
        return None
    s = 0.0
    for x in m.group(1).split(":"):
        s = s * 60 + float(x)
    return s


def selftest():
    t = "'a.b' depends on axioms: [propext, Classical.choice, Quot.sound]\n'c' does not depend on any axioms\n"
    assert axioms(t) == [("a.b", STD), ("c", set())]
    assert axioms("'x' depends on axioms: [propext, sorryAx]\n")[0][1] - STD == {"sorryAx"}
    assert axioms("'E.ex0' depends on axioms: [propext.olean serialization took 725ms\n, Classical.choice]\n") is None
    s = sections("x\n=== CHECK\na : B\n=== AXIOMS\n'a' does not depend on any axioms\n=== END\n\tCommand being timed: z")
    assert s == {"CHECK": "a : B", "AXIOMS": "'a' does not depend on any axioms", "END": ""}
    assert in_order("f (h : A 1) (g : B) : C 2", ["f", "A 1", "B", ": C 2"]) and not in_order("f : C 2 (h : A 1)", ["A 1", ": C 2"])
    assert wall_s("Elapsed (wall clock) time (h:mm:ss or m:ss): 8:15.47\n") == 495.47
    assert wall_s("Elapsed (wall clock) time (h:mm:ss or m:ss): 1:02:03\n") == 3723.0


# ---------------------------------------------------------------- gates and child units

def tctl():
    m = re.search(r"^Tctl:\s*\+?([0-9.]+)", subprocess.run(["sensors"], capture_output=True, text=True).stdout, re.M)
    return float(m.group(1)) if m else None


def cpu_free():
    r = subprocess.run([str(SKILL / "cpu_free.sh"), "esr,esv"], capture_output=True, text=True)
    try:
        return int(r.stdout.strip())
    except ValueError:
        return -1


def guard_use():
    """MB of anon + shmem + swap (what memguard.sh counts) over esr-ag-*.service and over all esr-*.service."""
    ag = tot = 0
    for d in APP.glob("esr-*.service"):
        try:
            st = dict(l.split() for l in (d / "memory.stat").read_text().splitlines())
            use = (int(st.get("anon", 0)) + int(st.get("shmem", 0)) + int((d / "memory.swap.current").read_text())) // MB
        except (OSError, ValueError):
            continue
        tot += use
        ag += use if d.name.startswith("esr-ag-") else 0
    return ag, tot


def active(unit):
    return subprocess.run(["systemctl", "--user", "is-active", "--quiet", unit]).returncode == 0


def fatal(kind, msg, step="?"):
    status(step, f"{kind}", msg)
    say(f"{kind}: {msg}")
    sys.exit(1)


def gate(job):
    t0 = time.time()
    while True:
        y, t, free, (ag, tot) = YIELD.exists(), tctl(), cpu_free(), guard_use()
        g = {"yield": y, "tctl": t, "cpu_free": free, "ag_mb": ag, "esr_mb": tot}
        if not y and t is not None and t < 86 and free >= 1 and ag + 1000 <= 8000 and tot + 1000 <= 36000:
            return g
        if not y and time.time() - t0 > 45 * 60:
            fatal("refused", f"gate unmet for 45 min before {job}: {g}", job)
        status(job, "waiting at the gate", g)       # YIELD: wait without bound (the driver's RuntimeMaxSec ends it)
        time.sleep(60)


def parse_unit_log(text):
    lean_out = text.split("\tCommand being timed:")[0]
    num = lambda pat: int(m.group(1)) if (m := re.search(pat, text)) else None
    ev = dict(re.findall(r"(\w+) (\d+)", (re.search(r"cgroup memory\.events: (.*)", text) or ["", ""])[1]))
    ax = axioms(lean_out)
    return {"lean_rc": num(r"lean_rc=(\d+)"), "exit_status": num(r"Exit status: (\d+)"),
            "signal": "Command terminated by signal" in text, "wall_s": wall_s(text),
            "user_s": float(m.group(1)) if (m := re.search(r"User time \(seconds\): ([0-9.]+)", text)) else None,
            "max_rss_mb": round(num(r"Maximum resident set size \(kbytes\): (\d+)") / 1024) if "Maximum resident" in text else None,
            "major_faults": num(r"Major \(requiring I/O\) page faults: (\d+)"),
            "cg_peak_mb": round(num(r"cgroup memory\.peak: (\d+)") / MB) if "memory.peak: " in text else None,
            "anon_peak_mb": round(num(r"anon\+shmem peak \(sampled every 0\.2 s\): (\d+)") / MB) if "anon+shmem peak" in text else None,
            "killed_80": "KILLED by the 80 % rule" in text, "events": ev,
            "errors": re.findall(r"^.*:\d+:\d+: error.*$", lean_out, re.M)[:5],
            "sorry": "declaration uses 'sorry'" in lean_out or "sorryAx" in lean_out,
            "axioms": None if ax is None else [[n, sorted(s)] for n, s in ax]}


def lean_ok(rec):
    return (rec["lean_rc"], rec["exit_status"], rec["signal"], rec["errors"], rec["sorry"]) == (0, 0, False, [], False) \
        and rec["axioms"] is not None and all(set(a) <= STD for _, a in rec["axioms"])


def run_unit(job, src, out, lp, runtime=1800):
    """One gated child unit; returns its record. Stops the driver on the memory rule."""
    g = gate(job)
    unit, log = f"esr-ag-fv4a-{job}", LOGS / f"{job}.log"
    while active(unit):                          # a child of an earlier driver run: let it finish, then redo the job
        status(job, "waiting for an earlier unit", unit)
        time.sleep(20)
    srcsha = sha(src, cache=False)
    cmd = ["systemd-run", "--user", "--wait", "--collect", "--quiet", f"--unit={unit}", "-p", "CPUQuota=100%",
           "-p", "MemoryMax=4000M", "-p", "MemorySwapMax=0", "-p", f"RuntimeMaxSec={runtime}", "--nice=10",
           f"--working-directory={W}", "-E", f"LEAN_PATH={lp}", "-E", "LEAN_NUM_THREADS=1",
           "/bin/bash", str(W / "tools/unit_lean.sh"), str(log), str(out) if out else "-", str(SRC), str(src)]
    status(job, "running", {"unit": unit, "gate": g})
    say(f"start {unit} ({src.relative_to(W)}; gate {g})")
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    text = log.read_text(errors="replace") if log.exists() else ""
    rec = {"job": job, "unit": unit, "utc_end": utc(), "seconds": round(time.time() - t0, 1), "gate": g,
           "systemd_run_rc": r.returncode, "systemd_run_stderr": r.stderr.strip()[-600:], "src": str(src),
           "src_sha256": srcsha, **parse_unit_log(text)}
    rec["olean"] = str(out) if out and out.is_file() else None
    rec["olean_sha256"] = sha(out, cache=False) if rec["olean"] else None
    with open(DATA / "units.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")
    say(f"done {unit}: lean_rc {rec['lean_rc']}, wall {rec['wall_s']} s, anon+shmem peak {rec['anon_peak_mb']} MB, "
        f"cgroup peak {rec['cg_peak_mb']} MB, max RSS {rec['max_rss_mb']} MB, events {rec['events']}")
    if rec["anon_peak_mb"] is None or rec["anon_peak_mb"] >= ANON_STOP_MB or rec["killed_80"] or \
            any(int(rec["events"].get(k, 0)) for k in ("oom", "oom_kill")):
        fatal("STOPPED by the memory rule", f"{job}: anon+shmem peak {rec['anon_peak_mb']} MB, events {rec['events']}",
              job)
    return rec


def reuse_or_run(job, src, out, lp, runtime):
    """A step can fail after its compile, in the parsing. Then a rerun parses the same log again instead of repeating
    the compile, provided the last unit record of the job has lean_rc 0, the same source sha256, the log still parses
    to the recorded values, and the olean (if any) still has the recorded sha256."""
    recs = [json.loads(l) for l in (DATA / "units.jsonl").read_text().splitlines()] if (DATA / "units.jsonl").exists() else []
    prev = [r for r in recs if r["job"] == job]
    log = LOGS / f"{job}.log"
    if prev and log.is_file():
        p, now = prev[-1], parse_unit_log(log.read_text(errors="replace"))
        same = all(now[k] == p[k] for k in ("lean_rc", "wall_s", "anon_peak_mb", "cg_peak_mb", "axioms", "events"))
        if same and p["lean_rc"] == 0 and p["src_sha256"] == sha(src, cache=False) and \
                (out is None or (out.is_file() and sha(out, cache=False) == p["olean_sha256"])):
            say(f"{job}: reusing the compile that ended {p['utc_end']} (same source sha256 and log, lean_rc 0)")
            return {**p, "reused": True}
    return run_unit(job, src, out, lp, runtime)


def step(name, fn):
    f = DATA / f"step_{name}.json"
    if f.exists():
        d = json.loads(f.read_text())
        if d.get("ok"):
            say(f"{name}: done before ({d.get('utc_end')}), skipped")
            return d
    status(name, "running")
    say(f"{name}: start")
    t0 = time.time()
    d = fn()
    d.setdefault("problems", [])
    d.setdefault("findings", [])
    d.update(ok=not d["problems"], utc_end=utc(), seconds=round(time.time() - t0, 1))
    f.write_text(json.dumps(d, indent=1) + "\n")
    if d["problems"]:
        fatal("FAILED", f"{name}: {d['problems'][:5]}", name)
    say(f"{name}: ok ({d['seconds']} s; {len(d['findings'])} findings)")
    return d


# ---------------------------------------------------------------- steps

def s_pins():
    probs, finds, out = [], [], {}
    r = subprocess.run(["python3", "-I", "-B", str(EXP / "check_pins_es304z.py")], capture_output=True, text=True)
    try:
        cp = json.loads(r.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        cp = None
    out["check_pins_es304z"] = {"rc": r.returncode, "result": cp, "stderr": r.stderr.strip()[-1000:],
                                "script_sha256": sha(EXP / "check_pins_es304z.py", cache=False)}
    if r.returncode != 0 or not cp or cp.get("problems") or cp.get("route_inputs") != 13 or not cp.get("symlinks_ok") \
            or not all(cp.get("catalogs_equal", {}).values()) or cp["library"].get("library_pinned_verified") != 4952:
        probs.append(f"check_pins_es304z.py: rc {r.returncode}, output {r.stdout.strip()[-400:]}")
    lib = json.loads((CHAIN / "library.json").read_text())
    clo = json.loads((CHAIN / "closure.json").read_text())
    roots = [unanon(x) for x in lib["roots"]]
    if roots != LAKE_ROOTS or roots != (CHAIN / "lake-lean-path.txt").read_text().strip().split(":"):
        probs.append("FV304 lean_path.txt's lake roots differ from library.json / chain311 lake-lean-path.txt")
    newer = [str(p) for rt in LAKE_ROOTS if rt.startswith(str(REPO / ".lake")) and os.path.isdir(rt)
             for p in Path(rt).rglob("*.olean") if p.stat().st_mtime >= FREEZE]
    if newer:
        probs.append(f"{len(newer)} lake .olean files are newer than the 4 Nov freeze, e.g. {newer[:3]}")
    lines = (CHAIN / "build.tsv").read_text().splitlines()
    cols, last = lines[0].split("\t"), {}
    for line in lines[1:]:
        row = dict(zip(cols, line.split("\t")))
        last[row["module"]] = row
    bad = [m for m in clo["modules"] if not (row := last.get(m)) or row["verdict"] != "ok"
           or not (CHAIN / "olean" / mpath(m)).is_file() or sha(CHAIN / "olean" / mpath(m)) != row["olean_sha256"]]
    if bad:
        probs.append(f"chain311: {len(bad)} .olean files differ from their last ok build.tsv row, e.g. {bad[:3]}")
    lz, bbz = sha(LEANZ / "LemmaZ.olean"), sha(FV / "olean/BalancedBudgetsZ.olean")
    if lz != LEMMAZ_PIN:
        probs.append(f"LemmaZ.olean {lz} != pin {LEMMAZ_PIN}")
    if bbz != BBZ_PIN:
        probs.append(f"fv304 BalancedBudgetsZ.olean {bbz} != pin {BBZ_PIN}")
    git = {}
    for rel, pin in GIT_FILES.items():
        g = subprocess.run(["git", "-C", str(REPO), "show", f"HEAD:{rel}"], capture_output=True)
        gh = hashlib.sha256(g.stdout).hexdigest() if g.returncode == 0 else None
        wh = sha(REPO / rel, cache=False)
        git[rel] = {"work": wh, "git_head": gh, "record_pin": pin}
        if gh is None or wh != gh or (pin and wh != pin):
            probs.append(f"{rel}: work {wh[:12]}, git HEAD {gh and gh[:12]}, record pin {pin and pin[:12]}")
    rr = json.loads((EXP / "logs/es311/final311-compact.json").read_text())
    links = {f.name: os.readlink(f) for f in (FV / "olean/CompactChecker").iterdir() if f.is_symlink()}
    plain = sorted(f.name for f in (FV / "olean/CompactChecker").iterdir() if not f.is_symlink())
    ver = subprocess.run([str(LEAN), "--version"], capture_output=True, text=True).stdout.strip()
    out.update(lake_roots=LAKE_ROOTS, lake_oleans_newer_than_freeze=len(newer), library_pinned=len(lib["modules"]),
               library_written_utc=lib["written"], library_digest_sha256=lib["digest_sha256"],
               chain311_modules=len(clo["modules"]), chain311_verified=len(clo["modules"]) - len(bad),
               lemmaz_olean_sha256=lz, balancedbudgetsz_olean_sha256=bbz, git=git,
               route_record={"file": str(EXP / "logs/es311/final311-compact.json"),
                             "sha256": sha(EXP / "logs/es311/final311-compact.json", cache=False),
                             "verified": rr.get("verified"), "route": rr.get("route"),
                             "inputs": {u: v["sha256"] for u, v in rr["chain"]["inputs"].items()}},
               fv304_compactchecker_symlinks=links, fv304_compactchecker_plain=plain,
               lean_binary=str(LEAN), lean_binary_sha256=sha(LEAN, cache=False), lean_version=ver,
               lean_path_txt_sha256=sha(FV / "lean_path.txt", cache=False))
    return {**out, "problems": probs, "findings": finds}


def s_shadow():
    probs = []
    d1, d2 = shadowed(FV_ROOTS), shadowed(CMB_ROOTS)
    neg = shadowed(FV_ROOTS + [str(RES / "olean")])
    want = {"BalancedBudgetsZ.olean"} | {f"CompactChecker/{m}.olean" for m in ("Packed", "Fast", "WordPack", "Split",
                                                                                "Fast2", "Path")}
    if d1:
        probs.append(f"FV304 LEAN_PATH: modules provided by two roots: {dict(list(d1.items())[:5])}")
    if d2:
        probs.append(f"FV304 LEAN_PATH + olean/: modules provided by two roots: {dict(list(d2.items())[:5])}")
    ctl = {"added_root": str(RES / "olean"), "refused": bool(neg), "duplicates": neg,
           "expected_names_present": want <= set(neg)}
    if not (ctl["refused"] and ctl["expected_names_present"]):
        probs.append(f"negative control: appending res118/olean was not refused as expected: {neg}")
    files = {r: sum(1 for _, _, fs in os.walk(r) for f in fs if f.endswith(".olean")) for r in CMB_ROOTS}
    return {"fv304_roots": FV_ROOTS, "combined_roots": CMB_ROOTS, "olean_files_per_root": files,
            "negative_control": ctl, "problems": probs}


def s_support():
    probs, finds, recs = [], [], {}
    (SRC / "CompactChecker").mkdir(parents=True, exist_ok=True)
    (RECOMP / "CompactChecker").mkdir(parents=True, exist_ok=True)
    pins = json.loads((DATA / "step_pins.json").read_text())["git"]
    for m in ("FcatZ", "BridgeZ"):
        rel = f"experiments/omission-compact-checker-2026-11-05/CompactChecker/{m}.lean"
        dst = SRC / f"CompactChecker/{m}.lean"
        if dst.exists():
            dst.chmod(0o644)
        shutil.copyfile(REPO / rel, dst)
        dst.chmod(0o444)
        if sha(dst, cache=False) != pins[rel]["git_head"]:
            probs.append(f"{dst} differs from git HEAD {rel}")
            continue
        rec = run_unit(f"sup-{m}", dst, RECOMP / f"CompactChecker/{m}.olean", ":".join(FV_ROOTS))
        old = sha(FV / f"olean/CompactChecker/{m}.olean", cache=False)
        rec["fv304_olean_sha256"], rec["byte_identical"] = old, rec["olean_sha256"] == old
        recs[f"CompactChecker.{m}"] = rec
        if not lean_ok(rec):
            probs.append(f"rebuild of {m} failed: {rec['errors']} rc {rec['lean_rc']} axioms {rec['axioms']}")
        elif not rec["byte_identical"]:
            finds.append(f"CompactChecker.{m}: off-path rebuild {rec['olean_sha256'][:12]} differs from fv304's "
                         f"{old[:12]} (provenance finding; the closure then marks it DIFFERS)")
    return {"rebuilds": recs, "problems": probs, "findings": finds}


def s_res118():
    probs, finds, recs = [], [], {}
    (OUT / "Res118").mkdir(parents=True, exist_ok=True)
    for m, pin in RES_SRC.items():
        dst = SRC / f"Res118/{m}.lean"
        if dst.exists():
            dst.chmod(0o644)
        shutil.copyfile(RES / f"lean/Res118/{m}.lean", dst)
        dst.chmod(0o444)
        if sha(dst, cache=False) != pin:
            probs.append(f"{dst}: sha256 differs from res118 README §7 ({pin[:12]})")
    if probs:
        return {"problems": probs}
    if (d := shadowed(CMB_ROOTS)):
        return {"problems": [f"before the rebuild, modules provided by two roots: {dict(list(d.items())[:5])}"]}
    for m in RES_SRC:
        if sha(SRC / f"Res118/{m}.lean", cache=False) != RES_SRC[m]:
            return {"problems": [f"src/Res118/{m}.lean changed before its compile"]}
        rec = run_unit(f"res-{m}", SRC / f"Res118/{m}.lean", OUT / f"Res118/{m}.olean", ":".join(CMB_ROOTS))
        old = sha(RES / f"olean/Res118/{m}.olean", cache=False)
        rec["res118_olean_sha256"], rec["byte_identical"] = old, rec["olean_sha256"] == old
        recs[f"Res118.{m}"] = rec
        if not lean_ok(rec):
            return {"rebuilds": recs, "problems": [f"Res118.{m}: rc {rec['lean_rc']}, errors {rec['errors']}, "
                                                    f"axioms {rec['axioms']}"]}
        if not rec["byte_identical"]:
            finds.append(f"Res118.{m}: rebuilt olean {rec['olean_sha256'][:12]} differs from res118's {old[:12]}")
    if (d := shadowed(CMB_ROOTS)):
        probs.append(f"after the rebuild, modules provided by two roots: {dict(list(d.items())[:5])}")
    return {"rebuilds": recs, "problems": probs, "findings": finds}


def check_lean_file(job, rec, names_ax, expect, info):
    """Statements (#check), axiom lines (#print axioms), module list of an Audit/Combined log."""
    probs, finds = [], []
    text = (LOGS / f"{job}.log").read_text(errors="replace")
    sec = sections(text)
    for k in ("CHECK", "AXIOMS", "DEFS", "MODULES", "END"):
        if k not in sec:
            probs.append(f"{job}: section {k} missing in the log")
    if probs:
        return probs, finds, {}
    # a #check message wraps at Lean's message width (format.width does not reach it): join indented continuations
    checks = [re.sub(r"\s+", " ", m).strip() for m in re.split(r"\n(?=\S)", sec["CHECK"].strip()) if m.strip()]
    stm = {}
    for name in list(expect) + list(info):
        hit = [l for l in checks if l.startswith(name + " ")]
        stm[name] = hit[0] if len(hit) == 1 else None
        ok = stm[name] is not None and in_order(stm[name], (expect | info)[name])
        if name == "FV4A.forces_304_of_slices_rows_n66" and stm[name] and "ExcludesHoleBudget" in stm[name]:
            ok = False
        if not ok:
            (probs if name in expect else finds).append(f"{job}: statement of {name} is not as expected: {stm[name]!r}")
    ax = axioms(sec["AXIOMS"])
    if ax is None or [n for n, _ in ax] != names_ax:
        probs.append(f"{job}: axiom lines do not match {names_ax}: {sec['AXIOMS'][:300]!r}")
        ax = []
    probs += [f"{job}: {n} depends on non-standard axioms {sorted(a - STD)}" for n, a in ax if a - STD]
    mods = sec["MODULES"].splitlines()
    if not mods or any(not re.fullmatch(r"module \S+", x) for x in mods):
        probs.append(f"{job}: unexpected lines in the module list: {[x for x in mods if not x.startswith('module ')][:3]}")
    mods = [x[len("module "):] for x in mods if x.startswith("module ")]
    if len(set(mods)) != len(mods):
        probs.append(f"{job}: the module list has duplicates")
    (DATA / f"modules_{job}.txt").write_text("\n".join(mods) + "\n")
    (DATA / f"defs_{job}.txt").write_text(sec["DEFS"] + "\n")
    (DATA / f"axioms_{job}.txt").write_text(sec["AXIOMS"] + "\n")
    (DATA / f"statements_{job}.txt").write_text(sec["CHECK"] + "\n")
    out = {"statements": stm, "axioms": {n: sorted(a) for n, a in ax}, "modules": len(mods),
           "modules_sha256": sha(DATA / f"modules_{job}.txt", cache=False)}
    return probs, finds, out


def s_audit():
    rec = reuse_or_run("audit", SRC / "Audit.lean", None, ":".join(FV_ROOTS), runtime=5400)
    probs = [] if lean_ok(rec) else [f"audit compile: rc {rec['lean_rc']}, errors {rec['errors']}, axioms {rec['axioms']}"]
    p, f, out = check_lean_file("audit", rec, ["E304Z.Final.excludes_67", "E304Z.Final.forces_304_of_n66_res",
                                               "E304Z.root", "E304Z.C260801.ex0", "E304Z.C325201.ex0"],
                                {k: EXPECT[k] for k in ("E304Z.Final.excludes_67", "E304Z.Final.forces_304_of_n66_res")},
                                INFO_EXPECT)
    return {"unit": rec, **out, "problems": probs + p, "findings": f}


def s_combined():
    (OUT / "FV4A").mkdir(parents=True, exist_ok=True)
    if (d := shadowed(CMB_ROOTS)):
        return {"problems": [f"before the compile, modules provided by two roots: {dict(list(d.items())[:5])}"]}
    rec = reuse_or_run("combined", SRC / "FV4A/Combined.lean", OUT / "FV4A/Combined.olean", ":".join(CMB_ROOTS),
                       runtime=5400)
    probs = [] if lean_ok(rec) and rec["olean"] else \
        [f"combined compile: rc {rec['lean_rc']}, errors {rec['errors']}, axioms {rec['axioms']}, olean {rec['olean']}"]
    p, f, out = check_lean_file("combined", rec, ["FV4A.forces_304_of_slices_rows_n66", "Res118.forces_304_of_slices",
                                                  "Res118.residual_bound_118_of_slices"],
                                {"FV4A.forces_304_of_slices_rows_n66": EXPECT["FV4A.forces_304_of_slices_rows_n66"],
                                 "E304Z.Final.excludes_67": EXPECT["E304Z.Final.excludes_67"]}, {})
    if (d := shadowed(CMB_ROOTS)):
        p.append(f"after the compile, modules provided by two roots: {dict(list(d.items())[:5])}")
    return {"unit": rec, **out, "problems": probs + p, "findings": f}


def resolve(mod, roots):
    hits = [Path(r) / mpath(mod) for r in roots if (Path(r) / mpath(mod)).is_file()]
    return hits[0] if len(hits) == 1 else None


def s_records(only=None):                     # only: a set of modules, for a quick test of this code (never in a step)
    probs, finds = [], []
    man, extally, ctxs = {}, collections.Counter(), set()
    for f in sorted((FV / "export/ctx").glob("ctx-*.json")):
        d = json.loads(f.read_text())
        ctxs.add(d["ctx"])
        extally[d["exporter_sha256"]] += 1
        for m in d["modules"]:
            if m["module"] in man:
                probs.append(f"{m['module']} is listed by two context manifests")
            man[m["module"]] = {"ctx": d["ctx"], "file": m["file"], "sha256": m["sha256"], "corrupted": m["corrupted"],
                                "exporter": d["exporter_sha256"], "leaves": m["leaves"]}
    if ctxs != set(range(8192)):
        probs.append(f"context manifests cover {len(ctxs)} contexts, not 0..8191")
    if any(v["corrupted"] for v in man.values()):
        probs.append("a manifest module is marked corrupted")
    cur_exporter = sha(EXP / "export_es304z.py", cache=False)
    if set(extally) - {cur_exporter}:
        pilot = sorted(d for d, v in ((json.loads(f.read_text())["ctx"], json.loads(f.read_text())["exporter_sha256"])
                                      for f in (FV / "export/ctx").glob("ctx-*.json")) if v != cur_exporter)
        finds.append(f"{sum(n for e, n in extally.items() if e != cur_exporter)} contexts {pilot} carry exporter "
                     f"sha256 {[e[:12] for e in extally if e != cur_exporter]} (pilot version, not in git) instead of "
                     f"the git HEAD export_es304z.py {cur_exporter[:12]}; Lean checked their chunks like all others")
    expected = sorted(man) + [f"E304Z.S3_{p}" for p in range(8)] + ["E304Z.Root", "E304Z.Final"]
    if only:
        expected = [m for m in expected if m in only]
    # Final.lean must be drive_es304z.FINAL (the git-tracked template), read with ast (no import, no execution)
    tree = ast.parse((EXP / "drive_es304z.py").read_text())
    final_t = next(n.value.value for n in tree.body if isinstance(n, ast.Assign) and
                   any(getattr(t, "id", None) == "FINAL" for t in n.targets))
    runrows = {}
    for line in (FV / "run.tsv").read_text().splitlines()[1:]:
        c = line.split("\t")
        runrows[c[1]] = {"time": c[0], "leaves": c[2], "lean_rc": c[3], "axiom_lines": c[5], "std_lines": c[6]}
    tok = collections.Counter()
    first, setopts, imports_ext, opens, prints = (collections.Counter() for _ in range(5))
    bycount = bydk = 0
    mtime_cache, rows, scan_bad = {}, {}, []
    for mod in expected:
        stem = mod.split(".")[-1]
        src = FV / "export/src/E304Z" / f"{stem}.lean"
        data = src.read_bytes()
        h = hashlib.sha256(data).hexdigest()
        r = {"module": mod, "source_sha256": h, "source_bytes": len(data)}
        if mod in man:
            r["source_check"] = "manifest" if h == man[mod]["sha256"] else "MISMATCH"
        elif stem == "Final":
            r["source_check"] = "template" if data == final_t.encode() else "MISMATCH"
        else:
            r["source_check"] = "recorded"
        if r["source_check"] == "MISMATCH":
            probs.append(f"{mod}: source sha256 {h[:12]} differs from its manifest/template")
        imps, pnames, ns = [], [], None
        if stem != "Final":                    # Final.lean is compared byte for byte with the template instead
            for t in TOKENS:
                if (n := data.count(t)):
                    tok[t.decode()] += n
                    scan_bad.append(f"{mod}: {t.decode()!r} x{n}")
            bycount += data.count(b"by ")
            bydk += data.count(b"by decide +kernel")
            for line in data.split(b"\n"):
                ft = line.split(b" ", 1)[0] if not line.startswith(b" ") else (line.split() or [b""])[0]
                first[ft.decode(errors="replace")] += 1
                if ft not in FIRST_OK:
                    scan_bad.append(f"{mod}: line starts with {ft[:40]!r}")
                if line.startswith(b"set_option "):
                    setopts[line.decode()] += 1
                elif line.startswith(b"import "):
                    imps.append(line.split()[1].decode())
                elif line.startswith(b"open "):
                    opens[line.decode()] += 1
                elif line.startswith(b"#print"):
                    prints[re.sub(r"\S+$", "<name>", line.decode())] += 1
                    pnames.append(line.split()[-1].decode())
                elif line.startswith(b"namespace "):
                    ns = line.split()[1].decode()
        else:
            imps = [l.split()[1] for l in final_t.splitlines() if l.startswith("import ")]
            pnames = [l.split()[-1] for l in final_t.splitlines() if l.startswith("#print axioms")]
            ns = next(l.split()[1] for l in final_t.splitlines() if l.startswith("namespace "))
        full = [f"{ns}.{n}" if ns else n for n in pnames]
        for i in imps:
            if not i.startswith("E304Z."):
                imports_ext[i] += 1
        # log and run.tsv
        lg = next((FV / "logs/lean" / n for n in (f"{stem}.log", f"c-{stem}.log", f"s-{stem}.log")
                   if (FV / "logs/lean" / n).is_file()), None)
        txt = lg.read_text(errors="replace") if lg else ""
        rc = [int(x) for x in re.findall(r"^lean_rc=(\d+)$", txt, re.M)]
        ax = axioms(txt)
        r.update(log=lg.name if lg else None, lean_rc=rc[-1] if rc else None,
                 axiom_lines=txt.count("depends on axioms"),
                 axioms_std=None if ax is None else all(a <= STD for _, a in ax),
                 garbled=ax is None, printed=[n for n, _ in ax] if ax else [], print_names=full,
                 log_errors=len(re.findall(r"^.*:\d+:\d+: error", txt, re.M)), run_tsv=runrows.get(mod))
        # every `#print axioms X` of the source must show up as one well-formed line; otherwise re-print it (step
        # reprint) from the olean: the profiler's stderr lines are sometimes spliced into the axiom line
        r["needs_reprint"] = r["garbled"] or sorted(r["printed"]) != sorted(full)
        if r["lean_rc"] != 0 or r["log_errors"] or r["axioms_std"] is False or not full:
            probs.append(f"{mod}: log {r['log']} lean_rc {r['lean_rc']}, errors {r['log_errors']}, axiom lines "
                         f"{r['axiom_lines']}, standard {r['axioms_std']}, #print names {full}")
        # olean mtime order: every import older than this module's compile start (olean mtime - wall)
        ol = FV / "olean/E304Z" / f"{stem}.olean"
        st = ol.stat()
        w = wall_s(txt)
        r.update(olean_mtime=st.st_mtime, olean_bytes=st.st_size, wall_s=w,
                 compile_start=st.st_mtime - (w or 0.0))
        late = []
        for i in imps:
            if i not in mtime_cache:
                p = resolve(i, FV_ROOTS)
                mtime_cache[i] = os.stat(p).st_mtime if p else None
            if mtime_cache[i] is None:
                late.append(f"{i} (not found once on the path)")
            elif mtime_cache[i] > r["compile_start"] + 1.0:
                late.append(i)
        r["imports"], r["late_imports"] = len(imps), late[:5]
        if late:
            probs.append(f"{mod}: imports newer than its compile start: {late[:3]}")
        rows[mod] = r
    newest = max(rows.values(), key=lambda x: x["olean_mtime"])["module"]
    if newest != "E304Z.Final":
        probs.append(f"the newest E304Z olean of the closure set is {newest}, not E304Z.Final")
    if scan_bad:
        probs.append(f"source scan: {len(scan_bad)} hits, e.g. {scan_bad[:5]}")
    if bycount != bydk:
        finds.append(f"'by ' occurs {bycount} times, 'by decide +kernel' {bydk} times")
    garbled = [m for m, r in rows.items() if r["needs_reprint"]]
    norow = [m for m in expected if m not in runrows]
    if garbled:
        finds.append(f"{len(garbled)} logs lack a well-formed axiom line for the source's #print (profiler stderr "
                     f"spliced into it): {garbled[:10]}; re-printed from the oleans in step reprint")
    silent = [m for m, r in rows.items() if r["run_tsv"] and r["run_tsv"]["axiom_lines"] == "0"]
    if silent:
        finds.append(f"FV304's driver accepted {silent} with 0 axiom lines and no ALERT (drive_es304z.verdict counts "
                     f"'depends on axioms' substrings; a split line counts 0 = 0 standard)")
    if norow:
        finds.append(f"{len(norow)} modules have no run.tsv row (pilot compiles or driver restarts): {norow[:20]}; "
                     f"their per-module logs were used")
    extra = sorted(p.stem for p in (FV / "olean/E304Z").glob("*.olean") if f"E304Z.{p.stem}" not in rows)
    with open(DATA / "e304z_modules.tsv", "w") as f:
        cols = ["module", "source_sha256", "source_check", "log", "lean_rc", "axiom_lines", "axioms_std", "garbled",
                "needs_reprint", "print_names", "olean_mtime", "wall_s", "compile_start", "imports", "late_imports"]
        f.write("\t".join(cols) + "\n")
        for m in expected:
            f.write("\t".join(str(rows[m].get(c)) for c in cols) + "\n")
    (DATA / "e304z_modules.json").write_text(json.dumps(rows) + "\n")
    return {"contexts": len(ctxs), "manifest_modules": len(man), "expected_e304z_modules": len(expected),
            "exporter_tally": dict(extally), "sources_checked": len(rows),
            "source_check_tally": dict(collections.Counter(r["source_check"] for r in rows.values())),
            "token_hits": dict(tok), "first_tokens": dict(first), "set_option_lines": dict(setopts),
            "non_e304z_imports": dict(imports_ext), "open_lines": dict(opens), "print_lines": dict(prints),
            "by_count": bycount, "by_decide_kernel_count": bydk, "needs_reprint": garbled, "silent_zero_axiom_rows": silent,
            "no_run_tsv_row": norow, "pilot_or_extra_oleans_not_expected": extra,
            "e304z_modules_tsv_sha256": sha(DATA / "e304z_modules.tsv", cache=False),
            "newest_olean": newest, "problems": probs, "findings": finds}


def s_reprint():
    """#print axioms, from the existing oleans, of every module whose log lacks a well-formed axiom line."""
    rows = json.loads((DATA / "e304z_modules.json").read_text())
    need = [m for m, r in rows.items() if r["needs_reprint"]]
    names = [n for m in need for n in rows[m]["print_names"]]
    if not need:
        return {"modules": [], "axioms": {}}
    src = SRC / "Reprint.lean"
    if src.exists():
        src.chmod(0o644)
    src.write_text("-- fv304-audit: axioms of the FV304 modules whose compile log has no well-formed axiom line, "
                   "re-printed from their oleans (read only; no olean written)\n"
                   + "".join(f"import {m}\n" for m in need) + "set_option Elab.async false\n#eval IO.println \"=== AXIOMS\"\n"
                   + "".join(f"#print axioms {n}\n" for n in names) + "#eval IO.println \"=== END\"\n")
    rec = reuse_or_run("reprint", src, None, ":".join(FV_ROOTS), 1800)
    probs = [] if lean_ok(rec) else [f"reprint compile: rc {rec['lean_rc']}, errors {rec['errors']}, axioms {rec['axioms']}"]
    sec = sections((LOGS / "reprint.log").read_text(errors="replace"))
    ax = axioms(sec.get("AXIOMS", ""))
    if ax is None or [n for n, _ in ax] != names:
        probs.append(f"reprint: axiom lines do not match {names}: {sec.get('AXIOMS', '')[:300]!r}")
        ax = []
    probs += [f"reprint: {n} depends on non-standard axioms {sorted(a - STD)}" for n, a in ax if a - STD]
    return {"modules": need, "source_sha256": sha(src, cache=False), "unit": rec,
            "axioms": {n: sorted(a) for n, a in ax}, "problems": probs}


def s_closure():
    probs, finds, out = [], [], {}
    lib = json.loads((CHAIN / "library.json").read_text())
    roots = [unanon(x) for x in lib["roots"]]
    libpin = {m: (roots[i], h) for m, (i, h) in lib["modules"].items()}
    lines = (CHAIN / "build.tsv").read_text().splitlines()
    cols, chainpin = lines[0].split("\t"), {}
    for line in lines[1:]:
        row = dict(zip(cols, line.split("\t")))
        if row["verdict"] == "ok":
            chainpin[row["module"]] = row["olean_sha256"]
        else:
            chainpin.pop(row["module"], None)
    rr = json.loads((EXP / "logs/es311/final311-compact.json").read_text())
    route = {"CompactChecker." + u.split("/", 1)[1].replace("/", "."): v["sha256"]
             for u, v in rr["chain"]["inputs"].items() if u.startswith("CompactChecker/")}
    sup = {m: r["olean_sha256"] for m, r in json.loads((DATA / "step_support.json").read_text())["rebuilds"].items()}
    built = {m: r["olean_sha256"] for m, r in json.loads((DATA / "step_res118.json").read_text())["rebuilds"].items()}
    built["FV4A.Combined"] = json.loads((DATA / "step_combined.json").read_text())["unit"]["olean_sha256"]
    e304 = json.loads((DATA / "e304z_modules.json").read_text())
    reprinted = {**json.loads((DATA / "step_audit.json").read_text())["axioms"],
                 **json.loads((DATA / "step_reprint.json").read_text())["axioms"]}
    ccdir = str(EXP / "build/CompactChecker") + "/"

    def classify(m, root, h, real):
        if root in LAKE_ROOTS:
            p = libpin.get(m)
            return "library.json", "ok" if p == (root, h) else ("MISMATCH" if p else "UNPINNED")
        if root == str(CHAIN / "olean"):
            p = chainpin.get(m)
            return "chain311 build.tsv", "ok" if p == h else ("MISMATCH" if p else "UNPINNED")
        if root == str(LEANZ):
            return "ES305 pin = comp-audit rebuild", "ok" if m == "LemmaZ" and h == LEMMAZ_PIN else "MISMATCH"
        if root == str(FV / "olean"):
            if m in route:
                return "311 route record", "ok" if h == route[m] and real.startswith(ccdir) else "MISMATCH"
            if m in sup:
                return "rebuilt here from git HEAD source", "ok" if h == sup[m] else "DIFFERS"
            if m == "BalancedBudgetsZ":
                return "comp-audit rebuild", "ok" if h == BBZ_PIN else "MISMATCH"
            if m in e304:
                r = e304[m]
                bad = r["source_check"] == "MISMATCH" or r["lean_rc"] != 0 or r["late_imports"] or r["axioms_std"] is False
                if r["needs_reprint"]:
                    bad = bad or any(n not in reprinted or set(reprinted[n]) - STD for n in r["print_names"])
                return "first recorded here (FV304 run.tsv has no hash)", "FLAG" if bad else "ok"
            return "none", "UNPINNED"
        if root == str(OUT):
            return "this build", "ok" if built.get(m) == h else "MISMATCH"
        return "none", "UNPINNED"

    sets = {}
    for job, roots_l in (("audit", FV_ROOTS), ("combined", CMB_ROOTS)):
        mods = (DATA / f"modules_{job}.txt").read_text().split()
        if job == "combined":
            mods = mods + ["FV4A.Combined"]
        rows, bad = [], []
        for m in mods:
            prov = [r for r in roots_l if (Path(r) / mpath(m)).is_file()]
            if len(prov) != 1:
                bad.append(f"{m}: provided by {prov}")
                continue
            f = Path(prov[0]) / mpath(m)
            real, h = str(f.resolve()), sha(f)
            cls, st = classify(m, prov[0], h, real)
            rows.append((m, prov[0], real, h, cls, st))
        tally = collections.Counter((c, s) for *_, c, s in rows)
        hard = [f"{m} ({c}: {s})" for m, _, _, _, c, s in rows if s not in ("ok", "DIFFERS")]
        probs += [f"{job}: {x}" for x in bad + hard[:20]]
        if any(s == "DIFFERS" for *_, s in rows):
            finds.append(f"{job}: support olean(s) differ from their off-path rebuild: "
                         f"{[m for m, *_, s in rows if s == 'DIFFERS']}")
        e = {m for m, *_ in rows if m.startswith("E304Z.")}
        want = set(e304)
        if e != want:
            probs.append(f"{job}: E304Z modules in the closure differ from the expected set: missing "
                         f"{sorted(want - e)[:5]}, extra {sorted(e - want)[:5]}")
        tsv = DATA / f"closure_{job}.tsv"
        with open(tsv, "w") as fh:
            fh.write("module\troot\tfile\tolean_sha256\tpin\tstatus\n")
            for r in rows:
                fh.write("\t".join(r) + "\n")
        dig = lambda sel: hashlib.sha256("".join(f"{m}\t{h}\n" for m, _, _, h, _, _ in sorted(rows) if sel(m)).encode()).hexdigest()
        sets[job] = set(mods)
        out[job] = {"modules": len(rows), "tsv": str(tsv), "tsv_sha256": sha(tsv, cache=False),
                    "by_root": dict(collections.Counter(r for _, r, *_ in rows)),
                    "pin_status": {f"{c} | {s}": n for (c, s), n in sorted(tally.items())},
                    "digest_all": dig(lambda m: True), "digest_e304z": dig(lambda m: m.startswith("E304Z.")),
                    "e304z_modules": len(e)}
    out["combined_minus_audit"] = sorted(sets["combined"] - sets["audit"])
    out["audit_minus_combined"] = sorted(sets["audit"] - sets["combined"])
    if out["audit_minus_combined"]:
        probs.append(f"modules of the E304Z.Final closure missing from the combined closure: {out['audit_minus_combined'][:5]}")
    return {**out, "problems": probs, "findings": finds}


def s_readonly():
    probs, finds, areas = [], [], {}
    ro = {"repo .lake": REPO / ".lake", "chain311/olean": CHAIN / "olean", "build/CompactChecker": EXP / "build/CompactChecker",
          "build/ext": EXP / "build/ext", "experiments dir (incl. __pycache__)": EXP, "zrow/leanz/olean": LEANZ,
          "fv304-20261120": FV, "res118": RES, "toolchain v4.24.0": LEAN.parent.parent}
    for name, d in list(ro.items()) + [("repo (all)", REPO)]:
        r = subprocess.run(["find", str(d), "-newer", str(MARKER), "-type", "f"], capture_output=True, text=True)
        hits = [x for x in r.stdout.splitlines() if x]
        areas[name] = {"dir": str(d), "newer_than_marker": len(hits), "examples": hits[:20]}
        if name in ro and hits:
            probs.append(f"{name}: {len(hits)} files newer than the marker, e.g. {hits[:3]}")
    if areas["repo (all)"]["newer_than_marker"]:
        finds.append(f"repo: {areas['repo (all)']['newer_than_marker']} files newer than the marker outside the "
                     f"read-only stores (not written by this audit, which has no repo writes): "
                     f"{areas['repo (all)']['examples'][:8]}")
    return {"marker": str(MARKER), "marker_mtime": MARKER.stat().st_mtime, "areas": areas, "problems": probs,
            "findings": finds}


def main():
    for d in (DATA, LOGS, SRC, OUT, RECOMP):
        d.mkdir(parents=True, exist_ok=True)
    selftest()
    say(f"driver start (pid {os.getpid()})")
    res = {}
    for name, fn in (("pins", s_pins), ("shadow", s_shadow), ("support", s_support), ("res118", s_res118),
                     ("audit", s_audit), ("combined", s_combined), ("records", s_records), ("reprint", s_reprint),
                     ("closure", s_closure), ("readonly", s_readonly)):
        t0 = time.time()                         # every step starts only without YIELD and below 86 C (house rule)
        while YIELD.exists() or (t := tctl()) is None or t >= 86:
            if not YIELD.exists() and time.time() - t0 > 45 * 60:
                fatal("refused", f"Tctl {t} C >= 86 for 45 min before step {name}", name)
            status(name, "paused before the step", {"yield": YIELD.exists(), "tctl": t})
            time.sleep(60)
        res[name] = step(name, fn)
    findings = [f"{k}: {x}" for k, v in res.items() for x in v.get("findings", [])]
    result = {"verdict": "audit passed", "utc": utc(), "findings": findings,
              "steps": {k: {"ok": v["ok"], "utc_end": v["utc_end"], "seconds": v["seconds"]} for k, v in res.items()},
              "statements": {**res["audit"]["statements"], **res["combined"]["statements"]},
              "axioms": {**res["audit"]["axioms"], **res["reprint"]["axioms"], **res["combined"]["axioms"]},
              "closure": {k: res["closure"][k] for k in ("audit", "combined")},
              "combined_olean_sha256": res["combined"]["unit"]["olean_sha256"],
              "units": {r["job"]: {k: r[k] for k in ("wall_s", "anon_peak_mb", "cg_peak_mb", "max_rss_mb", "events")}
                        for r in map(json.loads, (DATA / "units.jsonl").read_text().splitlines())}}
    (W / "result.json").write_text(json.dumps(result, indent=1) + "\n")
    status("done", "audit passed", {"findings": len(findings)})
    say(f"audit passed ({len(findings)} findings); result.json written")


if __name__ == "__main__":
    main()
