"""Dump every current row (cycle, block, coupled) as [[support, demand], ...] via rowsio."""
import json, sys, rowsio
rows = rowsio.load_all()
json.dump([[list(s), d] for s, (d, k) in rows.items()], open(sys.argv[1], 'w'))
import collections; print(len(rows), collections.Counter(k for d, k in rows.values()))
