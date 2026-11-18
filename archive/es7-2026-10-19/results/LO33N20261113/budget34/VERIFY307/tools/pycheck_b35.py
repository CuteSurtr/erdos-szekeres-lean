#!/usr/bin/env python3
"""Second, pure-Python implementation of the tree rules for budget 35 (copy of VERIFY308/tools/pycheck.py, track P307V).

usage: pycheck_b35.py CATALOG.json.gz EXTRA.json PACKET_DIR OUT.tsv [all | SAMPLE_N SEED | shard K k] [partial]
Reads rows straight from the JSON (not from rows.txt). Checks the master tree fully, then all contexts (or a sample, or
shard k of K by file size), writing one TSV line per context: id nodes leaves min_margin max_row errors seconds
(the first six columns as in pycheck.py, so compare_py.py works unchanged).
`partial` (progress tests on a live packet only): placeholders without a ctx file are skipped and counted; the run is
then NOT a full check and says so.  A full check never uses `partial`.

Differences from pycheck.py (B = 34) -- the leaf rule and the walk are unchanged:
  * B = 35;
  * master: budget field must be 35, contexts field = number of placeholders, source/extra fields = the files used;
  * strict parse: duplicate JSON keys, non-integer (float/bool) numbers, out-of-int64 values and unknown node keys are
    errors of that context (pycheck.py accepted floats silently);
  * memory: nodes are converted while parsing (object_pairs_hook) into tuples with array('q') weights, about 1 KB per
    node instead of about 6.9 KB with plain dicts (measured 18 Nov on a (20,15) context), so 300k-node contexts fit;
  * `partial` mode and a per-context seconds column.
"""
import gzip, json, os, random, resource, sys, time
from array import array

NS, B = 154, 35


def isint(x):
    return type(x) is int


def hook(pairs):
    keys = [k for k, _ in pairs]
    if len(set(keys)) != len(keys):
        raise ValueError("duplicate JSON key")
    d = dict(pairs)
    t = d.get("type")
    if t is None:
        return d  # top-level object
    if t == "branch":
        if set(d) != {"type", "vertex", "zero", "one"} or not all(isint(d[k]) for k in ("vertex", "zero", "one")):
            raise ValueError("bad branch node")
        return ("branch", d["vertex"], d["zero"], d["one"])
    if t == "weighted":
        ws = d.get("weights")
        if set(d) != {"type", "capacity", "weights"} or not isint(d["capacity"]) or not isinstance(ws, list) or not all(
                isinstance(p, list) and len(p) == 2 and isint(p[0]) and isint(p[1]) for p in ws):
            raise ValueError("bad weighted node")
        return ("weighted", d["capacity"], array("q", [p[0] for p in ws]), array("q", [p[1] for p in ws]))
    if t == "over_budget" and set(d) == {"type"}:
        return ("over_budget",)
    if t == "context" and set(d) == {"type", "context"} and isint(d["context"]):
        return ("context", d["context"])
    return ("other", str(t))


def load(path, gz):
    with (gzip.open(path, "rb") if gz else open(path, "rb")) as f:
        return json.loads(f.read(), object_pairs_hook=hook)


def load_rows(cat, extra):
    rows = [(x["rhs"], x["support"]) for x in json.load(gzip.open(cat))["constraints"]]
    rows += [(x["rhs"], x["support"]) for x in json.load(open(extra))]
    assert all(isint(d) and all(isint(i) for i in s) for d, s in rows), "non-integer row data"
    return [(d, s, frozenset(s)) for d, s in rows]


def walk(nodes, root, M, O, rows, allow_ctx, errs, ph):
    st = {"nodes": len(nodes), "leaves": 0, "min": None, "maxrow": -1}
    seen = [False] * len(nodes)
    stack = [(root, frozenset(M), frozenset(O))]
    while stack:
        v, M, O = stack.pop()
        if not isint(v) or not (0 <= v < len(nodes)) or seen[v]:
            errs.append(f"bad/repeated node {v}")
            continue
        seen[v] = True
        n = nodes[v]
        t = n[0] if isinstance(n, tuple) else "not-a-node"
        if t == "branch":
            _, x, zero, one = n
            if not (0 <= x < NS) or x in M or x in O:
                errs.append(f"node {v}: bad branch vertex")
                continue
            stack.append((one, M | {x}, O))
            stack.append((zero, M, O | {x}))
        elif t == "weighted":
            _, c, rs, ws = n
            st["leaves"] += 1
            if c < 0 or len(set(rs)) != len(rs) or any(not (0 <= r < len(rows)) for r in rs) or any(w < 0 for w in ws):
                errs.append(f"node {v}: bad weights")
                continue
            load_ = [0] * NS
            D = 0
            for r, w in zip(rs, ws):
                if w == 0:
                    continue
                st["maxrow"] = max(st["maxrow"], r)
                d, s, sset = rows[r]
                D += w * max(0, d - len(sset & M))
                for i in s:
                    load_[i] += w
            ex = sum(max(0, load_[i] - c) for i in range(NS) if i not in M and i not in O)
            m = D - c * (B - len(M)) - ex
            st["min"] = m if st["min"] is None else min(st["min"], m)
            if m < 1:
                errs.append(f"node {v}: margin {m}")
        elif t == "over_budget":
            st["leaves"] += 1
            if len(M) <= B:
                errs.append(f"node {v}: over_budget with |M|={len(M)}")
        elif t == "context" and allow_ctx:
            ph.append((n[1], M, O))
        else:
            errs.append(f"node {v}: leaf type {t}")
    if not all(seen):
        errs.append("unreachable nodes")
    return st


def main():
    args = sys.argv[1:]
    partial = args[-1] == "partial"
    if partial:
        args = args[:-1]
    cat, extra, pdir, out = args[:4]
    rows = load_rows(cat, extra)
    m = load(os.path.join(pdir, "master.json"), False)
    assert isinstance(m, dict) and set(m) == {"source", "extra", "budget", "root", "nodes", "contexts", "master_leaves"}, \
        "master top-level keys"
    errs, ph = [], []
    if m["budget"] != B:
        errs.append(f"master budget {m['budget']} != {B}")
    if os.path.realpath(m["source"]) != os.path.realpath(cat) or os.path.realpath(m["extra"]) != os.path.realpath(extra):
        errs.append("master source/extra differ from the files used")
    ms = walk(m["nodes"], m["root"], set(), {0}, rows, True, errs, ph)
    if m["contexts"] != len(ph) or m["master_leaves"] != ms["leaves"]:
        errs.append("master contexts/master_leaves fields differ from the tree")
    ids = [p[0] for p in ph]
    assert len(set(ids)) == len(ids), "duplicate context ids"
    files = {int(f[4:-8]) for f in os.listdir(pdir) if f.startswith("ctx-") and f.endswith(".json.gz")}
    assert files <= set(ids), "ctx files without a placeholder"
    missing = sorted(set(ids) - files)
    assert partial or not missing, "ctx files != placeholders"
    sel = [p for p in ph if p[0] in files]
    if len(args) > 4 and args[4] == "shard":  # shard K k: every K-th context by file size
        K, k = int(args[5]), int(args[6])
        bysize = sorted(sel, key=lambda p: -os.path.getsize(os.path.join(pdir, f"ctx-{p[0]}.json.gz")))
        sel = bysize[k::K]
    elif len(args) > 4 and args[4] != "all":
        random.seed(int(args[5]))
        sel = random.sample(sel, min(int(args[4]), len(sel)))
    with open(out, "w") as f:
        f.write(f"master\t{ms['nodes']}\t{ms['leaves']}\t{ms['min']}\t{ms['maxrow']}\t{len(errs)}\n")
        for cid, M, O in sel:
            t0 = time.time()
            e = []
            try:
                c = load(os.path.join(pdir, f"ctx-{cid}.json.gz"), True)
                hdr = isinstance(c, dict) and set(c) == {"context", "missing", "occupied", "root", "nodes"}
                if not hdr or not isint(c["context"]) or c["context"] != cid or not all(
                        isinstance(c[k], list) and all(isint(i) for i in c[k]) and len(set(c[k])) == len(c[k])
                        for k in ("missing", "occupied")) or set(c["missing"]) != M or set(c["occupied"]) != O:
                    e.append("context header mismatch")
                    s = {"nodes": 0, "leaves": 0, "min": None, "maxrow": -1}
                else:
                    s = walk(c["nodes"], c["root"], M, O, rows, False, e, None)
                del c
            except (ValueError, OverflowError, OSError, EOFError) as ex:  # parse errors count against this context
                e.append(f"parse: {ex!r}")
                s = {"nodes": 0, "leaves": 0, "min": None, "maxrow": -1}
            f.write(f"{cid}\t{s['nodes']}\t{s['leaves']}\t{s['min']}\t{s['maxrow']}\t{len(e)}\t{time.time() - t0:.3f}\n")
            f.flush()
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024
    print("master errors", errs[:5], "placeholders", len(ph), "checked", len(sel), "maxrss_MB", rss,
          f"PARTIAL: {len(missing)} placeholders without ctx file, NOT a full check" if partial else "full")


if __name__ == "__main__":
    main()
