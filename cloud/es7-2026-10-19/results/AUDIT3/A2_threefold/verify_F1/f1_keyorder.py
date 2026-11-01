#!/usr/bin/env python3
"""verify_F1 part 4: key-order signatures of certified records (json.dumps keeps dict insertion order,
so each generating script leaves a fixed key order); records with unusual signatures or extra fields
such as 'note' may have been edited by hand.  Also: are such records load-bearing in the cut?
usage: python3 -I f1_keyorder.py R AUDIT_REPORT_JSON"""
import collections, json, os, sys
R, rep = sys.argv[1], sys.argv[2]
BASE = "bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da"
def canon(r):
    n = r["node"]
    if "cube" in r:
        n += "__" + "-".join(f"{a}s{b}" for a, b in sorted((int(x), int(v)) for x, v in r["cube"].items()))
    return n
def ok(r):
    return (r.get("certified") is True and r.get("status") == "UNSATISFIABLE" and r.get("lrat_check") == "c VERIFIED"
            and r.get("cake_lpr") == "s VERIFIED UNSAT" and r.get("base_sha256", BASE) == BASE)
files = [l.strip() for l in open(os.path.join(R, "C3FINAL/compose_files.txt")) if l.strip()]
sig = collections.Counter(); ex = {}
cert = collections.defaultdict(list)
for f in files:
    for l in open(os.path.join(R, f)):
        l = l.strip()
        if not l: continue
        r = json.loads(l)
        if "node" in r and "meta" not in r and ok(r):
            k = tuple(r.keys())
            sig[k] += 1
            ex.setdefault(k, (f, r["node"]))
            cert[canon(r)].append((f, k))
cut = set(json.load(open(rep))["cut"])
for k, v in sig.most_common():
    print(v, ex[k][0], "|", ",".join(k))
rare = {k for k, v in sig.items() if v < 100}
# cut pieces whose every certified record has a rare signature
only_rare = [n for n in cut if all(k in rare for f, k in cert[n])]
print("cut pieces whose certified records all have a rare (<100) key signature:", len(only_rare))
for n in only_rare[:20]:
    print("   ", n, [(f, ",".join(k)) for f, k in cert[n]])
