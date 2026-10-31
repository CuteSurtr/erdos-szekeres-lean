"""solve and dual-check (real proofs) every certified node of a forged file, write real records.
usage: real_childless.py m k BASE IN.jsonl OUT.jsonl"""
import json, sys, os, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mydriver as D, mycompose as Y
m, k, base, fin, fout = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]
os.makedirs(D.WORK, exist_ok=True)
names = [json.loads(l)["node"] for l in open(fin)]
with cf.ProcessPoolExecutor(4) as ex:
    recs = list(ex.map(D.solve, [(m, k, base, Y.key(*Y.parse(n)), 10 ** 7) for n in names]))
open(fout, "w").write("".join(json.dumps(r) + "\n" for r in recs))
print({"nodes": len(recs), "certified": sum(1 for r in recs if r.get("certified"))})
