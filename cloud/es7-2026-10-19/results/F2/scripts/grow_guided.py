#!/usr/bin/env python3
"""Model-guided growth of realizable (7,5,7)@26 sets (no 5-cap, no 7-cup, no convex 7-gon; cup = ccw
x-sorted triple, gen_etv.py convention).

The realized core is a set of exact integer points at positions i_1 < .. < i_k of 1..26 (x increasing
with position).  Loop:
  1. prefix_server returns a model of the ETV CNF on 26 points in which the core's triples are fixed
     (assumptions) and the other decision phases are random, or UNSAT;
  2. with that model, every unused position q has a cell: the intersection of the half-planes given by
     its required orientations with all core pairs and by the x-order (an exact 2-D LP, the realizer's
     _cell_point).  The most constrained non-empty cell (fail-first) gets a point at its Chebyshev
     centre, rounded to integers after an exact scaling of the core, and checked exactly; repeat while
     some cell is non-empty.  The model stays a witness, so the core stays extendable;
  3. if every remaining cell is empty, ask for another model (new random phases); after S such
     failures drop a random core point.
  3b. exhaustive face step (core >= fthr, stuck): every face of the core's line arrangement inside each
     free x-slot is SAT-tested as the next point (faces_step); only if none extends is a point dropped;
     with >= dthr core points this becomes a bounded depth-first search (B SAT faces per level,
     dbudget face scans in total);
  4. hybrid: when stuck with >= rthr core points, the current model (which agrees with the core) is
     also handed to the validated realizer (budget rbudget CPU-s); its points need not keep the core,
     and their x-order need not match the model's (the caller re-checks caps in the actual direction).
At 26 points the exact chirotope of the core is checked against the CNF by brute force (caller).
No annealing and no known construction is used; the start is one point.
usage: grow_guided.py OUTDIR SEED HOURS --cnf CNF --server prefix_server"""
import argparse, itertools, json, math, os, random, subprocess, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools", "realizer"))
from realize import _cell_point, realize  # noqa
from chiro import verify_exact  # noqa
N = 26
TR = list(itertools.combinations(range(1, N + 1), 3))
TI = {t: v for v, t in enumerate(TR)}

def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

def msign(model, a, b, c):
    """orientation of (a, b, c) (positions, any order) in the model"""
    t = (a, b, c); inv = (a > b) + (a > c) + (b > c)
    s = 1 if model[TI[tuple(sorted(t))]] == '1' else -1
    return -s if inv & 1 else s

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("seed", type=int); ap.add_argument("hours", type=float)
    ap.add_argument("--cnf", required=True); ap.add_argument("--server", required=True)
    ap.add_argument("--S", type=int, default=6); ap.add_argument("--climit", type=int, default=5000)
    ap.add_argument("--maxq", type=int, default=400)
    ap.add_argument("--fthr", type=int, default=18); ap.add_argument("--dthr", type=int, default=22)
    ap.add_argument("--B", type=int, default=4); ap.add_argument("--dbudget", type=int, default=60); ap.add_argument("--rthr", type=int, default=21); ap.add_argument("--rbudget", type=float, default=3.0)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rnd = random.Random(a.seed)
    srv = subprocess.Popen([a.server, a.cnf, str(N), str(a.seed), str(a.climit)], stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE, text=True, bufsize=1)
    def query(core):
        ids = sorted(core); pts = [core[i] for i in ids]
        bits = "".join("1" if orient(pts[i], pts[j], pts[l]) > 0 else "0" for i, j, l in itertools.combinations(range(len(pts)), 3))
        srv.stdin.write(f"M {len(ids)} {' '.join(map(str, ids))} {bits or '-'}\n"); srv.stdin.flush()
        r = srv.stdout.readline().strip()
        return r, (srv.stdout.readline().strip() if r == "SAT" else None)
    def place(core, model):
        """fail-first insertion of one point under model; returns (q, p) or None"""
        ids = sorted(core); P = [core[i] for i in ids]
        cx = sum(p[0] for p in P) / len(P); cy = sum(p[1] for p in P) / len(P)
        sc = max(1.0, max(max(abs(p[0] - cx), abs(p[1] - cy)) for p in P))
        X = np.array([(p[0] - cx) / sc for p in P]); Y = np.array([(p[1] - cy) / sc for p in P])
        ii, jj = np.triu_indices(len(P), 1)
        best = None
        for q in range(1, N + 1):
            if q in core: continue
            s = [msign(model, ids[i], ids[j], q) for i, j in zip(ii, jj)]
            ax, ay, bx, by = list(X[ii]), list(Y[ii]), list(X[jj]), list(Y[jj])
            L = max([k for k, i in enumerate(ids) if i < q], default=None)
            R = min([k for k, i in enumerate(ids) if i > q], default=None)
            if L is not None: ax.append(X[L]); ay.append(0.0); bx.append(X[L]); by.append(1.0); s.append(-1)
            if R is not None: ax.append(X[R]); ay.append(0.0); bx.append(X[R]); by.append(1.0); s.append(1)
            if len(s) == 0: r = (rnd.uniform(-1, 1), rnd.uniform(-1, 1), 1.0)
            else: r = _cell_point(None, None, tuple(np.array(v, float) for v in (ax, ay, bx, by, s)), 3.0)
            if r is None or r[2] <= 1e-9: continue
            if best is None or r[2] < best[0]: best = (r[2], q, r[0], r[1])
        if best is None: return None
        t, q, u, v = best
        for extra in (0, 8, 16, 32):
            k = max(0, math.ceil(math.log2(8 / (t * sc)))) + extra if t * sc < 8 else extra
            f = 1 << k
            core2 = {i: (f * x, f * y) for i, (x, y) in core.items()}
            p = (round(f * (cx + sc * u)), round(f * (cy + sc * v)))
            ok = True
            for i, j in itertools.combinations(ids, 2):
                o = orient(core2[i], core2[j], p)
                if o == 0 or (o > 0) != (msign(model, i, j, q) > 0): ok = False; break
            L = max([i for i in ids if i < q], default=None); R = min([i for i in ids if i > q], default=None)
            if ok and L is not None and not p[0] > core2[L][0]: ok = False
            if ok and R is not None and not p[0] < core2[R][0]: ok = False
            if ok:
                # remove a common power of two (keeps coordinates small; orientations unchanged)
                core2[q] = p
                g = 0
                while all(x % 2 == 0 and y % 2 == 0 for x, y in core2.values()) and g < 64:
                    core2 = {i: (x // 2, y // 2) for i, (x, y) in core2.items()}; g += 1
                return core2
        return None
    def faces_step(core, want=1):
        """exhaustive one-point step: for unused positions q (random order) enumerate candidate points
        in every face of the arrangement of lines through core pairs (vertex + small offsets, float),
        restricted to q's x-slot, dedupe by float sign vector, and SAT-test each (exact bits); returns
        a list of up to `want` new cores (one per SAT candidate, at most 2 per position q)"""
        found = []
        nonlocal queries
        ids = sorted(core); P = np.array([core[i] for i in ids], dtype=float)
        cx, cy = P[:, 0].mean(), P[:, 1].mean(); sc = max(1.0, np.abs(P - [cx, cy]).max())
        Q = (P - [cx, cy]) / sc
        ii, jj = np.triu_indices(len(ids), 1)
        A = Q[ii]; B = Q[jj]; Dv = B - A; Dn = Dv / np.linalg.norm(Dv, axis=1)[:, None]
        nL = len(ii)
        # line l: n_l . z = c_l with normal n = (-dy, dx)
        Nn = np.stack([-Dn[:, 1], Dn[:, 0]], 1); C0 = (Nn * A).sum(1)
        l1, l2 = np.triu_indices(nL, 1)
        det = Nn[l1, 0] * Nn[l2, 1] - Nn[l1, 1] * Nn[l2, 0]
        ok = np.abs(det) > 1e-12
        l1, l2, det = l1[ok], l2[ok], det[ok]
        vx = (C0[l1] * Nn[l2, 1] - C0[l2] * Nn[l1, 1]) / det
        vy = (Nn[l1, 0] * C0[l2] - Nn[l2, 0] * C0[l1]) / det
        V = np.stack([vx, vy], 1)
        # also the core points themselves are vertices (many lines): use offsets along bisectors later
        dist = np.abs(V @ Nn.T - C0[None, :])            # (nv, nL)
        dist[np.arange(len(V)), l1] = np.inf; dist[np.arange(len(V)), l2] = np.inf
        eps = 0.25 * dist.min(1)
        good = eps > 1e-11
        cands = []
        for s1 in (-1, 1):
            for s2 in (-1, 1):
                d = s1 * Dn[l1] + s2 * Dn[l2]
                d = d / np.linalg.norm(d, axis=1)[:, None]
                cands.append((V + eps[:, None] * d)[good])
        Z = np.concatenate(cands)
        # points near core vertices: tiny offsets in random directions
        ang = np.random.default_rng(rnd.randint(0, 10**9)).uniform(0, 2 * np.pi, size=(len(Q), 64))
        r0 = 1e-7
        Z = np.concatenate([Z, (Q[:, None, :] + r0 * np.stack([np.cos(ang), np.sin(ang)], 2)).reshape(-1, 2)])
        sg = (Z @ Nn.T - C0[None, :]) > 0
        free = [q for q in range(1, N + 1) if q not in core]; rnd.shuffle(free)
        xs = Q[:, 0]
        for q in free:
            L = max([k for k, i in enumerate(ids) if i < q], default=None)
            R = min([k for k, i in enumerate(ids) if i > q], default=None)
            m = np.ones(len(Z), bool)
            if L is not None: m &= Z[:, 0] > xs[L] + 1e-12
            if R is not None: m &= Z[:, 0] < xs[R] - 1e-12
            if not m.any(): continue
            _, first = np.unique(np.packbits(sg[m], axis=1), axis=0, return_index=True)
            idx = list(np.nonzero(m)[0][first]); rnd.shuffle(idx)
            per_q = 0
            for t in idx:
                if per_q >= 2 or len(found) >= want: break
                z = Z[t]
                # exact integer point: scale the core so that the rounding error is far below the margin
                marg = max(1e-15, float(np.min(np.abs(Z[t] @ Nn.T - C0))))
                k = max(0, math.ceil(math.log2(16 / (marg * sc)))) if marg * sc < 16 else 0
                f = 1 << k
                core2 = {i: (f * x, f * y) for i, (x, y) in core.items()}
                p = (round(f * (cx + sc * z[0])), round(f * (cy + sc * z[1])))
                new = dict(core2); new[q] = p
                nid = sorted(new); pts = [new[i] for i in nid]
                if [pt[0] for pt in pts] != sorted(set(pt[0] for pt in pts)): continue
                bits = []
                bad = False
                for i1, j1, l1_ in itertools.combinations(range(len(pts)), 3):
                    o = orient(pts[i1], pts[j1], pts[l1_])
                    if o == 0: bad = True; break
                    bits.append("1" if o > 0 else "0")
                if bad: continue
                srv.stdin.write(f"{len(nid)} {' '.join(map(str, nid))} {''.join(bits)}\n"); srv.stdin.flush()
                queries += 1
                if srv.stdout.readline().strip() == "SAT":
                    g = 0
                    while all(x % 2 == 0 and y % 2 == 0 for x, y in new.values()) and g < 200:
                        new = {i: (x // 2, y // 2) for i, (x, y) in new.items()}; g += 1
                    found.append(new); per_q += 1
            if len(found) >= want: break
        return found
    def dfs(core, budget):
        """bounded depth-first search over SAT faces; returns a 26-point core or None"""
        if len(core) == N: return core
        if budget[0] <= 0 or time.time() > end: return None
        budget[0] -= 1
        for c2 in faces_step(core, want=a.B):
            r = dfs(c2, budget)
            if r is not None: return r
        return None
    end = time.time() + a.hours * 3600
    log = open(os.path.join(a.out, f"guided_{a.seed}.jsonl"), "a")
    chain = 0
    while time.time() < end:
        chain += 1; t0 = time.time()
        core = {rnd.randint(1, N): (0, 0)}
        queries = drops = stuck = rcalls = fcalls = fhits = 0; maxk = 1; via = "growth"
        while len(core) < N and time.time() < end and queries < a.maxq:
            queries += 1
            r, model = query(core)
            if r != "SAT":
                del core[rnd.choice(sorted(core))]; drops += 1
                if not core: core = {rnd.randint(1, N): (0, 0)}
                continue
            progressed = False
            while len(core) < N:
                c2 = place(core, model)
                if c2 is None: break
                core = c2; progressed = True
            maxk = max(maxk, len(core))
            if len(core) == N: break
            if len(core) >= a.rthr and a.rbudget > 0:
                # hybrid: hand the whole model (consistent with the core) to the realizer
                chi = {(i - 1, j - 1, k - 1): (1 if model[v] == '1' else -1) for v, (i, j, k) in enumerate(TR)}
                res = realize(chi, N, budget=a.rbudget, seed=rnd.randint(0, 10**6))
                rcalls += 1
                if res["realized"] and verify_exact([tuple(p) for p in res["points"]], chi)[0]:
                    core = {i + 1: tuple(p) for i, p in enumerate(res["points"])}; via = "realizer"; break
            stuck = 0 if progressed else stuck + 1
            if stuck >= a.S and len(core) >= a.fthr:
                fcalls += 1
                if len(core) >= a.dthr:
                    r = dfs(core, [a.dbudget])
                    if r is not None:
                        core = r; maxk = N; via = "dfs"; break
                else:
                    c2 = faces_step(core)
                    if c2:
                        core = c2[0]; stuck = 0; fhits += 1; maxk = max(maxk, len(core)); continue
            if stuck >= a.S:
                for _ in range(rnd.randint(1, 3)):
                    if len(core) > 1: del core[rnd.choice(sorted(core))]
                drops += 1; stuck = 0
        rec = {"chain": chain, "reached": len(core), "max_reached": maxk, "queries": queries, "drops": drops, "realizer_calls": rcalls, "face_calls": fcalls, "face_hits": fhits, "via": via,
               "secs": round(time.time() - t0, 1)}
        if len(core) == N:
            pts = [core[i] for i in sorted(core)]
            rec["max_abs_coord"] = max(max(abs(x), abs(y)) for x, y in pts)
            rec["name"] = name = f"gg{a.seed}_{chain}"
            with open(os.path.join(a.out, name + ".pts"), "w") as f:
                for x, y in pts: f.write(f"{x} {y}\n")
            print("GROWN", json.dumps(rec), flush=True)
        log.write(json.dumps(rec) + "\n"); log.flush()

if __name__ == "__main__":
    main()
