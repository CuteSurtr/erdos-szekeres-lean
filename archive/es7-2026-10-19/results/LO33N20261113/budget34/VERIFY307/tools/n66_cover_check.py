#!/usr/bin/env python3
"""Independent cover check for N66 <= 55 (level-14 cube campaign).  Track P307V, 18 Nov 2026.  Own code, written from
the definitions in N66N20261113/cubes20261115/README.md sections 2 and 6 and ROUTE307_1116.md section 4.2; it does not
import or read the campaign driver, AN's cover_check.py or any other checker.

Definitions used:
  * split states 25 12 16 29 17 37 (base cube id = 6 letters in this order), re-split literals `_<s><o|h>`;
  * sel_s = DIMACS variable 988541 + s; o = occupied = +sel_s (bit 1), h = hole = -sel_s (bit 0);
  * states 0 and 1 are fixed occupied (units +988541, +988542), so no cube may mention them.

A certificate directory <C14>/<id>/it<k>/ is ACCEPTED only if all of these hold (read-only):
  cert.json : ALL_OK is true, cake_lpr == "s VERIFIED UNSAT", budget 14, holes_at_least 15, bound 55, W_size 70,
              sb_pairs == the 27-pair list of the base layout (b14h2), cube well formed;
  verify.json: ALL_OK true, unclassified 0, budget 14, same cube, same sb_pairs, same trim hashes as cert.json, cake line;
  layout.json: L 14, W == range(70), sel == [988541, 988610], same cube, same sb_pairs, cnf_sha256 == cert full_cnf_sha256;
  cake.out  : contains the exact line "s VERIFIED UNSAT" (cake_lpr exits 0 on rejection, so only the line counts);
  id        : the literals parsed from the directory name equal the cube field (as sets);
  --deep    : SHA-256(trim.cnf) == cert.json trim_cnf_sha256, and every unit clause of trim.cnf is +sel_0, +sel_1 or a
              unit of the declared cube (so the refuted cube contains the declared one).
The cube literals used for the cover are the cert.json `cube` field of accepted directories (never the driver's state).

Cover: V = the base states plus every state in any accepted cube.  Every total assignment of V (2^|V|, sel_0 = sel_1 = 1
implicitly) must satisfy some accepted cube.  Measure = exact Fraction (uncovered assignments / 2^|V|).
The driver's campaign_status.json is read ONLY to name the uncovered region (its non-certified leaves); the program
checks that the uncovered assignments are exactly the union of those leaves and reports any disagreement.

usage: n66_cover_check.py [--c14 DIR] [--base-layout FILE] [--deep] [--out JSON] | --selftest
exit 0 = cover complete, 1 = not complete, 2 = input/consistency problem.
"""
import argparse, glob, hashlib, json, os, re, sys
from fractions import Fraction

BASE = (25, 12, 16, 29, 17, 37)
SEL0 = 988541
CAKE_LINE = "s VERIFIED UNSAT"
N66 = "/home/jay/research/data/n66-20261113/p2"


def parse_id(cid):
    """'ohohoo_23o_40o_52h' -> {25:1, 12:0, ...}; None if malformed."""
    parts = cid.split("_")
    if len(parts[0]) != 6 or set(parts[0]) - {"o", "h"}:
        return None
    lits = {s: int(ch == "o") for s, ch in zip(BASE, parts[0])}
    for p in parts[1:]:
        m = re.fullmatch(r"(\d+)([oh])", p)
        if not m or int(m.group(1)) in lits:
            return None
        lits[int(m.group(1))] = int(m.group(2) == "o")
    return lits


def cube_dict(cube):
    """cert-style [[s, bit], ...] -> {s: bit}; None if malformed (dup state, fixed state 0/1, bad range or bit)."""
    if not isinstance(cube, list) or not cube:
        return None
    d = {}
    for e in cube:
        if not (isinstance(e, list) and len(e) == 2 and all(type(x) is int for x in e)):
            return None
        s, b = e
        if not (2 <= s < 70) or b not in (0, 1) or s in d:
            return None
        d[s] = b
    return d


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 22), b""):
            h.update(blk)
    return h.hexdigest()


def accept(certdir, cid, ref_sb, deep):
    """Return (cube dict, []) if accepted, else (None, [reasons])."""
    why = []
    try:
        cert = json.load(open(os.path.join(certdir, "cert.json")))
        ver = json.load(open(os.path.join(certdir, "verify.json")))
        lay = json.load(open(os.path.join(certdir, "layout.json")))
        cake_lines = [l.rstrip("\r\n") for l in open(os.path.join(certdir, "cake.out"), errors="replace")]
    except (OSError, ValueError) as e:
        return None, [f"unreadable: {e!r}"]
    cube = cube_dict(cert.get("cube"))
    if cube is None:
        why.append("cert cube malformed")
    for k, v in (("ALL_OK", True), ("cake_lpr", CAKE_LINE), ("budget", 14), ("holes_at_least", 15), ("bound", 55),
                 ("W_size", 70), ("sb_pairs", ref_sb)):
        if cert.get(k) != v:
            why.append(f"cert.{k}={str(cert.get(k))[:40]}")
    for k, v in (("ALL_OK", True), ("unclassified", 0), ("budget", 14), ("sb_pairs", ref_sb), ("cake_lpr", CAKE_LINE),
                 ("cube", cert.get("cube")), ("trim_cnf_sha256", cert.get("trim_cnf_sha256")),
                 ("trim_lrat_sha256", cert.get("trim_lrat_sha256"))):
        if ver.get(k) != v:
            why.append(f"verify.{k}")
    for k, v in (("L", 14), ("W", list(range(70))), ("sel", [SEL0, SEL0 + 69]), ("sb_pairs", ref_sb),
                 ("cube", cert.get("cube")), ("cnf_sha256", cert.get("full_cnf_sha256"))):
        if lay.get(k) != v:
            why.append(f"layout.{k}")
    if CAKE_LINE not in cake_lines:
        why.append("cake.out lacks the exact line")
    if cube is not None and parse_id(cid) != cube:
        why.append("id literals != cert cube")
    if deep and not why:
        tc = os.path.join(certdir, "trim.cnf")
        if sha256(tc) != cert.get("trim_cnf_sha256"):
            why.append("trim.cnf sha256 != cert.json")
        allowed = {SEL0, SEL0 + 1} | {(SEL0 + s) if b else -(SEL0 + s) for s, b in cube.items()}
        units = {int(m.group(1)) for m in re.finditer(rb"^\s*(-?\d+)\s+0\s*$", open(tc, "rb").read(), re.M)}
        extra = units - allowed
        if extra:
            why.append(f"trim.cnf units outside cube+fixed: {sorted(extra)[:5]}")
    return (cube if not why else None), why


def cover(cubes, V):
    """cubes: list of {s: bit}; V: ordered states. Returns sorted list of uncovered assignments (ints, bit i = V[i])."""
    idx = {s: i for i, s in enumerate(V)}
    mv = []
    for c in cubes:
        m = v = 0
        for s, b in c.items():
            m |= 1 << idx[s]
            v |= b << idx[s]
        mv.append((m, v))
    mv = list(set(mv))
    # shortcut: brute force over 2^|V| (14 states: about 1 s; 18: about 20 s); use Shannon splitting if |V| grows past ~20
    return [a for a in range(1 << len(V)) if not any(a & m == v for m, v in mv)]


def selftest():
    full = [{25: a, 12: b} for a in (0, 1) for b in (0, 1)]
    assert cover(full, [25, 12]) == []
    assert len(cover(full[1:], [25, 12])) == 1
    split = [{25: 0}, {25: 1, 12: 0}, {25: 1, 12: 1, 40: 0}]
    assert len(cover(split, [25, 12, 40])) == 1          # {25:1,12:1,40:1} missing: 1/8
    assert cover(split + [{25: 1, 12: 1, 40: 1}], [25, 12, 40]) == []
    assert cover([{25: 1}, {12: 1}, {25: 0, 12: 0}], [25, 12]) == []  # overlapping cubes are fine for a cover
    assert parse_id("ohohoo_23o_40o_52h") == {25: 1, 12: 0, 16: 1, 29: 0, 17: 1, 37: 1, 23: 1, 40: 1, 52: 0}
    assert parse_id("ohohoo_25o") is None and parse_id("ohoho") is None and parse_id("ohohox") is None
    assert cube_dict([[25, 1], [25, 0]]) is None and cube_dict([[0, 1]]) is None and cube_dict([[25, 2]]) is None
    assert cube_dict([[25, True]]) is None and cube_dict([[25, 1], [12, 0]]) == {25: 1, 12: 0}
    print("selftest OK")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--c14", default=f"{N66}/c14")
    ap.add_argument("--base-layout", default=f"{N66}/b14h2/it1/layout.json")
    ap.add_argument("--deep", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    ref_sb = json.load(open(a.base_layout))["sb_pairs"]
    assert len(ref_sb) == 27, "base layout SB list is not 27 pairs"
    accepted, rejected = {}, {}
    for cj in sorted(glob.glob(os.path.join(a.c14, "*", "it*", "cert.json"))):
        certdir = os.path.dirname(cj)
        cid = os.path.basename(os.path.dirname(certdir))
        if not re.fullmatch(r"it\d+", os.path.basename(certdir)):
            continue  # e.g. stopped1116-it1 is not a certificate directory
        cube, why = accept(certdir, cid, ref_sb, a.deep)
        if cube is not None:
            accepted.setdefault(cid, (certdir, cube))
        else:
            rejected[certdir] = why
    cubes = [c for _, c in accepted.values()]
    V = list(BASE) + sorted({s for c in cubes for s in c} - set(BASE))
    unc = cover(cubes, V)
    meas_unc = Fraction(len(unc), 1 << len(V))
    res = {"c14": a.c14, "deep": a.deep, "accepted_cert_dirs": len(accepted), "rejected_cert_dirs": rejected,
           "split_states": V, "assignments": 1 << len(V), "uncovered_assignments": len(unc),
           "uncovered_measure": str(meas_unc), "covered_measure": str(1 - meas_unc),
           "uncovered_over_512": str(meas_unc * 512), "complete": not unc,
           "accepted": sorted(accepted), "up_refuted_base_patterns_accepted":
               sorted(c for c in accepted if re.fullmatch(r"h[oh][oh]o[oh]h", c))}
    # name the uncovered region by the driver's non-certified leaves (driver state used for naming only)
    st_path = os.path.join(a.c14, "campaign_status.json")
    problems = []
    if os.path.exists(st_path):
        st = json.load(open(st_path))["cubes"]
        leaves = {k: v for k, v in st.items() if v.get("status") != "split"}
        lv = {k: dict(map(tuple, v["lits"])) for k, v in leaves.items()}
        Vl = V + sorted({s for c in lv.values() for s in c} - set(V))
        tot = sum(Fraction(1, 1 << len(c)) for c in lv.values())
        if tot != 1 or cover(list(lv.values()), Vl):
            problems.append("driver leaves are not a partition of the split (measure %s)" % tot)
        unc_l = set(cover(cubes, Vl))
        open_leaves = sorted(k for k in lv if k not in accepted)
        unc_from_leaves = set(range(1 << len(Vl))) - set(cover([lv[k] for k in open_leaves], Vl))
        if unc_l != unc_from_leaves:
            problems.append("uncovered assignments != union of the driver's non-accepted leaves")
        drv_cert = sorted(k for k, v in leaves.items() if v.get("status") == "certified")
        res.update({"driver_leaves": len(lv), "driver_certified": len(drv_cert),
                    "driver_certified_not_accepted_here": sorted(set(drv_cert) - set(accepted)),
                    "accepted_here_not_driver_certified": sorted(set(accepted) - set(drv_cert)),
                    "uncovered_leaves": [{"id": k, "status": leaves[k].get("status"),
                                          "measure": str(Fraction(1, 1 << len(lv[k])))} for k in open_leaves]})
    res["problems"] = problems
    res["verdict"] = ("COVER COMPLETE" if not unc else "NOT COMPLETE") + (" (with problems)" if problems else "")
    if a.out:
        json.dump(res, open(a.out, "w"), indent=1)
    print(f"{res['verdict']}: accepted {len(accepted)} cert dirs, rejected {len(rejected)}; split states {len(V)}; "
          f"uncovered {len(unc)}/{1 << len(V)} = {meas_unc} = {float(meas_unc * 512):g}/512")
    for u in res.get("uncovered_leaves", []):
        print(f"  open leaf {u['id']:24s} {u['status']:10s} {u['measure']}")
    for p in problems:
        print("PROBLEM:", p)
    return 2 if problems else (0 if not unc else 1)


if __name__ == "__main__":
    sys.exit(main())
