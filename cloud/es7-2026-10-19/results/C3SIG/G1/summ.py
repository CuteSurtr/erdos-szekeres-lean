import json, sys, statistics
nodes = [l.rstrip("\n").split("\t") for l in open("/opt/work/nodes.tsv")]
recs = [json.loads(l) for l in open("/opt/work/out.jsonl")]
rows = []; ratios = []; tot = {3: [0, 0], 6: [0, 0]}
print("| row | node | K | cubes run | certified | open (UNKNOWN) | not run | solve s | check s | max cube s | σ cost s | recorded_core_s | ratio |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for row, node, strat, core in nodes:
    core = float(core); cost_all = 0; closed = False
    for K in (3, 6):
        rs = [r for r in recs if r["node"] == node and len(r["cube"]) == K]
        if not rs: continue
        cert = sum(1 for r in rs if r.get("certified")); unk = sum(1 for r in rs if r["status"] == "UNKNOWN")
        bad = [r for r in rs if r["status"] not in ("UNKNOWN", "UNSATISFIABLE") or (r["status"] == "UNSATISFIABLE" and not r.get("certified"))]
        sv = sum(r["solve_s"] for r in rs); ck = sum(r.get("check_s", 0) for r in rs)
        mx = max(r["solve_s"] + r.get("check_s", 0) for r in rs)
        cost_all += sv + ck
        tot[K][0] += unk + (2**K - len(rs)); tot[K][1] += 2**K
        if cert == 2**K: closed = True
        ratio = f"{(sv+ck)/core:.3f}" if cert == 2**K else "–"
        if cert == 2**K: ratios.append((sv + ck) / core)
        print(f"| {row} | {node} | {K} | {len(rs)} | {cert} | {unk} | {2**K-len(rs)} | {sv:.1f} | {ck:.1f} | {mx:.1f} | {sv+ck:.1f} | {core} | {ratio} |" + (f" BAD {bad}" if bad else ""))
print()
print("closed-node ratios (sigma cost of the closing K / recorded_core_s):", [round(x, 3) for x in ratios], "median", round(statistics.median(ratios), 3) if ratios else None)
for K in (3, 6):
    if tot[K][1]: print(f"K={K}: open-or-unrun cubes {tot[K][0]} of {tot[K][1]} = {tot[K][0]/tot[K][1]:.1%}")
