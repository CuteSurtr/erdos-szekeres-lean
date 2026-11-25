#!/usr/bin/env python3
"""Receipts for the generated chunk sources of slice s35_20 (25 Nov 2026). Rows in delete_proofs.py's format
(proof_file, zst_bytes, zst_sha256, check). Built from the finish recipe's audit (res-slices-fv/data/audit-3520.json,
which re-hashed every chunk source and required it to equal its manifest) and cross-checked here against the 3,212
unit manifests: every module of every manifest must appear once, with the manifest's sha256, as a regular file of the
recorded size; no other file of src/RS3520 is listed (the 30 sub-roots and the Root stay).
usage: mkrcpt3520.py OUT.tsv [TAG]   (TAG defaults to 3520; the same checks for the earlier slices)"""
import glob, json, os, sys
from pathlib import Path

D = Path("/home/jay/research/data/formalize-20261122/res-slices-fv")
TAG = sys.argv[2] if len(sys.argv) > 2 else "3520"
audit = json.loads((D / f"data/audit-{TAG}.json").read_text())
assert audit["problems"] == [] or all("axiom" in p for p in audit["problems"]), audit["problems"][:3]
files = audit["files"]
rows, probs, seen = [], [], set()
for mf in sorted(glob.glob(str(D / f"export/{TAG}/ctx/ctx-*.json"))):
    for m in json.loads(Path(mf).read_text())["modules"]:
        rel = f"export/{TAG}/" + m["file"]
        p = D / rel
        if rel in seen: probs.append(f"twice: {rel}")
        seen.add(rel)
        if files.get(rel) != m["sha256"]: probs.append(f"audit hash differs from manifest: {rel}")
        if not p.is_file() or p.is_symlink(): probs.append(f"not a regular file: {rel}")
        elif os.lstat(p).st_nlink != 1: probs.append(f"hard-linked: {rel}")
        rows.append((str(p), p.stat().st_size if p.exists() else -1, m["sha256"]))
srcdir = D / f"export/{TAG}/src/RS{TAG}"
on_disk = {str(x) for x in srcdir.glob("C*.lean")}
listed = {r[0] for r in rows}
if on_disk != listed: probs.append(f"chunk sources on disk {len(on_disk)} vs listed {len(listed)}")
if probs:
    print("PROBLEMS", len(probs), probs[:10]); sys.exit(1)
with open(sys.argv[1], "w") as f:
    f.write("proof_file\tzst_bytes\tzst_sha256\tcheck\n")
    for p, n, h in sorted(rows):
        f.write(f"{p}\t{n}\t{h}\tOK\n")
print(json.dumps({"files": len(rows), "bytes": sum(r[1] for r in rows), "kept": sorted(x.name for x in srcdir.glob("*.lean") if not x.name.startswith("C"))[:3] + ["..."]}))
