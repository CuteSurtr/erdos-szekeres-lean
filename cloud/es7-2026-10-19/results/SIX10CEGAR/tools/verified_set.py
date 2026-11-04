#!/usr/bin/env python3
"""verified_set.py AUDIT.tsv RECERT.tsv[,RECERT2.tsv] OUT.clauses : the cuts re-verified now (audit: full or sound; recert: any
exact method), written in cuts.clauses order; prints the counts."""
import sys, collections
from pathlib import Path
W = Path(__file__).resolve().parent.parent
cuts = [l for l in (W / 'cuts.clauses').read_text().splitlines() if l.strip()]
ok = {}
for r in Path(sys.argv[1]).read_text().splitlines():
    i, st = r.split('\t')[:2]
    if st in ('full', 'sound'): ok[int(i)] = 'audit-' + st
for rp in sys.argv[2].split(','):   # one or more re-certification tables
    if Path(rp).exists():
        for r in Path(rp).read_text().splitlines():
            i, st = r.split('\t')[:2]
            if st != 'not re-certified' and int(i) not in ok: ok[int(i)] = 'recert'
Path(sys.argv[3]).write_text(''.join(cuts[i] + '\n' for i in sorted(ok)))
c = collections.Counter(ok.values())
print('cuts %d; re-verified %d (%s); not re-verified %d' % (len(cuts), len(ok), dict(c), len(cuts) - len(ok)))
