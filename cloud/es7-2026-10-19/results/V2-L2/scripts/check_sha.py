#!/usr/bin/env python3
"""Compare the sha256 of the files written by `Emit.lean emit` with the V3 records.
usage: check_sha.py PICKED.tsv EMIT.log OUTDIR   (prints one line per leaf and a summary)"""
import hashlib, sys
picked = [l.rstrip("\n").split("\t") for l in open(sys.argv[1])]
logl = {}
for l in open(sys.argv[2]):
    t = l.rstrip("\n").split("\t")
    if len(t) >= 4 and t[3].startswith("leaf_of_tree="):
        logl[t[0]] = t[3]
ok = 0
cases = set()
for i, case, sha, lits, src in picked:
    try:
        data = open(f"{sys.argv[3]}/{i}.cnf", "rb").read()
    except OSError:
        data = b""
    got = hashlib.sha256(data).hexdigest()
    leaf = logl.get(i) == "leaf_of_tree=true"
    good = got == sha and leaf
    ok += good
    cases.add(case) if good else None
    print(i, case, src, "nlits", len(lits.split(",")), "sha", got, "MATCH" if got == sha else "DIFFER",
          "tree_leaf" if leaf else "NOT_TREE_LEAF")
print(f"summary: {ok}/{len(picked)} leaves match the V3 sha256 and are tree leaves; distinct cases {len(cases)}")
