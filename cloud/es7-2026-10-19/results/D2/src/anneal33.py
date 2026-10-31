#!/usr/bin/env python3
"""Diversified annealing at 33 points: minimise the exact number of convex 7-gons.

Each run: build an initial 33-point integer set of a random family, then run
`cgon anneal 7 33 ITERS T0 T1 SEED init out` (exact counts, log(1+E) energy,
Metropolis, cgon's multi-scale moves; it stops early if E reaches 0) and
record the best energy and the best set.  Families (all far from the
classical Erdos-Szekeres construction):
  layers   - 2..5 nested convex layers (ellipses, random angles, radial noise)
  lattice  - random points of a small square grid in general position, scaled
  nearpert - a near-miss set (nearfull seeds, AlphaEvolve) with a random affine
             map and random perturbation of relative size 1e-4..1e-1
  uniform  - uniform random points in a square (control)
  clusters - 3..8 clusters of random sizes at random positions and scales

usage: anneal33.py OUTDIR WORKER_ID SECONDS SEED SEEDFILES...
Output: OUTDIR/anneal_wID.jsonl, one line per run.
"""
import os, sys, json, time, random, math, resource, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dlib
from dlib import b

R = 1 << 24


def gp_ok(P, q):
    for i in range(len(P)):
        if P[i] == q:
            return False
        for j in range(i + 1, len(P)):
            if dlib.orient(P[i], P[j], q) == 0:
                return False
    return True


def add_points(gen, n=33, tries=100000):
    P = []
    t = 0
    while len(P) < n and t < tries:
        t += 1
        q = gen()
        q = (int(q[0]), int(q[1]))
        if max(abs(q[0]), abs(q[1])) >= (1 << 29):
            continue
        if gp_ok(P, q):
            P.append(q)
    return P if len(P) == n else None


def init_layers(rng):
    L = rng.randint(2, 5)
    sizes = [3] * L
    for _ in range(33 - 3 * L):
        sizes[rng.randrange(L)] += 1
    rng.shuffle(sizes)
    pts = []
    radii = sorted([rng.uniform(0.05, 1.0) for _ in range(L)], reverse=True)
    for li, (sz, r) in enumerate(zip(sizes, radii)):
        ax = r * rng.uniform(0.6, 1.0); ay = r * rng.uniform(0.6, 1.0); rot = rng.uniform(0, 2 * math.pi)
        cx = rng.gauss(0, 0.05 * r); cy = rng.gauss(0, 0.05 * r)
        angs = sorted(rng.uniform(0, 2 * math.pi) for _ in range(sz))
        for a in angs:
            rr = 1 + rng.gauss(0, 0.02)
            x = ax * rr * math.cos(a); y = ay * rr * math.sin(a)
            pts.append((cx + x * math.cos(rot) - y * math.sin(rot), cy + x * math.sin(rot) + y * math.cos(rot)))
    it = iter(pts)
    def gen():
        try:
            x, y = next(it)
        except StopIteration:
            x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
        return (x * R + rng.uniform(-1, 1), y * R + rng.uniform(-1, 1))
    return add_points(gen), {"layers": L, "sizes": sizes}


def init_lattice(rng):
    n = rng.randint(24, 64)  # 33 points in general position need n >= 17
    sc = R // n
    return add_points(lambda: ((rng.randrange(n) - n // 2) * sc, (rng.randrange(n) - n // 2) * sc), tries=400000), {"grid": n}


def init_uniform(rng):
    return add_points(lambda: (rng.randrange(-R, R), rng.randrange(-R, R))), {}


def init_clusters(rng):
    c = rng.randint(3, 8)
    cen = [(rng.uniform(-1, 1), rng.uniform(-1, 1), 10 ** rng.uniform(-3, -0.5)) for _ in range(c)]
    def gen():
        x, y, s = rng.choice(cen)
        return ((x + rng.gauss(0, s)) * R, (y + rng.gauss(0, s)) * R)
    return add_points(gen), {"clusters": c}


def init_nearpert(rng, seeds):
    lab, S = rng.choice(seeds)
    xs = [x for x, _ in S]; ys = [y for _, y in S]
    cx = (max(xs) + min(xs)) / 2; cy = (max(ys) + min(ys)) / 2
    ext = max(max(xs) - min(xs), max(ys) - min(ys))
    sig = 10 ** rng.uniform(-4, -1)
    a, bb, c, d = 1 + rng.gauss(0, 0.3), rng.gauss(0, 0.3), rng.gauss(0, 0.3), 1 + rng.gauss(0, 0.3)
    if abs(a * d - bb * c) < 0.2:
        a, bb, c, d = 1, 0, 0, 1
    pts = []
    for x, y in S:
        u = (x - cx) / ext; v = (y - cy) / ext
        u, v = a * u + bb * v, c * u + d * v
        u += rng.gauss(0, sig); v += rng.gauss(0, sig)
        pts.append((u, v))
    m = max(max(abs(u), abs(v)) for u, v in pts)
    it = iter(pts)
    def gen():
        try:
            u, v = next(it)
        except StopIteration:
            u, v = rng.uniform(-m, m), rng.uniform(-m, m)
        return (u / m * (1 << 25) + rng.uniform(-1, 1), v / m * (1 << 25) + rng.uniform(-1, 1))
    return add_points(gen), {"seed": lab, "sigma": round(sig, 6)}


def main():
    outdir, wid, seconds, seed = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
    seeds = []
    for p in sys.argv[5:]:
        if p.startswith("int:"):
            seeds.append((os.path.basename(p[4:]), dlib.read_pts(p[4:])))
        else:
            for line in open(p):
                f = line.split()
                if f:
                    seeds.append((os.path.basename(p) + ":" + f[0], dlib.parse_line_pts(f, 2)))
    rng = random.Random(seed)
    deadline = time.time() + seconds
    tmp = os.path.join(outdir, f"tmp_a{wid}")
    os.makedirs(tmp, exist_ok=True)
    log = open(os.path.join(outdir, f"anneal_w{wid}.jsonl"), "a")
    run = 0
    fams = ["layers", "lattice", "nearpert", "uniform", "clusters"]
    weights = [3, 3, 3, 1, 2]
    while time.time() < deadline:
        fam = rng.choices(fams, weights)[0]
        if fam == "layers":
            P, info = init_layers(rng)
        elif fam == "lattice":
            P, info = init_lattice(rng)
        elif fam == "uniform":
            P, info = init_uniform(rng)
        elif fam == "clusters":
            P, info = init_clusters(rng)
        else:
            P, info = init_nearpert(rng, seeds)
        if P is None:
            continue
        c0 = dlib.cgon_count(P, 7)
        if c0 is None:
            continue
        iters = rng.choice([100000, 200000, 400000])
        T0 = rng.choice([0.3, 1.0, 3.0]); T1 = T0 / rng.choice([30, 100, 300])
        rs = rng.randrange(1 << 40)
        ip = os.path.join(tmp, "init.txt"); op = os.path.join(tmp, "out.txt")
        dlib.write_pts(ip, P)
        r = subprocess.run([b("cgon"), "anneal", "7", "33", str(iters), str(T0), str(T1), str(rs), ip, op],
                           capture_output=True, text=True)
        line = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
        best = None; cpu = None
        for tok in line.split():
            if tok.startswith("best="):
                best = int(tok[5:])
            if tok.startswith("cpu="):
                cpu = float(tok[4:].rstrip("s"))
        if best is None:
            log.write(json.dumps({"w": wid, "run": run, "family": fam, "error": r.stderr[-300:]}) + "\n")
            log.flush()
            continue
        Q = dlib.read_pts(op)
        cq = dlib.cgon_count(Q, 8)
        rec = {"w": wid, "run": run, "family": fam, "info": info, "E0": c0[7], "iters": iters, "T0": T0, "T1": T1,
               "seed": rs, "best": best, "recount7": cq[7], "c8": cq.get(8), "cpu": cpu, "pts": Q}
        log.write(json.dumps(rec) + "\n")
        log.flush()
        if cq[7] == 0:
            with open(os.path.join(outdir, f"FOUND_a{wid}.txt"), "a") as f:
                f.write(json.dumps(rec) + "\n")
            print(f"[a{wid}] !!! zero-heptagon candidate run {run}", flush=True)
        run += 1
    ru = resource.getrusage(resource.RUSAGE_CHILDREN)
    json.dump({"w": wid, "runs": run, "child_cpu": round(ru.ru_utime + ru.ru_stime, 1),
               "self_cpu": round(time.process_time(), 1)}, open(os.path.join(outdir, f"anneal_w{wid}_summary.json"), "w"))


if __name__ == "__main__":
    main()
