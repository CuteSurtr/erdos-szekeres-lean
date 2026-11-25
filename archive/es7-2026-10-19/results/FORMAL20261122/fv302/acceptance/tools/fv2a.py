#!/usr/bin/env python3
"""fv302-audit (25 Nov 2026): acceptance of FV302 (fv302-20261124/PLAN.md "Pre-registration", items 1-4) plus a
forbidden-token scan of the join sources, the olean build order and a plain list of deviations. Read-only on the
campaign and on the olean stores; writes only this folder (data/, result.json). Run in a unit (README).
Steps (each writes data/step_<name>.json; a rerun skips steps with "ok": true unless named on the command line):
  item1  E302ZZ.Final: lean_rc 0; both `#print axioms` lines exactly the standard three (profiler fragment
         stripped); Final.lean byte-equal to drive302.py's FINAL template (read with ast, never imported)
  item2  32,618 manifests: gz_sha256 = contexts302.jsonl, one exporter sha256 (= pins-launch.sha256), leaves sum
         43,967,444, every min_margin >= 1 with minimum 1, lean_test_failures 0; every chunk source sha256 = manifest
  item3  run.tsv: last row of every module lean_rc 0 and axiom_lines = std_lines; axiom_audit.py's rule over every
         module log (standard axioms only, lean_rc=0, no sorryAx/ofReduceBool)
  scan   forbidden tokens in the join sources (S_*, P_*, Root, Final, FinalTest) and in src/CompactChecker/*.lean;
         the chunk sources were shape-checked by the exporter (export_es310's 311 line-shape check)
  item4  import closure = the module list printed by logs/Audit302.log: exactly one provider per module on the
         compile LEAN_PATH, olean sha256; E302ZZ.* and the two new CompactChecker modules from the FV302 olean root;
         every other module equal (file and sha256) to the audited closure combined/data/closure2.tsv
  order  every E302ZZ olean is newer than the E302ZZ oleans its source imports
Usage: python3 -I -B tools/fv2a.py [STEP ...]"""
import ast, hashlib, json, mmap, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

A = Path(__file__).resolve().parent.parent
W = Path("/home/jay/research/data/fv302-20261124")
C = Path("/home/jay/research/data/formalize-20261122/combined")
OLEAN, SRC, CTX = W / "olean", W / "export/src", W / "export/ctx"
STD = "depends on axioms: [propext, Classical.choice, Quot.sound]"
FRAG = re.compile(r"\.olean serialization took [0-9.]+m?s\n")
N_CTX, LEAVES = 32618, 43967444
FORBID = re.compile(r"\b(sorry|admit|axiom|native_decide|ofReduceBool|ofReduceNat|implemented_by|extern|unsafe|opaque"
                    r"|partial|run_cmd|run_tac|run_elab|macro|syntax|elab|macro_rules|initialize)\b|#exit|skipKernelTC"
                    r"|set_option\s+debug|@\[csimp")
BUF = 1 << 22


def sha(path):
    """sha256 with O_DIRECT reads into a page-aligned buffer (no page cache charged); buffered fallback."""
    mm = mmap.mmap(-1, BUF); mv = memoryview(mm); h = hashlib.sha256(); size = os.stat(path).st_size; done = 0
    try:
        fd = os.open(path, os.O_RDONLY | os.O_DIRECT)
        try:
            while done < size:
                n = os.readv(fd, [mm])
                if n <= 0: break
                h.update(mv[:min(n, size - done)]); done += n
        finally:
            os.close(fd)
        if done >= size:
            return h.hexdigest()
    except OSError:
        pass
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(BUF), b""): h.update(b)
    return h.hexdigest()


def hash_many(paths, jobs=3):
    with ThreadPoolExecutor(jobs) as ex:
        return dict(zip(paths, ex.map(sha, paths)))


def axiom_ok(text):
    t = FRAG.sub("", text)
    rc = [l[8:] for l in t.splitlines() if l.startswith("lean_rc=")]
    ax = [l for l in t.splitlines() if "depends on axioms" in l]
    return rc[-1:] == ["0"] and bool(ax) and all(l.endswith(STD) for l in ax) and "sorryAx" not in t \
        and "ofReduceBool" not in t, ax


def item1():
    p = []
    log = (W / "logs/lean/Final.log").read_text(errors="replace")
    ok, ax = axiom_ok(log)
    if not ok: p.append("Final.log: lean_rc/axioms not standard")
    for name in ("E302ZZ.Final.excludes_69", "E302ZZ.Final.forces_302_of_n54_res"):
        if not any(l.startswith(f"'{name}' {STD}") for l in FRAG.sub("", log).splitlines()):
            p.append(f"no standard axiom line for {name}")
    tree = ast.parse((W / "tools/drive302.py").read_text())
    tmpl = [n.value.value for n in tree.body if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "FINAL"
            for t in n.targets) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str)]
    src = (SRC / "E302ZZ/Final.lean").read_bytes()
    if len(tmpl) != 1 or tmpl[0].encode() != src: p.append("Final.lean differs from the FINAL template")
    return {"axiom_lines": ax, "final_sha256": hashlib.sha256(src).hexdigest(), "problems": p}


def item2():
    p = []
    ctxs = {}
    for line in open(W / "contexts302.jsonl"):
        d = json.loads(line); ctxs[d["ctx"]] = d["gz_sha256"]
    files = sorted(CTX.glob("ctx-*.json"))
    exporters, leaves, margins, fails, mods = set(), 0, [], 0, []
    for f in files:
        d = json.loads(f.read_text())
        if ctxs.get(d["ctx"]) != d["gz_sha256"]: p.append(f"{f.name}: gz_sha256 differs from contexts302.jsonl")
        exporters.add(d["exporter_sha256"]); leaves += d["stats"]["leaves"]; margins.append(d["stats"]["min_margin"])
        fails += d["stats"].get("lean_test_failures", 0)
        mods += [(m["module"], m["file"], m["sha256"]) for m in d["modules"]]
    pin = [l.split()[0] for l in open(W / "pins-launch.sha256") if l.strip().endswith("export302.py")]
    if len(files) != N_CTX: p.append(f"{len(files)} manifests, expected {N_CTX}")
    if exporters != set(pin): p.append(f"exporter sha256 {sorted(exporters)} != pin {pin}")
    if leaves != LEAVES: p.append(f"leaves {leaves} != {LEAVES}")
    if min(margins) != 1 or any(m < 1 for m in margins): p.append(f"min margin {min(margins)}")
    if fails: p.append(f"lean_test_failures {fails}")
    hs = hash_many([str(W / "export" / f) for _, f, _ in mods])
    bad = [m for m, f, h in mods if hs[str(W / "export" / f)] != h]
    if bad: p.append(f"{len(bad)} chunk sources differ from their manifest sha256, e.g. {bad[:3]}")
    return {"manifests": len(files), "chunk_modules": len(mods), "leaves": leaves, "min_margin": min(margins),
            "exporters": sorted(exporters), "problems": p}


def item3():
    p = []
    rows = {}
    lines = (W / "run.tsv").read_text().splitlines()
    head = lines[0].split("\t")
    for l in lines[1:]:
        r = dict(zip(head, l.split("\t"))); rows[r["module"]] = r
    explained = []  # drive302 counts a profiler-split axiom line as non-standard; the log audit decides (deviation 1)
    for m, r in rows.items():
        if r["lean_rc"] != "0":
            p.append(f"run.tsv {m}: lean_rc {r['lean_rc']}")
        elif r["axiom_lines"] != r["std_lines"]:
            lg = W / "logs/lean" / (m.split(".", 1)[1] + ".log")
            if lg.exists() and axiom_ok(lg.read_text(errors="replace"))[0]:
                explained.append(m)
            else:
                p.append(f"run.tsv {m}: axiom_lines {r['axiom_lines']} != std_lines {r['std_lines']} and the log fails")
    adopted = sorted(m for m, r in rows.items() if r["leaves"] == "-1")
    logs = sorted((W / "logs/lean").glob("*.log"))
    bad = [str(l.name) for l in logs if not axiom_ok(l.read_text(errors="replace"))[0]]
    if bad: p.append(f"{len(bad)} module logs fail the axiom rule, e.g. {bad[:5]}")
    alerts = sum(1 for l in open(W / "logs/driver.log") if "ALERT" in l)
    return {"run_rows": len(rows), "logs": len(logs), "adopted_leaves_minus1": adopted, "driver_alerts": alerts,
            "split_axiom_lines_explained_by_log_audit": explained, "problems": p}


def scan():
    p = []
    joins = [f for f in (SRC / "E302ZZ").glob("*.lean") if not re.match(r"C\d+\.lean$", f.name)]
    files = joins + sorted((W / "src/CompactChecker").glob("*.lean"))
    for f in files:
        for i, line in enumerate(f.read_text(errors="replace").splitlines(), 1):
            code = line.split("--")[0]
            if code.lstrip().startswith("#print axioms"): continue
            m = FORBID.search(code)
            if m: p.append(f"{f.name}:{i}: {m.group(0)!r} in {line.strip()[:120]}")
    return {"files": len(files), "joins": sorted(f.name for f in joins), "problems": p}


def lean_path():
    out = subprocess.run(["bash", "-c", f". {C}/tools/env2.sh; printf %s \"$LEAN_PATH\""], capture_output=True,
                         text=True, check=True).stdout
    return [str(OLEAN)] + [r for r in out.split(":") if r]


def item4():
    p = []
    log = (A / "logs/Audit302.log").read_text(errors="replace")
    if not log.rstrip().splitlines() or "lean_rc=0" not in log: p.append("Audit302.log missing or lean_rc != 0")
    mods = [l[7:].strip() for l in log.splitlines() if l.startswith("module ")]
    roots = lean_path()
    pins = {}
    lines = (C / "data/closure2.tsv").read_text().splitlines()
    for l in lines[1:]:
        m, root, f, h, pin, st = l.split("\t"); pins[m] = (f, h)
    prov, files, shared = {}, {}, []
    for m in mods:
        rel = m.replace(".", "/") + ".olean"
        have = [r for r in roots if os.path.isfile(os.path.join(r, rel))]
        real = sorted({os.path.realpath(os.path.join(r, rel)) for r in have})  # a symlink and its target are one file
        prov[m] = have
        if len(real) != 1: p.append(f"{m}: {len(real)} distinct provider files {real}")
        elif len(have) > 1: shared.append(f"{m}: one file {real[0]} reached from {len(have)} roots")
        if have: files[m] = os.path.join(have[0], rel)   # Lean takes the first root
    hs = hash_many(list(files.values()))
    rows, classes = [], {}
    for m in mods:
        f = files.get(m); h = hs.get(f)
        if m.startswith("E302ZZ.") or m in ("CompactChecker.FcatZZs16", "CompactChecker.BridgeZZs16"):
            cls = "fv302 (this campaign)"
            if not f or not f.startswith(str(OLEAN) + "/"): p.append(f"{m}: not from the FV302 olean root")
        elif m in pins:
            cls = "combined closure2"
            pf, ph = pins[m]
            if (os.path.realpath(f), h) != (os.path.realpath(pf), ph): p.append(f"{m}: {f} {h} differs from closure2 {pins[m]}")
        else:
            cls = "NOT PINNED"; p.append(f"{m}: not in the audited combined closure")
        classes[cls] = classes.get(cls, 0) + 1
        rows.append(f"{m}\t{f}\t{h}\t{cls}")
    (A / "data/closure302.tsv").write_text("module\tfile\tolean_sha256\tclass\n" + "\n".join(rows) + "\n")
    mirror = Path("/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/FORMAL20261122/fv302/src")
    for n in ("FcatZZs16", "BridgeZZs16"):
        if (W / f"src/CompactChecker/{n}.lean").read_bytes() != (mirror / f"CompactChecker/{n}.lean").read_bytes():
            p.append(f"src/CompactChecker/{n}.lean differs from its git mirror")
    return {"modules": len(mods), "classes": classes, "roots": len(roots), "shared_files": shared, "problems": p}


def order():
    p = []
    imp = re.compile(r"^import\s+(E302ZZ\.\S+)", re.M)
    oleans = {f.stem: f for f in (OLEAN / "E302ZZ").glob("*.olean")}
    for name, ol in oleans.items():
        s = SRC / "E302ZZ" / f"{name}.lean"
        if not s.exists(): continue
        t = ol.stat().st_mtime
        for dep in imp.findall(s.read_text(errors="replace")):
            d = oleans.get(dep.split(".", 1)[1])
            if d is None: p.append(f"{name}: imported {dep} has no olean")
            elif d.stat().st_mtime > t: p.append(f"{name}: older than its import {dep}")
    return {"oleans": len(oleans), "problems": p}


STEPS = {"item1": item1, "item2": item2, "item3": item3, "scan": scan, "item4": item4, "order": order}
DEVIATIONS = [
    "PLAN item 3 says 'driver.log without ALERT'; driver.log has profiler-interleaving ALERTs (count in item3). Since "
    "24 Nov 04:55 (PLAN.md log, after the launch) item 3 is decided by axiom_audit.py's rule over every module log.",
    "Compiles adopted at the 04:56 driver restart have leaves -1 in run.tsv (list in item3); their manifests, sources "
    "and logs are checked like all others.",
    "drive302.py was re-pinned after the first pin (PLAN.md: done-cache and 3 s cycle added at launch).",
    "The pre-launch advisor call timed out; the launch rested on the pilot, two controls and the gates.",
    "The join sources (S_*, P_*, Root, Final) are not shape-checked by the exporter; the token scan covers them.",
]

if __name__ == "__main__":
    (A / "data").mkdir(exist_ok=True)
    want = sys.argv[1:] or list(STEPS)
    allp = []
    for name in STEPS:
        out = A / f"data/step_{name}.json"
        if name not in want and out.exists() and json.loads(out.read_text()).get("ok"):
            res = json.loads(out.read_text())
        elif name in want or not out.exists():
            try:
                res = STEPS[name]()
            except Exception as e:  # a missing input is a problem, not a crash
                res = {"problems": [f"{type(e).__name__}: {e}"]}
            res["ok"] = not res["problems"]
            out.write_text(json.dumps(res, indent=1))
        else:
            res = json.loads(out.read_text())
        allp += [f"{name}: {x}" for x in res["problems"]]
        print(name, "ok" if res.get("ok") else f"PROBLEMS {len(res['problems'])}", flush=True)
    result = {"verdict": "ACCEPT" if not allp else "NOT ACCEPTED", "problems": allp[:200], "n_problems": len(allp),
              "deviations": DEVIATIONS}
    (A / "result.json").write_text(json.dumps(result, indent=1))
    print(json.dumps({k: result[k] for k in ("verdict", "n_problems")}))
    sys.exit(0 if not allp else 1)
