#!/usr/bin/env python3
"""combined: build links/ (file-level symlinks to finished oleans of other work dirs), compare every link target with
its earlier sha256 pin, and run the two-roots check on the whole LEAN_PATH (plus a negative control).
Run in a unit:  python3 -I -B tools/mklinks.py [TAG ...]    (default tags 3318 3418 3518 3419)
Writes only links/ and data/links.json; exit 1 on any missing target, pin mismatch or duplicate module file."""
import hashlib, json, os, shutil, subprocess, sys
from pathlib import Path

W = Path("/home/jay/research/data/formalize-20261122/combined")
F = Path("/home/jay/research/data/formalize-20261122")
RSO, R118, CA = F / "res-slices-fv/olean", F / "res118/olean", F / "comp-audit/out/olean"
TAGS = sys.argv[1:] or ["3318", "3418", "3518", "3419"]  # add 3519 only after RS.Final3519 is accepted (README)
EXT = (".olean", ".olean.server", ".olean.private")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def shadowed(roots):
    """{relative module file: [roots]} for every module file two roots provide (comp-audit's check). File-level
    symlinks are listed by os.walk; there are no directory symlinks in links/."""
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


def pins():
    """{target realpath: (sha256, source)} from the earlier records."""
    p = {}
    for line in (F / "res118/data/olean_sha256_after_resume.txt").read_text().split("\n"):
        if line.strip():
            h, rel = line.split(None, 1)
            p[str((F / "res118" / rel).resolve())] = (h, "res118 data/olean_sha256_after_resume.txt")
    for t in TAGS:
        a = F / f"res-slices-fv/data/audit-{t}.json"
        if a.is_file():
            for rel, h in json.loads(a.read_text())["files"].items():
                if rel.endswith(".olean"):
                    p[str((F / "res-slices-fv" / rel).resolve())] = (h, f"res-slices-fv data/audit-{t}.json")
    lines = (F / "comp-audit/closure.tsv").read_text().splitlines()
    for line in lines[1:]:
        m, root, h, src, st = line.split("\t")
        if src == "this build" and st == "ok":
            p[str((Path(root) / Path(*m.split("."))).with_suffix(".olean").resolve())] = (h, "comp-audit closure.tsv")
    return p


def wanted():
    """[(module file relative to links/, target)]"""
    out = [(f"Res118/{m}.olean", R118 / f"Res118/{m}.olean") for m in ("Rows", "LemmaA", "Glue", "Final", "Adapter")]
    out += [(f"{m}.olean", CA / f"{m}.olean") for m in ("FixedStatesZ", "LemmaZStar", "BalancedBudgetsZZs",
                                                       "BalancedBudgetsZZsN")]
    out.append(("RS/Lib.olean", RSO / "RS/Lib.olean"))
    for t in TAGS:
        names = [f"Cat{t}.olean", f"Bridge{t}.olean", f"Final{t}.olean"]
        names += sorted(x.name for x in (RSO / "RS").glob(f"Cat{t}_p*.olean"))
        out += [(f"RS/{n}", RSO / "RS" / n) for n in names]
        out += [(f"RS{t}/{x.name}", x) for x in sorted((RSO / f"RS{t}").glob("*.olean"))]
    return out


def main():
    env = subprocess.run(["bash", "-c", f". {W}/tools/env.sh; echo $LEAN_PATH"], capture_output=True, text=True)
    roots = env.stdout.strip().split(":")
    probs, rows = [], []
    lp = Path("/home/jay/research/data/fv304-20261120/lean_path.txt")
    if sha(lp) != "65463fd5680b9f1ccadb2e7ea0bb9a2820d5d4d5ae445d61318834d477f4a2cf":
        probs.append("fv304 lean_path.txt differs from the hash fv304-audit recorded")
    links = W / "links"
    if links.exists():
        shutil.rmtree(links)
    pin = pins()
    for rel, tgt in wanted():
        if not tgt.is_file():
            probs.append(f"missing target {tgt}")
            continue
        dst = links / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(tgt, dst)
        real = str(tgt.resolve())
        h = sha(real)
        ph, src = pin.get(real, (None, "no earlier pin"))
        st = "ok" if ph == h else ("first recorded here" if ph is None else "MISMATCH")
        if st == "MISMATCH":
            probs.append(f"{rel}: {h} differs from {src} {ph}")
        rows.append({"file": rel, "target": real, "sha256": h, "pin": src, "status": st})
    dup = shadowed(roots)
    probs += [f"module file provided by two roots: {k} {v}" for k, v in list(dup.items())[:10]]
    ctl = shadowed(roots + [str(R118)])  # negative control: res118/olean duplicates CompactChecker/* and Res118/*
    ctl_ok = "BalancedBudgetsZ.olean" in ctl and "CompactChecker/Fast2.olean" in ctl
    if not ctl_ok:
        probs.append("negative control: adding res118/olean was not refused")
    res = {"tags": TAGS, "lean_path": roots, "links": len(rows),
           "by_status": {s: sum(1 for r in rows if r["status"] == s) for s in {r["status"] for r in rows}},
           "duplicates": dup, "negative_control": {"added_root": str(R118), "refused": ctl_ok,
                                                   "duplicates": sorted(ctl)}, "problems": probs, "rows": rows}
    (W / "data/links.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
    sys.exit(1 if probs else 0)


if __name__ == "__main__":
    main()
