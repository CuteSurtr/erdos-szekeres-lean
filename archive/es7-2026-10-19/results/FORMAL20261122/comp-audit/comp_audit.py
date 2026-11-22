#!/usr/bin/env python3
"""comp-audit (22 Nov 2026): rebuild the 30x composition Lean files in ONE fresh olean directory and audit it.
Run: python3 -I -B comp_audit.py     (writes only under its own directory; never runs lake; no git writes)
Steps (any failure stops with "refused"/"FAILED", writes result.json and exits 1):
 1. copy the ten record sources to src/ (read-only); each copy's sha256 must equal the record value and the blob at
    git HEAD (read with git show). Composition306 has no record value: git HEAD only.
 2. pins (steps 2 and 4 of assemble_final310.sh; drive_es310.check_library copied, lake NOT re-queried):
    lean-toolchain and lake-manifest sha256 = library.json and closure.json; the LEAN_PATH roots are library.json's
    and equal chain311/lake-lean-path.txt; each of library.json's 4,952 .olean files has its pinned sha256; no lake
    .olean is newer than the 4 Nov freeze; each chain311 .olean has the sha256 of its last build.tsv row (ok).
 3. LEAN_PATH = the 11 roots : chain311/olean : out/olean (wiped); a module file provided by two roots refuses.
 4. the ten files in dependency order, one esr-ag-lcmp-<module> unit at a time (gates and memory rule: README);
    each copy re-hashed right before its compile; rc 0, no error, no sorry, every axiom line standard.
 5. audit/Audit.lean: #check and #print axioms for every name in NAMES, then its environment's module list; each
    module must have exactly one providing root and its pinned sha256 (library.json / build.tsv / this build).
 6. negative control: the two-roots check with zrow/leanz/olean added must name LemmaZ. Report only: the fresh
    .olean sha256 against the older leanz/leanzs/fv304 copies.
Outputs: result.json, closure.tsv, axioms.txt, checks.txt, logs/."""
import datetime, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path

W = Path(__file__).resolve().parent
REPO = Path("/home/jay/research/lean/erdos-szekeres-lean")
REC = REPO / "archive/es7-2026-10-19/results"
CHAIN = REPO / "experiments/omission-compact-checker-2026-11-05/build/chain311"
LEAN = Path("/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean")
SRC, OUT, LOGS, AUD = W / "src", W / "out/olean", W / "logs", W / "audit"
ZROW = Path("/home/jay/research/data/bal186-20261119/zrow")
OLD = [ZROW / "leanz/olean", ZROW / "leanzs/olean", Path("/home/jay/research/data/fv304-20261120/olean")]
YIELD = Path("/home/jay/research/data/agents-20261121/YIELD")
APP = Path(f"/sys/fs/cgroup/user.slice/user-{os.getuid()}.slice/user@{os.getuid()}.service/app.slice")
STD = {"propext", "Classical.choice", "Quot.sound"}
MB = 2 ** 20
MEM_STOP = 2800 * MB  # 80 % of MemoryMax=3500M: the pre-registered stop rule (README)
FREEZE = datetime.datetime(2026, 11, 4, 14, 46, tzinfo=datetime.timezone.utc).timestamp()  # assemble_final310.sh
FILES = [  # (module, record file, record sha256), in dependency order
    ("LemmaZ", "ES305N20261119/LemmaZ.lean", "e6b28efaa80cb2158180daf12dd4ce76cf2b86cc833ae9d79b1c08ffca005d65"),
    ("BalancedBudgetsZ", "ES305N20261119/BalancedBudgetsZ.lean",
     "3e0651a023a58df5a9a0fff4c7d0fc1c5859dfe40b67e9a4e17cdc313224ab1a"),
    ("FixedStatesZ", "ES305N20261119/FixedStatesZ.lean",
     "20945f03e3c2ea7623f8cebcfd92622a3b13cf49c01bb20c863d71d2a2818988"),
    ("LemmaZStar", "ES303N20261120/LemmaZStar.lean", "47bd1f5618ee515b4f9f5c398bd6239b1c650a16dc6aa1ae687b7dafd49fd61c"),
    ("BalancedBudgetsZZs", "ES303N20261120/BalancedBudgetsZZs.lean",
     "7684a1deb0297c7444b1719d0403d1e814ddbab3623ec5c13320294f03278a8e"),
    ("BalancedBudgetsZZsN", "ES303N20261120/BalancedBudgetsZZsN.lean",
     "4cfface86e87798e34e60c98228a757505f13ea491c763a2caa67b73b41203f7"),
    ("Composition305", "ES305N20261119/Composition305.lean",
     "d7d1b2c30d6986ab5104630054e663bb5639e0f67fb3fa03ab1ef5c82b05eeae"),
    ("Composition304", "ES304N20261119/Composition304.lean",
     "a58df4a713d6c37247f9930accbf46d7f9dd31db351bf463b21ff8150f34fe96"),
    ("Composition303", "ES303N20261120/Composition303.lean",
     "bbecd6cf67b12cfa377f7f252923a0b910e27f20ea10e4174d131d358cfe426e"),
    ("Composition306", "ES306N20261119/Composition306.lean", None),  # ES306 records no sha256: git HEAD only
]
NAMES = [  # the task's list, then the theorems the files print themselves
    "OmissionBalancedZ.composition_304_z", "OmissionBalancedZ.composition_305_z",
    "OmissionBalancedZF.composition_304_zf", "OmissionBalancedZF.composition_303_zf",
    "OmissionBalancedZZsF.composition_303_zzsf", "OmissionBalancedZZsF.composition_302_zzsf",
    "OmissionBalancedZZsF.composition_301_zzsf", "OmissionBalancedZZsF.composition_300_zzsf",
    "OmissionBalancedZZsN.composition_302_n54", "OmissionBalancedZZsN.composition_301_n53",
    "composition_304", "composition_303", "composition_305", "composition_306",
    "OmissionZRow.z_row", "OmissionZStarRow.zs_row", "OmissionBalancedZZsN.z_row_of", "OmissionBalancedZZsN.zs_row_of",
    "OmissionBalancedZ.balanced_bound_of_hole_budget_z", "OmissionBalancedZZsF.balanced_bound_of_hole_budget_zzsf",
    "OmissionBalancedZZsN.balanced_bound_of_hole_budget_zzsn",
    "OmissionZRow.Z_eq", "OmissionZStarRow.Zs_eq", "OmissionBalancedZ.feasible_holes_z",
    "OmissionBalancedZF.feasible_holes_zf", "OmissionBalancedZF.balanced_bound_of_hole_budget_zf",
    "OmissionBalancedZZsN.zzsn_55_iff", "avoiding_302", "avoiding_303", "avoiding_304", "avoiding_305",
]
R = {"started_utc": None, "verdict": "running", "steps": {}}
AXRE = re.compile(r"^'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)\s*$", re.M)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def save():
    (W / "result.json").write_text(json.dumps(R, indent=1) + "\n")


def say(msg):
    print(f"comp_audit: {utc()} {msg}", flush=True)


def stop(kind, msg):
    R["verdict"], R["ended_utc"] = f"{kind}: {msg}", utc()
    save()
    say(f"{kind}: {msg}")
    sys.exit(1)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def mpath(m):
    return Path(*m.split(".")).with_suffix(".olean")


def shadowed(roots):
    """{file: [roots]} for every module file (.olean, .olean.server, .olean.private) that two roots provide
    (drive_es310.shadowed_modules, widened to the module-system companions of the v4.24.0 core)."""
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
    """[(name, set of axioms)] of the #print axioms lines; None when a line mentioning axioms does not parse."""
    found = [(m.group(1), {a.strip() for a in (m.group(2) or "").split(",") if a.strip()}) for m in AXRE.finditer(text)]
    return found if len(found) == len(re.findall(r"depends? on (?:any )?axioms", text)) else None


def selftest():
    t = "'a.b' depends on axioms: [propext, Classical.choice, Quot.sound]\n'c' does not depend on any axioms\n"
    assert axioms(t) == [("a.b", STD), ("c", set())]
    assert axioms("'x' depends on axioms: [propext, sorryAx]\n")[0][1] - STD == {"sorryAx"}
    assert axioms("'x' depends on axioms: [propext,\n Quot.sound]\n'y' depends on axioms: [") is None
    with tempfile.TemporaryDirectory(dir=W) as d:
        for sub in ("r1/A", "r2/A"):
            Path(d, sub).mkdir(parents=True)
            Path(d, sub, "M.olean").write_bytes(b"x")
        Path(d, "r2/A/M.olean.tmp").write_bytes(b"x")
        Path(d, "r1/A/N.olean.hash").write_bytes(b"x")
        Path(d, "r2/A/N.olean.hash").write_bytes(b"x")
        assert shadowed([f"{d}/r1", f"{d}/r2"]) == {"A/M.olean": [f"{d}/r1", f"{d}/r2"]}


def sources():
    if SRC.exists():
        shutil.rmtree(SRC)
    SRC.mkdir(parents=True)
    rows = []
    for m, rel, pin in FILES:
        g = subprocess.run(["git", "-C", str(REPO), "show", f"HEAD:archive/es7-2026-10-19/results/{rel}"],
                           capture_output=True)
        if g.returncode:
            stop("refused", f"{rel} is not in git HEAD")
        git = hashlib.sha256(g.stdout).hexdigest()
        dst = SRC / f"{m}.lean"
        shutil.copyfile(REC / rel, dst)
        dst.chmod(0o444)
        h = sha(dst)
        if h != (pin or git) or h != git:
            stop("refused", f"{rel}: copy {h}, record {pin}, git HEAD {git}")
        rows.append({"module": m, "record_file": str(REC / rel), "sha256": h, "record_sha256": pin, "git_head": git})
    R["steps"]["sources"] = rows
    save()
    return {r["module"]: r["sha256"] for r in rows}


def pins():
    t0 = time.time()
    lib = json.loads((CHAIN / "library.json").read_text())
    clo = json.loads((CHAIN / "closure.json").read_text())
    tc, mf = sha(REPO / "lean-toolchain"), sha(REPO / "lake-manifest.json")
    probs = []
    for name, rec in (("closure.json", clo), ("library.json", lib)):
        if rec["lean_toolchain_sha256"] != tc:
            probs.append(f"lean-toolchain differs from {name}")
        if rec["lake_manifest_sha256"] != mf:
            probs.append(f"lake-manifest.json differs from {name}")
    roots = [r.replace("<repo>", str(REPO)).replace("<home>", str(Path.home())) for r in lib["roots"]]
    if roots != (CHAIN / "lake-lean-path.txt").read_text().strip().split(":"):
        probs.append("library.json's roots differ from chain311/lake-lean-path.txt")
    absent = [r for r in roots if not os.path.isdir(r)]  # the Cli root was never built; allowed if nothing is pinned there
    pinned = {roots[i] for i, _ in lib["modules"].values()}
    probs += [f"root {r} is missing but library.json pins modules under it" for r in absent if r in pinned]
    if not set(clo["library_imports"]) <= set(lib["modules"]):
        probs.append("library.json does not cover closure.json's library imports")
    libpin = {m: (roots[i], h) for m, (i, h) in lib["modules"].items()}
    bad = [m for m, (r, h) in libpin.items() if not (Path(r) / mpath(m)).is_file() or sha(Path(r) / mpath(m)) != h]
    if bad:
        probs.append(f"{len(bad)} library .olean files differ from library.json, e.g. {bad[:4]}")
    lake = [r for r in roots if r.startswith(str(REPO / ".lake"))]
    newer = [str(p) for r in lake for p in Path(r).rglob("*.olean") if p.stat().st_mtime >= FREEZE]
    if newer:
        probs.append(f"{len(newer)} lake .olean files are newer than the 4 Nov freeze, e.g. {newer[:3]}")
    lines = (CHAIN / "build.tsv").read_text().splitlines()
    cols, last = lines[0].split("\t"), {}
    for line in lines[1:]:
        row = dict(zip(cols, line.split("\t")))
        last[row["module"]] = row
    chainpin = {}
    for m in clo["modules"]:
        row, f = last.get(m), CHAIN / "olean" / mpath(m)
        if not row or row["verdict"] != "ok":
            probs.append(f"chain311 {m}: last build.tsv row is not ok")
        elif not f.is_file() or sha(f) != row["olean_sha256"]:
            probs.append(f"chain311 {m}: .olean differs from its build.tsv row")
        else:
            chainpin[m] = row["olean_sha256"]
    R["steps"]["pins"] = {"lean_toolchain_sha256": tc, "lake_manifest_sha256": mf, "roots": roots, "absent_roots_no_pins": absent,
                          "library_pinned": len(libpin), "library_written_utc": lib["written"],
                          "library_digest_sha256": lib["digest_sha256"], "lake_oleans_newer_than_freeze": len(newer),
                          "chain311_modules": len(clo["modules"]), "chain311_verified": len(chainpin),
                          "lean_binary_sha256": sha(LEAN), "seconds": round(time.time() - t0, 1), "problems": probs}
    save()
    if probs:
        stop("refused", "; ".join(probs))
    return roots, libpin, chainpin


def tctl():
    m = re.search(r"^Tctl:\s*\+?([0-9.]+)", subprocess.run(["sensors"], capture_output=True, text=True).stdout, re.M)
    return float(m.group(1)) if m else None


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


def gate():
    for i in range(31):
        t, (ag, tot) = tctl(), guard_use()
        if not YIELD.exists() and t is not None and t < 86 and ag + 1500 <= 7000 and tot + 1500 <= 34000:
            return {"tctl": t, "ag_mb": ag, "esr_mb": tot}
        if i == 30:
            stop("refused", f"gate unmet for 30 min: YIELD {YIELD.exists()}, Tctl {t}, ag {ag} MB, esr {tot} MB")
        say(f"waiting: YIELD {YIELD.exists()}, Tctl {t} C, ag {ag} MB, esr {tot} MB")
        time.sleep(60)


def run_unit(job, cwd, src, out, lp):
    """One gated unit; returns the parsed record. Stops on a failed compile or on the memory rule."""
    g = gate()
    log = LOGS / f"{job}.log"
    cmd = ["systemd-run", "--user", "--wait", "--collect", f"--unit=esr-ag-lcmp-{job}", "-p", "CPUQuota=100%",
           "-p", "MemoryMax=3500M", "-p", "MemorySwapMax=0", "-p", "RuntimeMaxSec=7200", "--nice=10",
           f"--working-directory={cwd}", "-E", f"LEAN_PATH={lp}", "-E", "LEAN_NUM_THREADS=1",
           "/bin/sh", str(W / "unit_compile.sh"), str(log), str(out), src]
    say(f"start esr-ag-lcmp-{job} ({g})")
    r = subprocess.run(cmd, capture_output=True, text=True)
    text = log.read_text(errors="replace") if log.exists() else ""
    lean_out = text.split("\tCommand being timed:")[0]
    num = lambda pat: int(m.group(1)) if (m := re.search(pat, text)) else None
    ev = dict(re.findall(r"(\w+) (\d+)", (re.search(r"cgroup memory\.events: (.*)", text) or ["", ""])[1]))
    rec = {"job": job, "gate": g, "systemd_run_rc": r.returncode, "systemd_run_stderr": r.stderr.strip()[-600:],
           "lean_rc": num(r"lean_rc=(\d+)"), "exit_status": num(r"Exit status: (\d+)"),
           "signal": "Command terminated by signal" in text,
           "wall": (re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): (\S+)", text) or [None, None])[1],
           "user_s": float(m.group(1)) if (m := re.search(r"User time \(seconds\): ([0-9.]+)", text)) else None,
           "max_rss_mb": round(num(r"Maximum resident set size \(kbytes\): (\d+)") / 1024) if "Maximum resident" in text else None,
           "cg_peak_mb": round(num(r"cgroup memory\.peak: (\d+)") / MB) if "memory.peak: " in text else None,
           "anon_peak_mb": round(num(r"anon peak \(sampled every 0\.2 s\): (\d+)") / MB) if "anon peak" in text else None,
           "swap_peak": num(r"cgroup memory\.swap\.peak: (\d+)"), "events": ev,
           "errors": re.findall(r"^.*:\d+:\d+: error.*$", lean_out, re.M), "sorry": "sorry" in lean_out,
           "axioms": None if (ax := axioms(lean_out)) is None else [[n, sorted(s)] for n, s in ax],
           "olean": str(out) if out.is_file() else None}
    rec["olean_sha256"] = sha(out) if out.is_file() else None
    say(f"done esr-ag-lcmp-{job}: lean_rc {rec['lean_rc']}, wall {rec['wall']}, max RSS {rec['max_rss_mb']} MB, "
        f"cgroup peak {rec['cg_peak_mb']} MB, anon peak {rec['anon_peak_mb']} MB, events {ev}")
    R["steps"].setdefault("compiles", []).append(rec)
    save()
    if rec["cg_peak_mb"] is None or rec["cg_peak_mb"] * MB >= MEM_STOP or \
            any(int(ev.get(k, 1)) for k in ("high", "max", "oom", "oom_kill")):
        stop("STOPPED by the memory rule", f"{job}: cgroup peak {rec['cg_peak_mb']} MB, events {ev}")
    if (rec["lean_rc"], rec["exit_status"], rec["signal"], rec["errors"], rec["sorry"]) != (0, 0, False, [], False) \
            or rec["olean"] is None or ax is None or any(a - STD for _, a in ax):
        stop("FAILED", f"{job}: see {log} (lean_rc {rec['lean_rc']}, errors {rec['errors'][:2]}, axioms {rec['axioms']})")
    return rec


def main():
    R["started_utc"] = utc()
    selftest()
    srcsha = sources()
    say("sources ok")
    roots, libpin, chainpin = pins()
    say(f"pins ok ({R['steps']['pins']['seconds']} s)")
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    LOGS.mkdir(exist_ok=True)
    lproots = roots + [str(CHAIN / "olean"), str(OUT)]
    lp = ":".join(lproots)
    if (dup := shadowed(lproots)):
        stop("refused", f"modules provided by two roots: {dict(list(dup.items())[:5])}")
    fresh = {}
    for m, _, _ in FILES:
        if sha(SRC / f"{m}.lean") != srcsha[m]:
            stop("refused", f"src/{m}.lean changed after step 1")
        fresh[m] = run_unit(m, SRC, f"{m}.lean", OUT / f"{m}.olean", lp)["olean_sha256"]
    if (dup := shadowed(lproots)):
        stop("refused", f"after the compiles, modules provided by two roots: {dict(list(dup.items())[:5])}")
    if AUD.exists():
        shutil.rmtree(AUD)
    AUD.mkdir()
    (AUD / "Audit.lean").write_text("".join(f"import {m}\n" for m, _, _ in FILES) + "set_option format.width 1000\n"
                                    + "".join(f"#check {n}\n" for n in NAMES)
                                    + "".join(f"#print axioms {n}\n" for n in NAMES)
                                    + "open Lean in\n#eval show CoreM Unit from do\n"
                                    "  for m in (← getEnv).header.moduleNames do\n    IO.println s!\"module {m}\"\n")
    a = run_unit("audit", AUD, "Audit.lean", AUD / "Audit.olean", lp)
    text = (LOGS / "audit.log").read_text().split("\tCommand being timed:")[0]
    msgs = re.split(r"\n(?=\S)", text.strip())  # a wrapped message continues on indented lines
    checks, axl, mods = msgs[:len(NAMES)], msgs[len(NAMES):2 * len(NAMES)], msgs[2 * len(NAMES):]
    probs = [f"#check {n}: {c[:80]!r}" for n, c in zip(NAMES, checks) if not re.match(re.escape(n) + r"[ :]", c)]
    ax = axioms("\n".join(axl))
    if ax is None or [n for n, _ in ax] != NAMES:
        probs.append(f"axiom lines do not match NAMES: {axl[:3]}")
    else:
        probs += [f"{n}: non-standard axioms {sorted(s - STD)}" for n, s in ax if s - STD]
    if not mods or any(not x.startswith("module ") or "\n" in x for x in mods):
        probs.append(f"unexpected messages after the axiom lines: {[x for x in mods if not x.startswith('module ')][:3]}")
    (W / "checks.txt").write_text("\n".join(checks) + "\n")
    (W / "axioms.txt").write_text("\n".join(axl) + "\n")
    rows, comp = [], []
    for x in mods:
        m = x[len("module "):]
        prov = [r for r in lproots if (Path(r) / mpath(m)).is_file()]
        if len(prov) != 1:
            probs.append(f"{m}: provided by {prov}")
            continue
        h = sha(Path(prov[0]) / mpath(m))
        if prov[0] == str(OUT):
            src, ok = "this build", fresh.get(m) == h
        elif prov[0] == str(CHAIN / "olean"):
            src, ok = "chain311 build.tsv", chainpin.get(m) == h
        else:
            src, ok = "library.json", libpin.get(m) == (prov[0], h)
        probs += [] if ok else [f"{m}: sha256 {h} does not match its pin ({src})"]
        rows.append(f"{m}\t{prov[0]}\t{h}\t{src}\t{'ok' if ok else 'MISMATCH'}")
        f = str(Path(prov[0]) / mpath(m))
        comp += [f"{m}{s}\t{sha(f + s)}" for s in (".server", ".private") if os.path.isfile(f + s)]
    (W / "closure.tsv").write_text("module\troot\tolean_sha256\tpin\tstatus\n" + "\n".join(rows) + "\n")
    dupc = shadowed(lproots + [str(OLD[0])])
    control = {"added_root": str(OLD[0]), "refused": "LemmaZ.olean" in dupc, "duplicates": dupc}
    if not control["refused"]:
        probs.append("negative control: the two-roots check did not name LemmaZ.olean")
    older = {f"{d}/{m}.olean": sha(d / f"{m}.olean") == h for m, h in fresh.items() for d in OLD if (d / f"{m}.olean").is_file()}
    R["steps"]["audit"] = {"names": len(NAMES), "modules": len(mods), "closure_rows": len(rows),
                           "closure_tsv_sha256": sha(W / "closure.tsv"), "axioms_txt_sha256": sha(W / "axioms.txt"),
                           "by_root": {r: sum(1 for x in rows if x.split("\t")[1] == r) for r in lproots},
                           "companions": len(comp), "companions_digest": hashlib.sha256("\n".join(comp).encode()).hexdigest(),
                           "negative_control": control, "older_copies_equal": older, "problems": probs}
    if probs:
        stop("FAILED", "; ".join(probs[:6]))
    R["verdict"], R["ended_utc"] = "audit passed", utc()
    save()
    say("audit passed")


if __name__ == "__main__":
    main()
