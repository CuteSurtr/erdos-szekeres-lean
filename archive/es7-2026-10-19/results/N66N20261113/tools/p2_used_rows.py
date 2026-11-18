"""Phase 2: rows whose clauses survive trimming.  usage: p2_used_rows.py <certdir>
reads layout.json (row clause range, row list in clause order) and used_ids.txt (original clause ids kept by
p2_lrat_trim); writes used_rows.json ([[support, 1], ...]) and used_summary.json (kept clauses per family)."""
import sys, json, os
od = sys.argv[1]
lay = json.load(open(os.path.join(od, 'layout.json')))
used = [int(x) for x in open(os.path.join(od, 'used_ids.txt'))]
r0, r1 = lay['rows']; rows = lay['row_list']
ur = [rows[i - r0] for i in used if r0 <= i <= r1]
json.dump([[s, 1] for s in ur], open(os.path.join(od, 'used_rows.json'), 'w'))
fam = {k: sum(1 for i in used if lay[k][0] <= i <= lay[k][1]) for k in ('eager', 'quad', 'units', 'rows', 'card', 'sb') if k in lay}
summ = {'used_original_clauses': len(used), 'per_family': fam, 'used_rows': len(ur)}
json.dump(summ, open(os.path.join(od, 'used_summary.json'), 'w')); print(json.dumps(summ))
