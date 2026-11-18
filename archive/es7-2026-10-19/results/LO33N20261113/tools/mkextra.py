"""Write the extra-row file (certified coupled rows + the two capacity rows) for a pair (c, c2).
Usage: mkextra.py c c2 out.json"""
import json, sys, hashlib
from lo_common import *
c, c2, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
rows = extra_rows(c, c2)
json.dump(rows, open(out, 'w'))
print(out, len(rows), 'rows; cap rows', [(len(r['support']), r['rhs']) for r in rows if r['rhs'] != 1],
      hashlib.sha256(open(out, 'rb').read()).hexdigest())
