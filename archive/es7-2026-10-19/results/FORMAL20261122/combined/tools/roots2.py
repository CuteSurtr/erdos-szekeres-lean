#!/usr/bin/env python3
"""combined part 2 (P1): check the part-2 LEAN_PATH before any compile, and pin the N66 level-15 oleans.
Run in a unit:  python3 -I -B tools/roots2.py
- two-roots check: no module file (.olean/.olean.server/.olean.private) may be provided by two roots of tools/env2.sh;
- negative control: adding n66-rowsvalid's store must be refused (a module file it shares with res118-rowblocks;
  both use the RowEnc/RowGeo namespaces, but at file level only some module names coincide);
- sha256 (O_DIRECT reads), size and mtime of every .olean in the two N66 stores; each must be newer than its source
  (lean/<module>.lean in its project) and older than the l15 review (started 22:47) and data/MARKER_START2;
- the olean hashes printed by the n66-level15 review compile (review/review_compile.log) must equal today's files;
- sha256 (O_DIRECT) re-check of both N66 projects' source and freeze manifests.
Writes data/n66_oleans2.tsv and data/roots2.json (only these); exit 1 on any problem."""
import datetime, hashlib, json, mmap, os, re, subprocess, sys
from pathlib import Path

W = Path("/home/jay/research/data/formalize-20261122/combined")
F = Path("/home/jay/research/data/formalize-20261122")
L15, L15R, NRV = F / "n66-level15", F / "n66-l15-rows", F / "n66-rowsvalid/build/olean"
STORES = {str(L15 / "build/olean"): L15, str(L15R / "build/olean"): L15R}
REVIEW_START = datetime.datetime(2026, 11, 22, 22, 47).timestamp()  # n66-l15-rows review start (its README)
EXT = (".olean", ".olean.server", ".olean.private")
BUF = 1 << 22
MM = mmap.mmap(-1, BUF)
MV = memoryview(MM)


def sha(path):
    """sha256 with O_DIRECT reads into a page-aligned buffer (no page cache charged); buffered fallback."""
    size, h, total = os.stat(path).st_size, hashlib.sha256(), 0
    try:
        fd = os.open(path, os.O_RDONLY | os.O_DIRECT)
        try:
            while True:
                n = os.readv(fd, [MM])
                h.update(MV[:n])
                total += n
                if n < BUF:
                    break
        finally:
            os.close(fd)
        if total == size:
            return h.hexdigest()
    except OSError:
        pass
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(BUF), b""):
            h.update(b)
    return h.hexdigest()


def shadowed(roots):
    seen, dup = {}, {}
    for r in roots:
        for dirpath, _, files in os.walk(r):
            for fn in files:
                if fn.endswith(EXT):
                    rel = os.path.relpath(os.path.join(dirpath, fn), r)
                    if rel in seen:
                        dup.setdefault(rel, [seen[rel]]).append(r)
                    else:
                        seen[rel] = r
    return dup


def manifest(mf, base):
    """(entries, [bad paths]) for a sha256sum-format manifest; relative paths resolve against base."""
    bad, n = [], 0
    for line in mf.read_text().splitlines():
        if not line.strip():
            continue
        h, p = line.split(None, 1)
        p = p.lstrip("*")
        f = Path(p) if p.startswith("/") else base / p
        n += 1
        if not f.is_file() or sha(f) != h:
            bad.append(p)
    return n, bad


def main():
    roots = subprocess.run(["bash", "-c", f". {W}/tools/env2.sh; echo $LEAN_PATH"], capture_output=True,
                           text=True).stdout.strip().split(":")
    probs = []
    for s in STORES:
        if s not in roots:
            probs.append(f"store not on the part-2 LEAN_PATH: {s}")
    dup = shadowed(roots)
    probs += [f"module file provided by two roots: {k} {v}" for k, v in list(dup.items())[:20]]
    ctl = shadowed(roots + [str(NRV)])
    ctl_ok = bool(ctl) and all(k.split("/")[0] in ("RowEnc", "RowGeo", "RowChk") for k in ctl)
    if not ctl_ok:
        probs.append("negative control: adding n66-rowsvalid's store was not refused")
    marker = (W / "data/MARKER_START2").stat().st_mtime
    rows = []
    for s, proj in STORES.items():
        for dirpath, _, files in os.walk(s):
            for fn in sorted(files):
                if not fn.endswith(".olean"):
                    continue
                f = os.path.join(dirpath, fn)
                rel = os.path.relpath(f, s)
                mod = rel[:-len(".olean")].replace("/", ".")
                st = os.stat(f)
                src = proj / "lean" / (rel[:-len(".olean")] + ".lean")
                fresh = src.is_file() and src.stat().st_mtime <= st.st_mtime
                if not fresh:
                    probs.append(f"{mod}: source {src} missing or newer than its olean")
                if st.st_mtime >= min(REVIEW_START, marker):
                    probs.append(f"{mod}: olean newer than the l15 review start / MARKER_START2")
                rows.append((mod, s, sha(f), str(st.st_size),
                             datetime.datetime.fromtimestamp(st.st_mtime).isoformat(sep=" ", timespec="seconds")))
    (W / "data/n66_oleans2.tsv").write_text("module\tstore\tolean_sha256\tsize\tmtime\n" +
                                            "".join("\t".join(r) + "\n" for r in rows))
    # olean hashes printed by the n66-level15 review compile
    pins = []
    for line in (L15 / "review/review_compile.log").read_text(errors="replace").splitlines():
        m = re.fullmatch(r"([0-9a-f]{64})  (/\S+\.olean)", line.strip())
        if m:
            now = sha(m.group(2)) if os.path.isfile(m.group(2)) else None
            pins.append({"file": m.group(2), "review_sha256": m.group(1), "now": now, "ok": now == m.group(1)})
            if now != m.group(1):
                probs.append(f"n66-level15 review pin differs: {m.group(2)}")
    if len(pins) < 6:
        probs.append(f"only {len(pins)} pins parsed from n66-level15 review_compile.log")
    mans = {}
    for mf, base in ((L15R / "logs/source_manifest.sha256", L15R), (L15R / "logs/freeze_manifest.sha256", L15R),
                     (L15 / "logs/final_source_manifest.sha256", L15), (L15 / "logs/freeze_manifest.sha256", L15)):
        n, bad = manifest(mf, base)
        mans[str(mf)] = {"entries": n, "bad": bad}
        probs += [f"{mf}: {b} missing or changed" for b in bad]
    res = {"lean_path": roots, "roots": len(roots), "duplicates": dup,
           "negative_control": {"added_root": str(NRV), "refused": ctl_ok,
                                "duplicates": sorted(k for k in ctl if k.endswith(".olean"))[:12],
                                "n_duplicates": len(ctl)},
           "n66_oleans": len(rows), "by_store": {s: sum(1 for r in rows if r[1] == s) for s in STORES},
           "newest_n66_olean_mtime": max(r[4] for r in rows), "marker2_mtime": marker,
           "n66_oleans_digest": hashlib.sha256("".join(f"{r[0]}\t{r[2]}\n" for r in sorted(rows)).encode()).hexdigest(),
           "n66_oleans_tsv_sha256": sha(W / "data/n66_oleans2.tsv"),
           "level15_review_pins": pins, "manifests": mans, "problems": probs}
    (W / "data/roots2.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k not in ("lean_path", "level15_review_pins")}, indent=1))
    sys.exit(1 if probs else 0)


if __name__ == "__main__":
    main()
