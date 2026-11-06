#!/usr/bin/env python3
"""Test-only helper for the path-enforcement test E4 of the ES(8) <= 310 compact check (6 Nov 2026).
ES(8) <= 310 is NOT proved; this only builds hand-edited COPIES of a test export so that coverage_es310.py
and Lean can be shown a context stated at a wrong base path.

  make_pathflip_es310.py SRC_OUT DST_OUT --prefix E310BT --ctx 2407 --mode MODE --index I [--index2 J]
                         [--with-oleans]

SRC_OUT is an export_es310.py + merge_es310.py --subtree test export (e.g. build/es310/test-e2e). DST_OUT must
not exist and must lie in build/es310/test-* (refused otherwise). The copy holds src/, ctx/ and the merged
manifest; with --with-oleans also olean/ (without the .olean of any edited module or of the sub-Root),
run.tsv and logs/ (byte copies, never links, so SRC_OUT is never changed). Then the base path B of context --ctx (12 decisions, innermost first, from ctx/ctx-<kkkk>.json) is
replaced by B' wherever it ends a Lean path literal:
  --mode flip-all   B' = B with decision I flipped ((v, 1) <-> (v, 2)), in every module of the context, in
                    the context's internal skeleton theorems of the sub-Root, and in the context manifest's
                    base_path: the context consistently stated at a wrong path (a mispathed export).
  --mode flip-root  the same B', but only in the sub-Root (the context's internal skeleton theorems); the
                    chunk modules keep the true path.
  --mode swap-root  B' = B with decisions I and J swapped (the SAME mask: es310-crit1 item 3), sub-Root only.
Every sha256 that records an edited file is re-recorded (context manifest module entries, merged manifest
module and root entries, merge's ctx_manifests pins), so a checker has to catch the edit semantically, and
the driver accepts the sources. The text of B is matched as the exact tail "(v, x), ..., (v, x)]" of a path
literal, so the other context (whose path differs in its innermost decision) and the top skeleton (whose
paths are shorter) are untouched; the number of replacements per file is printed.
"""
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEST_AREA = HERE / "build" / "es310"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def tail(path):
    return ", ".join(f"({v}, {x})" for v, x in path) + "]"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--ctx", type=int, required=True)
    ap.add_argument("--mode", required=True, choices=["flip-all", "flip-root", "swap-root"])
    ap.add_argument("--index", type=int, required=True)
    ap.add_argument("--index2", type=int)
    ap.add_argument("--with-oleans", action="store_true")
    a = ap.parse_args()
    src, dst = a.src.resolve(), a.dst.resolve()
    if dst.parent != TEST_AREA or not dst.name.startswith("test-"):
        sys.exit(f"refusing: {dst} is not build/es310/test-*")
    if a.prefix == "E310B":
        sys.exit("refusing: test prefixes only")
    if dst.exists():
        sys.exit(f"refusing: {dst} exists")
    mf_name = f"manifest-{a.prefix}.json"
    if not (src / mf_name).is_file():
        sys.exit(f"{src / mf_name} missing")
    dst.mkdir()
    shutil.copytree(src / "src", dst / "src")
    shutil.copytree(src / "ctx", dst / "ctx")
    shutil.copy2(src / mf_name, dst / mf_name)
    if a.with_oleans:
        for d in ("olean", "logs"):
            if (src / d).is_dir():
                shutil.copytree(src / d, dst / d)
        shutil.copy2(src / "run.tsv", dst / "run.tsv")
        ro = dst / "olean" / Path(*a.prefix.split(".")) / "Root.olean"
        if ro.exists():
            ro.unlink()  # the sub-Root is always edited: a failed compile must leave no Root .olean behind
    cm_path = dst / "ctx" / f"ctx-{a.ctx:04d}.json"
    cm = json.loads(cm_path.read_text())
    base = [tuple(x) for x in cm["base_path"]]
    new = list(base)
    if a.mode in ("flip-all", "flip-root"):
        v, x = new[a.index]
        new[a.index] = (v, 3 - x)
    else:
        if a.index2 is None or a.index2 == a.index:
            sys.exit("--mode swap-root needs a different --index2")
        new[a.index], new[a.index2] = new[a.index2], new[a.index]
    old_t, new_t = tail(base), tail(new)
    report = {"ctx": a.ctx, "mode": a.mode, "base_path": base, "new_base_path": new, "files": {}}

    def edit(p):
        t = p.read_text()
        n = t.count(old_t)
        p.write_text(t.replace(old_t, new_t))
        report["files"][str(p.relative_to(dst))] = n
        return n

    mf = json.loads((dst / mf_name).read_text())
    if a.mode == "flip-all":
        for m in cm["modules"]:
            if edit(dst / m["file"]) == 0:
                sys.exit(f"no occurrence of the base path in {m['file']}")
            m["sha256"] = sha(dst / m["file"])
            mo = dst / "olean" / Path(*m["module"].split(".")).with_suffix(".olean")
            if mo.exists():
                mo.unlink()  # edited module: a failed compile must leave no .olean behind
        cm["base_path"] = [list(x) for x in new]
        cm_path.write_text(json.dumps(cm, indent=1) + "\n")
        shas = {m["module"]: m["sha256"] for m in cm["modules"]}
        for m in mf["modules"]:
            if m["module"] in shas:
                m["sha256"] = shas[m["module"]]
        for c in mf.get("ctx_manifests", []):
            if c["ctx"] == a.ctx:
                c["sha256"] = sha(cm_path)
    root = dst / mf["root"]["file"]
    if edit(root) == 0:
        sys.exit("no occurrence of the base path in the Root")
    mf["root"]["sha256"] = sha(root)
    (dst / mf_name).write_text(json.dumps(mf, indent=1) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
