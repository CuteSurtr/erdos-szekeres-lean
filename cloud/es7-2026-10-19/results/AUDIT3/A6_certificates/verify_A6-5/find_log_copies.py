#!/usr/bin/env python3
"""A6-5 check: for every small (non-.zst) file in the es7-symmetry proof archive, look for a byte-identical copy
(same SHA-256) anywhere in the repository worktree (excluding .git), and report also same-name files that differ.
Read-only on both trees.  Usage: python3 -I find_log_copies.py ARCHIVE_ROOT WORKTREE_ROOT
"""
import hashlib, os, sys

arch, wt = sys.argv[1], sys.argv[2]
SUBDIRS = ["mirror34", "mirror33", "c5", "c3hex", "central34", "tools"]
MAXSZ = 50 * 1024 * 1024  # only hash worktree files up to 50 MB (logs are tiny)

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

# index the worktree by size first, hash lazily
by_size = {}
by_name = {}
for root, dirs, files in os.walk(wt):
    dirs[:] = [d for d in dirs if d != ".git"]
    for fn in files:
        p = os.path.join(root, fn)
        try:
            st = os.lstat(p)
        except OSError:
            continue
        if not os.path.isfile(p) or os.path.islink(p) or st.st_size > MAXSZ:
            continue
        by_size.setdefault(st.st_size, []).append(p)
        by_name.setdefault(fn, []).append(p)

hcache = {}
def h(p):
    if p not in hcache:
        hcache[p] = sha(p)
    return hcache[p]

for sd in SUBDIRS:
    d = os.path.join(arch, sd)
    for fn in sorted(os.listdir(d)):
        p = os.path.join(d, fn)
        if fn.endswith(".zst") or not os.path.isfile(p):
            continue
        sz = os.path.getsize(p)
        a = sha(p)
        same = [q for q in by_size.get(sz, []) if h(q) == a]
        rel = lambda q: os.path.relpath(q, wt)
        status = "COPY" if same else "NO-COPY"
        print(f"{sd}/{fn}\t{sz}\t{a[:16]}\t{status}\t" + ";".join(rel(q) for q in same))
        if not same:
            nm = by_name.get(fn, [])
            for q in nm:
                print(f"    same-name-but-different: {rel(q)} ({os.path.getsize(q)} bytes, {h(q)[:16]})")
