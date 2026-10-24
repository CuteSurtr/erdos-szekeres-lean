#!/usr/bin/env python3
"""LBS2 L5 pipeline: for each candidate 32-point set: coordinate reduction if needed (uniform
scaling, order type re-checked exactly), independent exact check with vfy7 (general position,
c6, c7 == 0), exact order-type hash, then tools/realizer/saturate.py --K 7 (sat.c).
Input: a JSONL file of {"gen":..., "seed":..., "pts":[[x,y],...]}; appends to out.jsonl.
Sets with |coord| >= 2^27 go to sat_wide (src/sat_wide.c, src/saturate_wide.py). A set whose
order type (ot_hash) was already tested is recorded as a duplicate and not re-tested.
usage: pipeline.py IN.jsonl OUT.jsonl SATBIN VFYBIN SATURATE_PY SATWIDEBIN SATURATE_WIDE_PY"""
import hashlib, json, os, subprocess, sys, tempfile, time

B27 = 1 << 27

def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

def sgn(v):
    return (v > 0) - (v < 0)

def chirotope(pts):
    n = len(pts)
    return [sgn(orient(pts[i], pts[j], pts[k])) for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n)]

def ot_hash(pts):
    """Canonical form under relabelling and reflection (general position): for each hull vertex h
    and each orientation, label h = 0 and the others by angle around h; minimum sign string."""
    n = len(pts)
    O = {}
    def o(a, b, c):
        return sgn(orient(pts[a], pts[b], pts[c]))
    hull = []
    for h in range(n):
        others = [a for a in range(n) if a != h]
        # h is a hull vertex iff some other point a has all remaining points on one side of h->a
        for a in others:
            s = {o(h, a, b) for b in others if b != a}
            if len(s) == 1:
                hull.append(h); break
    best = None
    import functools
    for h in hull:
        for mir in (1, -1):
            others = [a for a in range(n) if a != h]
            others.sort(key=functools.cmp_to_key(lambda a, b: -mir * o(h, a, b)))
            lab = [h] + others
            s = bytes(1 + mir * o(lab[i], lab[j], lab[k]) for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n))
            if best is None or s < best:
                best = s
    return hashlib.sha256(best).hexdigest()[:16]

def main():
    inp, outp, satb, vfyb, satpy, satbw, satpyw = sys.argv[1:8]
    done = set(); tested = {}
    if os.path.exists(outp):
        for l in open(outp):
            try:
                r = json.loads(l); done.add(r["id"])
                if r.get("status") == "tested": tested.setdefault(r["ot_hash"], r["id"])
            except Exception: pass
    for line in open(inp):
        rec = json.loads(line)
        rid = rec.get("id") or f'{rec["gen"]}:{rec["seed"]}'
        if rid in done:
            continue
        t0 = time.time()
        pts = [tuple(p) for p in rec["pts"]]
        out = {"id": rid, "gen": rec["gen"], "seed": rec["seed"], "N": len(pts)}
        out["max_abs_coord_in"] = max(max(abs(x), abs(y)) for x, y in pts)
        q = pts
        wide = out["max_abs_coord_in"] >= B27
        out["sat_variant"] = "sat_wide" if wide else "sat"
        h = ot_hash(q)
        if h in tested:
            out.update({"ot_hash": h, "status": "duplicate order type (not re-tested)", "duplicate_of": tested[h]})
            print(json.dumps(out), flush=True); open(outp, "a").write(json.dumps(out) + "\n"); continue
        with tempfile.TemporaryDirectory() as td:
            f = os.path.join(td, "set.pts")
            open(f, "w").write("".join(f"{x} {y}\n" for x, y in q))
            v = subprocess.run([vfyb, f], capture_output=True, text=True).stdout.split()
            vd = dict(zip(v[0::2], v[1::2]))
            out["vfy_gp"] = vd.get("gp") == "1"
            out["c7"] = int(vd.get("c7", -1)); out["c6"] = int(vd.get("c6", -1)); out["c5"] = int(vd.get("c5", -1))
            out["ot_hash"] = h
            out["pts"] = [list(p) for p in q]
            if not out["vfy_gp"] or out["c7"] != 0:
                out["status"] = "rejected: not general position or c7 > 0"
            else:
                r = subprocess.run([sys.executable, satpyw if wide else satpy, "--sat", satbw if wide else satb, "--K", "7", f], capture_output=True, text=True)
                js = [l for l in r.stdout.splitlines() if l.startswith("{")]
                if not js:
                    out["status"] = "error: " + (r.stdout + r.stderr)[-400:]
                else:
                    s = json.loads(js[-1])
                    sat = s.get("sat", {})
                    out.update({"saturate_gp": s.get("general_position"), "largest_convex_subset": s.get("largest_convex_subset"),
                                "faces": sat.get("faces_euler"), "faces_hit": sat.get("faces_hit_by_valid_candidates"),
                                "faces_euler_eq_hit": s.get("faces_covered"), "bad_candidates": sat.get("bad_candidates"),
                                "saturated": s.get("saturated"), "sat_cpu_seconds": sat.get("cpu_seconds")})
                    if s.get("bad_file_head"): out["bad_file_head"] = s["bad_file_head"]
                    out["status"] = "tested"
                    tested.setdefault(h, rid)
        out["seconds"] = round(time.time() - t0, 2)
        print(json.dumps({k: v for k, v in out.items() if k != "pts"}), flush=True)
        open(outp, "a").write(json.dumps(out) + "\n")
        if out.get("bad_candidates"):
            print("BAD CANDIDATES FOUND", flush=True); sys.exit(7)

if __name__ == "__main__":
    main()
