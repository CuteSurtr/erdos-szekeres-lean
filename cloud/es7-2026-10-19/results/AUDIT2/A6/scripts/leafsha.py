"""For every tree leaf (from mytrees.json), recompute the sha256 of the leaf CNF in the V3 layout
(header 'p cnf NV NC+k', F body, case cube units sorted by |x|, then the leaf literals not in the
case cube sorted by |x|) and compare with the cnf_sha256 of the V3 VERIFIED records.
usage: leafsha.py RESULTS F.cnf mytrees.json"""
import hashlib, json, sys, os, collections
R, FC, MT = sys.argv[1:4]
raw = open(FC, "rb").read(); assert hashlib.sha256(raw).hexdigest().startswith("69c1dc8f")
hdr, body = raw.split(b"\n", 1); _, _, nv, nc = hdr.split(); nv, nc = int(nv), int(nc)
cases = [json.loads(l) for l in open(os.path.join(R, "Mii-S/cases.jsonl")) if l.strip()]
cubes = [l.split()[1:-1] for l in open(os.path.join(R, "Mii-S/cases.icnf")) if l.startswith("a ")]
cube = {}
for c, cb in zip(cases, cubes):
    cb = sorted(map(int, cb), key=abs)
    assert len(cb) == c["nlits"], c["case"]
    d = b"p cnf %d %d\n" % (nv, nc + len(cb)) + body + b"".join(b"%d 0\n" % x for x in cb)
    assert hashlib.sha256(d).hexdigest() == c["cnf_sha256"], c["case"]
    cube[c["case"]] = cb
print("450 case CNFs hash to cases.jsonl")
v3 = collections.defaultdict(set)
for f in open(os.path.join(R, "V3Z/aggregate_inputs.txt")).read().split():
    for l in open(os.path.join(R, f.replace("results/", "", 1))):
        if not l.strip(): continue
        r = json.loads(l)
        if r["kind"] == "leaf" and r["verdict"] == "VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
            v3[(r["case"], tuple(sorted(r["lits"])))].add(r["cnf_sha256"])
M = json.load(open(MT))["cases"]
pref = {}
ok = bad = contra = 0; badl = []
for case, v in M.items():
    if v["src"] == "direct": continue
    cs = set(cube[case])
    for lf in v["leaves"]:
        if any(-x in cs for x in lf): contra += 1; continue
        extra = sorted({x for x in lf if x not in cs}, key=abs)
        if len(extra) != len([x for x in lf if x not in cs]): print("dup lit in leaf", case, lf)
        n = len(cube[case]) + len(extra)
        k = (case, n)
        if k not in pref:
            h = hashlib.sha256(b"p cnf %d %d\n" % (nv, nc + n)); h.update(body); h.update(b"".join(b"%d 0\n" % x for x in cube[case])); pref[k] = h
        h = pref[k].copy(); h.update(b"".join(b"%d 0\n" % x for x in extra))
        got = v3.get((case, tuple(sorted(lf))), set())
        if h.hexdigest() in got and len(got) == 1: ok += 1
        else: bad += 1; badl.append((case, lf, list(got)))
print("leaves: sha match", ok, "mismatch", bad, "contradicting case cube", contra, "prefix states", len(pref))
for b in badl[:10]: print(b)
