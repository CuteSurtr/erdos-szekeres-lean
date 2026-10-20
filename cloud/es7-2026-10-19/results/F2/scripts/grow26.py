#!/usr/bin/env python3
"""SAT-lookahead geometric growth of realizable (7,5,7)@26 sets (no 5-cap, no 7-cup, no convex 7-gon;
cup = ccw x-sorted triple).  The realized core occupies positions i_1 < .. < i_k of 1..26 (x increasing with
position).  A random unused position q and a random integer point p with x between the core
neighbours of q are drawn; p is accepted only if the orientation pattern of core + p (every triple
fixed as an assumption at those positions) still extends to a model of the ETV CNF on 26 points
(prefix_server).  At k = 26 the assumptions fix every variable, so SAT means the
realized set itself satisfies the CNF; it is then re-checked by brute force and exact arithmetic.
Candidates are sampled from a random multi-scale distribution; nothing is annealed, and no known
construction is used.  After A consecutive failures a random core point is removed (backtracking).
usage: grow26.py OUTDIR SEED HOURS --cnf CNF --server prefix_server [--A 40]"""
import argparse, itertools, json, math, os, random, subprocess, sys, time
N = 26
def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("seed", type=int); ap.add_argument("hours", type=float)
    ap.add_argument("--cnf", required=True); ap.add_argument("--server", required=True)
    ap.add_argument("--A", type=int, default=40); ap.add_argument("--climit", type=int, default=2000)
    ap.add_argument("--U0", type=int, default=1 << 20); ap.add_argument("--maxq", type=int, default=3000)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rnd = random.Random(a.seed)
    srv = subprocess.Popen([a.server, a.cnf, str(N), str(a.seed), str(a.climit)], stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE, text=True, bufsize=1)
    def query(pts):
        k = len(pts)
        bits = "".join("1" if orient(pts[i], pts[j], pts[l]) > 0 else "0" for i, j, l in itertools.combinations(range(k), 3))
        srv.stdin.write(f"{k} {bits}\n"); srv.stdin.flush()
        return srv.stdout.readline().strip(), bits
    end = time.time() + a.hours * 3600
    log = open(os.path.join(a.out, f"grow_{a.seed}.jsonl"), "a")
    chain = 0
    while time.time() < end:
        chain += 1; t0 = time.time()
        core = {rnd.randint(1, N): (0, 0)}   # position in 1..N -> integer point; x increases with position
        queries = 0; backtracks = 0; fails = 0; maxk = 1
        while 0 < len(core) < N and time.time() < end and queries < a.maxq:
            idxs = sorted(core); P = [core[i] for i in idxs]
            xs = [p[0] for p in P]; ys = [p[1] for p in P]
            D = max(max(xs) - min(xs), max(ys) - min(ys), a.U0)
            q = rnd.choice([i for i in range(1, N + 1) if i not in core])
            L = max([i for i in idxs if i < q], default=None); R = min([i for i in idxs if i > q], default=None)
            if L is not None and R is not None:
                lo = core[L][0] + (q - L); hi = core[R][0] - (R - q)
                if hi < lo:   # no integer room: exact scaling (orientations unchanged)
                    core = {i: (1024 * x, 1024 * y) for i, (x, y) in core.items()}; continue
                u = rnd.random(); u = u ** 3 if rnd.random() < 0.3 else (1 - (1 - u) ** 3 if rnd.random() < 0.5 else u)
                x = lo + int(u * (hi - lo))
                t = (x - core[L][0]) / (core[R][0] - core[L][0])
                yb = core[L][1] + t * (core[R][1] - core[L][1])
            elif L is not None:
                x = core[L][0] + (q - L) + int(D * math.exp(rnd.uniform(-5, 0.7))); yb = core[L][1]
            else:
                x = core[R][0] - (R - q) - int(D * math.exp(rnd.uniform(-5, 0.7))); yb = core[R][1]
            y = int(yb + D * math.exp(rnd.uniform(-7, 0.7)) * rnd.gauss(0, 1))
            p = (x, y)
            if any(orient(P[i], P[j], p) == 0 for i, j in itertools.combinations(range(len(P)), 2)):
                continue
            new = dict(core); new[q] = p
            ids = sorted(new); pts = [new[i] for i in ids]
            bits = "".join("1" if orient(pts[i], pts[j], pts[l]) > 0 else "0" for i, j, l in itertools.combinations(range(len(pts)), 3))
            srv.stdin.write(f"{len(ids)} {' '.join(map(str, ids))} {bits}\n"); srv.stdin.flush()
            queries += 1
            if srv.stdout.readline().strip() == "SAT":
                core = new; fails = 0; maxk = max(maxk, len(core))
            else:
                fails += 1
                if fails >= a.A and len(core) > 1:   # backtrack: drop a random realized point
                    del core[rnd.choice(sorted(core))]; fails = 0; backtracks += 1
        rec = {"chain": chain, "reached": len(core), "max_reached": maxk, "queries": queries, "backtracks": backtracks,
               "secs": round(time.time() - t0, 1)}
        if len(core) == N:
            pts = [core[i] for i in sorted(core)]
            rec["max_abs_coord"] = max(max(abs(x), abs(y)) for x, y in pts)
            name = f"g{a.seed}_{chain}"
            rec["name"] = name
            with open(os.path.join(a.out, name + ".pts"), "w") as f:
                for x, y in pts: f.write(f"{x} {y}\n")
            print("GROWN", json.dumps(rec), flush=True)
        log.write(json.dumps(rec) + "\n"); log.flush()

if __name__ == "__main__":
    main()
