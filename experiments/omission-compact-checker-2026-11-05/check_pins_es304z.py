#!/usr/bin/env python3
"""FV304 (20 Nov 2026): the 310 assembly's olean pin checks, run before the FV304 compiles (read only).
1. drive_es310.check_library: lean-toolchain and lake-manifest sha256 = build/chain311 closure.json/library.json;
   lake's LEAN_PATH roots = library.json's; every pinned library .olean has its pinned sha256.
2. drive_es310.check_route_inputs: the CompactChecker and build/ext .olean files = the verified 311 assembly record.
3. build/ext = build/chain311/olean for the two catalogs Bridge311Bal imports.
4. The FV304 olean folder's CompactChecker symlinks point at build/CompactChecker files (checked in 2).
Prints one JSON line; exit 1 on any problem."""
import hashlib, json, os, sys
from pathlib import Path
D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
import drive_es310 as DR  # noqa: E402
O = Path("/home/jay/research/data/fv304-20261120")
lp = (O / "lean_path.txt").read_text().strip().split(":")
lake_lp = ":".join(lp[:lp.index(str(D / "build/chain311/olean"))])
probs = []
info, p1 = DR.check_library(lake_lp)
probs += p1
route, p2 = DR.check_route_inputs()
probs += p2
h = lambda f: hashlib.sha256(Path(f).read_bytes()).hexdigest()
cats = {}
for m in ("BalancedProof/Catalog.olean", "BalancedCoverCutsV2.olean"):
    a, b = D / "build/ext" / m, D / "build/chain311/olean" / m
    cats[m] = (h(a) == h(b))
    if not cats[m]:
        probs.append(f"build/ext/{m} differs from build/chain311/olean/{m}")
links = {}
for f in (O / "olean/CompactChecker").iterdir():
    if f.is_symlink():
        t = Path(os.readlink(f))
        links[f.name] = str(t).startswith(str(D / "build/CompactChecker"))
        if not links[f.name]:
            probs.append(f"symlink {f.name} -> {t} is outside build/CompactChecker")
print(json.dumps({"library": info, "route_inputs": len(route), "catalogs_equal": cats, "symlinks_ok": all(links.values()),
                  "problems": probs}))
sys.exit(1 if probs else 0)
