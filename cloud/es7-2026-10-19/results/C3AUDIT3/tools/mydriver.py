"""C3AUDIT3: own small-instance tree closer with sigma-cube splits (from results/C3U/TASK.md rules
1-4, using mycompose's tree and units only).  Deterministic: CaDiCaL conflict limit per depth.
usage: mydriver.py m k BASE OUT.jsonl ROOT --conf c0,c1,... [--sigma K] [--levels S] [--jobs J]"""
import argparse, concurrent.futures as cf, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mycompose as Y  # noqa: E402
from c3cnf import C3Enc  # noqa: E402

WORK = "/opt/work/mydrv"


def dual(cnf, prf):
    a = subprocess.run(["/opt/bin/lrat-check", cnf, prf], capture_output=True, text=True).stdout
    a = next((l for l in a.splitlines() if l.startswith("c VERIFIED") or l.startswith("c NOT VERIFIED")), "none")
    b = subprocess.run(["/opt/bin/cake_lpr", cnf, prf], capture_output=True, text=True).stdout.strip().splitlines()
    b = b[0] if b else "none"
    return a, b, a == "c VERIFIED" and b == "s VERIFIED UNSAT"


def solve(args):
    m, k, base, kk, conf = args
    E = C3Enc(m, k)
    us = Y.units(m, E, *kk)
    name = Y.kname(kk)
    cnf, prf = os.path.join(WORK, name + ".cnf"), os.path.join(WORK, name + ".lrat")
    with open(base) as f, open(cnf, "w") as g:
        h = f.readline().split()
        g.write(f"p cnf {h[2]} {int(h[3]) + len(us)}\n"); g.write(f.read())
        g.write("".join(f"{u} 0\n" for u in us))
    rec = {"node": name, "units": len(us), "cnf_sha256": Y.fsha(cnf), "base_sha256": Y.fsha(base), "conflicts": conf}
    r = subprocess.run(["/opt/bin/cadical", "-q", "-c", str(conf), "--lrat", "--binary=false", cnf, prf],
                       capture_output=True, text=True).stdout
    rec["status"] = next((l[2:] for l in r.splitlines() if l.startswith("s ")), "UNKNOWN")
    if rec["status"] == "UNSATISFIABLE":
        a, b, ok = dual(cnf, prf)
        rec.update({"lrat_check": a, "cake_lpr": b, "certified": ok})
    for x in (cnf, prf):
        if os.path.exists(x): os.remove(x)
    return rec


def main():
    ap = argparse.ArgumentParser()
    for x in ("m", "k"): ap.add_argument(x, type=int)
    ap.add_argument("base"); ap.add_argument("out"); ap.add_argument("root")
    ap.add_argument("--conf", default="1000"); ap.add_argument("--sigma", type=int, default=0)
    ap.add_argument("--levels", type=int, default=2); ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    os.makedirs(WORK, exist_ok=True)
    confs = [int(x) for x in a.conf.split(",")]
    m, k = a.m, a.k
    front = [(Y.key(*Y.parse(a.root)), 0)]
    stats = {"solved": 0, "sigma_splits": 0, "layer_splits": 0, "cube_layer_splits": 0, "dropped_conflicting": 0, "max_cube": 0}
    with open(a.out, "w") as fo, cf.ProcessPoolExecutor(a.jobs) as ex:
        while front:
            res = list(ex.map(solve, [(m, k, a.base, kk, confs[min(d, len(confs) - 1)]) for kk, d in front]))
            nxt = []
            for (kk, d), r in zip(front, res):
                fo.write(json.dumps(r) + "\n"); stats["solved"] += 1
                if r["status"] == "SATISFIABLE":
                    print("SAT", r["node"]); stats["sat"] = r["node"]; continue
                if r.get("certified"): continue
                assert r["status"] == "UNKNOWN", r
                layers, cube = kk
                fr = Y.free(m, layers, cube)
                K = a.sigma
                if K and len(layers) >= 2 and len(cube) < a.levels * K and len(fr) >= K:
                    ch = Y.sigma_kids(m, layers, cube, fr[:K])
                    fo.write(json.dumps({"node": r["node"], "split": True, "sigma_bits": fr[:K], "children": len(ch)}) + "\n")
                    stats["sigma_splits"] += 1; stats["max_cube"] = max(stats["max_cube"], len(cube) + K)
                else:
                    ch = Y.cube_layer_kids(m, k, layers, cube) if cube else [Y.key(c, ()) for c in Y.layer_children(m, k, layers)]
                    if cube:
                        stats["cube_layer_splits"] += 1
                        stats["dropped_conflicting"] += len(Y.layer_children(m, k, layers)) - len(ch)
                    else:
                        stats["layer_splits"] += 1
                    fo.write(json.dumps({"node": r["node"], "split": True, "children": len(ch)}) + "\n")
                nxt += [(c, d + 1) for c in ch]
            front = nxt
    print(json.dumps(stats))


if __name__ == "__main__":
    main()
