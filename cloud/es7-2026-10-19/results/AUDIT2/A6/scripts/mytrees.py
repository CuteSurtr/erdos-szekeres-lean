"""Independent recomputation of the per-case cube trees from WAVE1..4 (A6 audit).
usage: mytrees.py RESULTS OUT_JSON
Dir-to-case: parsed from the directory NAME (own regex), then cross-checked against every hash
the records carry; a mismatch is reported (not silently resolved)."""
import json, re, sys, os, collections
R, OUT = sys.argv[1:3]
VER = "s VERIFIED UNSAT"
cases = [json.loads(l) for l in open(os.path.join(R, "Mii-S/cases.jsonl")) if l.strip()]
byname = {c["case"]: c for c in cases}
sha2 = {c["cnf_sha256"]: c["case"] for c in cases}
rx = re.compile(r"^(U(?:\d+(?:-\d+)?)?_L(?:\d+(?:-\d+)?)?)")
def name_case(d):
    m = rx.match(d)
    if not m: return None
    n = m.group(1)
    return n if n in byname else ("?" + n)
def cube_of(v):
    if isinstance(v, str): v = json.loads(v)
    return v
issues = collections.defaultdict(list)
per = collections.defaultdict(lambda: {"dirs": [], "tops": {}, "closed": collections.defaultdict(set), "splits": collections.defaultdict(set), "unver": set()})
nodir = []
for w in ("WAVE1", "WAVE2", "WAVE3", "WAVE4"):
    for vm in sorted(os.listdir(os.path.join(R, w))):
        vp = os.path.join(R, w, vm)
        if not os.path.isdir(vp): continue
        for d in sorted(os.listdir(vp)):
            dp = os.path.join(vp, d); rel = "%s/%s/%s" % (w, vm, d)
            if not os.path.isdir(dp): continue
            lj = os.path.join(dp, "leaves.jsonl")
            nc = name_case(d)
            if not os.path.exists(lj):
                if nc: nodir.append(rel)
                continue
            if nc is None: issues["unnamed_dir_with_leaves"].append(rel); continue
            if nc.startswith("?"): issues["name_not_a_case"].append(rel); continue
            recs, badl = [], 0
            for l in open(lj):
                s = l.strip()
                if not s: continue
                try: recs.append(json.loads(s))
                except ValueError: badl += 1
            if badl: issues["unparsable_lines"].append((rel, badl))
            hs = collections.Counter()
            for r in recs:
                for key in ("case_sha256", "cnf_sha256"):
                    h = r.get(key)
                    if h is None: continue
                    if h in sha2: hs[sha2[h]] += 1
                    else: issues["unknown_hash"].append((rel, key, h[:16], r.get("status"), "top" if r.get("top") else ""))
            if set(hs) - {nc}: issues["hash_vs_name_mismatch"].append((rel, nc, dict(hs)))
            if not hs: issues["no_hash"].append(rel)
            P = per[nc]; P["dirs"].append(rel)
            tp = os.path.join(dp, "top.icnf")
            if os.path.exists(tp):
                P["tops"][rel] = [tuple(map(int, x.split()[1:-1])) for x in open(tp) if x.startswith("a ")]
            for r in recs:
                st = r.get("status")
                if st == "UNSAT":
                    ok = r.get("cake_lpr") == VER
                    if r.get("direct") or r.get("whole"): c = ()
                        # a whole record with a nonempty cube would be odd
                    else: c = r.get("cube")
                    if (r.get("direct") or r.get("whole")) and cube_of(r.get("cube", [])): issues["whole_with_cube"].append(rel)
                    if c is None: issues["unsat_no_cube"].append(rel); continue
                    c = tuple(cube_of(c))
                    if ok: P["closed"][c].add(rel)
                    else: P["unver"].add(c); issues["unsat_not_verified"].append((rel, r.get("cake_lpr")))
                elif st == "SPLIT":
                    sub = r.get("subs", r.get("children"))
                    if sub is None: issues["split_no_list"].append(rel); continue
                    c = tuple(cube_of(r["cube"]))
                    P["splits"][c].add(tuple(tuple(x) for x in cube_of(sub)))
def covers(cs):
    # independent cover check: DPLL-style on literal of first clause; brute but fine
    cs = [frozenset(c) for c in cs]
    def go(cs):
        if any(not c for c in cs): return True
        if not cs: return False
        z = next(iter(min(cs, key=len)))
        return all(go([c - {y} for c in cs if -y not in c]) for y in (z, -z))
    return go(cs)
out = {}
for c in cases:
    name = c["case"]
    if c["status"] == "UNSAT_VERIFIED":
        out[name] = {"src": "direct", "leaves": [[]]}; continue
    P = per.get(name)
    if P is None: issues["no_dirs"].append(name); out[name] = {"src": "none"}; continue
    if () in P["closed"]:
        out[name] = {"src": "empty", "leaves": [[]], "by": sorted(P["closed"][()])}; continue
    multi = {k: v for k, v in P["splits"].items() if len(v) > 1}
    if multi: issues["conflicting_splits"].append((name, len(multi)))
    split = {k: next(iter(v)) for k, v in P["splits"].items()}
    tl = list(P["tops"].values())
    if len({tuple(t) for t in tl}) > 1:
        # distinct top lists across shards: record it
        issues["distinct_top_lists"].append((name, [(d, len(t)) for d, t in P["tops"].items()]))
    tops = []
    for t in tl:
        for x in t:
            if x not in tops: tops.append(x)
    kids = {p + s for p, ss in split.items() for s in ss}
    roots = [t for t in tops if t not in kids]
    leaves, openc, nsplit = [], [], 0
    def walk(cube, depth):
        global nsplit
        if cube in P["closed"]: leaves.append(list(cube)); return
        if cube in split:
            nsplit += 1
            if not covers(split[cube]): issues["split_not_cover"].append((name, cube))
            for s in split[cube]: walk(cube + s, depth + 1)
            return
        openc.append(list(cube))
    for r in roots: walk(r, 1)
    if not covers(roots): issues["roots_not_cover"].append(name)
    if openc: issues["open"].append((name, len(openc)))
    out[name] = {"src": "tree", "leaves": leaves, "roots": len(roots), "split": nsplit, "open": len(openc),
                 "closed_records": len(P["closed"]), "dirs": P["dirs"]}
json.dump({"cases": out, "issues": issues, "nodir": nodir}, open(OUT, "w"))
print({k: len(v) for k, v in issues.items()})
print("src", collections.Counter(v["src"] for v in out.values()), "tree leaves", sum(len(v.get("leaves", [])) for v in out.values() if v["src"] == "tree"))
