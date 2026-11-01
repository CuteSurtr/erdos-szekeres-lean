#!/usr/bin/env python3
"""C3H6M step 2: tree_children of C3T (ff9b09ee) against C3-S (132398c) with --mirror-h6 off, and the
reduced H6 children against an own from-scratch implementation of Lemma H6M and the h6m_kept columns
of results/C3W3/lists/*.tsv.  usage: test_tree.py C3S_TOOLS_DIR C3T_TOOLS_DIR RESULTS_DIR"""
import csv, glob, importlib.util, itertools, json, os, random, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(path, "hullcase.py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

OLD, NEW = load(sys.argv[1], "hc_old"), load(sys.argv[2], "hc_new")
RES = sys.argv[3]
M, K = 11, 7
fails = []
def chk(cond, what):
    if not cond: fails.append(what)

# ---- own implementation (strings only; no repository code) -------------------------------------
def own_options(used):
    rem = [r for r in range(M) if r not in used]
    out = [((r, None),) for r in rem]
    for b, c in itertools.combinations(rem, 2):
        for sb in (0, 1):
            for sc in (0, 1):
                out.append(((b, sb), (c, sc)))
    return out
def own_phi(a, s, opt):
    img = []
    for r, sg in opt:
        rho = (a - r) % M
        img.append((rho, None if sg is None else sg ^ (1 if r < a else 0) ^ (1 if s == 0 else 0)))
    return tuple(sorted(img))
def own_key(opt):  # total order on options: sorted (residue, sigma) with None < 0 < 1
    return tuple((r, -1 if sg is None else sg) for r, sg in sorted(opt))
def own_kept(a, s):
    return [o for o in own_options({0, a}) if own_key(o) <= own_key(own_phi(a, s, o))]
def nm(layers):  # name in tree format
    return "_".join("-".join(f"{r}" if sg is None else f"{r}s{sg}" for r, sg in L) for L in layers)

out = {}
# ---- (a) flag off: C3T == C3-S --------------------------------------------------------------
def kids(mod, layers, **kw):
    return [mod.layers_name(c) for c in mod.tree_children(M, K, layers, mirror=True, **kw)]
root_old, root_new = kids(OLD, []), kids(NEW, [])
chk(root_old == root_new, "root")
tops = [NEW.parse_layers(x) for x in root_new]
chk(len(tops) == 11, "11 tops")
n_top = n_d2 = n_deep = 0
d2 = []
for t in tops:
    a, b = kids(OLD, t), kids(NEW, t); chk(a == b, f"top {NEW.layers_name(t)}"); n_top += 1
    d2 += [NEW.parse_layers(x) for x in b]
chk(len(d2) == 1630, f"depth-2 count {len(d2)}")
man = [r["node"] for r in csv.DictReader(open(os.path.join(RES, "C3-S/manifest_depth2.tsv")), delimiter="\t") if r["depth"] == "2"]
chk(sorted(man) == sorted(NEW.layers_name(x) for x in d2), "manifest depth-2 == tree depth-2 (flag off)")
for L in d2:
    chk(kids(OLD, L) == kids(NEW, L), f"d2 {NEW.layers_name(L)}"); n_d2 += 1
    chk(kids(NEW, L, mirror_h6=True) == kids(OLD, L), f"d2 flag-on {NEW.layers_name(L)}")
rng = random.Random(20261021)
deep_by_depth = {}
while n_deep < 3000:
    L = rng.choice(d2)
    depth = rng.randint(3, 7)
    while len(L) < depth:
        ch = NEW.tree_children(M, K, L)
        if not ch: break
        L = rng.choice(ch)
    if len(L) < 3: continue
    a, b = kids(OLD, L), kids(NEW, L)
    c = kids(NEW, L, mirror_h6=True)
    chk(a == b, f"deep {NEW.layers_name(L)}")
    chk(c == b, f"deep flag-on {NEW.layers_name(L)}")
    # own: complete children
    used = {r for X in L for r, _ in X}
    chk(sorted(b) == sorted(nm(L + [list(o)]) for o in own_options(used)), f"deep own {NEW.layers_name(L)}")
    n_deep += 1; deep_by_depth[len(L)] = deep_by_depth.get(len(L), 0) + 1
out["a"] = {"root": 1, "tops": n_top, "depth2": n_d2, "deeper_random": n_deep, "deeper_by_depth": deep_by_depth}

# ---- (b) flag on --------------------------------------------------------------------------------
chk(kids(NEW, [], mirror_h6=True) == root_new, "root flag on")
per_case = {}
total = 0
kept_names = set()
for t in tops:
    off, on = kids(NEW, t), kids(NEW, t, mirror_h6=True)
    tn = NEW.layers_name(t)
    if tn == "0s0":
        chk(on == off, "H3 unchanged with flag"); chk(len(on) == 100, "H3 100"); continue
    a, s = t[0][1]
    own = [nm(t + [list(o)]) for o in own_kept(a, s)]
    chk(set(on) <= set(off), f"subset {tn}")
    chk(sorted(on) == sorted(own), f"own rule {tn}")
    chk(len(off) == 153 and len(on) == 81, f"counts {tn} {len(off)} {len(on)}")
    # exactly one of each phi-pair, every self-mirror kept
    opts = own_options({0, a}); pairs = selfm = 0
    keptset = {own_key(o) for o in own_kept(a, s)}
    for o in opts:
        p = own_phi(a, s, o)
        chk(own_phi(a, s, p) == tuple(sorted(o)), f"involution {tn}")
        chk(p in {tuple(sorted(x)) for x in opts}, f"phi maps to options {tn}")
        if p == tuple(sorted(o)): selfm += 1; chk(own_key(o) in keptset, f"self kept {tn}")
        elif own_key(o) < own_key(p):
            pairs += 1; chk(own_key(o) in keptset and own_key(p) not in keptset, f"one per pair {tn}")
    # NEW.h6_phi equals own phi on every option
    for o in opts:
        chk(tuple(tuple(x) for x in NEW.h6_phi(M, a, s, list(o))) == own_phi(a, s, o), f"h6_phi {tn}")
    one = sum(1 for x in on if "s" not in x.split("_")[1])
    per_case[tn] = {"children_off": len(off), "children_on": len(on), "one_orbit_kept": one,
                    "self_mirror": selfm, "pairs": pairs}
    total += len(on); kept_names |= set(on)
    # grandchildren below kept options stay complete
    for x in on[:: 10]:
        L = NEW.parse_layers(x)
        chk(kids(NEW, L, mirror_h6=True) == kids(OLD, L), f"below kept {x}")
chk(total == 810, f"total {total}")
out["b"] = {"per_case": per_case, "total_kept": total}
# h6m_kept columns
col = {"rows": 0, "h6_rows": 0, "agree": 0, "disagree": []}
for f in sorted(glob.glob(os.path.join(RES, "C3W3/lists/*.tsv"))):
    for r in csv.DictReader(open(f), delimiter="\t"):
        if "h6m_kept" not in r: continue
        col["rows"] += 1
        L = NEW.parse_layers(r["node"])
        is_h6 = len(L) >= 2 and len(L[0]) == 2
        if not is_h6:
            if r["h6m_kept"] != "na": col["disagree"].append((os.path.basename(f), r["node"], r["h6m_kept"]))
            continue
        col["h6_rows"] += 1
        a, s = L[0][1]
        mine = "yes" if own_key(L[1]) <= own_key(own_phi(a, s, L[1])) else "no"
        if len(L) == 2: chk((r["node"] in kept_names) == (mine == "yes"), f"kept_names {r['node']}")
        if mine == r["h6m_kept"]: col["agree"] += 1
        else: col["disagree"].append((os.path.basename(f), r["node"], r["h6m_kept"], mine))
out["h6m_kept_columns"] = col
chk(not col["disagree"], "h6m_kept column")
# ---- mutations: wrong maps must be told apart from C3T's kept sets, and they leave true pairs uncovered
muts = {
    "h3_map_m_minus_r": lambda a, s, o: tuple(sorted(((M - r) % M, None if g is None else 1 - g) for r, g in o)),
    "no_sigma_change": lambda a, s, o: tuple(sorted(((a - r) % M, g) for r, g in o)),
    "no_r_lt_a_term": lambda a, s, o: tuple(sorted(((a - r) % M, None if g is None else g ^ (s == 0)) for r, g in o)),
    "no_s_eq_0_term": lambda a, s, o: tuple(sorted(((a - r) % M, None if g is None else g ^ (r < a)) for r, g in o)),
}
mres = {}
for mn, f in muts.items():
    differ = uncovered = 0
    for t in tops[1:]:
        a, s = t[0][1]
        opts = own_options({0, a})
        kept_m = {own_key(o) for o in opts if own_key(o) <= own_key(f(a, s, o))}
        c3t = {own_key(tuple(tuple(x) for x in o)) for o in NEW.h6_layer2_kept(M, a, s)}
        differ += kept_m != c3t
        uncovered += sum(1 for o in opts if own_key(o) not in kept_m and own_key(own_phi(a, s, o)) not in kept_m)
    mres[mn] = {"cases_differing_from_c3t": differ, "options_uncovered_by_true_phi": uncovered}
    chk(differ > 0 and uncovered > 0, f"mutation {mn} not detected")
out["mutations"] = mres
out["failures"] = len(fails); out["failure_sample"] = fails[:20]
print(json.dumps(out, indent=1))
