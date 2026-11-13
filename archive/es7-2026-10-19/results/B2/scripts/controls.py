#!/usr/bin/env python3
"""Encoder validation for the ETV ladder (task B step 1).

For every control (k, a, u, N) build the CNF with gen_etv.py (ours) and with Baek-Balko's
etv_signotope (bb_emit.py), optionally add the x-reflection lex-leader (lexx.py), solve each
with CaDiCaL, brute-force-check every SAT model with sigcheckB, and require agreement with
the expected answer and between encoders.

Triple convention: (k, a, u) = (gon size, cap bound, cup bound) = Baek-Balko's (n, a, b).
Conjectured maximum (ETV 1996): f(k,a,u) = sum_{i=k-u}^{a-2} C(k-2, i) for k <= a+u-2.

usage: controls.py WORKDIR OUT.json [--jobs J] [--timeout S] [--sb]
"""
import argparse, json, math, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[2] / "tools"  # cloud/es7-2026-10-19/tools


def f_etv(k, a, u):
    return sum(math.comb(k - 2, i) for i in range(k - u, a - 1))


def control_list():
    C = []
    # k = 5 and k = 6: every (a, u) with 3 <= a, u <= k and k <= a + u - 2, both orders
    for k in (5, 6):
        for a in range(3, k + 1):
            for u in range(3, k + 1):
                if k <= a + u - 2:
                    m = f_etv(k, a, u)
                    C.append((k, a, u, m, "SAT")); C.append((k, a, u, m + 1, "UNSAT"))
    # k = 7: small rungs known as theorems (a = 4 by Baek; cup-cap range; a = 3 trivial)
    for (a, u) in ((3, 7), (7, 3), (4, 5), (4, 6), (4, 7), (7, 4), (5, 5)):
        m = f_etv(7, a, u)
        C.append((7, a, u, m, "SAT")); C.append((7, a, u, m + 1, "UNSAT"))
    # k = 7 positive controls at the conjectured maxima of the open rungs
    for (a, u) in ((5, 6), (6, 5), (5, 7), (7, 5), (6, 6)):
        C.append((7, a, u, f_etv(7, a, u), "SAT"))
    return C


def run(cmd, timeout=None):
    t = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p, time.time() - t


def solve(cadical, cnf, model_path, tlim):
    t = time.time()
    p = subprocess.run([cadical, "-t", str(tlim), cnf], capture_output=True, text=True)
    dt = time.time() - t
    res = {10: "SAT", 20: "UNSAT"}.get(p.returncode, "UNKNOWN")
    if res == "SAT":
        lits = []
        for line in p.stdout.splitlines():
            if line.startswith("v "):
                lits.extend(int(x) for x in line[2:].split() if x != "0")
        Path(model_path).write_text(" ".join(map(str, lits)) + "\n")
    return res, round(dt, 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir"); ap.add_argument("out")
    ap.add_argument("--jobs", type=int, default=6); ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--sb", action="store_true", help="also run both encoders with the x-reflection lex-leader")
    ap.add_argument("--only", default=None, help="comma list of k:a:u:N to run")
    args = ap.parse_args()
    W = Path(args.workdir).resolve(); W.mkdir(parents=True, exist_ok=True)
    cadical = str(W.parent / "ext/cadical/build/cadical")
    bbrepo = str(W.parent / "ext/erdos-szekeres-sat")
    sigcheck = str(W.parent / "sigcheckB")
    ctl = control_list()
    if args.only:
        want = {tuple(map(int, s.split(":"))) for s in args.only.split(",")}
        ctl = [c for c in ctl if c[:4] in want] + [(*w, "?") for w in want if w not in {c[:4] for c in ctl}]

    def one(c):
        k, a, u, N, exp = c
        tag = f"k{k}a{a}u{u}N{N}"
        rec = {"k": k, "a": a, "u": u, "N": N, "conj_max": f_etv(k, a, u), "expected": exp, "runs": {}}
        variants = [("ours", None), ("bb", None)]
        if args.sb:
            variants += [("ours", "lexx"), ("bb", "lexx")]
        for enc, sb in variants:
            name = f"{tag}_{enc}" + (f"_{sb}" if sb else "")
            cnf = W / f"{name}.cnf"
            if enc == "ours":
                p, _ = run([sys.executable, str(TOOLS / "etv/gen_etv.py"), str(N), str(a), str(u), str(k), "-o", str(cnf)])
            else:
                p, _ = run([sys.executable, str(HERE / "bb_emit.py"), bbrepo, str(k), str(a), str(u), str(N), str(cnf)])
            assert p.returncode == 0, p.stderr
            info = json.loads(p.stdout.strip().splitlines()[-1])
            if sb:
                p2, _ = run([sys.executable, str(HERE / "lexx.py"), str(cnf), str(N), str(cnf) + ".sb"])
                assert p2.returncode == 0, p2.stderr
                os.replace(str(cnf) + ".sb", cnf)
            model = W / f"{name}.model"
            res, dt = solve(cadical, str(cnf), str(model), args.timeout)
            r = {"result": res, "time_s": dt, "vars": info["vars"], "clauses": info["clauses"]}
            if res == "SAT":
                pc, _ = run([sigcheck, str(N), str(a), str(u), str(k), str(model)])
                r["check"] = json.loads(pc.stdout)
            rec["runs"][name.split("_", 1)[1]] = r
            cnf.unlink()
        results = {v["result"] for v in rec["runs"].values()}
        rec["agree"] = len(results) == 1
        rec["match_expected"] = results == {exp}
        rec["models_ok"] = all(v.get("check", {}).get("ok", True) for v in rec["runs"].values())
        print(json.dumps({"ctl": tag, "exp": exp, **{kk: (v["result"], v["time_s"]) for kk, v in rec["runs"].items()},
                          "agree": rec["agree"], "ok": rec["match_expected"] and rec["models_ok"]}), flush=True)
        return rec

    with ThreadPoolExecutor(args.jobs) as ex:
        out = list(ex.map(one, ctl))
    summary = {"n": len(out), "all_agree": all(r["agree"] for r in out),
               "all_match_expected": all(r["match_expected"] for r in out),
               "all_models_ok": all(r["models_ok"] for r in out)}
    Path(args.out).write_text(json.dumps({"summary": summary, "controls": out}, indent=1))
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
