#!/usr/bin/env python3
"""Every hole that C3AUDIT3's brute force (tools/mybrute.py, run unchanged via runpy) finds must lie below a node of
the composer's uncovered frontier (frontier node L or L__C with L a layer prefix of the hole's path).
usage: brute_vs_frontier.py TOOLSDIR m k BASE RECORDS.jsonl [...]   (frontier from TOOLSDIR/compose.py)"""
import contextlib, hashlib, importlib.util, io, json, os, runpy, sys
tools, m, k, base, files = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:]
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "C3AUDIT3", "tools")
sys.path.insert(0, A); sys.path.insert(0, os.path.join(tools, "..", "..", "C3a")); sys.path.insert(0, tools)
sys.argv = ["mybrute.py", m, k] + files
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(os.path.join(A, "mybrute.py"))
holes = [h for h, _ in g["holes"]]
spec = importlib.util.spec_from_file_location("compose_t", os.path.join(tools, "compose.py"))
comp = importlib.util.module_from_spec(spec); spec.loader.exec_module(comp)
comp.M, comp.K = int(m), int(k)
comp.BASE_SHA = hashlib.sha256(open(base, "rb").read()).hexdigest()
cap = {}
class Shim:
    def __getattr__(self, a): return getattr(json, a)
    def dumps(self, o, *a, **kw):
        f = sys._getframe(1)
        if "missing" in f.f_locals: cap["missing"] = list(f.f_locals["missing"])
        return json.dumps(o, *a, **kw)
comp.json = Shim()
sys.argv = ["compose.py", base] + files
with contextlib.redirect_stdout(io.StringIO()):
    comp.main()
fr = [n.split("__")[0].split("_") for n in cap["missing"]]
below = lambda h: any(h.split("_")[:len(f)] == f for f in fr)
out = [h for h in holes if not below(h)]
print(json.dumps({"tools": tools.rstrip("/").split("/")[-2], "holes": len(holes), "frontier": len(fr),
                  "holes_not_below_frontier": len(out), "sample": out[:10]}))
