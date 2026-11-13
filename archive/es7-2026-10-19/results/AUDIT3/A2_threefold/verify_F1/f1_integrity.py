#!/usr/bin/env python3
"""verify_F1 part 2: record-integrity probes that bear on the severity of F1.

 (a) UNSAT records that were NOT certified (checker failures) and what became of their nodes;
 (b) odd status strings;
 (c) timing plausibility of certified records: proof size vs check time (a record claiming that both
     checkers verified a multi-GB LRAT file in a fraction of a second would be suspect);
 (d) duplicate certified records of one node: do cnf/proof hashes agree?
 (e) per-lane (record file) coverage of the auditor's cut by the C3SPOT re-solves;
 (f) which code paths produced the cut pieces (field signatures of the records).
usage: python3 -I f1_integrity.py R AUDIT_REPORT_JSON
"""
import collections
import json
import os
import statistics
import sys

BASE_SHA = "bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da"


def canon(rec):
    n = rec["node"]
    if "cube" in rec:
        toks = sorted((int(r), int(v)) for r, v in rec["cube"].items())
        n = n + "__" + "-".join(f"{r}s{v}" for r, v in toks)
    return n


def strict_ok(rec):
    return (rec.get("certified") is True and rec.get("status") == "UNSATISFIABLE"
            and rec.get("lrat_check") == "c VERIFIED" and rec.get("cake_lpr") == "s VERIFIED UNSAT"
            and rec.get("base_sha256", BASE_SHA) == BASE_SHA)


def main():
    R, rep = sys.argv[1], sys.argv[2]
    files = [l.strip() for l in open(os.path.join(R, "C3FINAL/compose_files.txt")) if l.strip()]
    cert = collections.defaultdict(list)
    allrec = collections.defaultdict(list)
    failed, oddstat = [], []
    for f in files:
        for line in open(os.path.join(R, f)):
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if "node" not in rec or "meta" in rec:
                continue
            name = canon(rec)
            allrec[name].append((f, rec))
            st = rec.get("status")
            if st not in (None, "UNSATISFIABLE", "UNKNOWN"):
                oddstat.append((f, rec))
            if st == "UNSATISFIABLE" and not strict_ok(rec):
                failed.append((f, name, rec))
            if strict_ok(rec):
                cert[name].append((f, rec))
    cut = json.load(open(rep))["cut"]
    cutset = set(cut)

    print("(a) UNSAT but not certified:", len(failed))
    fate = collections.Counter()
    for f, name, rec in failed:
        later = "certified elsewhere" if name in cert else (
            "split" if any(r.get("split") for _, r in allrec[name]) else "neither")
        fate[later] += 1
    print("    fate of those nodes:", dict(fate))
    for f, name, rec in failed[:6]:
        print("    e.g.", f, name, {k: rec.get(k) for k in ("lrat_check", "cake_lpr", "proof_bytes", "check_s", "certified")})
    print("    proof_bytes of failed records: min %.2f GB, max %.2f GB" % (
        min(r.get("proof_bytes", 0) for _, _, r in failed) / 1e9, max(r.get("proof_bytes", 0) for _, _, r in failed) / 1e9))

    print("(b) odd status strings:", len(oddstat))
    for f, rec in oddstat:
        print("    ", f, {k: rec.get(k) for k in ("node", "status", "certified", "lrat_check", "cake_lpr")})

    # (c) throughput of the two checkers together, bytes per second of check time
    thr = []
    nocheck = 0
    for name, L in cert.items():
        for f, r in L:
            pb, cs = r.get("proof_bytes"), r.get("check_s")
            if not isinstance(pb, (int, float)) or not isinstance(cs, (int, float)):
                nocheck += 1
                continue
            thr.append((pb / max(cs, 0.05), f, name, pb, cs, r.get("solve_s")))
    thr.sort()
    vals = [t[0] for t in thr]
    print("(c) certified records with proof_bytes and check_s:", len(thr), "missing:", nocheck)
    print("    check throughput MB/s: median %.1f, p99 %.1f, p99.9 %.1f, max %.1f" % (
        statistics.median(vals) / 1e6, vals[int(0.99 * len(vals))] / 1e6, vals[int(0.999 * len(vals))] / 1e6, vals[-1] / 1e6))
    print("    top 5 throughputs:")
    for t in thr[-5:]:
        print("      %.1f MB/s" % (t[0] / 1e6), t[1], t[2], "proof %.1f MB" % (t[3] / 1e6), "check_s", t[4], "solve_s", t[5])
    small = sum(1 for t in thr if t[3] < 1000)
    print("    certified records with proof_bytes < 1000:", small)
    zero_solve = sum(1 for t in thr if not t[5] or t[5] <= 0)
    print("    certified records with solve_s <= 0 or missing:", zero_solve)

    # (d) duplicates
    dup = {n: L for n, L in cert.items() if len(L) > 1}
    cnf_dis = sum(1 for n, L in dup.items() if len({r.get("cnf_sha256") for _, r in L}) > 1)
    pf = [(n, L) for n, L in dup.items() if sum(1 for _, r in L if r.get("proof_sha256")) > 1]
    pf_same = sum(1 for n, L in pf if len({r["proof_sha256"] for _, r in L if r.get("proof_sha256")}) == 1)
    print("(d) nodes with >1 certified record:", len(dup), "; cnf sha disagreements:", cnf_dis,
          "; nodes with >=2 proof hashes:", len(pf), "of which all identical:", pf_same)

    # (e) per-lane coverage of the cut by C3SPOT
    spot = {json.loads(l)["node"] for l in open(os.path.join(R, "C3SPOT/out.jsonl")) if l.strip()}
    lane_cut = collections.Counter()
    lane_spot = collections.Counter()
    for n in cut:
        lanes = {f for f, _ in cert[n]}
        for f in lanes:
            lane_cut[f] += 1
            if n in spot:
                lane_spot[f] += 1
    zero = [(f, c) for f, c in lane_cut.items() if lane_spot[f] == 0]
    print("(e) record files contributing to the cut:", len(lane_cut), "; with 0 re-solved cut pieces:", len(zero),
          "holding", sum(c for _, c in zero), "cut pieces")
    for f, c in sorted(zero, key=lambda x: -x[1])[:15]:
        print("     ", f, c)
    # (f) code-path signatures of cut records
    sig = collections.Counter()
    for n in cut:
        f, r = cert[n][0]
        keys = tuple(sorted(k for k in r.keys() if k in ("cube", "cap", "cadical_opts", "cadical_args", "proof_sha256", "base_sha256")))
        sig[keys] += 1
    print("(f) field signatures of the first certified record of each cut piece:")
    for k, v in sig.most_common():
        print("     ", v, k)


if __name__ == "__main__":
    main()
