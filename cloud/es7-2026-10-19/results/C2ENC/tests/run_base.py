"""Evaluate the real t = 17 base CNF (zcnf.py rot 17 7 --m 2 --hull) on real centrally symmetric 34-point sets.

For each configuration and each chosen first point p0 the set is labelled in the normal form (geom.normal_form), the
exact real assignment is computed (model.py), and evalcnf streams the CNF and lists the violated clauses.
Requirements checked:
  p0 a hull vertex : the violated clauses are exactly the KGON clauses of the canonical 7-sets in convex position;
  p0 not a hull vertex (negative control): in addition only HULL clauses are violated, and their number equals the
                     number of triangles of other points that contain p0 (one of the two signs each); the number
                     is compared, not the identity of the HULL clauses (clause identity on three full-base
                     controls: referee/scripts/refbase.py).
Family index ranges are the consecutive blocks verified by spec.py on this CNF.

usage: run_base.py BASE.cnf BASE.json OUTDIR [--quick]
"""
import json
import os
import random
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import geom   # noqa: E402
import model  # noqa: E402

FAMS = [("GP", 12588160), ("A4", 413440), ("CONV4", 138992), ("CONV5", 139128), ("CONV6", 672792),
        ("KGON", 2689808), ("SB", 136), ("HULL", 10880)]


def ranges():
    r, lo = {}, 1
    for name, n in FAMS:
        r[name] = (lo, lo + n - 1)
        lo += n
    assert lo - 1 == 16653336
    return r


def family_of(idx, R):
    for name, (lo, hi) in R.items():
        if lo <= idx <= hi:
            return name
    raise ValueError(idx)


def triangles_containing(P, p0):
    others = [q for q in P if q != p0]
    n = 0
    import itertools
    for a, b, d in itertools.combinations(others, 3):
        if geom.inside_triangle(p0, a, b, d):
            n += 1
    return n


def configurations(rng, quick=False):
    """(name, points, centre)"""
    cfg = []
    R = os.path.join(HERE, "..", "..")   # cloud/es7-2026-10-19/results
    sym32 = geom.read_points(os.path.join(R, "SYM2", "sym7_32points.txt"))
    assert len(sym32) == 32 and geom.general_position(sym32)
    # near-extremal: the 7-gon-free 32-point set plus one antipodal pair; keep the ones with fewest convex 7-gons
    cand = []
    tries = 0
    while len(cand) < (3 if quick else 12) and tries < 4000:
        tries += 1
        q = (rng.randint(-1300000, 1300000), rng.randint(-1300000, 1300000))
        P = sym32 + [q, (-q[0], -q[1])]
        if (0, 0) in P or not geom.general_position(P):
            continue
        cand.append(P)
    cfg += [("sym32+pair#%d" % i, P, (0, 0)) for i, P in enumerate(cand)]
    # near-extremal: an added pair next to a point of the 32-point set (found with count7, work_nearpairs.json)
    near = os.path.join(HERE, "work_nearpairs.json")
    if os.path.exists(near) and not quick:
        quota = {2: 5, 12: 1, 30: 1, 120: 1, 360: 1}
        for cnt, q in json.load(open(near)):
            q = tuple(q)
            if quota.get(cnt, 0) == 0:
                continue
            quota[cnt] -= 1
            P = sym32 + [q, (-q[0], -q[1])]
            cfg.append((f"near{cnt}#{len(cfg)}", P, (0, 0)))
    shapes = ["box", "radial", "nearline", "ring"] if not quick else ["box"]
    for i, sh in enumerate(shapes):
        c = (0, 0) if i % 2 == 0 else (rng.randint(-50, 50), rng.randint(-50, 50))
        cfg.append((f"random-{sh}", geom.random_central(17, rng, box=10 ** 6, centre=c, shape=sh), c))
    return cfg


def main():
    base, mp, out = sys.argv[1], sys.argv[2], sys.argv[3]
    quick = "--quick" in sys.argv
    os.makedirs(out, exist_ok=True)
    rng = random.Random(20261101)
    t0 = time.time()
    M = model.Model(mp)
    R = ranges()
    print(f"model ready ({time.time() - t0:.0f} s); family ranges {R}", flush=True)
    jobs = []
    for name, P, c in configurations(rng, quick):
        assert len(P) == 34 and geom.general_position(P) and c not in P
        H = geom.hull_vertices(P)
        interior = [p for p in P if p not in H]
        firsts = [(p, True) for p in H] if (not quick or name.startswith("random") or name.endswith("#0")) else \
                 [(H[0], True), (H[len(H) // 2 + 1], True)]
        firsts += [(rng.choice(interior), False)]
        for p0, onhull in firsts:
            jobs.append((name, P, c, p0, onhull, len(H)))
    print(f"{len(jobs)} labellings", flush=True)
    results = []
    batch = 16
    allok = True
    for b0 in range(0, len(jobs), batch):
        chunk = jobs[b0:b0 + batch]
        files, meta = [], []
        for k, (name, P, c, p0, onhull, nh) in enumerate(chunk):
            X = geom.normal_form(P, c, p0)
            t1 = time.time()
            val, rep = M.assignment(X)
            bad = M.spot_check_convexity(X, rng, 800)
            fn = os.path.join(out, f"a{b0 + k}.bin")
            with open(fn, "wb") as f:
                f.write(bytes(val))
            files.append(fn)
            ntri = triangles_containing(P, p0) if not onhull else 0
            meta.append(dict(name=name, p0=p0, onhull=onhull, hull_size=nh, centre=c,
                             zero_ok=rep["zero_pattern_matches_map"], ident_ok=rep["identities_hold"],
                             conv_spot_mismatch=bad, convex7=len(rep["convex_K_ranks"]),
                             ranks=rep["convex_K_ranks"], tri_containing_p0=ntri, secs=round(time.time() - t1, 1)))
            print(f"  [{b0 + k}] {name} p0={p0} hull={onhull} |H|={nh}: zero_ok={rep['zero_pattern_matches_map']} "
                  f"ident_ok={rep['identities_hold']} spot_bad={bad} convex7(canonical)={len(rep['convex_K_ranks'])} "
                  f"({time.time() - t1:.0f} s)", flush=True)
        pref = os.path.join(out, f"batch{b0}")
        r = subprocess.run([os.path.join(HERE, "evalcnf"), base, pref] + files, capture_output=True, text=True)
        print(r.stdout.strip(), flush=True)
        if r.returncode != 0:
            print("evalcnf error", r.stderr)
            allok = False
        for k, m in enumerate(meta):
            viol = []
            with open(f"{pref}.{k}.viol") as f:
                for line in f:
                    viol.append(int(line.split()[0]))
            byfam = {}
            for idx in viol:
                byfam.setdefault(family_of(idx, R), []).append(idx)
            kexp = {R["KGON"][0] + rk for rk in m["ranks"]}
            kgot = set(byfam.get("KGON", []))
            other = {f: len(v) for f, v in byfam.items() if f not in ("KGON", "HULL")}
            nh = len(byfam.get("HULL", []))
            ok = m["zero_ok"] and m["ident_ok"] and m["conv_spot_mismatch"] == 0 and kgot == kexp and not other
            ok &= (nh == 0) if m["onhull"] else (nh == m["tri_containing_p0"] and nh > 0)
            allok &= ok
            m.update(violated_total=len(viol), kgon_violated=len(kgot), kgon_expected=len(kexp),
                     kgon_exact=(kgot == kexp), hull_violated=nh, other_violated=other, ok=ok)
            m.pop("ranks")
            print(f"  [{b0 + k}] {m['name']} hull={m['onhull']}: violated {len(viol)} = KGON {len(kgot)} "
                  f"(expected {len(kexp)}, exact={kgot == kexp}) + HULL {nh} (expected "
                  f"{0 if m['onhull'] else m['tri_containing_p0']}) + other {other} -> {'OK' if ok else 'FAIL'}",
                  flush=True)
            results.append(m)
            os.remove(f"{pref}.{k}.viol")
        for fn in files:
            os.remove(fn)
    with open(os.path.join(out, "results.json"), "w") as f:
        json.dump(results, f, indent=1, default=str)
    print(f"{len(results)} labellings, {sum(1 for m in results if m['onhull'])} from hull vertices, "
          f"{sum(1 for m in results if not m['onhull'])} non-hull controls; "
          f"min convex 7-gons (canonical) among hull labellings: "
          f"{min(m['convex7'] for m in results if m['onhull'])}")
    print("BASE EVALUATION", "PASSED" if allok else "FAILED", f"({time.time() - t0:.0f} s)")


if __name__ == "__main__":
    main()
