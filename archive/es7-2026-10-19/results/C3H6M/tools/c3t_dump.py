#!/usr/bin/env python3
"""Run C3T compose.py main() unchanged (same argv) and record which nodes it expands, to get its
frontier list and the depth-2 roots it covers.  usage: c3t_dump.py C3T_TOOLS DUMP_PREFIX BASE FILES... [--mirror-h6] [--no-sha]"""
import io, json, sys, contextlib
tools, dump = sys.argv[1], sys.argv[2]
sys.path.insert(0, tools)
import compose  # noqa: E402
from hullcase import layers_name, parse_layers  # noqa: E402
calls = {}
orig = compose.children
def rec(layers):
    ch = orig(layers)
    calls[layers_name(layers) if layers else "ROOT"] = [layers_name(c) for c in ch]
    return ch
compose.children = rec
sys.argv = [sys.argv[0]] + sys.argv[3:]
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    try:
        compose.main()
    except SystemExit as e:
        print(buf.getvalue(), file=sys.stderr); raise
res = json.loads(buf.getvalue())
# certified set exactly as compose filters it
cert = set()
for f in [a for a in sys.argv[2:] if not a.startswith("--")]:
    for l in open(f):
        r = json.loads(l)
        if r.get("certified") and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
            cert.add(layers_name(parse_layers(r["node"])))
leaves = {c for p, ch in calls.items() for c in ch if c not in calls}
frontier = sorted(c for c in leaves if c not in cert)
assert len(frontier) == res["uncovered_frontier_nodes"], (len(frontier), res["uncovered_frontier_nodes"])
memo = {}
def cov(n):
    if n in memo: return memo[n]
    v = n in cert or (n in calls and all(cov(c) for c in calls[n]))
    memo[n] = v; return v
assert cov("ROOT") == res["class_covered"]
d2 = [layers_name(c) for t in calls["ROOT"] for c in orig(parse_layers(t))]  # also below tops compose did not expand
res["depth2_roots"] = len(d2); res["depth2_open"] = sum(1 for c in d2 if not cov(c))
res["certified_in_tree_leaves"] = sum(1 for c in leaves if c in cert)
open(dump + ".frontier", "w").write("".join(x + "\n" for x in frontier))
open(dump + ".d2", "w").write("".join(f"{c}\t{int(cov(c))}\n" for c in d2))
print(json.dumps(res))
