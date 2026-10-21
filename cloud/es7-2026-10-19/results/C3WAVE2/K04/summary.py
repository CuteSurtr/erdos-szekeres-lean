import json, sys
sys.path.insert(0, "/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools")
from hullcase import layers_name, parse_layers, tree_children
from collections import defaultdict
recs = [json.loads(l) for l in open("/opt/work/out.jsonl") if l.strip()]
cert, split, att = {}, {}, defaultdict(list)
for r in recs:
    if r.get("certified"): cert[r["node"]] = r
    if r.get("split"): split[r["node"]] = r
    if "status" in r: att[r["node"]].append(r)
roots = [l.split("\t")[1] for l in open("/opt/work/roots.tsv").read().splitlines()[1:]]
def walk(n, acc):
    d = len(parse_layers(n))
    if n in cert: acc["cert"][d] += 1; return True
    if n in split:
        acc["split"][d] += 1
        ok = True
        for c in tree_children(11, 7, parse_layers(n)):
            ok = walk(layers_name(c), acc) and ok
        return ok
    acc["open"][d] += 1; return False
out = []
for R in roots:
    touched = any(k == R or k.startswith(R + "_") for k in att) or R in split
    acc = {"cert": defaultdict(int), "split": defaultdict(int), "open": defaultdict(int)}
    closed = walk(R, acc)
    nodes = [k for k in att if k == R or k.startswith(R + "_")]
    ss = sum(x.get("solve_s", 0) or 0 for k in nodes for x in att[k])
    cs = sum(x.get("check_s", 0) or 0 for k in nodes for x in att[k])
    unk = sum(1 for k in nodes for x in att[k] if x["status"] not in ("UNSATISFIABLE",))
    st = "closed" if closed else ("partial" if touched else "not reached")
    out.append(dict(root=R, status=st, certified={f"d{k}": v for k, v in sorted(acc["cert"].items())},
        splits={f"d{k}": v for k, v in sorted(acc["split"].items())}, open={f"d{k}": v for k, v in sorted(acc["open"].items())} if touched else {},
        non_unsat_attempts=unk, solve_s=round(ss), check_s=round(cs)))
for o in out: print(json.dumps(o))
