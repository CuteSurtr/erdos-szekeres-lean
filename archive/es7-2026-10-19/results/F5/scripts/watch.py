#!/usr/bin/env python3
"""Watch the generator outputs (arm_f.py JSON lines with "points"; grow_guided.py *.pts), and for every
realized 26-point set: exact re-check of the arm-F record (distinct x, general position, recorded model
= exact signs), canonical fingerprint, dedup against F2 (data/f2_fingerprints.txt) and earlier F5
sets, then process_set.sh (verify26, brute26, all 32-point deep-below sets, check32).
Appends to data/realized26.jsonl; ALERT lines go to watch.log for any free face or SAT position.
usage: watch.py RUNDIR OUTDIR (loops until the file STOP exists in RUNDIR)"""
import glob, hashlib, itertools, json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../tools/realizer"))
from chiro import canonical_form, chirotope_of
run, outd = sys.argv[1:3]
F5 = os.path.join(HERE, "..")
def o(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
def fp(P): return hashlib.sha1(canonical_form(chirotope_of(P), len(P)).encode()).hexdigest()
known = {l.split()[1]: l.split()[0] for l in open(os.path.join(F5, "data/f2_fingerprints.txt"))}
regf = os.path.join(F5, "data/realized26.jsonl")
done = set()
if os.path.exists(regf):
    for l in open(regf):
        r = json.loads(l); done.add(r["src"])
        if r.get("new"): known.setdefault(r["fingerprint"], r["name"])
def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)
while not os.path.exists(os.path.join(run, "STOP")):
    cands = []
    for f in sorted(glob.glob(os.path.join(run, "armF_*.jsonl"))):
        for k, l in enumerate(open(f)):
            if '"points"' not in l: continue
            r = json.loads(l); cands.append((f"{os.path.basename(f)}:{k}", r["id"], r["points"], r))
    for f in sorted(glob.glob(os.path.join(run, "gg*/gg*.pts"))):
        cands.append((f, os.path.basename(f)[:-4], [list(map(int, l.split())) for l in open(f) if l.strip()], None))
    for src, name, P, rec in cands:
        if src in done: continue
        done.add(src); P = [tuple(map(int, p)) for p in P]
        ent = {"src": src, "name": name, "n": len(P)}
        Q = sorted(P)
        ent["distinct_x"] = len({p[0] for p in P}) == len(P)
        sg = "".join("+" if o(Q[i], Q[j], Q[k]) > 0 else ("-" if o(Q[i], Q[j], Q[k]) < 0 else "0") for i, j, k in itertools.combinations(range(len(Q)), 3))
        ent["general_position"] = "0" not in sg
        if rec is not None: ent["model_matches_points"] = (P == Q and sg == rec.get("model")); ent["arm_exact_ok"] = rec.get("exact_ok")
        if len(P) != 26 or not ent["general_position"]:
            ent["new"] = False; ent["skip"] = "bad"; open(regf, "a").write(json.dumps(ent) + "\n"); continue
        h = fp(P); ent["fingerprint"] = h
        if h in known:
            ent["new"] = False; ent["duplicate_of"] = known[h]; log("DUP", name, known[h])
            open(regf, "a").write(json.dumps(ent) + "\n"); continue
        known[h] = name; ent["new"] = True; log("NEW", name, h[:16])
        tmp = os.path.join(run, name + ".S.pts"); open(tmp, "w").write("".join(f"{x} {y}\n" for x, y in P))
        od = os.path.join(outd, name)
        r = subprocess.run([os.path.join(HERE, "process_set.sh"), name, tmp, od], capture_output=True, text=True)
        try:
            s = json.load(open(os.path.join(od, "summary.json")))
        except Exception:
            s = {"error": (r.stdout + r.stderr)[-1000:]}
        ent["summary"] = s
        open(regf, "a").write(json.dumps(ent) + "\n")
        log("DONE", name, json.dumps({k: v for k, v in s.items() if k != "verify26"})[:600])
        if s.get("geom_bad") or s.get("ext_sat") or s.get("ext_unknown") or "error" in s or s.get("n32", 0) == 0 or s.get("brute26", "").startswith("FAIL"):
            log("ALERT", name, json.dumps(s)[:2000])
    time.sleep(30)
