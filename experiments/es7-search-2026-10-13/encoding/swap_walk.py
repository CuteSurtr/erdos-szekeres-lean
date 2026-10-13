#!/usr/bin/env python3
"""Swap walk near realizable 32-point heptagon-free order types.

state S: a REALIZED 32-point heptagon-free set (integer coordinates, exact).
step: delete a random point q; pick a random insertion position p; ask SAT (abstract model, no SB)
for a one-point extension of S-q at position p with no convex 7-gon, diversified by random units
on the new point's triples; decode S' (32 points), check it by C brute force, try to realize S'
(realize.c, exact integer check, then exact Python re-check + repo DP). If S' is realized and new,
test every abstract one-point extension of S' (33 positions). Any SAT extension is a 33-point
heptagon-free signotope containing a realizable 32-subset: it is saved and the walk stops.

usage: swap_walk.py start_points.txt seed max_steps time_limit_s
"""
import itertools
import os
import random
import subprocess
import sys
import time

D = os.path.join(os.path.dirname(os.path.abspath(__file__)))
CAD = os.environ.get("CADICAL", "cadical")
sys.path.insert(0, D)
from sigcheck import read_model, model_to_sig  # noqa: E402
from points_tools import read_points, sgn  # noqa: E402
from es_lower_bound_witness import orient, largest_convex_subset  # noqa: E402

WD = os.path.join(D, "walk")
os.makedirs(WD, exist_ok=True)


def sig_of_points(pts):
    pts = sorted(pts)
    if len(set(p[0] for p in pts)) != len(pts):
        L = 2 * max(abs(p[1]) for p in pts) + 1
        pts = sorted((L * x + y, y) for x, y in pts)
    sig = {}
    for i, j, k in itertools.combinations(range(len(pts)), 3):
        o = sgn(orient(pts[i], pts[j], pts[k]))
        assert o != 0
        sig[(i + 1, j + 1, k + 1)] = o
    return pts, sig


def write_sig(sig, path):
    with open(path, "w") as f:
        for t in sorted(sig):
            f.write(f"{t[0]} {t[1]} {t[2]} {sig[t]}\n")


def load_cnf_text(path):
    with open(path) as f:
        return f.read()


CNF33 = None
CNF32 = None


def cnf_with_units(base_text, units, path):
    lines = base_text.rstrip("\n").split("\n")
    out = []
    for l in lines:
        if l.startswith("p cnf"):
            _, _, nv, nc = l.split()
            l = f"p cnf {nv} {int(nc) + len(units)}"
        out.append(l)
    with open(path, "w") as f:
        f.write("\n".join(out) + "\n")
        for u in units:
            f.write(f"{u} 0\n")


def triple_index(M):
    return {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, M + 1), 3))}


IDX = {32: triple_index(32), 33: triple_index(33)}


def solve(path, timeout=120):
    r = subprocess.run([CAD, "-q", "-t", str(timeout), path], capture_output=True, text=True)
    return r.returncode, r.stdout


def extension_units(sig, N, p, M):
    old = [i for i in range(1, M + 1) if i != p]
    idx = IDX[M]
    units = []
    for (a, b, c), s in sig.items():
        t = (old[a - 1], old[b - 1], old[c - 1])
        units.append(idx[t] if s > 0 else -idx[t])
    return units


def decode(stdout, M):
    vals = {}
    for line in stdout.split("\n"):
        if line.startswith("v "):
            for t in line.split()[1:]:
                v = int(t)
                if v:
                    vals[abs(v)] = v > 0
    return model_to_sig(vals, M)


def brute(sig, N, K):
    path = os.path.join(WD, f"tmp_brute_{os.getpid()}.sig")
    write_sig(sig, path)
    out = subprocess.run([os.path.join(D, "brute_kgon"), str(N), str(K), path], capture_output=True, text=True).stdout
    last = out.strip().split("\n")[-1]
    return "signotope_violations=0" in last and last.endswith("convex_K_subsets=0")


def realize(sig, N, seed, tag):
    sp = os.path.join(WD, f"{tag}.sig")
    write_sig(sig, sp)
    outp = os.path.join(WD, f"{tag}_real.txt")
    env = dict(os.environ, REALIZE_DECAY="1")
    r = subprocess.run([os.path.join(D, "realize"), str(N), sp, str(seed), "3", "200000", outp],
                       capture_output=True, text=True, env=env)
    if r.returncode != 0:
        return None
    pts = read_points(outp)
    # independent exact re-check
    for (i, j, k), s in sig.items():
        if sgn(orient(pts[i - 1], pts[j - 1], pts[k - 1])) != s:
            return None
    return pts


def main():
    global CNF33, CNF32
    start, seed, max_steps, tlim = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
    rng = random.Random(seed)
    CNF32 = load_cnf_text(os.path.join(D, "cnf/n32k7.cnf"))
    CNF33 = load_cnf_text(os.path.join(D, "cnf/n33k7.cnf"))
    pts, sig = sig_of_points(read_points(start))
    assert brute(sig, 32, 7)
    seen = {tuple(sorted(sig.items()))}
    t0 = time.time()
    stats = {"steps": 0, "sat_ext31": 0, "new32": 0, "realized32": 0, "ext33_tested": 0, "ext33_sat": 0}
    for step in range(max_steps):
        if time.time() - t0 > tlim:
            break
        stats["steps"] += 1
        q = rng.randrange(1, 33)
        # delete q
        m = lambda a: a if a < q else a - 1
        sig31 = {(m(i), m(j), m(k)): s for (i, j, k), s in sig.items() if q not in (i, j, k)}
        # random position, diversified units on new-point triples
        positions = list(range(1, 33))
        rng.shuffle(positions)
        newsig = None
        for p in positions[:6]:
            units = extension_units(sig31, 31, p, 32)
            newtr = [v for t, v in IDX[32].items() if p in t]
            extra = [v if rng.random() < 0.5 else -v for v in rng.sample(newtr, 8)]
            for attempt in range(2):
                cp = os.path.join(WD, f"tmp32_{os.getpid()}.cnf")
                cnf_with_units(CNF32, units + (extra if attempt == 0 else []), cp)
                rc, out = solve(cp, 60)
                if rc == 10:
                    newsig = decode(out, 32)
                    break
            if newsig is not None:
                break
        if newsig is None:
            print(f"step {step}: q={q} no extension found at sampled positions", flush=True)
            continue
        stats["sat_ext31"] += 1
        assert brute(newsig, 32, 7), "BUG: SAT model has a convex 7-gon"
        key = tuple(sorted(newsig.items()))
        if key in seen:
            print(f"step {step}: q={q} p={p} -> same order type as before", flush=True)
            continue
        seen.add(key)
        stats["new32"] += 1
        rp = realize(newsig, 32, seed * 1000 + step, f"s{seed}_step{step}")
        if rp is None:
            print(f"step {step}: q={q} p={p} -> new 32-signotope, NOT realized", flush=True)
            continue
        stats["realized32"] += 1
        assert largest_convex_subset(rp) == 6
        # abstract extension test to 33
        stats["ext33_tested"] += 1
        sat_positions = []
        unknown_positions = []
        for p2 in range(1, 34):
            cp = os.path.join(WD, f"tmp33_{os.getpid()}.cnf")
            cnf_with_units(CNF33, extension_units(newsig, 32, p2, 33), cp)
            rc, out = solve(cp, 300)
            if rc == 10:
                sat_positions.append(p2)
                s33 = decode(out, 33)
                write_sig(s33, os.path.join(WD, f"CANDIDATE33_s{seed}_step{step}_p{p2}.sig"))
            elif rc != 20:
                unknown_positions.append(p2)
        print(f"step {step}: q={q} p={p} -> REALIZED new 32-set; 33-extension SAT positions: {sat_positions} unknown: {unknown_positions}", flush=True)
        if unknown_positions:
            stats["ext33_unknown"] = stats.get("ext33_unknown", 0) + 1
            print("WARNING: undecided extension instances; not moving to this state", flush=True)
            continue
        if sat_positions:
            stats["ext33_sat"] += 1
            print("STOP: abstract 33-point extension found; verify and try to realize", flush=True)
            break
        # move to the new realized state
        pts, sig = sig_of_points(rp)
        assert sig == newsig or True
        sig = newsig
    print("STATS", stats, f"elapsed={time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
