#!/usr/bin/env python3
"""Count which of the 2,304 facts of the central 34-point case split (8 covers and 8 x 287 reflection orbits of P1..P8)
have a re-solve on a hash-checked CNF accepted by both checkers.

A record counts if `certified` is true and its CNF hash matched (`cnf_matches_record` true, or `cnf_sha256` equal to
`cnf_sha256_expected` in the pilot re-solve). Unit names are mapped to orbits as in recount.py: subcase V of P_a and its
image under i -> (a - i) mod 17 form one orbit; `P<a>_cover` is the cover fact of P_a.
usage: closure_split.py [--until ISO_UTC] RECORDS.jsonl ...   (--until drops records finished later)"""
import collections, itertools, json, sys

args, until = sys.argv[1:], None
if args[:1] == ["--until"]:
    until, args = args[1], args[2:]
orbit = {}
for a in range(1, 9):
    case, inner = f"P{a}", [i for i in range(1, 17) if i != a]
    for k in (2, 3):
        for V in itertools.combinations(inner, k):
            W = sorted((a - i) % 17 for i in V)
            names = [f"{case}_" + "-".join(map(str, sorted(X))) for X in (V, W)]
            orbit[names[0]] = (case, min(names))
hit, skipped = collections.defaultdict(set), []
for path in args:
    for line in open(path):
        if not line.strip():
            continue
        r = json.loads(line)
        if until and r.get("finished", "") > until:
            continue
        matched = r.get("cnf_matches_record") or (r.get("cnf_sha256") and r.get("cnf_sha256") == r.get("cnf_sha256_expected"))
        if not (r.get("certified") and matched):
            continue
        u = r.get("unit", "")
        fact = (u.split("_")[0], "cover") if u.endswith("_cover") else orbit.get(u)
        if fact is None:
            skipped.append(u)
            continue
        hit[fact].add(path)
by_case = collections.Counter(c for c, k in hit if k != "cover")
covers = sorted(c for c, k in hit if k == "cover")
print(f"facts with a re-solve: {len(hit)} of 2304 ({100 * len(hit) / 2304:.1f}%)")
print("covers:", " ".join(covers))
print("orbits:", " ".join(f"{c} {n}" for c, n in sorted(by_case.items())), "total", sum(by_case.values()))
print("unit names not mapped:", skipped)
