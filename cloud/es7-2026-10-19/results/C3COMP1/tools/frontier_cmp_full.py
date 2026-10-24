#!/usr/bin/env python3
"""Run compose.py of TOOLSDIR (C3U2 or C3U) and C3AUDIT3's mycompose.py (its fixed version) on the
same records and compare: summary, the full uncovered frontier, and the status of every depth-2 root.
Neither tool is changed: each is imported and its module-level `json` is replaced by a shim whose
dumps() also reads the caller's locals (memo, missing) when the summary is printed.
usage: frontier_cmp.py TOOLSDIR m k BASE OUTPREFIX RECORDS.jsonl [...] [--mirror-h6] [--nodes=N1,N2,...]
(--nodes: also report whether each named plain node is covered by each tool)
Writes OUTPREFIX.json (summaries, frontier sizes, differences) and OUTPREFIX_roots.tsv (root, status
and frontier size by both tools; with --mirror-h6 the roots are those of the reduced cut, and
mycompose, which has no H6 mirror, is read on the same roots).  mycompose's tree is the C3-S tree
without the H6 mirror, so with --mirror-h6 only the root table and the certified counts are compared."""
import hashlib, importlib.util, json, os, sys
tools, m, k, base, outp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
nodes = [a.split("=", 1)[1].split(",") for a in sys.argv[6:] if a.startswith("--nodes=")]
nodes = nodes[0] if nodes else []
files = [a for a in sys.argv[6:] if not a.startswith("--")]
mh6 = "--mirror-h6" in sys.argv
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, os.path.join(tools, "..", "..", "C3a")); sys.path.insert(0, tools)


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
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod


import hullcase  # noqa: E402  (of TOOLSDIR)
comp = load("compose", os.path.join(tools, "compose.py"))
comp.M, comp.K = m, k
if (m, k) != (11, 7):
    comp.BASE_SHA = hashlib.sha256(open(base, "rb").read()).hexdigest()
s1 = Shim(); comp.json = s1
sys.argv = ["compose.py", base] + files + (["--mirror-h6"] if mh6 else [])
comp.main()
my = load("mycompose", os.path.join(R, "C3AUDIT3", "tools", "mycompose.py"))
s2 = Shim(); my.json = s2
sys.argv = ["mycompose.py", "--m", str(m), "--k", str(k), base] + files
my.main()
(o1, memo1, miss1), (o2, memo2, miss2) = s1.cap, s2.cap
roots = sorted(hullcase.layers_name(c2) for c1 in hullcase.tree_children(m, k, [], mirror=True, mirror_h6=mh6)
               for c2 in hullcase.tree_children(m, k, c1, mirror=True, mirror_h6=mh6))
pre = lambda n: "_".join(n.split("__")[0].split("_")[:2])
fs1, fs2 = {}, {}
for n in miss1: fs1[pre(n)] = fs1.get(pre(n), 0) + 1
for n in miss2: fs2[pre(n)] = fs2.get(pre(n), 0) + 1
rows, diff = [], []
for r in roots:
    c1 = memo1.get(r); c2 = memo2.get(my.key(my.parse(r)[0], ()))
    rows.append((r, "closed" if c1 else "open", fs1.get(r, 0), "closed" if c2 else "open", fs2.get(r, 0)))
    if bool(c1) != bool(c2) or (c1 is None) or (c2 is None):
        diff.append(r)
with open(outp + "_roots.tsv", "w") as f:
    f.write("root\tcompose_status\tcompose_frontier\tmycompose_status\tmycompose_frontier\n")
    f.writelines("\t".join(map(str, x)) + "\n" for x in rows)
res = {"tools": tools, "mirror_h6": mh6, "files": len(files), "compose": o1, "mycompose": o2,
       "roots": len(roots), "open_roots_compose": sum(1 for x in rows if x[1] == "open"),
       "open_roots_mycompose": sum(1 for x in rows if x[3] == "open"), "root_status_differences": diff[:20],
       "n_root_status_differences": len(diff),
       "frontier_compose_in_roots": sum(fs1.get(r, 0) for r in roots),
       "frontier_mycompose_in_roots": sum(fs2.get(r, 0) for r in roots),
       "frontier_size_differences_per_root": sum(1 for x in rows if x[2] != x[4])}
if not mh6:
    a, b = set(miss1), set(miss2)
    res.update({"frontier_sets_equal": a == b, "only_compose": sorted(a - b), "only_mycompose": sorted(b - a), "n_only_compose": len(a - b), "n_only_mycompose": len(b - a)})
if nodes:
    res["nodes_covered"] = {n: {"compose": memo1.get(n), "mycompose": memo2.get(my.key(*my.parse(n)))} for n in nodes}
json.dump(res, open(outp + ".json", "w"), indent=1)
print(json.dumps({x: res[x] for x in res if x not in ("compose", "mycompose")}))
