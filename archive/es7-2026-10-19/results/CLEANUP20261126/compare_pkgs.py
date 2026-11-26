#!/usr/bin/env python3
"""compare_pkgs.py (26 Nov 2026): is each duplicate .lake/packages copy a byte-identical subset of the main repo's
.lake/packages? Read-only. For every regular file of a copy (all files, .git included, reported separately): same
relative path in the main copy, same size, same SHA-256; also the link count (1 = a real copy). Writes pkgs.json."""
import hashlib, json, os, sys
MAIN = "/home/jay/research/lean/erdos-szekeres-lean/.lake/packages"
COPIES = ["/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/LEANLB7_20261126/.lake/packages",
          "/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/LEANLB20261111/.lake/packages",
          "/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN/geo/.lake/packages",
          "/home/jay/research/tools/e810-lean/research/hall-reduction/.lake/packages"]
cache = {}
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""): h.update(b)
    return h.hexdigest()
def msha(rel):
    if rel not in cache:
        p = os.path.join(MAIN, rel); cache[rel] = sha(p) if os.path.isfile(p) and not os.path.islink(p) else None
    return cache[rel]
out = {}
for c in COPIES:
    r = {"files": 0, "bytes": 0, "git_files": 0, "git_bytes": 0, "equal": 0, "differ": [], "missing_in_main": [],
         "symlinks": 0, "nlink_gt1": 0}
    dig = hashlib.sha256()
    for root, dirs, files in os.walk(c):
        dirs.sort(); files.sort()
        for fn in files:
            p = os.path.join(root, fn); rel = os.path.relpath(p, c)
            if os.path.islink(p): r["symlinks"] += 1; continue
            st = os.stat(p); g = "/.git/" in "/" + rel
            r["files"] += 1; r["bytes"] += st.st_size
            if g: r["git_files"] += 1; r["git_bytes"] += st.st_size
            if st.st_nlink > 1: r["nlink_gt1"] += 1
            h = sha(p); dig.update(f"{rel}\t{h}\n".encode())
            m = msha(rel)
            if m is None: r["missing_in_main"].append(rel)
            elif m == h: r["equal"] += 1
            else: r["differ"].append(rel)
    r["digest"] = dig.hexdigest()
    r["differ_non_git"] = [x for x in r["differ"] if "/.git/" not in "/" + x]
    r["missing_non_git"] = [x for x in r["missing_in_main"] if "/.git/" not in "/" + x]
    for k in ("differ", "missing_in_main", "differ_non_git", "missing_non_git"):
        r[k + "_n"] = len(r[k]); r[k] = r[k][:30]
    out[c] = r
    print(c.split("/results/")[-1] if "/results/" in c else c, {k: r[k] for k in ("files", "bytes", "equal", "differ_n", "differ_non_git_n", "missing_non_git_n", "nlink_gt1", "symlinks")}, flush=True)
json.dump(out, open("/home/jay/research/data/cleanup-20261126/pkgs.json", "w"), indent=1)
