#!/usr/bin/env python3
"""Rebuild leaves.icnf / open.icnf of a case dir from leaves.jsonl + top.icnf alone
(same rules as the end of close_w25.py): leaves = cubes whose last record is UNSAT with
cake_lpr `s VERIFIED UNSAT`; open = every other unsplit node of the trie."""
import json, os, sys
for d in sys.argv[1:]:
    last = {}
    for l in open(os.path.join(d, "leaves.jsonl")):
        r = json.loads(l)
        if "cube" in r and not r.get("plain"): last[tuple(r["cube"])] = r
    ok = lambda r: r is not None and r.get("status") == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT"
    ver, opn = [], []
    stack = [list(map(int, l.split()[1:-1])) for l in open(os.path.join(d, "top.icnf")) if l.startswith("a")]
    while stack:
        cu = stack.pop(); r = last.get(tuple(cu))
        if r is not None and r.get("status") == "SPLIT": stack += [cu + s for s in r["subs"]]
        elif ok(r): ver.append(tuple(cu))
        else: opn.append(cu)
    with open(os.path.join(d, "leaves.icnf"), "w") as f:
        for k in sorted(ver, key=lambda k: (len(k), k)): f.write("a " + " ".join(map(str, k)) + " 0\n")
    with open(os.path.join(d, "open.icnf"), "w") as f:
        for k in opn: f.write("a " + " ".join(map(str, k)) + " 0\n")
    print(d, "verified", len(ver), "open", len(opn))
