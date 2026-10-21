#!/usr/bin/env python3
"""C3X: compare methods on one node at a fixed wall budget (4 cores).
usage: c3x.py BASE NODE METHOD BUDGET_S RECORDS.jsonl
METHOD: ref (close_tree.py, caps 300,300,600, --sat, --split-singles, killed at budget)
        march<D> (march_cu -d D on the node CNF, then each cube solved by CaDiCaL --sat)
        split (tree_children of the node = next layer's orbit choice, each child solved by CaDiCaL --sat)
        opt (4 CaDiCaL option sets not in C3-S/logs/cadical_options.jsonl, one per core, on the node CNF)
Every UNSAT subproblem is checked by lrat-check (E2 patch) and cake_lpr (C3-S controls.dual), after the budget window."""
import concurrent.futures as cf, json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, "..", "..", "C3-S", "tools")
sys.path.insert(0, os.path.join(T, "..", "..", "C3a")); sys.path.insert(0, T)
from c3cnf import C3Enc
from hullcase import layer_clauses, layers_name, parse_layers, tree_children
from controls import dual
E = C3Enc(11, 7); W = "/opt/work/c3x"; MARCH = "/opt/build/CnC/march_cu/march_cu"
OPTS = [["--sat", "--reducetarget=50"], ["--sat", "--reducetier1glue=3", "--reducetier2glue=8"],
        ["--sat", "--bumpreasondepth=2"], ["--unsat", "--vivifytier1eff=20"]]

def node_units(node):
    return [c[0] for c in layer_clauses(11, parse_layers(node), E.ccw, E.sig)]

def write_cnf(base, units, path):
    with open(base) as f, open(path, "w") as g:
        h = f.readline().split()
        g.write(f"p cnf {h[2]} {int(h[3]) + len(units)}\n")
        while True:
            b = f.read(1 << 24)
            if not b: break
            g.write(b)
        g.write("".join(f"{u} 0\n" for u in units))

def solve(job):
    tag, base, units, cap, opts = job
    cnf, prf = os.path.join(W, tag + ".cnf"), os.path.join(W, tag + ".lrat")
    write_cnf(base, units, cnf)
    t = time.time()
    r = subprocess.run(["cadical", "-q", "-t", str(max(1, int(cap)))] + opts + ["--lrat", "--binary=false", cnf, prf],
                       capture_output=True, text=True).stdout
    st = next((l[2:] for l in r.splitlines() if l.startswith("s ")), "UNKNOWN")
    rec = {"sub": tag, "status": st, "solve_s": round(time.time() - t, 1), "opts": opts}
    if st == "SATISFIABLE":
        open(os.path.join(W, "MODEL_" + tag + ".out"), "w").write(r)
    if st != "UNSATISFIABLE":
        for x in (cnf, prf):
            if os.path.exists(x): os.remove(x)
    return rec

def check(rec):
    cnf, prf = os.path.join(W, rec["sub"] + ".cnf"), os.path.join(W, rec["sub"] + ".lrat")
    t = time.time(); a, b, ok = dual(cnf, prf)
    rec.update(lrat_check=a, cake_lpr=b, certified=ok, check_s=round(time.time() - t, 1))
    for x in (cnf, prf): os.remove(x)

def main():
    base, node, meth, budget, out = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5]
    os.makedirs(W, exist_ok=True)
    t0 = time.time(); us = node_units(node); subs = []; extra = {}
    if meth == "ref":
        o = os.path.join(W, "ref_" + node + ".jsonl")
        if os.path.exists(o): os.remove(o)
        p = subprocess.Popen([sys.executable, os.path.join(T, "close_tree.py"), base, o, node, "--jobs", "4",
                              "--caps", "300,300,600", "--cadopts=--sat", "--split-singles", "--hours", str(budget / 3600)],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        try: p.wait(timeout=budget + 30)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, 9); p.wait(); extra["killed"] = True
        subprocess.run("pkill -9 -f 'cadical.*/opt/work/ct/' ; rm -f /opt/work/ct/*", shell=True)
        rs = [json.loads(l) for l in open(o)] if os.path.exists(o) else []
        subs = [{"sub": r["node"], "status": r.get("status"), "solve_s": r.get("solve_s"), "certified": r.get("certified"),
                 "check_s": r.get("check_s")} for r in rs if "status" in r]
        extra["splits"] = sum(1 for r in rs if r.get("split"))
        root_cert = any(r["node"] == node and r.get("certified") for r in rs)
        # closed iff node certified, or close_tree reported an empty open frontier (not observable when killed)
        closed = root_cert
        wall = time.time() - t0
    else:
        jobs = []
        if meth.startswith("march"):
            d = int(meth[5:]); cnf = os.path.join(W, "m_" + node + ".cnf"); ic = cnf + ".icnf"
            write_cnf(base, us, cnf); tm = time.time()
            try:
                subprocess.run(f"ulimit -s unlimited; {MARCH} {cnf} -d {d} -o {ic}", shell=True, timeout=budget,
                               capture_output=True)
            except subprocess.TimeoutExpired:
                subprocess.run("pkill -9 -f march_cu", shell=True)
            extra["march_s"] = round(time.time() - tm, 1); os.remove(cnf)
            cubes = [[int(x) for x in l.split()[1:-1]] for l in open(ic) if l.startswith("a ")] if os.path.exists(ic) else []
            extra["cubes"] = len(cubes)
            jobs = [(f"{node}__c{i}", base, us + c, None, ["--sat"]) for i, c in enumerate(cubes)]
        elif meth == "split":
            ch = [layers_name(c) for c in tree_children(11, 7, parse_layers(node))]
            jobs = [(c, base, node_units(c), None, ["--sat"]) for c in ch]
        elif meth == "opt":
            jobs = [(f"{node}__o{i}", base, us, None, o) for i, o in enumerate(OPTS)]
        with cf.ProcessPoolExecutor(4) as ex:
            futs = []
            for j in jobs:
                futs.append(ex.submit(solve, (j[0], j[1], j[2], max(1, budget - (time.time() - t0)), j[4])))
            for fu in cf.as_completed(futs):
                subs.append(fu.result())
        wall = time.time() - t0
        for s in subs:
            if s["status"] == "UNSATISFIABLE": check(s)
        if meth == "opt":
            closed = any(s.get("certified") for s in subs)
        else:
            closed = bool(jobs) and len(subs) == len(jobs) and all(s.get("certified") for s in subs) and \
                     (meth == "split" or extra.get("cubes", 0) > 0)
        # unsubmitted jobs (budget ran out before start) count as open: cap is clamped to >= 1 s so they run 1 s
    sat = [s["sub"] for s in subs if s["status"] == "SATISFIABLE"]
    rec = {"node": node, "depth": node.count("_") + 1, "method": meth, "budget_s": budget, "closed": closed,
           "wall_s": round(wall, 1), "solve_s_total": round(sum(s.get("solve_s") or 0 for s in subs), 1),
           "check_s_total": round(sum(s.get("check_s") or 0 for s in subs), 1), "subproblems": len(subs),
           "unsat": sum(1 for s in subs if s["status"] == "UNSATISFIABLE"),
           "certified": sum(1 for s in subs if s.get("certified")),
           "max_sub_s": max([s.get("solve_s") or 0 for s in subs] or [0]), "sat": sat, **extra, "subs": subs}
    open(out, "a").write(json.dumps(rec) + "\n")
    print(json.dumps({k: v for k, v in rec.items() if k != "subs"}), flush=True)
    if sat: print("SAT FOUND", sat, flush=True)

if __name__ == "__main__":
    main()
