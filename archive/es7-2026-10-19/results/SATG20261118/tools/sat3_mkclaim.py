# usage: python3 mk.py id K n datafile label "how found" "extra statement" -> claims/<id>.json (SAT3 claim)
import json, sys, hashlib, time
cid, K, n, f, label, how, extra = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
R = '/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/SATG20261118'
sha = hashlib.sha256(open(f, 'rb').read()).hexdigest()
pts = [tuple(map(int, l.split())) for l in open(f) if l.strip()]
assert len(pts) == n, len(pts)
mc = max(max(abs(x), abs(y)) for x, y in pts)
d = {
 "id": cid, "filed_by": "SAT3", "time": time.strftime('%Y-%m-%d %H:%M KST'),
 "statement": f"sat_g({K}) <= {n}: the {n}-point integer set S = {f} (sha256 {sha}, |coordinates| <= {mc}) is {K}-gon-saturated in the sense of DDSZ (arXiv:2312.01223): (a) S is in general position and no {K} points of S are in convex position; (b) every point q not in S with S+q in general position is a vertex of a convex {K}-gon of S+q. " + extra,
 "label_claimed": label,
 "definitions": "DDSZ: P in general position is n-gon-saturated if it has no n points in convex position while every q not in P with P+q in general position lies on a convex n-gon of P+q; sat_g(n) = smallest size of an n-gon-saturated set. Saturation is a property of the coordinates (not of the order type).",
 "files": [f"{f} (sha256 {sha})", f"{R}/tools/sat3ls.cpp (SAT3 finder, HEURISTIC search only)", "/home/jay/research/data/roadmap-20261115/pm1115/vx2/vx2sat.cpp (VX2 checker, sha256 9b243cd156a6341f190240eb95960d1d51d4f3495678b63dfe8954bdccf3a55d; binary vx2sat2 sha256 3537f4936d2efd71005cc914cf75980ef3231e33870e4c76e6b95e017397d90b)"],
 "how_to_check": f"Own exact code preferred. (1) general position; no convex {K}-gon. (2) Enumerate all open cells of the arrangement of the C({n},2) lines through two points of S (cells must equal the Euler count F = 1 + L + sum_v (k_v - 1)), one exact sample per cell; each sample must lie on a convex {K}-gon with {K-1} points of S. One sample per open cell suffices (the order type of S+q is constant on an open cell). Record's check: VX2's vx2sat2 run unchanged, logs in /home/jay/research/data/roadmap-20261115/pm1115/sat3/vx/. How found: {how} (HEURISTIC, not part of the proof).",
 "record_folder": R,
 "verify_file": f"{R}/VERIFY_{cid}.md",
}
json.dump(d, open(f'/home/jay/research/data/roadmap-20261115/pm1115/sat3/claims/{cid}.json', 'w'), indent=1, ensure_ascii=False)
print('wrote', cid, sha[:16], mc)
