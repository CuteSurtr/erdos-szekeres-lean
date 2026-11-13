#!/usr/bin/env python3
"""A2 audit: independent composer for the 3-fold class (m = 11, k = 7).

Written from the soundness argument (C3-S soundness.md Lemmas 1-5, the H6M addendum and the sigma
split rules), not from compose.py / mycompose.py.  From the repository it uses only the variable
numbering of the vendored, byte-identical c3cnf.py (C3Enc.__init__: the T and s literal maps), and
hullcase.node_units purely as a cross-check of this file's own unit generator.

Cover rules (each one is a complete cover of its parent, so 'covered' is sound whatever order the
search tries them in):
  * certified: a record with certified is True, status UNSATISFIABLE, lrat_check == 'c VERIFIED',
    cake_lpr == 's VERIFIED UNSAT', whose cnf_sha256 equals sha256(header' + BASE body + units),
    units re-derived here from the node name.
  * root: all 11 top cases covered.
  * depth-1 node T (H3 or H6(a,s)): for every pair {O, phi(O)} of layer-2 options, the plain node
    T+O or the plain node T+phi(O) is covered (Lemma 5 for H3, Lemma H6M for H6; phi re-derived
    here).  No sigma split at depth <= 1.
  * depth >= 2, single-bit sigma split: (L, C) is covered if for some free residue r both
    (L, C + {r: 0}) and (L, C + {r: 1}) are covered.  Any K-bit split is a composition of these.
  * depth >= 2, layer split: (L, C) is covered if it has at least one child and every next layer O
    (one orbit on an unused residue, or two orbits with all 4 sigma values) that does not give a
    residue of C an explicit sigma different from C's value has (L + O, C) covered.
usage: a2compose.py BODY RESULTS_DIR FILELIST [--no-sha] [--report OUT.json]"""
import hashlib
import itertools
import json
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
from c3cnf import C3Enc  # noqa: E402

M, K = 11, 7
N = 3 * M
BASE_SHA = "bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da"
BASE_V, BASE_C = 168399, 4154921
sys.setrecursionlimit(100000)


# ----------------------------------------------------------------------------- names
def parse(name):
    """-> (layers, cube) with layers a tuple of tuples of (r, s|None), cube a tuple of (r, v)."""
    if "__" in name:
        lay, cub = name.split("__")
    else:
        lay, cub = name, None
    layers = []
    for L in lay.split("_"):
        out = []
        for tok in L.split("-"):
            if "s" in tok:
                r, s = tok.split("s")
                out.append((int(r), int(s)))
            else:
                out.append((int(tok), None))
        layers.append(tuple(out))
    cube = []
    if cub is not None:
        for tok in cub.split("-"):
            r, v = tok.split("s")
            cube.append((int(r), int(v)))
    return tuple(layers), tuple(cube)


def fmt(layers, cube=()):
    s = "_".join("-".join(str(r) if g is None else f"{r}s{g}" for r, g in L) for L in layers)
    if cube:
        s += "__" + "-".join(f"{r}s{v}" for r, v in cube)
    return s


def valid(layers, cube):
    """structural validity of a tree node name (canonical spelling)."""
    if not layers:
        return False
    top = layers[0]
    if top == ((0, 0),):
        pass
    elif len(top) == 2 and top[0] == (0, 0) and top[1][1] in (0, 1) and 1 <= top[1][0] <= M // 2:
        pass
    else:
        return False
    used = {r for r, _ in top}
    for L in layers[1:]:
        if len(L) == 1:
            if L[0][1] is not None:
                return False
        elif len(L) == 2:
            if L[0][0] >= L[1][0] or L[0][1] not in (0, 1) or L[1][1] not in (0, 1):
                return False
        else:
            return False
        for r, _ in L:
            if r in used or not (1 <= r < M):
                return False
            used.add(r)
    rs = [r for r, _ in cube]
    if rs != sorted(rs) or len(set(rs)) != len(rs):
        return False
    explicit = {r: s for L in layers for r, s in L if s is not None}
    for r, v in cube:
        # a cube bit may sit on a residue that a later layer uses (rule-3 children keep C); it must
        # not contradict an explicit layer sigma (such a node is not a tree node)
        if not (1 <= r < M) or v not in (0, 1) or (r in explicit and explicit[r] != v):
            return False
    return True


# ----------------------------------------------------------------------------- units (own code)
E = C3Enc(M, K)  # __init__ only: literal maps T (chi_S per orbit) and s (sigma bits)


def ccw_lit(p, q, r):
    t = (p, q, r)
    st = tuple(sorted(t))
    inv = (p > q) + (p > r) + (q > r)
    return (-1 if inv & 1 else 1) * E.T[st]


def sig_lit(i):
    """literal 'sigma_i = 1': sigma_r = s_r, sigma_{r+m} = not s_r, sigma_{r+2m} = s_r."""
    r, w = i % M, i // M
    return -E.s[r] if w == 1 else E.s[r]


def ring(L):
    """ccw boundary order of a layer = angular order about c (Lemma 1/3)."""
    if len(L) == 1:
        r = L[0][0]
        # one orbit: R(r) = r - m = r + 2m is 120 deg further ccw, then R^2(r) = r + m
        return [r, r + 2 * M, r + M]
    pts = []
    for r, s in L:
        pts += [((s, r)), ((1 - s, r + M)), ((s, r + 2 * M))]
    return [lab for _, lab in sorted(pts)]


def my_units(layers, cube):
    out, used = [], set()
    for L in layers:
        for r, s in L:
            if s is not None and r != 0:
                out.append(sig_lit(r) if s else -sig_lit(r))
        H = ring(L)
        rest = [w for w in range(N) if w not in used]
        for t in range(len(H)):
            u, v = H[t], H[(t + 1) % len(H)]
            for w in rest:
                if w != u and w != v:
                    out.append(ccw_lit(u, v, w))
        used |= set(H)
    for r, v in cube:
        out.append(sig_lit(r) if v else -sig_lit(r))
    return out


# ----------------------------------------------------------------------------- tree (own code)
def options(used):
    rem = [r for r in range(M) if r not in used]
    out = [((r, None),) for r in rem]
    for b, c in itertools.combinations(rem, 2):
        for sb in (0, 1):
            for sc in (0, 1):
                out.append(((b, sb), (c, sc)))
    return out


def phi_h3(L):
    return tuple(sorted(((M - r) % M, None if s is None else 1 - s) for r, s in L))


def phi_h6(a, s0, L):
    return tuple(sorted(((a - r) % M, None if g is None else g ^ int(r < a) ^ int(s0 == 0)) for r, g in L))


def conflicts(O, cube):
    cv = dict(cube)
    return any(s is not None and r in cv and cv[r] != s for r, s in O)


def top_cases():
    out = [((0, 0),)]
    for a in range(1, M // 2 + 1):
        for s in (0, 1):
            out.append(((0, 0), (a, s)))
    return out


# ----------------------------------------------------------------------------- main
def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    body_path, rdir, flist = args[:3]
    nosha = "--no-sha" in sys.argv
    rep_path = None
    if "--report" in sys.argv:
        rep_path = sys.argv[sys.argv.index("--report") + 1]
    files = [l.strip() for l in open(flist) if l.strip()]
    t0 = time.time()
    stats = {"files": len(files), "records": 0, "certified_records": 0, "with_proof_sha256": 0,
             "bad_names": [], "noncanonical_names": [], "status_not_unsat_but_certified": 0,
             "base_sha_mismatch": 0, "units_field_mismatch": 0, "cnf_sha_mismatch": [],
             "sigma_cube_format_records": 0, "certified_true_but_checker_strings_wrong": 0}
    cert = {}  # name -> list of records
    known = set()  # every node name seen in any record (certified, split, unknown)
    for f in files:
        for ln, l in enumerate(open(os.path.join(rdir, f))):
            l = l.strip()
            if not l:
                continue
            r = json.loads(l)
            stats["records"] += 1
            if "node" not in r or "meta" in r:
                continue
            if "--skip-cube-format" in sys.argv and "cube" in r:
                continue  # audit variant: ignore sigma_cubes.py-format records
            try:
                if "cube" in r:
                    lay, cub = parse(r["node"])
                    if cub:
                        raise ValueError("cube record on a cube node")
                    cub = tuple(sorted((int(x), int(v)) for x, v in r["cube"].items()))
                    stats["sigma_cube_format_records"] += 1
                else:
                    lay, cub = parse(r["node"])
            except Exception as ex:  # noqa: BLE001
                stats["bad_names"].append((f, ln + 1, r["node"], str(ex)))
                continue
            name = fmt(lay, cub)
            if not valid(lay, cub):
                stats["noncanonical_names"].append((f, ln + 1, r["node"]))
                continue
            known.add(name)
            ok = (r.get("certified") is True and r.get("status") == "UNSATISFIABLE"
                  and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT")
            if r.get("certified") is True and not ok:
                if r.get("status") != "UNSATISFIABLE":
                    stats["status_not_unsat_but_certified"] += 1
                else:
                    stats["certified_true_but_checker_strings_wrong"] += 1
            if ok:
                if "base_sha256" in r and r["base_sha256"] != BASE_SHA:
                    stats["base_sha_mismatch"] += 1
                    continue
                stats["certified_records"] += 1
                if r.get("proof_sha256"):
                    stats["with_proof_sha256"] += 1
                cert.setdefault(name, []).append((f, ln + 1, r))
    stats["certified_nodes"] = len(cert)
    stats["certified_cube_nodes"] = sum(1 for n in cert if "__" in n)
    stats["certified_nodes_with_a_proof_sha256_record"] = sum(1 for n, L in cert.items() if any(x[2].get("proof_sha256") for x in L))
    print("loaded", json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in stats.items()}), f"{time.time() - t0:.1f}s", flush=True)

    # ---- units and sha re-derivation (units are generated on the fly, never all stored)
    import hullcase  # noqa: E402  (cross-check only)

    def unit_count(name):
        lay, cub = parse(name)
        cnt, used = 0, 0
        for L in lay:
            cnt += sum(1 for r, s in L if s is not None and r != 0)
            h = 3 * len(L)
            cnt += h * (N - used - 2)
            used += h
        return cnt + len(cub)

    ucount = {name: unit_count(name) for name in cert}
    for name, L in cert.items():
        for f, ln, r in L:
            if "units" in r and r["units"] != ucount[name]:
                stats["units_field_mismatch"] += 1
    shaok = {}
    xbad = 0
    if not nosha:
        need = sorted(set(ucount.values()))
        hs = {n: hashlib.sha256(f"p cnf {BASE_V} {BASE_C + n}\n".encode()) for n in need}
        bh = hashlib.sha256(f"p cnf {BASE_V} {BASE_C}\n".encode())
        with open(body_path, "rb") as fb:
            for b in iter(lambda: fb.read(1 << 22), b""):
                bh.update(b)
                for h in hs.values():
                    h.update(b)
        stats["base_sha_recomputed"] = bh.hexdigest()
        if bh.hexdigest() != BASE_SHA:
            print("BASE BODY DOES NOT GIVE THE BASE SHA", flush=True)
            sys.exit(1)
        stats["distinct_unit_counts"] = len(need)
        for name, L in cert.items():
            us = my_units(*parse(name))
            assert len(us) == ucount[name]
            if us != hullcase.node_units(M, name, E.ccw, E.sig):
                xbad += 1
            h = hs[len(us)].copy()
            h.update("".join(f"{u} 0\n" for u in us).encode())
            d = h.hexdigest()
            good = [x for x in L if x[2].get("cnf_sha256") == d]
            for f, ln, r in L:
                if r.get("cnf_sha256") != d:
                    stats["cnf_sha_mismatch"].append((f, ln, name, r.get("cnf_sha256"), d))
            shaok[name] = bool(good)
        print("sha re-derived", f"{time.time() - t0:.1f}s", "mismatches", len(stats["cnf_sha_mismatch"]),
              "own-units vs hullcase mismatches", xbad, flush=True)
    else:
        shaok = {n: True for n in cert}
    stats["own_units_vs_hullcase_mismatch"] = xbad
    certified = {n for n in cert if shaok[n]}

    # ---- index of known names for search hints (hints only steer the search; every rule is sound)
    by_layers = {}  # layers -> list of cubes seen with exactly these layers
    layer_prefix = set()  # (proper layer prefix, cube) of known names: a layer split was explored there
    for name in known:
        lay, cub = parse(name)
        by_layers.setdefault(lay, []).append(cub)
        for j in range(1, len(lay)):
            layer_prefix.add((lay[:j], cub))

    memo = {}
    used_cert = set()
    calls = [0]

    def cube_ext(c_small, c_big):
        """c_big extends c_small (as partial sigma assignments)"""
        d = dict(c_big)
        return all(d.get(r) == v for r, v in c_small)

    def covered(lay, cub):
        key = (lay, cub)
        if key in memo:
            return memo[key]
        calls[0] += 1
        memo[key] = False
        name = fmt(lay, cub)
        if name in certified:
            used_cert.add(name)
            memo[key] = True
            return True
        if len(lay) == 1:
            memo[key] = (not cub) and cover_depth1(lay)
            return memo[key]
        used = {r for L in lay for r, _ in L}
        cres = {r for r, _ in cub}
        # single-bit sigma splits, hinted by known names with the same layers and a larger cube
        hint = set()
        for c2 in by_layers.get(lay, []):
            if len(c2) > len(cub) and cube_ext(cub, c2):
                hint |= {r for r, _ in c2} - cres
        for r in sorted(hint):
            if r in used or r in cres or r == 0:
                continue
            c0 = tuple(sorted(cub + ((r, 0),)))
            c1 = tuple(sorted(cub + ((r, 1),)))
            if covered(lay, c0) and covered(lay, c1):
                memo[key] = True
                return True
        # layer split, tried when some known node extends these layers with the same cube
        if (lay, cub) in layer_prefix:
            ch = [O for O in options(used) if not conflicts(O, cub)]
            if ch and all(covered(lay + (O,), cub) for O in ch):
                memo[key] = True
                return True
        return False

    pair_report = {}

    def cover_depth1(lay):
        top = lay[0]
        used = {r for r, _ in top}
        if top == ((0, 0),):
            phi = phi_h3
        else:
            a, s0 = top[1]
            phi = lambda L, a=a, s0=s0: phi_h6(a, s0, L)  # noqa: E731
        opts = options(used)
        seen, okall, npairs, nself, open_pairs = set(), True, 0, 0, []
        for O in opts:
            if O in seen:
                continue
            P = phi(O)
            assert P in opts and phi(P) == O, ("phi is not an involution on options", lay, O, P)
            seen |= {O, P}
            npairs += 1
            nself += (P == O)
            cO = covered(lay + (O,), ())
            cP = cO if P == O else covered(lay + (P,), ())
            if not (cO or cP):
                okall = False
                open_pairs.append(fmt(lay + (O,)))
        pair_report[fmt(lay)] = {"options": len(opts), "pairs": npairs, "self_paired": nself, "open_pairs": open_pairs}
        return okall

    root_ok = all(covered((t,), ()) for t in top_cases())
    # one explicit cut: follow, from the root, the first rule that succeeded (memo values only)
    cut = set()
    stack = [((t,), ()) for t in top_cases()] if root_ok else []
    seen2 = set()
    while stack:
        lay, cub = stack.pop()
        if (lay, cub) in seen2:
            continue
        seen2.add((lay, cub))
        name = fmt(lay, cub)
        if name in certified:
            cut.add(name)
            continue
        assert memo.get((lay, cub)), name
        used = {r for L in lay for r, _ in L}
        if len(lay) == 1:
            top = lay[0]
            phi = phi_h3 if top == ((0, 0),) else (lambda L, a=top[1][0], s0=top[1][1]: phi_h6(a, s0, L))
            done = set()
            for O in options(used):
                if O in done:
                    continue
                P = phi(O)
                done |= {O, P}
                stack.append((lay + (O,), ()) if memo.get((lay + (O,), ())) else (lay + (P,), ()))
            continue
        cres = {r for r, _ in cub}
        nxt = None
        for r in range(1, M):
            if r in used or r in cres:
                continue
            c0, c1 = tuple(sorted(cub + ((r, 0),))), tuple(sorted(cub + ((r, 1),)))
            if memo.get((lay, c0)) and memo.get((lay, c1)):
                nxt = [(lay, c0), (lay, c1)]
                break
        if nxt is None:
            nxt = [(lay + (O,), cub) for O in options(used) if not conflicts(O, cub)]
            assert nxt and all(memo.get(x) for x in nxt), name
        stack += nxt
    # status of each depth-2 node (all 1,720), for comparison with C3FINAL_mirrorh6_roots.tsv
    d2 = {}
    for t in top_cases():
        for O in options({r for r, _ in t}):
            d2[fmt((t, O))] = covered((t, O), ())
    res = {"class_covered": root_ok, "search_calls": calls[0], "certified_nodes_reached_by_search": len(used_cert),
           "certified_nodes_in_one_explicit_cut": len(cut),
           "depth1": pair_report, "depth2_covered": sum(d2.values()), "depth2_total": len(d2),
           "stats": {k: (v if not isinstance(v, list) else len(v)) for k, v in stats.items()},
           "cnf_sha_mismatch_sample": stats["cnf_sha_mismatch"][:20], "bad_names": stats["bad_names"][:20],
           "noncanonical_names": stats["noncanonical_names"][:20], "seconds": round(time.time() - t0, 1)}
    print(json.dumps({k: v for k, v in res.items() if k != "depth1"}, indent=1))
    for k, v in pair_report.items():
        print(k, v["options"], "options,", v["pairs"], "pairs,", v["self_paired"], "self-paired, open pairs:", len(v["open_pairs"]))
    if rep_path:
        res["depth2_status"] = d2
        res["cut"] = sorted(cut)
        json.dump(res, open(rep_path, "w"))
    pass

if __name__ == "__main__":
    main()
