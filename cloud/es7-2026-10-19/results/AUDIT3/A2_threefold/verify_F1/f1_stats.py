#!/usr/bin/env python3
"""verify_F1: independent recount of the numbers in audit finding F1 (threefold piece verdicts).

Reads (read-only): the 280 record files listed in R/C3FINAL/compose_files.txt, the auditor's cut list
(logs/a2compose_report.json, key 'cut'), and R/C3SPOT/{units6.tsv,out.jsonl}.
Written from scratch; does not import the auditor's code.

usage: python3 -I f1_stats.py R AUDIT_REPORT_JSON [OUT_JSON]
"""
import collections
import json
import os
import sys

BASE_SHA = "bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da"


def canon(rec):
    """record -> canonical node name; cube-format records get '__' + sorted 'rsv' tokens."""
    n = rec["node"]
    if "cube" in rec:
        assert "__" not in n
        toks = sorted((int(r), int(v)) for r, v in rec["cube"].items())
        n = n + "__" + "-".join(f"{r}s{v}" for r, v in toks)
    return n


def strict_ok(rec):
    return (rec.get("certified") is True and rec.get("status") == "UNSATISFIABLE"
            and rec.get("lrat_check") == "c VERIFIED" and rec.get("cake_lpr") == "s VERIFIED UNSAT"
            and rec.get("base_sha256", BASE_SHA) == BASE_SHA)


def srcdir(path):
    p = path.split("/")
    # keep LOCAL* subdirectories distinct (C3W6/LOCAL, C3H1/LOCAL2, ...)
    if len(p) > 2 and p[1].startswith("LOCAL"):
        return p[0] + "/" + p[1]
    return p[0]


def main():
    R, rep = sys.argv[1], sys.argv[2]
    out_path = sys.argv[3] if len(sys.argv) > 3 else None
    files = [l.strip() for l in open(os.path.join(R, "C3FINAL/compose_files.txt")) if l.strip()]
    n_rec = 0
    cert = collections.defaultdict(list)  # name -> [(file, rec)]
    per_dir = collections.defaultdict(lambda: collections.Counter())
    odd = collections.Counter()
    status_counts = collections.Counter()
    checker_strings = collections.Counter()
    for f in files:
        for line in open(os.path.join(R, f)):
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            n_rec += 1
            if "node" not in rec or "meta" in rec:
                odd["no_node_or_meta"] += 1
                continue
            st = rec.get("status")
            status_counts[st] += 1
            if st == "UNSATISFIABLE":
                checker_strings[(rec.get("lrat_check"), rec.get("cake_lpr"), rec.get("certified"))] += 1
            d = srcdir(f)
            per_dir[d]["records"] += 1
            if rec.get("certified") is True and not strict_ok(rec):
                odd["certified_true_not_strict"] += 1
            if strict_ok(rec):
                name = canon(rec)
                cert[name].append((f, rec))
                per_dir[d]["certified"] += 1
                if rec.get("proof_sha256"):
                    per_dir[d]["certified_with_proof_sha"] += 1
                if "cube" in rec:
                    per_dir[d]["certified_cube_format"] += 1
    n_cert_rec = sum(len(v) for v in cert.values())
    n_cert_hash = sum(1 for v in cert.values() for f, r in v if r.get("proof_sha256"))
    print(f"records {n_rec}; certified records {n_cert_rec}; certified nodes {len(cert)}; "
          f"certified records with proof_sha256 {n_cert_hash}; nodes with a hashed record "
          f"{sum(1 for v in cert.values() if any(r.get('proof_sha256') for f, r in v))}")
    print("odd:", dict(odd))
    print("status counts:", dict(status_counts))
    print("UNSAT records by (lrat_check, cake_lpr, certified):")
    for k, v in checker_strings.most_common():
        print("   ", k, v)
    print("\nper source dir: records / certified / certified with proof_sha256 / cube-format certified")
    for d in sorted(per_dir):
        c = per_dir[d]
        print(f"  {d:14s} {c['records']:7d} {c['certified']:7d} {c['certified_with_proof_sha']:7d} {c['certified_cube_format']:5d}")

    # ---------------- the auditor's cut
    cut = json.load(open(rep))["cut"]
    assert len(cut) == len(set(cut))
    missing = [n for n in cut if n not in cert]
    print(f"\ncut size {len(cut)}; cut names without a certified record: {len(missing)}")
    with_hash = [n for n in cut if any(r.get("proof_sha256") for f, r in cert[n])]
    print(f"cut names with >=1 certified record carrying proof_sha256: {len(with_hash)} "
          f"({100.0 * len(with_hash) / len(cut):.2f}%)")
    multi = sum(1 for n in cut if len(cert[n]) > 1)
    print(f"cut names with >1 certified record: {multi}")
    # source attribution: a cut name counts for each directory that holds a certified record of it
    cut_dir = collections.Counter()
    cut_dir_hash = collections.Counter()
    cut_only_dir = collections.Counter()
    for n in cut:
        ds = {srcdir(f) for f, r in cert[n]}
        for d in ds:
            cut_dir[d] += 1
        dh = {srcdir(f) for f, r in cert[n] if r.get("proof_sha256")}
        for d in dh:
            cut_dir_hash[d] += 1
        if len(ds) == 1:
            cut_only_dir[next(iter(ds))] += 1
    print("cut names per source dir (any certified record there) / with a hashed record there / only that dir")
    for d in sorted(cut_dir):
        print(f"  {d:14s} {cut_dir[d]:7d} {cut_dir_hash[d]:7d} {cut_only_dir[d]:7d}")
    cube_fmt_only = sum(1 for n in cut if all("cube" in r for f, r in cert[n]))
    print(f"cut names whose certified records are all sigma_cubes-format (outside C3SPOT's frame): {cube_fmt_only}")

    # ---------------- costs
    def pick(n, how):
        rs = [r for f, r in cert[n]]
        if how == "first":
            return rs[0]
        return min(rs, key=lambda r: r.get("solve_s", 0.0))

    for how in ("first", "min_solve"):
        tot = collections.Counter()
        nmiss = collections.Counter()
        for n in cut:
            r = pick(n, how)
            for k in ("solve_s", "check_s", "proof_bytes"):
                if isinstance(r.get(k), (int, float)):
                    tot[k] += r[k]
                else:
                    nmiss[k] += 1
        print(f"cut cost ({how} record): solve {tot['solve_s'] / 3600:.1f} h, check {tot['check_s'] / 3600:.1f} h, "
              f"proof {tot['proof_bytes'] / 1e12:.2f} TB; fields missing: {dict(nmiss)}")
    tot = collections.Counter()
    nmiss = collections.Counter()
    for n, v in cert.items():
        for f, r in v:
            for k in ("solve_s", "check_s", "proof_bytes"):
                if isinstance(r.get(k), (int, float)):
                    tot[k] += r[k]
                else:
                    nmiss[k] += 1
    print(f"all certified records: solve {tot['solve_s'] / 3600:.1f} h, check {tot['check_s'] / 3600:.1f} h, "
          f"proof {tot['proof_bytes'] / 1e12:.2f} TB; fields missing: {dict(nmiss)}")

    # ---------------- C3SPOT
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(R, "C3SPOT/units6.tsv")) if l.strip()]
    rowsha = {row[1]: row[3] for row in rows}
    rowsrc = {row[1]: row[4] for row in rows}
    spot = [json.loads(l) for l in open(os.path.join(R, "C3SPOT/out.jsonl")) if l.strip()]
    spot_pass = {}
    for s in spot:
        n = s["node"]
        ok = (s.get("status") == "UNSATISFIABLE" and s.get("certified") is True
              and s.get("lrat_check") == "c VERIFIED" and s.get("cake_lpr") == "s VERIFIED UNSAT"
              and s.get("cnf_sha256") == rowsha.get(n))
        spot_pass[n] = ok
    print(f"\nC3SPOT: sample rows {len(rows)}, re-solved {len(spot)} (distinct {len(spot_pass)}), "
          f"pass {sum(spot_pass.values())}")
    # does the sample row's sha equal a certified record's sha for that node?
    agree = sum(1 for n in spot_pass if any(r.get("cnf_sha256") == rowsha[n] for f, r in cert.get(n, [])))
    print(f"re-solved nodes whose sample sha equals a certified record's cnf_sha256: {agree}")
    cutset = set(cut)
    sp_cut = [n for n, ok in spot_pass.items() if ok and n in cutset]
    print(f"re-solved and passing nodes that lie in the cut: {len(sp_cut)}; cut names never re-solved: "
          f"{len(cut) - len(sp_cut)} ({100.0 * (len(cut) - len(sp_cut)) / len(cut):.2f}%)")
    sample_in_cut = sum(1 for row in rows if row[1] in cutset)
    print(f"sample rows (all 3,084) that lie in the cut: {sample_in_cut}")
    # identical proofs: original record proof_sha256 vs re-solve proof_sha256
    same = diff = nohash = 0
    diff_list = []
    for s in spot:
        n = s["node"]
        orig = [r for f, r in cert.get(n, []) if r.get("proof_sha256")]
        if not orig:
            nohash += 1
            continue
        if any(r["proof_sha256"] == s.get("proof_sha256") for r in orig):
            same += 1
        else:
            diff += 1
            diff_list.append((n, rowsrc.get(n), [(r.get("cadical_args"), r.get("cap")) for r in orig],
                              s.get("cadical_args")))
    print(f"re-solved rows with a hashed original: {same + diff}; identical proof sha {same}; different {diff}; "
          f"original without proof hash {nohash}")
    for x in diff_list[:10]:
        print("   differs:", x)
    # spot coverage by source dir, restricted to the cut
    spot_cut_dir = collections.Counter(srcdir(rowsrc[n]) for n in sp_cut)
    print("re-solved cut nodes by the sample's recorded source dir:", dict(sorted(spot_cut_dir.items())))
    if out_path:
        json.dump({"cut_with_hash": len(with_hash), "spot_cut": sorted(sp_cut)}, open(out_path, "w"))


if __name__ == "__main__":
    main()
