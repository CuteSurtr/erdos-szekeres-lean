#!/usr/bin/env python3
"""Are two close_tree record files the same multiset of records, apart from timings (solve_s, check_s)
and base_sha256?  usage: same_records.py A.jsonl B.jsonl  -> one JSON line"""
import collections, json, sys
T = {"solve_s", "check_s", "base_sha256"}
k = lambda r: json.dumps({x: v for x, v in r.items() if x not in T}, sort_keys=True)
a, b = [collections.Counter(k(json.loads(l)) for l in open(p)) for p in sys.argv[1:3]]
print(json.dumps({"a": sys.argv[1].split("/")[-1], "b": "/".join(sys.argv[2].split("/")[-4:]), "records": [sum(a.values()), sum(b.values())],
                  "equal": a == b, "only_a": sum((a - b).values()), "only_b": sum((b - a).values())}))
