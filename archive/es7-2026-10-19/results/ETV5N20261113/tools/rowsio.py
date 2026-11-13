"""Row files of this run: rows_cycle.json (cycle rows), rows_block.json (Baek block rows), cores.jsonl and
trows.jsonl (coupled demand-one rows).  load_all() -> {support tuple: (demand, kind)}."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
def load_all(here=HERE):
    rows = {}
    def put(s, d, kind):
        s = tuple(sorted(s))
        if s not in rows or rows[s][0] < d: rows[s] = (d, kind)
    p = os.path.join(here, 'rows_cycle.json')
    if os.path.exists(p):
        for s, d in json.load(open(p)): put(s, d, 'cycle')
    p = os.path.join(here, 'rows_block.json')
    if os.path.exists(p):
        for s, d in json.load(open(p)): put(s, d, 'block')
    for fn in ('cores.jsonl', 'trows.jsonl'):
        p = os.path.join(here, fn)
        if os.path.exists(p):
            for line in open(p): put(json.loads(line)['support'], 1, 'coupled')
    return rows
