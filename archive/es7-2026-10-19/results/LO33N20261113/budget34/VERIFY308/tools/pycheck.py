#!/usr/bin/env python3
"""Second, pure-Python implementation of the same tree rules, used to cross-check tcheck.cpp.

usage: pycheck.py CATALOG.json.gz EXTRA.json PACKET_DIR OUT.tsv [all | SAMPLE_N SEED | shard K k]
Reads rows straight from the JSON (not from rows.txt). Checks the master tree fully, then all contexts or a random
sample of them, writing one TSV line per context: id nodes leaves min_margin max_row errors.
"""
import gzip, json, os, random, sys

NS, B = 154, 34


def load_rows(cat, extra):
    rows = [(x["rhs"], x["support"]) for x in json.load(gzip.open(cat))["constraints"]]
    rows += [(x["rhs"], x["support"]) for x in json.load(open(extra))]
    return [(d, s, frozenset(s)) for d, s in rows]


def walk(nodes, root, M, O, rows, allow_ctx, errs, ph):
    st = {"nodes": len(nodes), "leaves": 0, "min": None, "maxrow": -1}
    seen = [False] * len(nodes)
    stack = [(root, frozenset(M), frozenset(O))]
    while stack:
        v, M, O = stack.pop()
        if not (0 <= v < len(nodes)) or seen[v]:
            errs.append(f"bad/repeated node {v}")
            continue
        seen[v] = True
        n = nodes[v]
        t = n["type"]
        if t == "branch":
            assert set(n) == {"type", "vertex", "zero", "one"}
            x = n["vertex"]
            if not (0 <= x < NS) or x in M or x in O:
                errs.append(f"node {v}: bad branch vertex")
                continue
            stack.append((n["one"], M | {x}, O))
            stack.append((n["zero"], M, O | {x}))
        elif t == "weighted":
            assert set(n) == {"type", "capacity", "weights"}
            st["leaves"] += 1
            c = n["capacity"]
            ws = n["weights"]
            rs = [r for r, w in ws]
            if c < 0 or len(set(rs)) != len(rs) or any(not (0 <= r < len(rows)) or w < 0 for r, w in ws):
                errs.append(f"node {v}: bad weights")
                continue
            load = [0] * NS
            D = 0
            for r, w in ws:
                if w == 0:
                    continue
                st["maxrow"] = max(st["maxrow"], r)
                d, s, sset = rows[r]
                D += w * max(0, d - len(sset & M))
                for i in s:
                    load[i] += w
            ex = sum(max(0, load[i] - c) for i in range(NS) if i not in M and i not in O)
            m = D - c * (B - len(M)) - ex
            st["min"] = m if st["min"] is None else min(st["min"], m)
            if m < 1:
                errs.append(f"node {v}: margin {m}")
        elif t == "over_budget":
            st["leaves"] += 1
            if len(M) <= B:
                errs.append(f"node {v}: over_budget with |M|={len(M)}")
        elif t == "context" and allow_ctx:
            ph.append((n["context"], M, O))
        else:
            errs.append(f"node {v}: leaf type {t}")
    if not all(seen):
        errs.append("unreachable nodes")
    return st


def main():
    cat, extra, pdir, out = sys.argv[1:5]
    rows = load_rows(cat, extra)
    m = json.load(open(os.path.join(pdir, "master.json")))
    errs, ph = [], []
    ms = walk(m["nodes"], m["root"], set(), {0}, rows, True, errs, ph)
    ids = [p[0] for p in ph]
    assert len(set(ids)) == len(ids), "duplicate context ids"
    files = {int(f[4:-8]) for f in os.listdir(pdir) if f.startswith("ctx-") and f.endswith(".json.gz")}
    assert files == set(ids), "ctx files != placeholders"
    sel = ph
    if len(sys.argv) > 5 and sys.argv[5] == "shard":  # shard K k: every K-th context by file size
        K, k = int(sys.argv[6]), int(sys.argv[7])
        bysize = sorted(ph, key=lambda p: -os.path.getsize(os.path.join(pdir, f"ctx-{p[0]}.json.gz")))
        sel = bysize[k::K]
    elif len(sys.argv) > 5 and sys.argv[5] != "all":
        random.seed(int(sys.argv[6]))
        sel = random.sample(ph, min(int(sys.argv[5]), len(ph)))
    with open(out, "w") as f:
        f.write(f"master\t{ms['nodes']}\t{ms['leaves']}\t{ms['min']}\t{ms['maxrow']}\t{len(errs)}\n")
        for cid, M, O in sel:
            c = json.load(gzip.open(os.path.join(pdir, f"ctx-{cid}.json.gz")))
            e = []
            if c["context"] != cid or set(c["missing"]) != M or set(c["occupied"]) != O or set(c) != {
                    "context", "missing", "occupied", "root", "nodes"}:
                e.append("context header mismatch")
            s = walk(c["nodes"], c["root"], M, O, rows, False, e, None)
            f.write(f"{cid}\t{s['nodes']}\t{s['leaves']}\t{s['min']}\t{s['maxrow']}\t{len(e)}\n")
    print("master errors", errs[:5], "placeholders", len(ph), "checked", len(sel))


if __name__ == "__main__":
    main()
