"""Referee check: does the path-compression mutant (uf_compress) change the triple map, and how deep do union-find
paths get?  Builds only the union-find (no clauses) of the original and the mutant for t = 4..17, rot m = 2."""
import importlib.util
import os
import sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

here = os.path.dirname(os.path.abspath(__file__))
orig = load(sys.argv[1], "orig")
mut = load(sys.argv[2], "mut")
tmp = os.path.join(here, "ufdepth.body")

# instrument: maximum path length seen by _find in the original
class Probe(orig.ZEncoding):
    maxdepth = 0
    def _find(self, x):
        d, r = 0, x
        while self.par[r][0] != r:
            r = self.par[r][0]
            d += 1
        Probe.maxdepth = max(Probe.maxdepth, d)
        return super()._find(x)

for t in list(range(4, 10)) + [17]:
    Probe.maxdepth = 0
    a = Probe("rot", t, 7, 2, body=tmp)
    b = mut.ZEncoding("rot", t, 7, 2, body=tmp)
    same = a.tv == b.tv
    print(f"t={t}: classes {a.nv} vs {b.nv}; triple maps identical: {same}; max path length seen by _find: {Probe.maxdepth}")
    a.sink.f.close(); b.sink.f.close()
os.remove(tmp)
