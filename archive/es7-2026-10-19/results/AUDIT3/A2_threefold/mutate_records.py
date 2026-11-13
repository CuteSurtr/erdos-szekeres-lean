#!/usr/bin/env python3
"""A2 audit: tampering tests for a2compose.py.  Picks cut nodes certified by exactly one record and
writes mutated copies of the record files (only the chosen line changed) plus file lists:
  drop   - the record removed
  sha    - its cnf_sha256 changed in the last hex digit
  cake   - its cake_lpr string changed to 's VERIFIED UNSAT ' (trailing space)
  units  - its node renamed to a sibling's name (keeping the old cnf_sha256)
usage: mutate_records.py RESULTS_DIR FILELIST REPORT.json OUTDIR SEED"""
import json, os, random, sys
rdir, flist, rep, out, seed = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
files = [l.strip() for l in open(flist) if l.strip()]
cut = json.load(open(rep))["cut"]
where = {}
for f in files:
    for i, l in enumerate(open(os.path.join(rdir, f))):
        l = l.strip()
        if not l:
            continue
        r = json.loads(l)
        if r.get("certified") is True and "node" in r and "cube" not in r:
            where.setdefault(r["node"], []).append((f, i))
rng = random.Random(seed)
cands = [n for n in cut if len(where.get(n, [])) == 1]
picks = rng.sample(cands, 3)
os.makedirs(out, exist_ok=True)
for n in picks:
    f, i = where[n][0]
    lines = open(os.path.join(rdir, f)).read().split("\n")
    for kind in ("drop", "sha", "cake", "units"):
        L = list(lines)
        r = json.loads(L[i])
        if kind == "drop":
            L[i] = ""
        elif kind == "sha":
            r["cnf_sha256"] = r["cnf_sha256"][:-1] + ("0" if r["cnf_sha256"][-1] != "0" else "1"); L[i] = json.dumps(r)
        elif kind == "cake":
            r["cake_lpr"] = "s VERIFIED UNSAT "; L[i] = json.dumps(r)
        else:
            parts = r["node"].split("_")
            last = parts[-1]
            # rename to another node with the same unit count: swap the sigma of a two-orbit layer, or move a one-orbit layer
            if "s" in last and "-" in last:
                a, b = last.split("-")
                b2 = b[:-1] + ("1" if b[-1] == "0" else "0")
                parts[-1] = a + "-" + b2
            else:
                parts[-1] = str((int(last) % 10) + 1) if str((int(last) % 10) + 1) not in r["node"] else last
            r["node"] = "_".join(parts); L[i] = json.dumps(r)
        mf = os.path.join(out, f"{kind}_{n.replace('/', '_')}.jsonl")
        open(mf, "w").write("\n".join(L))
        fl = os.path.join(out, f"{kind}_{n.replace('/', '_')}.files")
        open(fl, "w").write("\n".join((mf if g == f else g) for g in files) + "\n")
        print(kind, n, fl)
