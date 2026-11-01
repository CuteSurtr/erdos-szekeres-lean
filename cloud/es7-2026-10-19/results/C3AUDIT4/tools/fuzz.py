"""C3AUDIT4: random close_tree-like record sets plus targeted mutations, judged by composers and by an own
brute-force cover check.  Soundness criterion: a composer that says "covered" must have 0 brute holes;
a forged sha must be rejected.  Agreement: covered / frontier / open depth-2 roots between composers.
Records carry the true cnf_sha256 (own units, C3AUDIT3 mycompose.units for the bytes) so that every
forgery is structural unless stated.
usage: fuzz.py m k BASE NCASES SEED OUTDIR COMPOSER [COMPOSER ...]   (COMPOSER: 'mine' or a tools dir)"""
import hashlib, itertools, json, os, random, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(R, "C3a")); sys.path.insert(0, os.path.join(R, "C3AUDIT3", "tools"))
from c3cnf import C3Enc  # noqa
import mycompose as Y  # noqa  (only for units(): CNF bytes)

m, k, BASE, N, SEED, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
COMPS = sys.argv[7:]
H6M = os.environ.get("FUZZ_H6M") == "1"  # tree and composers with the Lemma H6M reduction (--mirror-h6)
os.makedirs(OUT, exist_ok=True)
E = C3Enc(m, k)
hdr, body = None, None
with open(BASE, "rb") as f:
    hdr = f.readline().decode().split(); body = f.read()
_pre = {}


def true_sha(layers, cube):
    us = Y.units(m, E, layers, cube)
    if len(us) not in _pre:
        h = hashlib.sha256(); h.update(f"p cnf {hdr[2]} {int(hdr[3]) + len(us)}\n".encode()); h.update(body); _pre[len(us)] = h
    h = _pre[len(us)].copy(); h.update("".join(f"{u} 0\n" for u in us).encode()); return h.hexdigest()


# ---- own tree (independent of hullcase.py and mycompose.py) ----
def nm(layers, cube=()):
    s = "_".join("-".join(str(r) if v is None else f"{r}s{v}" for r, v in L) for L in layers)
    return s + ("__" + "-".join(f"{r}s{v}" for r, v in sorted(cube)) if cube else "")


def kids(layers):
    if not layers:
        o = [(((0, 0),),)]
        if k >= 7:
            o += [(((0, 0), (a, s)),) for a in range(1, m // 2 + 1) for s in (0, 1)]
        return o
    used = {r for L in layers for r, _ in L}
    free = [r for r in range(m) if r not in used]
    opts = [((r, None),) for r in free] + [((b, x), (c, y)) for b, c in itertools.combinations(free, 2) for x in (0, 1) for y in (0, 1)]
    if layers == (((0, 0),),):
        mir = lambda L: tuple(sorted(((m - r) % m, None if v is None else 1 - v) for r, v in L))
        kk = lambda L: tuple((r, -1 if v is None else v) for r, v in sorted(L))
        opts = [o for o in opts if kk(o) <= kk(mir(o))]
    if H6M and len(layers) == 1 and len(layers[0]) == 2:
        a, s = layers[0][1]
        phi = lambda O: tuple(sorted(((a - r) % m, None if v is None else v ^ int(r < a) ^ int(s == 0)) for r, v in O))
        kk = lambda L: tuple((r, -1 if v is None else v) for r, v in sorted(L))
        opts = [o for o in opts if kk(o) <= kk(phi(o))]
    return [layers + (o,) for o in opts]


def freeres(layers, cube):
    u = {r for L in layers for r, _ in L} | {r for r, _ in cube}
    return [r for r in range(1, m) if r not in u]


def cube_kids(layers, cube):
    cv = dict(cube)
    return [(c, cube) for c in kids(layers) if not any(v is not None and r in cv and cv[r] != v for r, v in c[-1])]


def sig_kids(layers, cube, K):
    b = freeres(layers, cube)[:K]
    return b, [(layers, tuple(sorted(cube + tuple(zip(b, vs))))) for vs in itertools.product((0, 1), repeat=K)]


CERT = {"status": "UNSATISFIABLE", "lrat_check": "c VERIFIED", "cake_lpr": "s VERIFIED UNSAT", "certified": True}


def crec(layers, cube):
    return dict(CERT, node=nm(layers, cube), cnf_sha256=true_sha(layers, cube))


def drive(rng, p, K, S, maxd, old_childless, as_cubes):
    """random close_tree (rules 2-4): returns records."""
    recs = []

    def go(layers, cube, d):
        if not layers:
            for c in kids(()):
                go(c, (), d + 1)
            return
        if d > maxd:
            return
        if d == maxd or rng.random() < p(d, layers, cube):
            recs.append(crec(layers, cube)); return
        recs.append({"node": nm(layers, cube), "status": "UNKNOWN"})
        if K and len(layers) >= 2 and len(cube) < S * K and len(freeres(layers, cube)) >= K:
            b, ch = sig_kids(layers, cube, K)
            if as_cubes and not cube and rng.random() < 0.5:
                # sigma_cubes.py format, no split record; children solved directly (all certified here)
                for L2, C2 in ch:
                    r = crec(L2, C2); r["node"] = nm(layers); r["cube"] = {str(a): v for a, v in C2}; recs.append(r)
                return
            recs.append({"node": nm(layers, cube), "split": True, "sigma_bits": b, "children": len(ch)})
            for L2, C2 in ch:
                go(L2, C2, d + 1)
            return
        ch = cube_kids(layers, cube) if layers else [(c, ()) for c in kids(layers)]
        if not ch:
            if old_childless:
                recs.append({"node": nm(layers, cube), "split": True, "children": 0})
            return
        recs.append({"node": nm(layers, cube), "split": True, "children": len(ch)})
        for L2, C2 in ch:
            go(L2, C2, d + 1)
    go((), (), 0)
    return recs


# ---- own brute force ----
def brute(recs):
    leaves = {}
    for r in recs:
        if r.get("certified") is True and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
            lay, _, cub = r["node"].partition("__")
            L = tuple(tuple(sorted(((int(t.split("s")[0]), int(t.split("s")[1]) if "s" in t else None) for t in x.split("-")))) for x in lay.split("_"))
            C = {int(t.split("s")[0]): int(t.split("s")[1]) for t in cub.split("-")} if cub else {}
            if "cube" in r:
                C = {int(a): v for a, v in r["cube"].items()}
            if nm(L, tuple(sorted(C.items()))) != (r["node"] if "cube" not in r else nm(L, tuple(sorted(C.items())))):
                continue  # non-canonical name: not a tree node
            leaves.setdefault(L, []).append(C)
    holes = []

    def dfs(P, U):
        if P:
            U = [s for s in U if not any(all(s[r] == v for r, v in C.items()) for C in leaves.get(P, []))]
        if not U:
            return
        ch = kids(P)
        if not ch:
            holes.append((nm(P), len(U))); return
        for c in ch:
            dfs(c, [s for s in U if all(v is None or r == 0 or s[r] == v for r, v in c[-1])])
    dfs((), [(0,) + v for v in itertools.product((0, 1), repeat=m - 1)])
    return holes


def run_comp(who, path, extra=()):
    extra = list(extra) + (["--mirror-h6"] if H6M else [])
    x = subprocess.run([sys.executable, os.path.join(HERE, "runcomp.py"), who, str(m), str(k), BASE, path] + extra,
                       capture_output=True, text=True)
    try:
        return json.loads(x.stdout.strip().splitlines()[-1])
    except Exception:
        return {"crash": x.stderr[-300:]}


def verdict(j):
    if "crash" in j: return "crash"
    if j.get("reject"): return "reject"
    return "covered" if j["covered"] else "not covered"


def mutate(rng, recs, kind):
    R = [dict(r) for r in recs]
    certs = [i for i, r in enumerate(R) if r.get("certified")]
    if kind == "drop_cert" and certs:
        del R[rng.choice(certs)]; return R, None
    if kind == "drop_split":
        sp = [i for i, r in enumerate(R) if r.get("split")]
        if sp: del R[rng.choice(sp)]; return R, None
    if kind == "forge_sha" and certs:
        i = rng.choice(certs); R[i]["cnf_sha256"] = hashlib.sha256(R[i]["cnf_sha256"].encode()).hexdigest(); return R, "reject"
    if kind == "flip_cube_bit":
        cs = [i for i in certs if "__" in R[i]["node"]]
        if cs:
            i = rng.choice(cs); L, C = R[i]["node"].split("__"); t = C.split("-"); j = rng.randrange(len(t))
            t[j] = t[j][:-1] + str(1 - int(t[j][-1]))
            lay = tuple(tuple(((int(a.split("s")[0]), int(a.split("s")[1]) if "s" in a else None) for a in x.split("-"))) for x in L.split("_"))
            cub = tuple((int(a.split("s")[0]), int(a.split("s")[1])) for a in t)
            R[i] = crec(lay, cub); return R, None
    if kind == "sigma_wrong_bits":
        sp = [i for i, r in enumerate(R) if "sigma_bits" in r]
        if sp:
            i = rng.choice(sp); b = list(R[i]["sigma_bits"]); b[-1] = b[-1] + 1 if b[-1] + 1 < m else b[0] - 1
            if b[-1] <= 0 or len(set(b)) < len(b): b = b[::-1] if len(b) > 1 else [0]
            R[i]["sigma_bits"] = b; return R, "reject"
    if kind == "sigma_depth1":
        R.append({"node": "0s0", "split": True, "sigma_bits": [1, 2], "children": 4}); return R, "reject"
    if kind == "childless_quarter":
        # replace a certified plain node P (>= 2 layers) by certificates of its children except one path
        # down to a fully layered node FULL, of which only one cube is certified
        ps = [i for i in certs if "__" not in R[i]["node"] and R[i]["node"].count("_") >= 1 and "cube" not in R[i]]
        if ps:
            i = rng.choice(ps)
            lay = tuple(tuple(((int(a.split("s")[0]), int(a.split("s")[1]) if "s" in a else None) for a in x.split("-"))) for x in R[i]["node"].split("_"))
            del R[i]
            cur = lay
            while kids(cur):
                ch = kids(cur); nxt = rng.choice(ch)
                R += [crec(c, ()) for c in ch if c != nxt]
                cur = nxt
            fr = freeres(cur, ())
            cube = tuple((r, rng.randrange(2)) for r in fr[:rng.randrange(1, max(2, len(fr) + 1))]) if fr else ()
            if cube:
                R.append(crec(cur, cube))
            else:
                R.append({"node": nm(cur), "split": True, "children": 0})
            return R, None
    if kind == "childless_cube_split":
        # a cube node L__C split by layers down to a fully layered L'__C left uncertified
        cs = [i for i in certs if "__" in R[i]["node"] and "cube" not in R[i]]
        if cs:
            i = rng.choice(cs); L, C = R[i]["node"].split("__")
            lay = tuple(tuple(((int(a.split("s")[0]), int(a.split("s")[1]) if "s" in a else None) for a in x.split("-"))) for x in L.split("_"))
            cub = tuple((int(a.split("s")[0]), int(a.split("s")[1])) for a in C.split("-"))
            del R[i]
            cur = lay
            while True:
                ch = cube_kids(cur, cub)
                R.append({"node": nm(cur, cub), "split": True, "children": len(ch)})
                if not ch: break
                nxt = rng.choice(ch)[0]
                R += [crec(c, cub) for c, _ in ch if c != nxt]
                cur = nxt
            return R, None
    if kind == "cubes_into_split_node":
        # sigma_cubes records for a node that also has an incomplete layer route: give 2^K - 1 cubes
        ps = [i for i in certs if "__" not in R[i]["node"] and R[i]["node"].count("_") >= 1 and "cube" not in R[i]]
        if ps:
            i = rng.choice(ps)
            lay = tuple(tuple(((int(a.split("s")[0]), int(a.split("s")[1]) if "s" in a else None) for a in x.split("-"))) for x in R[i]["node"].split("_"))
            fr = freeres(lay, ())
            if len(fr) >= 2:
                del R[i]
                b, ch = sig_kids(lay, (), 2)
                for L2, C2 in ch[:-1]:
                    r = crec(L2, C2); r["node"] = nm(lay); r["cube"] = {str(a): v for a, v in C2}; R.append(r)
                lc = kids(lay)
                R.append({"node": nm(lay), "split": True, "children": len(lc)})
                R += [crec(c, ()) for c in lc[:-1]]
                return R, None
    return None, None


KINDS = ["none", "drop_cert", "drop_split", "forge_sha", "flip_cube_bit", "sigma_wrong_bits", "sigma_depth1",
         "childless_quarter", "childless_cube_split", "cubes_into_split_node"]
rng = random.Random(SEED)
stats = {"cases": 0, "unsound": {c: 0 for c in COMPS}, "forge_not_rejected": {c: 0 for c in COMPS},
         "disagree": 0, "verdicts": {}}
log = open(os.path.join(OUT, f"fuzz_m{m}k{k}_s{SEED}{'_h6m' if H6M else ''}.jsonl"), "w")
for t in range(N):
    K = rng.choice([0, 1, 2, 2, 3])
    base_p = rng.uniform(0.3, 0.9) if os.environ.get("FUZZ_HIGH") != "1" else rng.uniform(0.75, 0.97)
    recs = drive(rng, lambda d, L, C: 0.0 if d < 2 else (base_p if (L and len(L[-1]) == 2) or os.environ.get("FUZZ_HIGH") != "1" or freeres(L, C) else 1.0), K, rng.choice([1, 2]), rng.choice([4, 5, 6]),
                 rng.random() < 0.5, rng.random() < 0.5)
    kind = KINDS[t % len(KINDS)]
    if kind == "none":
        R2, exp = recs, None
    else:
        R2, exp = mutate(rng, recs, kind)
        if R2 is None: continue
    rng.shuffle(R2) if rng.random() < 0.3 else None
    p = os.path.join(OUT, f"cur_m{m}k{k}_s{SEED}.jsonl")
    open(p, "w").write("".join(json.dumps(r) + "\n" for r in R2))
    holes = brute(R2)
    res = {c: run_comp(c, p) for c in COMPS}
    v = {c: verdict(res[c]) for c in COMPS}
    stats["cases"] += 1
    for c in COMPS:
        if v[c] == "covered" and holes: stats["unsound"][c] += 1
        if exp == "reject" and v[c] != "reject": stats["forge_not_rejected"][c] += 1
    sig = {c: (v[c], tuple(res[c].get("frontier", ())), tuple(res[c].get("open_d2", ()))) for c in COMPS}
    agree = len(set(sig.values())) == 1
    if not agree: stats["disagree"] += 1
    key = kind + ":" + "/".join(v[c] for c in COMPS) + (":holes" if holes else ":noholes")
    stats["verdicts"][key] = stats["verdicts"].get(key, 0) + 1
    entry = {"t": t, "kind": kind, "K": K, "nrec": len(R2), "holes": len(holes), "verdicts": v, "agree": agree,
             "frontier_n": {c: res[c].get("frontier_n") for c in COMPS}}
    log.write(json.dumps(entry) + "\n")
    if (not agree) or any(v[c] == "covered" and holes for c in COMPS) or (exp == "reject" and any(v[c] != "reject" for c in COMPS)):
        bad = os.path.join(OUT, f"case_m{m}k{k}_s{SEED}_t{t}_{kind}.jsonl")
        open(bad, "w").write("".join(json.dumps(r) + "\n" for r in R2))
        entry["file"] = os.path.basename(bad)
        print(json.dumps(entry), flush=True)
print(json.dumps(stats))
