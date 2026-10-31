#!/usr/bin/env python3
"""Build the acceptance manifest for mirror sub-case (ii) wave results.

Reads every leaves.icnf under the given wave directories (results/WAVE1/Wxx/<dir>/leaves.icnf,
and any later waves), assigns each directory to one of the 450 hull cases, parses every line
strictly, and writes one record per distinct (case, leaf) with a global index.

A directory is assigned to a case in two independent ways, and both must agree when both exist:
  (a) a "case_sha256" field in its leaves.jsonl, matched against cnf_sha256 in cases.jsonl;
  (b) its name: the longest case name N such that the directory name is N, or N followed by a
      character other than a digit, and not by '-' plus a digit (so "U_L4-s1" is U_L4, while
      "U_L4-9.s0" is U_L4-9).
Leaves are compared as sets of literals; literals are stored sorted by (abs, sign).

usage: v3_manifest.py ROOT OUT_MANIFEST.jsonl OUT_CASES.jsonl WAVEDIR [WAVEDIR ...]
  ROOT     the cloud/es7-2026-10-19 directory of a checkout
  WAVEDIR  e.g. results/WAVE1 (relative to ROOT)
Exit status 0 only if no directory was rejected; problems are listed in OUT_CASES.jsonl.
"""
import sys, os, re, json, hashlib, collections

LINE = re.compile(rb"^a( -?[1-9][0-9]*)* 0\n$")


def case_of_dirname(d, names):
    best = None
    for n in names:
        if not d.startswith(n):
            continue
        rest = d[len(n):]
        if rest and (rest[0].isdigit() or (rest[0] == "-" and len(rest) > 1 and rest[1].isdigit())):
            continue
        if best is None or len(n) > len(best):
            best = n
    return best


def main():
    root, out_m, out_c, waves = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
    cases = [json.loads(l) for l in open(os.path.join(root, "results/Mii-S/cases.jsonl"))]
    assert len(cases) == 450, len(cases)
    by_name = {c["case"]: c for c in cases}
    by_sha = {c["cnf_sha256"]: c["case"] for c in cases}
    names = sorted(by_name)

    leaves = collections.defaultdict(dict)   # case -> frozenset(lits) -> sorted list of source paths
    dirs = collections.defaultdict(list)     # case -> list of dir records
    problems = []
    for w in waves:
        wroot = os.path.join(root, w)
        for vm in sorted(os.listdir(wroot)):
            vmdir = os.path.join(wroot, vm)
            if not os.path.isdir(vmdir):
                continue
            for d in sorted(os.listdir(vmdir)):
                p = os.path.join(vmdir, d)
                lf = os.path.join(p, "leaves.icnf")
                if not os.path.isfile(lf):
                    continue
                rel = os.path.relpath(p, root)
                by_dir = case_of_dirname(d, names)
                shas, shards = set(), set()
                jf = os.path.join(p, "leaves.jsonl")
                if os.path.isfile(jf):
                    for l in open(jf):
                        l = l.strip()
                        if not l.startswith("{"):
                            continue
                        try:
                            r = json.loads(l)
                        except ValueError:
                            continue
                        if "case_sha256" in r:
                            shas.add(r["case_sha256"])
                        if "shard" in r and "nshards" in r:
                            shards.add((r["shard"], r["nshards"]))
                by_jsonl = {by_sha.get(s, "UNKNOWN_SHA:" + s) for s in shas}
                if len(by_jsonl) > 1:
                    problems.append({"dir": rel, "problem": "several case_sha256 values", "values": sorted(by_jsonl)})
                    continue
                cj = next(iter(by_jsonl)) if by_jsonl else None
                if cj is not None and cj.startswith("UNKNOWN_SHA:"):
                    problems.append({"dir": rel, "problem": "case_sha256 not in cases.jsonl", "value": cj})
                    continue
                if cj is not None and by_dir is not None and cj != by_dir:
                    problems.append({"dir": rel, "problem": "name and case_sha256 disagree", "by_name": by_dir, "by_sha": cj})
                    continue
                case = cj or by_dir
                if case is None:
                    problems.append({"dir": rel, "problem": "cannot assign a case"})
                    continue
                raw = open(lf, "rb").read()
                if raw and not raw.endswith(b"\n"):
                    problems.append({"dir": rel, "problem": "leaves.icnf does not end with a newline"})
                    continue
                bad, n = 0, 0
                parsed = []
                for line in raw.splitlines(keepends=True):
                    if line.strip() == b"":
                        continue
                    if line.startswith(b"c"):
                        continue
                    if not LINE.match(line):
                        bad += 1
                        continue
                    lits = [int(t) for t in line.split()[1:-1]]
                    if len(set(lits)) != len(lits) or any(-x in lits for x in lits):
                        bad += 1
                        continue
                    parsed.append(lits)
                    n += 1
                if bad:
                    problems.append({"dir": rel, "problem": "malformed or contradictory lines", "count": bad})
                    continue
                for lits in parsed:
                    key = frozenset(lits)
                    leaves[case].setdefault(key, []).append(rel)
                dirs[case].append({"dir": rel, "lines": n, "shards": sorted(shards),
                                   "leaves_icnf_sha256": hashlib.sha256(raw).hexdigest()})

    idx = 0
    with open(out_m, "w") as f:
        for case in sorted(leaves):
            keys = sorted(leaves[case], key=lambda k: sorted(k, key=lambda x: (abs(x), x)))
            for k in keys:
                lits = sorted(k, key=lambda x: (abs(x), x))
                f.write(json.dumps({"idx": idx, "case": case, "lits": lits,
                                    "sources": sorted(set(leaves[case][k]))}) + "\n")
                idx += 1
    with open(out_c, "w") as f:
        for case in names:
            c = by_name[case]
            f.write(json.dumps({"case": case, "status": c["status"], "method": c.get("method"),
                                "nleaves": len(leaves.get(case, {})), "dirs": dirs.get(case, [])}) + "\n")
        for p in problems:
            f.write(json.dumps({"problem": p}) + "\n")
    print("leaves", idx, "cases with leaves", len(leaves), "problems", len(problems))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
