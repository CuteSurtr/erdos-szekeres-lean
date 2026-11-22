#!/usr/bin/env python3
"""combined: import audit of the end modules (after comp-audit and fv304-audit).
Run in a unit:  python3 -I -B tools/audit.py [LOG ...]   (default: the four compile logs in logs/)
- closure = union of the module lists the end modules printed at compile time (their environments' module lists);
- every module must be provided by exactly one LEAN_PATH root (tools/env.sh); its file is resolved and hashed;
- pins: library.json (library roots), chain311 build.tsv (chain311 root), the verified 311 assembly record
  logs/es311/final311-compact.json (CompactChecker/* resolved into build/CompactChecker), fv304-audit closure_combined.tsv (leanz and
  fv304 roots: LemmaZ, BalancedBudgetsZ, CompactChecker/*, E304Z/*), res118-rowblocks manifest (RowEnc/RowGeo),
  sevenfold review oleans_before.sha256 (EncB), data/links.json (links/: res118, res-slices-fv, comp-audit records),
  this build (out/: hash recorded here);
- companions (.olean.server/.private) of closure modules are hashed and compared with fv304-audit's table;
- every imported file outside out/ must be older than the start marker (data/MARKER_START, 21:10 KST; env MARKER
  overrides it, for the s35_19 switch whose 3519 oleans are newer).
Writes data/closure.tsv and data/audit.json; exit 1 on any problem."""
import hashlib, json, os, re, subprocess, sys
from pathlib import Path

W = Path("/home/jay/research/data/formalize-20261122/combined")
F = Path("/home/jay/research/data/formalize-20261122")
REPO = Path("/home/jay/research/lean/erdos-szekeres-lean")
CHAIN = REPO / "experiments/omission-compact-checker-2026-11-05/build/chain311"
LOGS = sys.argv[1:] or [str(W / f"logs/{m}.log") for m in ("Residual", "ES303", "ES302", "ES304")]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def mpath(m):
    return Path(*m.split(".")).with_suffix(".olean")


def modules(log):
    t = Path(log).read_text(errors="replace")
    body = t.split("=== MODULES\n", 1)[1].split("=== END", 1)[0]
    ms = [x[len("module "):] for x in body.splitlines()]
    assert ms and all(x and " " not in x for x in ms), f"bad module list in {log}"
    return ms


def digest(rows):
    return hashlib.sha256("".join(f"{m}\t{h}\n" for m, h in sorted(rows)).encode()).hexdigest()


def main():
    roots = subprocess.run(["bash", "-c", f". {W}/tools/env.sh; echo $LEAN_PATH"], capture_output=True,
                           text=True).stdout.strip().split(":")
    out_root, links_root = str(W / "out"), str(W / "links")
    probs = []
    lists = {Path(l).stem: modules(l) for l in LOGS}
    union = sorted(set().union(*lists.values()))
    if "Residual" in lists:
        probs += [f"Residual's closure is not inside {k}'s" for k, v in lists.items() if not set(lists["Residual"]) <= set(v)]
    # pins
    lib = json.loads((CHAIN / "library.json").read_text())
    lroots = [r.replace("<repo>", str(REPO)).replace("<home>", str(Path.home())) for r in lib["roots"]]
    libpin = {m: (lroots[i], h) for m, (i, h) in lib["modules"].items()}
    lines = (CHAIN / "build.tsv").read_text().splitlines()
    cols, chainpin = lines[0].split("\t"), {}
    for line in lines[1:]:
        row = dict(zip(cols, line.split("\t")))
        chainpin[row["module"]] = row["olean_sha256"] if row["verdict"] == "ok" else None
    fvpin = {}
    for line in (F / "fv304-audit/data/closure_combined.tsv").read_text().splitlines()[1:]:
        m, root, f, h, pin, st = line.split("\t")
        fvpin[m] = (root, h, st)
    rbpin = {}
    for line in (F / "res118-rowblocks/data/manifest.sha256").read_text().splitlines():
        h, p = line.split(None, 1)
        if p.startswith("build/olean/"):
            rbpin[p[len("build/olean/"):]] = h
    exp_dir = REPO / "experiments/omission-compact-checker-2026-11-05"
    rr = json.loads((exp_dir / "logs/es311/final311-compact.json").read_text())  # verified 311 assembly (in git)
    route = {"CompactChecker." + u.split("/", 1)[1].replace("/", "."): v["sha256"]
             for u, v in rr["chain"]["inputs"].items() if u.startswith("CompactChecker/")}
    ccdir = str(exp_dir / "build/CompactChecker") + "/"
    encpin = {}
    for line in (F / "sevenfold/review/oleans_before.sha256").read_text().splitlines():
        h, p = line.split(None, 1)
        encpin[p[2:] if p.startswith("./") else p] = h
    links = {r["file"]: r for r in json.loads((W / "data/links.json").read_text())["rows"]}
    marker = Path(os.environ.get("MARKER", str(W / "data/MARKER_START"))).stat().st_mtime  # switch: a later marker
    rows, newest = [], 0.0
    for m in union:
        rel = str(mpath(m))
        prov = [r for r in roots if os.path.isfile(os.path.join(r, rel))]
        if len(prov) != 1:
            probs.append(f"{m}: provided by {prov}")
            continue
        r = prov[0]
        f = os.path.realpath(os.path.join(r, rel))
        h = sha(f)
        if r != out_root:
            newest = max(newest, os.stat(f).st_mtime)
            if os.stat(f).st_mtime >= marker:
                probs.append(f"{m}: {f} is newer than the start marker")
        if r == out_root:
            pin, exp = "this build", h
        elif r == links_root:
            lk = links.get(rel)
            pin, exp = (f"links.json: {lk['pin']}", lk["sha256"]) if lk and lk["target"] == f else ("links.json", None)
            if lk and lk["status"] == "first recorded here":
                pin = "first recorded here (links.json)"
        elif m in libpin and libpin[m][0] == r:
            pin, exp = "library.json", libpin[m][1]
        elif r == str(CHAIN / "olean"):
            pin, exp = "chain311 build.tsv", chainpin.get(m)
        elif m in route and f.startswith(ccdir):
            pin, exp = "311 route record final311-compact.json", route[m]
        elif m in fvpin and fvpin[m][0] == r and fvpin[m][2] == "ok":
            pin, exp = "fv304-audit closure_combined.tsv", fvpin[m][1]
        elif rel in rbpin:
            pin, exp = "res118-rowblocks manifest.sha256", rbpin[rel]
        elif rel in encpin:
            pin, exp = "sevenfold review oleans_before.sha256", encpin[rel]
        else:
            pin, exp = "first recorded here", h
        st = "ok" if exp == h else "MISMATCH"
        if st != "ok":
            probs.append(f"{m}: sha256 {h} differs from its pin ({pin}: {exp})")
        rows.append((m, r, f, h, pin, st))
    (W / "data/closure.tsv").write_text("module\troot\tfile\tolean_sha256\tpin\tstatus\n" +
                                        "".join("\t".join(x) + "\n" for x in rows))
    # companions
    fvc = {}
    for line in (F / "fv304-audit/data/companions_combined.tsv").read_text().splitlines()[1:]:
        fn, root, h = line.split("\t")
        fvc[fn] = (root, h)
    comp, cprobs = {}, []
    for m, r, f, h, pin, st in rows:
        for s in (".server", ".private"):
            hits = [x for x in roots if os.path.isfile(os.path.join(x, str(mpath(m)) + s))]
            if hits:
                if len(hits) != 1:
                    cprobs.append(f"{m}{s}: provided by {hits}")
                    continue
                ch = sha(os.path.join(hits[0], str(mpath(m)) + s))
                comp[f"{m}.{s[1:]}"] = (hits[0], ch)
                if f"{m}.{s[1:]}" in fvc and fvc[f"{m}.{s[1:]}"] != (hits[0], ch):
                    cprobs.append(f"{m}{s}: differs from fv304-audit's companion table")
    probs += cprobs
    e304 = [(m, h) for m, r, f, h, p, s in rows if m.startswith("E304Z.")]
    res = {"logs": LOGS, "modules_per_log": {k: len(v) for k, v in lists.items()}, "closure": len(union),
           "rows": len(rows), "lean_path": roots,
           "by_root": {x: sum(1 for y in rows if y[1] == x) for x in roots},
           "by_pin": {p: sum(1 for y in rows if y[4] == p) for p in sorted({y[4] for y in rows})},
           "by_status": {s: sum(1 for y in rows if y[5] == s) for s in sorted({y[5] for y in rows})},
           "e304z_modules": len(e304), "digest_all": digest([(y[0], y[3]) for y in rows]),
           "digest_e304z": digest(e304),
           "digest_e304z_fv304_audit": "fa02576ef5752c7fa509ea9f74b95feb46e4fdce9de26292b6df19c654b36c76",
           "companions": len(comp), "companions_in_fv304_table": sum(1 for k in comp if k in fvc),
           "companions_digest": digest([(k, v[1]) for k, v in comp.items()]),
           "newest_imported_mtime": newest, "marker_mtime": marker,
           "closure_tsv_sha256": sha(W / "data/closure.tsv"), "problems": probs}
    if "ES304" in lists and res["digest_e304z"] != res["digest_e304z_fv304_audit"]:
        probs.append("E304Z part of the closure differs from fv304-audit's")
    (W / "data/audit.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "lean_path"}, indent=1))
    sys.exit(1 if probs else 0)


if __name__ == "__main__":
    main()
