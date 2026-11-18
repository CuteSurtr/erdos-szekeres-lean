import json, sys, os
for d in sys.argv[1:]:
    fn = os.path.join(d, 'results.jsonl')
    if not os.path.exists(fn): continue
    rows = [json.loads(l) for l in open(fn)]
    for r in rows:
        print('%-7s a=%d n=%d m=%2d %-6s b=%d %-7s cl=%-7d cad=%7.1fs lrat=%-11s cake=%-16s %6ss %s' % (d, r['a'], r['n'], r['m'], r['form'], r['b'], r['status'], r['clauses'], r['cadical_s'], r.get('lrat_bytes', '-'), r.get('cake_lpr', '-')[:16], r.get('cake_s', '-'), r.get('verdict', '')))
