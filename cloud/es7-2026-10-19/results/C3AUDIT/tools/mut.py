import sys, runpy
sys.path.insert(0, "/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3-S/tools")
import hullcase as HC
which = sys.argv.pop(1)
if which == "rev2":   # reversed orientation of two-orbit layers
    o = HC.layer_order
    HC.layer_order = lambda m, L: o(m, L)[::-1] if len(L) == 2 else o(m, L)
if which == "nosigflip":
    HC.mirror_layer = lambda m, L: sorted(((m - r) % m, s) for r, s in L)
if which == "noswap":   # sigma of r+m not flipped in layer key
    def lo(m, L):
        if len(L) == 1: r = L[0][0]; return [r, r + 2*m, r + m]
        return [i for _, i in sorted(((s, i) for r, s in L for i in (r, r+m, r+2*m)))]
    HC.layer_order = lo
sys.argv = ["drive.py"] + sys.argv[1:]
runpy.run_path("/opt/audit/ind/drive.py", run_name="__main__")
