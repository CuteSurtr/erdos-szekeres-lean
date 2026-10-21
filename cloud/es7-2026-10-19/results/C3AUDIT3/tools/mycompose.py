"""C3AUDIT3: independent cut check with sigma-cube nodes (results/C3U/TASK.md rules 1-5).
Grown from results/C3AUDIT/tools/mycompose.py; written from the specification only (no C3U/C3T
code).  Own tree, own name parser, own layer units (re-derived CNF sha256); from the repository it
uses only the base encoding C3a/c3cnf.py (variable numbering of ccw and sigma).
usage: mycompose.py [--m M --k K] [--no-sha] [--base-sha HEX] BASE RECORDS.jsonl [...]
Exit 1 with {"error": ...} on a malformed or forged input; else prints a JSON summary."""
import hashlib, itertools, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "C3a"))
from c3cnf import C3Enc  # noqa: E402

BASE_SHA_11_7 = "bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da"


def die(msg):
    print(json.dumps({"error": msg})); sys.exit(1)


# ---- names ------------------------------------------------------------------------------------
# layer: tuple of (r, s) with s in {0, 1, None}, in name order; node: (layers, cube) where cube is
# a tuple of (r, v), in name order.  Canonical key: residues of a layer sorted, layers in order,
# cube as written (the specification fixes it sorted; an unsorted cube never matches a tree node).

def parse_layer(txt):
    out = []
    for t in txt.split("-"):
        if "s" in t:
            a, b = t.split("s")
            if not a.isdigit() or b not in ("0", "1"): raise ValueError(t)
            out.append((int(a), int(b)))
        else:
            if not t.isdigit(): raise ValueError(t)
            out.append((int(t), None))
    return tuple(out)


def parse(name):
    if name.count("__") > 1: raise ValueError(name)
    lay, _, cub = name.partition("__")
    layers = tuple(parse_layer(x) for x in lay.split("_"))
    cube = ()
    if "__" in name:
        cube = []
        for t in cub.split("-"):
            a, b = t.split("s")
            if not a.isdigit() or b not in ("0", "1"): raise ValueError(t)
            cube.append((int(a), int(b)))
        cube = tuple(cube)
        if not cube or len({r for r, _ in cube}) != len(cube): raise ValueError(name)
    return layers, cube


def key(layers, cube):
    return (tuple(tuple(sorted(L, key=lambda x: x[0])) for L in layers), tuple(cube))


def lname(L):
    return "-".join(f"{r}" if s is None else f"{r}s{s}" for r, s in L)


def kname(k):
    layers, cube = k
    return "_".join(lname(L) for L in layers) + ("__" + "-".join(f"{r}s{v}" for r, v in cube) if cube else "")


# ---- tree -------------------------------------------------------------------------------------

def options(unused):
    o = [((r, None),) for r in unused]
    for b, c in itertools.combinations(sorted(unused), 2):
        for sb in (0, 1):
            for sc in (0, 1):
                o.append(((b, sb), (c, sc)))
    return o


def okey(L):
    return tuple(sorted((r, -1 if s is None else s) for r, s in L))


def mirror(m, L):
    return tuple(((m - r) % m, None if s is None else 1 - s) for r, s in L)


def layer_children(m, k, layers):
    """children layer tuples of a plain node (C3-S tree, H3 mirror reduction, no H6 mirror)."""
    if not layers:
        out = [(((0, 0),),)]
        if k - 1 >= 6:
            out += [(((0, 0), (a, s)),) for a in range(1, m // 2 + 1) for s in (0, 1)]
        return out
    used = {r for L in layers for r, _ in L}
    o = options([r for r in range(m) if r not in used])
    if layers == (((0, 0),),):
        o = [x for x in o if okey(x) <= okey(mirror(m, x))]
    return [layers + (x,) for x in o]


def free(m, layers, cube):
    used = {r for L in layers for r, _ in L} | {r for r, _ in cube}
    return [r for r in range(1, m) if r not in used]


def sigma_kids(m, layers, cube, bits):
    out = []
    for vals in itertools.product((0, 1), repeat=len(bits)):
        out.append(key(layers, tuple(sorted(cube + tuple(zip(bits, vals))))))
    return out


def cube_layer_kids(m, k, layers, cube):
    cv = dict(cube)
    out = []
    for L2 in layer_children(m, k, layers):
        if any(s is not None and r in cv and cv[r] != s for r, s in L2[-1]):
            continue  # newest layer contradicts the cube: empty
        out.append(key(L2, cube))
    return out


# ---- units (own re-implementation of the layer clauses) ---------------------------------------

def ring(m, L):
    if len(L) == 1:
        r = L[0][0]
        return [r, r + 2 * m, r + m]
    keys = []
    for r, s in L:
        keys += [(s, r), (1 - s, r + m), (s, r + 2 * m)]
    return [i for _, i in sorted(keys)]


def units(m, E, layers, cube):
    n, used, us = 3 * m, set(), []
    for L in layers:
        us += [E.sig(r) if s else -E.sig(r) for r, s in L if s is not None and r != 0]
        H = ring(m, L)
        for t in range(len(H)):
            u, v = H[t], H[(t + 1) % len(H)]
            us += [E.ccw(u, v, w) for w in range(n) if w not in used and w != u and w != v]
        used |= set(H)
    us += [E.sig(r) if v else -E.sig(r) for r, v in cube]
    return us


def fsha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""): h.update(b)
    return h.hexdigest()


def main():
    av = sys.argv[1:]
    m, k, nosha, bsha = 11, 7, False, None
    files = []
    i = 0
    while i < len(av):
        a = av[i]
        if a == "--m": m = int(av[i + 1]); i += 2
        elif a == "--k": k = int(av[i + 1]); i += 2
        elif a == "--base-sha": bsha = av[i + 1]; i += 2
        elif a == "--no-sha": nosha = True; i += 1
        elif a.startswith("--"): die(f"unknown option {a}")
        else: files.append(a); i += 1
    if len(files) < 1: die("usage")
    base, files = files[0], files[1:]
    if bsha is None:
        bsha = BASE_SHA_11_7 if (m, k) == (11, 7) else None
    real = fsha(base)
    if bsha is not None and real != bsha: die(f"base sha {real} != {bsha}")
    cert, ssplit, lsplit, cubes, allcert = {}, {}, set(), {}, []
    for f in files:
        for ln, l in enumerate(open(f), 1):
            r = json.loads(l)
            if r.get("base_sha256") not in (None, real): die(f"{f}:{ln} base_sha256 mismatch")
            if "node" not in r: continue
            try:
                layers, cube = parse(r["node"])
                if "cube" in r:
                    if cube: die(f"{f}:{ln} sigma_cubes record on a cube node")
                    cube = tuple(sorted((int(a), int(b)) for a, b in r["cube"].items()))
                    if not cube or any(v not in (0, 1) for _, v in cube): die(f"{f}:{ln} bad cube")
            except (ValueError, AttributeError) as e:
                die(f"{f}:{ln} bad name {r['node']!r}: {e}")
            kk = key(layers, cube)
            if r.get("split"):
                if "sigma_bits" in r:
                    b = r["sigma_bits"]
                    fr = free(m, layers, cube)
                    if (not isinstance(b, list) or not b or len(layers) < 2 or b != fr[:len(b)]
                            or not all(type(x) is int for x in b)):
                        die(f"{f}:{ln} sigma split of {r['node']} with bits {b}, free {fr} (layers {len(layers)})")
                    ssplit.setdefault(kk, set()).add(tuple(b))
                elif cube:
                    lsplit.add(kk)
            if r.get("certified") is True and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
                allcert.append((f, ln, r, layers, cube))
                cert[kk] = r
                if "cube" in r:
                    cubes.setdefault(key(layers, ()), {}).setdefault(tuple(x for x, _ in cube), set()).add(kk)
    # implied sigma splits from sigma_cubes records: all 2^K cubes on the K smallest free residues certified
    for pk, d in cubes.items():
        layers = pk[0]
        for res, got in d.items():
            if len(layers) >= 2 and list(res) == free(m, layers, ())[:len(res)] and set(sigma_kids(m, layers, (), list(res))) <= got:
                ssplit.setdefault(pk, set()).add(res)
    nsha = 0
    if not nosha:
        E = C3Enc(m, k)
        with open(base, "rb") as fb:
            hdr = fb.readline().decode().split(); body = fb.read()
        if len(hdr) != 4 or hdr[:2] != ["p", "cnf"]: die("bad base header")
        pre = {}
        for f, ln, r, layers, cube in allcert:
            us = units(m, E, layers, cube)
            if len(us) not in pre:
                h = hashlib.sha256(); h.update(f"p cnf {hdr[2]} {int(hdr[3]) + len(us)}\n".encode()); h.update(body)
                pre[len(us)] = h
            h = pre[len(us)].copy(); h.update("".join(f"{u} 0\n" for u in us).encode())
            if h.hexdigest() != r.get("cnf_sha256"): die(f"{f}:{ln} cnf_sha256 mismatch for {r['node']}")
            if "units" in r and r["units"] != len(us): die(f"{f}:{ln} units {r['units']} != {len(us)}")
            nsha += 1
    prefixes = set()
    for kk in list(cert) + list(ssplit) + list(lsplit):
        for j in range(1, len(kk[0]) + 1):
            prefixes.add(kk[0][:j])
    memo, missing, used_sig = {}, [], set()

    def cov(kk):
        if kk in memo: return memo[kk]
        memo[kk] = False
        layers, cube = kk
        res = False
        if kk in cert:
            res = True
        if not res:
            for b in sorted(ssplit.get(kk, ())):
                if all([cov(c) for c in sigma_kids(m, layers, cube, list(b))]):
                    res = True; used_sig.add(kk); break
        if not res:
            if cube:
                if kk in lsplit:
                    res = all([cov(c) for c in cube_layer_kids(m, k, layers, cube)])
            elif not layers or layers in prefixes:
                res = all([cov(key(c, ())) for c in layer_children(m, k, layers)])
        if not res and kk not in cert and kk not in ssplit and kk not in lsplit and not (not cube and (not layers or layers in prefixes)):
            missing.append(kname(kk))
        memo[kk] = res
        return res

    ok = cov(((), ()))
    print(json.dumps({"m": m, "k": k, "certified_records": len(allcert), "certified_nodes": len(cert),
                      "certified_cube_nodes": sum(1 for x in cert if x[1]), "sha_checked": nsha,
                      "sigma_split_nodes": len(ssplit), "sigma_splits_used": len(used_sig),
                      "cube_layer_split_nodes": len(lsplit), "class_covered": ok,
                      "uncovered_frontier": len(missing), "uncovered_sample": sorted(missing)[:5]}))


if __name__ == "__main__":
    main()
