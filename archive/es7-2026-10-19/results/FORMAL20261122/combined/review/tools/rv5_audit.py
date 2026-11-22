#!/usr/bin/env python3
"""rv5 (reviewer's own code): import audit of the ONE review compile (lean/RV5Review.lean).

Input: the "MOD <module> <path>" lines of logs/RV5Review.log, printed by Lean's own `findOLean` (the file Lean
resolved). For every module of the closure:
  - per-file providers over the LEAN_PATH roots (tools/env.sh): exactly one root may hold <root>/<mod>.olean, and it
    must be the file Lean resolved;
  - sha256 of the resolved file (O_DIRECT reads: no page cache charged to this unit) and of its .olean.server /
    .olean.private companions;
  - every earlier pin found for the module (library.json, chain311 build.tsv last ok row, final311-compact.json route,
    fv304-audit closure_combined.tsv, res118 olean_sha256_after_resume.txt, res-slices-fv audit-<tag>.json,
    comp-audit closure.tsv, res118-rowblocks manifest.sha256, sevenfold oleans_before.sha256) must equal it;
  - the worker's data/closure.tsv hash must equal it;
  - mtimes: newest imported file outside the worker's out/.
Writes data/audit_rv5.json and data/closure_rv5.tsv. Exit 1 on any problem."""
import hashlib, json, mmap, os, subprocess, sys
from pathlib import Path

RV = Path("/home/jay/research/data/formalize-20261122/combined/review")
W = Path("/home/jay/research/data/formalize-20261122/combined")
F = Path("/home/jay/research/data/formalize-20261122")
REPO = Path("/home/jay/research/lean/erdos-szekeres-lean")
EXP = REPO / "experiments/omission-compact-checker-2026-11-05"
CHAIN = EXP / "build/chain311"
BUF = 1 << 22
MM = mmap.mmap(-1, BUF)
MV = memoryview(MM)


def sha_direct(path):
    """sha256 with O_DIRECT reads (page-aligned mmap buffer); falls back to buffered reads if O_DIRECT fails."""
    size = os.stat(path).st_size
    h, total = hashlib.sha256(), 0
    try:
        fd = os.open(path, os.O_RDONLY | os.O_DIRECT)
        try:
            while True:
                n = os.readv(fd, [MM])
                if n > 0:
                    h.update(MV[:n])
                    total += n
                if n < BUF:
                    break
        finally:
            os.close(fd)
        if total == size:
            return h.hexdigest(), "direct"
    except OSError:
        pass
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(BUF), b""):
            h.update(b)
    return h.hexdigest(), "buffered"


def roots():
    out = subprocess.run(["bash", "-c", f". {RV}/tools/env.sh; printf %s \"$LEAN_PATH\""], capture_output=True,
                         text=True, check=True).stdout
    return out.split(":")


def mods_from_log(log):
    mods, n = [], None
    for line in Path(log).read_text(errors="replace").splitlines():
        if line.startswith("NMODULES "):
            n = int(line.split()[1])
        elif line.startswith("MOD "):
            _, m, p = line.split(" ", 2)
            mods.append((m, p))
    return n, mods


def add(pins, m, h, src):
    pins.setdefault(m, []).append((h, src))


def load_pins():
    pins = {}
    lib = json.loads((CHAIN / "library.json").read_text())
    lroots = [r.replace("<repo>", str(REPO)).replace("<home>", str(Path.home())) for r in lib["roots"]]
    for m, (i, h) in lib["modules"].items():
        add(pins, m, h, "library.json")
    last = {}
    lines = (CHAIN / "build.tsv").read_text().splitlines()
    cols = lines[0].split("\t")
    for line in lines[1:]:
        r = dict(zip(cols, line.split("\t")))
        if r.get("verdict") == "ok":
            last[r["module"]] = r["olean_sha256"]
    for m, h in last.items():
        add(pins, m, h, "chain311 build.tsv")
    rr = json.loads((EXP / "logs/es311/final311-compact.json").read_text())
    for u, v in rr["chain"]["inputs"].items():
        if u.startswith("CompactChecker/"):
            add(pins, u.replace("/", "."), v["sha256"], "final311-compact.json")
    for line in (F / "fv304-audit/data/closure_combined.tsv").read_text().splitlines()[1:]:
        m, root, f, h, pin, st = line.split("\t")
        add(pins, m, h, "fv304-audit closure_combined.tsv")
    for line in (F / "res118/data/olean_sha256_after_resume.txt").read_text().splitlines():
        if line.strip():
            h, rel = line.split(None, 1)
            if rel.startswith("olean/") and rel.endswith(".olean"):
                add(pins, rel[len("olean/"):-len(".olean")].replace("/", "."), h, "res118 olean_sha256")
    for t in ("3318", "3418", "3518", "3419"):
        a = json.loads((F / f"res-slices-fv/data/audit-{t}.json").read_text())
        for rel, h in a["files"].items():
            if rel.startswith("olean/") and rel.endswith(".olean"):
                add(pins, rel[len("olean/"):-len(".olean")].replace("/", "."), h, f"res-slices-fv audit-{t}.json")
    for line in (F / "comp-audit/closure.tsv").read_text().splitlines()[1:]:
        m, root, h, src, st = line.split("\t")
        add(pins, m, h, "comp-audit closure.tsv")
    for line in (F / "res118-rowblocks/data/manifest.sha256").read_text().splitlines():
        h, p = line.split(None, 1)
        if p.startswith("build/olean/") and p.endswith(".olean"):
            add(pins, p[len("build/olean/"):-len(".olean")].replace("/", "."), h, "res118-rowblocks manifest")
    for line in (F / "sevenfold/review/oleans_before.sha256").read_text().splitlines():
        h, p = line.split(None, 1)
        p = p[2:] if p.startswith("./") else p
        if p.endswith(".olean"):
            add(pins, p[:-len(".olean")].replace("/", "."), h, "sevenfold oleans_before")
    return pins


def main():
    log = RV / "logs/RV5Review.log"
    rs = roots()
    n, mods = mods_from_log(log)
    probs = []
    if n is None or n != len(mods):
        probs.append(f"NMODULES {n} != MOD lines {len(mods)}")
    pins = load_pins()
    worker = {}
    for line in (W / "data/closure.tsv").read_text().splitlines()[1:]:
        m, root, f, h, pin, st = line.split("\t")
        worker[m] = h
    out_root = str(W / "out")
    rows, newest, newest_f, modes = [], 0.0, "", {}
    comp_rows = []
    by_pin_count = {}
    for m, p in mods:
        rel = os.path.join(*m.split(".")) + ".olean"
        prov = [r for r in rs if os.path.isfile(os.path.join(r, rel))]
        provs = sorted(set(prov))  # the toolchain root appears twice in LEAN_PATH (FV304 roots + builtin)
        if len(provs) != 1:
            probs.append(f"{m}: per-file providers {provs}")
        elif os.path.realpath(os.path.join(provs[0], rel)) != os.path.realpath(p):
            probs.append(f"{m}: Lean resolved {p}, the unique provider is {provs[0]}")
        real = os.path.realpath(p)
        h, mode = sha_direct(real)
        modes[mode] = modes.get(mode, 0) + 1
        st = os.stat(real)
        if not real.startswith(out_root + "/") and not p.startswith(out_root + "/"):
            if st.st_mtime > newest:
                newest, newest_f = st.st_mtime, real
        pl = pins.get(m, [])
        bad = [(ph, src) for ph, src in pl if ph != h]
        if bad:
            probs.append(f"{m}: sha256 {h} differs from pins {bad}")
        if m in worker and worker[m] != h:
            probs.append(f"{m}: sha256 {h} differs from the worker's closure.tsv {worker[m]}")
        srcs = sorted({src for ph, src in pl})
        key = "+".join(srcs) if srcs else "NO PIN"
        by_pin_count[key] = by_pin_count.get(key, 0) + 1
        rows.append((m, p, real, h, str(st.st_size), str(int(st.st_mtime)), ";".join(srcs) or "NO PIN",
                     "worker-equal" if worker.get(m) == h else ("not in worker closure" if m not in worker else "DIFF")))
        for suf in (".server", ".private"):
            c = real + suf
            if os.path.isfile(c):
                ch, _ = sha_direct(c)
                comp_rows.append((m + suf, ch))
    # companions vs fv304-audit's table
    fvc = {}
    for line in (F / "fv304-audit/data/companions_combined.tsv").read_text().splitlines()[1:]:
        fn, root, h = line.split("\t")
        fvc[fn] = h
    comp_cmp = {"companions": len(comp_rows), "in_fv304_table": 0, "equal": 0, "diff": []}
    for key, h in comp_rows:  # key "<module>.server" / "<module>.private", the format of fv304-audit's table
        if key in fvc:
            comp_cmp["in_fv304_table"] += 1
            if fvc[key] == h:
                comp_cmp["equal"] += 1
            else:
                comp_cmp["diff"].append(key)
    if comp_cmp["diff"]:
        probs.append(f"companions differ from fv304-audit: {comp_cmp['diff'][:5]}")
    mods_set = {m for m, _ in mods}
    only_mine = sorted(mods_set - set(worker))
    only_worker = sorted(set(worker) - mods_set)
    e304 = sorted((r[0], r[3]) for r in rows if r[0].startswith("E304Z."))
    dig = lambda xs: hashlib.sha256("".join(f"{m}\t{h}\n" for m, h in xs).encode()).hexdigest()
    worker_out = {}
    for name in ("Residual", "ES303", "ES302", "ES304"):
        worker_out[name] = sha_direct(str(W / f"out/Combined/{name}.olean"))[0]
    res = {"log": str(log), "nmodules": n, "mod_lines": len(mods), "lean_path": rs,
           "pin_classes": by_pin_count, "no_pin": [r[0] for r in rows if r[6] == "NO PIN"],
           "hash_modes": modes, "only_in_reviewer_closure": only_mine, "only_in_worker_closure": only_worker,
           "worker_closure_equal": sum(1 for r in rows if r[7] == "worker-equal"),
           "e304z_modules": len(e304), "e304z_digest": dig(e304),
           "e304z_digest_fv304_audit_recorded": "fa02576ef5752c7fa509ea9f74b95feb46e4fdce9de26292b6df19c654b36c76",
           "companions": comp_cmp, "newest_imported_mtime": newest, "newest_imported_file": newest_f,
           "worker_out_oleans": worker_out, "problems": probs}
    if res["e304z_digest"] != res["e304z_digest_fv304_audit_recorded"]:
        probs.append("E304Z digest differs from fv304-audit's recorded digest")
    (RV / "data/closure_rv5.tsv").write_text("module\tlean_path\trealpath\tsha256\tbytes\tmtime\tpins\tworker\n" +
                                            "".join("\t".join(r) + "\n" for r in rows))
    (RV / "data/audit_rv5.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k not in ("lean_path",)}, indent=1)[:6000])
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
