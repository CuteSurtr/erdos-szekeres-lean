"""Attribute violated clauses of a (mutant) encoder to its families.

Imports the given encoder file as a module (a copy written by mutate.py or the original copy), runs the same steps as
its build() one method at a time and records the clause count after each, then evaluates real labellings (no convex
K-gon) with evalcnf and reports the violated clauses per family.
usage: famviol.py ENCODER.py t K [--no-sb] [--hull] [--ncfg N]
"""
import importlib.util
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import geom    # noqa: E402
import mutate  # noqa: E402


def main():
    path, t, K = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    sb = "--no-sb" not in sys.argv
    hull = "--hull" in sys.argv
    ncfg = int(sys.argv[sys.argv.index("--ncfg") + 1]) if "--ncfg" in sys.argv else 6
    spec = importlib.util.spec_from_file_location("encmod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = os.path.join(os.path.dirname(path), f"fam_t{t}k{K}{'' if sb else '_nosb'}{'_h' if hull else ''}")
    enc = mod.ZEncoding("rot", t, K, 2, body=out + ".body", axis=0)
    bounds = []
    enc.add_gp(); bounds.append(("GP", enc.sink.n))
    enc.add_a4(); bounds.append(("A4", enc.sink.n))
    enc.add_centre_facts(); bounds.append(("CENTRE", enc.sink.n))
    enc.add_kgon(); bounds.append(("KGON(defs+sets)", enc.sink.n))
    if sb:
        enc.add_sb(); bounds.append(("SB", enc.sink.n))
    if hull:
        enc.add_hull_sb(); bounds.append(("HULL", enc.sink.n))
    info = enc.write(out + ".cnf", out + ".json", out + ".body")
    info = json.load(open(out + ".json"))
    info["Kc"] = K
    rng = random.Random(20261101)
    cfgs = mutate.configs_for(t, K, rng, n=ncfg)
    vals = []
    for P in cfgs:
        for p0 in geom.hull_vertices(P):
            v, cons, zok = mutate.assignment_for(info, geom.normal_form(P, (0, 0), p0))
            vals.append(v)
    viol = mutate.evaluate(out + ".cnf", vals, os.path.dirname(path))
    # indices are not returned by mutate.evaluate; recompute by matching clause text order
    lines = [l for l in open(out + ".cnf") if l[0] not in "cp"]
    index = {}
    for i, l in enumerate(lines, 1):
        index.setdefault(tuple(map(int, l.split()[:-1])), []).append(i)

    def fam(i):
        lo = 0
        for name, hi in bounds:
            if lo < i <= hi:
                return name
            lo = hi
        return "?"
    tot = {}
    for vv in viol:
        for cl in vv:
            for i in index[tuple(cl)][:1]:
                tot[fam(i)] = tot.get(fam(i), 0) + 1
    print(f"{os.path.basename(os.path.dirname(path))} t={t} K={K} sb={sb} hull={hull}: {len(vals)} labellings, "
          f"{sum(1 for vv in viol if vv)} with violations; violated clauses by family {tot}; bounds {bounds}")


if __name__ == "__main__":
    main()
