#!/usr/bin/env python3
"""print the RESULTS.md table from records.jsonl"""
import json, sys
print("| node | depth | method | closed | certified/unsat/subproblems | wall s | solve s (sum) | check s (sum) | largest sub s | notes |")
print("|---|---|---|---|---|---|---|---|---|---|")
for l in open(sys.argv[1]):
    r = json.loads(l)
    note = []
    if "cubes" in r: note.append(f"march {r['march_s']} s, {r['cubes']} cubes")
    if r["method"] == "ref": note.append(f"splits {r.get('splits', 0)}; wall includes checks")
    if r["method"] == "opt": note.append("4 option sets in parallel; closed if any one certified")
    if r["sat"]: note.append("SAT " + ",".join(r["sat"]))
    print(f"| `{r['node']}` | {r['depth']} | {r['method']} | {'yes' if r['closed'] else 'no'} | {r['certified']}/{r['unsat']}/{r['subproblems']} | "
          f"{r['wall_s']} | {r['solve_s_total']} | {r['check_s_total']} | {r['max_sub_s']} | {'; '.join(note)} |")
