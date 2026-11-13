"""Check that pb_lrat.py's CNF equals pbcnf5.build's CNF (the self-tested encoder) for a rows file."""
import json, sys, hashlib
import etv_common as ec
from pbcnf5 import build, selftest
selftest()
rows = json.load(open(sys.argv[1])); B = int(sys.argv[2])
top, cls = build(rows, B, ec.N, ec.FIXED_OCC)
txt = f'p cnf {top} {len(cls)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in cls)
print(hashlib.sha256(txt.encode()).hexdigest())
