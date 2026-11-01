#!/usr/bin/env python3
"""verify_F2: per-root status of the 910 reduced-cut depth-2 roots, by the project's two composers,
run unchanged and with --no-sha (so that neither loads the 110 MB base body into memory; the CNF
hashes were re-derived in full elsewhere).  Modelled on results/C3U2/tests/frontier_cmp.py: each tool
is imported read-only and its module-level `json` is replaced by a shim whose dumps() captures the
caller's locals (memo, missing) when the summary is printed.  Nothing in the repository is written
(run with python -I -B).
usage: roots_nosha.py RESULTS_DIR BASE OUT.json RECORDS.jsonl [...]"""
import importlib.util
import json
import os
import sys

sys.dont_write_bytecode = True
RD, base, outp = sys.argv[1:4]
files = sys.argv[4:]
tools = os.path.join(RD, "C3U2", "tools")
sys.path.insert(0, os.path.join(RD, "C3a"))
sys.path.insert(0, tools)


class Shim:
    def __init__(self):
        self.cap = None

    def __getattr__(self, a):
        return getattr(json, a)

    def dumps(self, obj, *a, **kw):
        f = sys._getframe(1)
        if "memo" in f.f_locals and "missing" in f.f_locals:
            self.cap = (obj, dict(f.f_locals["memo"]), list(f.f_locals["missing"]))
        return json.dumps(obj, *a, **kw)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


import hullcase  # noqa: E402
comp = load("compose", os.path.join(tools, "compose.py"))
s1 = Shim()
comp.json = s1
sys.argv = ["compose.py", base] + files + ["--mirror-h6", "--no-sha"]
comp.main()
my = load("mycompose", os.path.join(RD, "C3AUDIT3", "tools", "mycompose.py"))
s2 = Shim()
my.json = s2
sys.argv = ["mycompose.py", "--m", "11", "--k", "7", "--no-sha", base] + files
my.main()
(o1, memo1, miss1), (o2, memo2, miss2) = s1.cap, s2.cap
roots = sorted(hullcase.layers_name(c2) for c1 in hullcase.tree_children(11, 7, [], mirror=True, mirror_h6=True)
               for c2 in hullcase.tree_children(11, 7, c1, mirror=True, mirror_h6=True))
rows = []
for r in roots:
    c1 = memo1.get(r)
    c2 = memo2.get(my.key(my.parse(r)[0], ()))
    rows.append((r, bool(c1), bool(c2)))
open1 = [r for r, a, _ in rows if not a]
open2 = [r for r, _, b in rows if not b]
res = {"files": len(files), "compose_summary": {k: v for k, v in o1.items() if k != "sigma_split_nodes_sample"},
       "mycompose_summary": o2, "roots": len(roots),
       "open_roots_compose": open1, "open_roots_mycompose": open2,
       "root_status_differences": [r for r, a, b in rows if a != b]}
json.dump(res, open(outp, "w"), indent=1)
print(json.dumps({"roots": len(roots), "compose_class_covered": o1.get("class_covered"),
                  "n_open_roots_compose": len(open1), "n_open_roots_mycompose": len(open2),
                  "n_root_status_differences": len(res["root_status_differences"]),
                  "open_roots_compose": open1}))
