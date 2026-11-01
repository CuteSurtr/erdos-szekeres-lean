#!/usr/bin/env python3
"""C3COMP1 part 2: for the open H3 and one-orbit roots of OPEN_ROOTS.tsv, the state of each root's 64 six-bit
sigma cubes (the C3U definition: two sigma_children(·, 3) steps from the root, as close_tree.py --sigma-split 3
--sigma-levels 2 builds them), read from the record files given (C3W4 and C3SIG2): certified / timed out at
300 s / never ran (other: only records at other caps); solve times of certified six-bit cubes; and the layer
subtrees under timed-out cubes (nodes L'__C below root__C: split, run, certified, timed out, open leaves).
sigma_cubes.py records ("cube" field) are read as records of node__C, as compose.py and close_tree.py do.
usage: part2.py TOOLSDIR OPEN_ROOTS.tsv OUTPREFIX RECORDS.jsonl [...]"""
import collections, json, os, statistics, sys
tools, ortsv, outp, files = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
sys.path.insert(0, os.path.join(tools, "..", "..", "C3a")); sys.path.insert(0, tools)
from hullcase import cube_layer_children, node_name, parse_node, sigma_children  # noqa: E402
M, KC = 11, 7
roots = [l.rstrip("\n").split("\t") for l in open(ortsv)][1:]
roots = [(r[0], r[1]) for r in roots if r[2] == "open" and (r[1].startswith("H3") or r[1].endswith("/one"))]
recs, split, cert = collections.defaultdict(list), {}, {}
for f in files:
    for l in open(f):
        r = json.loads(l)
        n = r["node"]
        if "cube" in r:
            n = node_name(parse_node(n)[0], sorted((int(x), v) for x, v in r["cube"].items()))
        if r.get("split"):
            split.setdefault(n, r); continue
        recs[n].append(dict(r, _f=f))
        if r.get("certified"):
            cert.setdefault(n, r)


def cubes64(R):
    L, C = parse_node(R)
    out = []
    for c1 in sigma_children(M, L, C, 3)[1]:
        out += [node_name(*c2) for c2 in [sigma_children(M, *c1, 3)[1]][0]]
    return out


def layer_kids(n):
    return [node_name(L, C) for L, C in cube_layer_children(M, KC, *parse_node(n))]


def subtree(n, d=0, st=None):
    # walk the layer subtree below a timed-out cube n: counts of runs, certified, timeouts, open leaves
    st = st if st is not None else collections.Counter()
    for c in layer_kids(n) if (n in split and "sigma_bits" not in split[n]) else []:
        st["nodes"] += 1; st["maxdepth"] = max(st["maxdepth"], d + 1)
        if c in cert:
            st["certified"] += 1; st["solve_s"] += cert[c]["solve_s"]; st["check_s"] += cert[c].get("check_s", 0); continue
        if recs.get(c):
            st["timed_out"] += 1
        if c in split:
            st["split"] += 1; subtree(c, d + 1, st)
        else:
            st["open"] += 1; st["never_ran" if not recs.get(c) else "open_timed_out"] += 1
    return st


rows, times, ctimes, sub_rows = [], [], [], []
for R, stratum in roots:
    cs = cubes64(R)
    assert len(cs) == 64 and len(set(cs)) == 64, R
    k = collections.Counter()
    for c in cs:
        if c in cert:
            k["certified"] += 1; times.append(cert[c]["solve_s"]); ctimes.append(cert[c].get("check_s", 0))
        elif any(r.get("cap") == 300 and r["status"] == "UNKNOWN" for r in recs.get(c, [])):
            k["timeout300"] += 1
            if c in split:
                st = subtree(c)
                sub_rows.append((R, stratum, c, st))
            else:
                sub_rows.append((R, stratum, c, None))
        elif not recs.get(c):
            k["never_ran"] += 1
        else:
            k["other"] += 1
    other6 = sum(1 for n in recs if n.startswith(R + "__") and len(parse_node(n)[1]) == 6 and n not in set(cs))
    rows.append((R, stratum, k["certified"], k["timeout300"], k["never_ran"], k["other"], other6))
with open(outp + "_cubes.tsv", "w") as f:
    f.write("root\tstratum\tcertified\ttimeout300\tnever_ran\tother\tother_6bit_cube_records\n")
    f.writelines("\t".join(map(str, x)) + "\n" for x in rows)
with open(outp + "_subtrees.tsv", "w") as f:
    f.write("root\tstratum\tcube\tsplit\tlayer_nodes\tcertified\ttimed_out\topen_leaves\tnever_ran\tmaxdepth\tcert_solve_s\n")
    for R, s, c, st in sub_rows:
        if st is None:
            f.write(f"{R}\t{s}\t{c}\tno\t0\t0\t0\t1\t0\t0\t0\n")
        else:
            f.write(f"{R}\t{s}\t{c}\tyes\t{st['nodes']}\t{st['certified']}\t{st['timed_out']}\t{st['open']}\t{st['never_ran']}\t{st['maxdepth']}\t{round(st['solve_s'],1)}\n")
tot = collections.Counter()
by = collections.defaultdict(collections.Counter)
for R, s, a, b, c, d, e in rows:
    for key, v in zip(("roots", "certified", "timeout300", "never_ran", "other"), (1, a, b, c, d)):
        tot[key] += v; by[s][key] += v
print("stratum\troots\tcertified\ttimeout300\tnever_ran\tother")
for s in sorted(by):
    print(s, *(by[s][x] for x in ("roots", "certified", "timeout300", "never_ran", "other")), sep="\t")
print("total", *(tot[x] for x in ("roots", "certified", "timeout300", "never_ran", "other")), sep="\t")
if times:
    q = statistics.quantiles(times, n=20)
    print(f"certified six-bit cube solve_s: n={len(times)} min={min(times)} p10={q[1]:.1f} p25={q[4]:.1f} median={statistics.median(times):.1f} "
          f"p75={q[14]:.1f} p90={q[17]:.1f} max={max(times)} mean={statistics.mean(times):.1f}")
    print(f"  their check_s: total {sum(ctimes):.0f}, mean {statistics.mean(ctimes):.1f}; solve_s total {sum(times):.0f}")
    for lo in range(0, 300, 25):
        print(f"  [{lo},{lo+25}) s: {sum(1 for t in times if lo <= t < lo + 25)}")
sp = [st for *_, st in sub_rows if st is not None]
print(f"timed-out cubes: {len(sub_rows)}, layer-split: {len(sp)}, not split: {len(sub_rows) - len(sp)}")
if sp:
    for key in ("nodes", "certified", "timed_out", "open", "never_ran", "maxdepth"):
        v = [st[key] for st in sp]
        print(f"  {key}: total {sum(v)}, per cube min {min(v)} median {statistics.median(v)} max {max(v)}")
    full = sum(1 for st in sp if st["open"] == 0)
    print(f"  layer subtrees fully certified: {full} of {len(sp)}; certified layer-node solve_s total {sum(st['solve_s'] for st in sp):.0f}, check_s total {sum(st['check_s'] for st in sp):.0f}")
    print("  per stratum: stratum, timed-out cubes, layer nodes, certified, timed out, open leaves, subtrees fully certified")
    for s in sorted({x[1] for x in sub_rows}):
        o = [st for R, s2, c, st in sub_rows if s2 == s and st is not None]
        print(f"    {s}\t{sum(1 for x in sub_rows if x[1] == s)}\t{sum(x['nodes'] for x in o)}\t{sum(x['certified'] for x in o)}\t"
              f"{sum(x['timed_out'] for x in o)}\t{sum(x['open'] for x in o)}\t{sum(1 for x in o if x['open'] == 0)}")
    # solve and check times of the certified layer children of timed-out cubes (first layer below the cube)
    lt, lc = [], []
    for R, s, c, st in sub_rows:
        if st is not None:
            for k in layer_kids(c):
                if k in cert:
                    lt.append(cert[k]["solve_s"]); lc.append(cert[k].get("check_s", 0))
    if lt:
        q = statistics.quantiles(lt, n=20)
        print(f"  certified first-layer children: n={len(lt)} solve_s median {statistics.median(lt):.1f} p90 {q[17]:.1f} max {max(lt)} "
              f"mean {statistics.mean(lt):.1f}; check_s mean {statistics.mean(lc):.1f}")
