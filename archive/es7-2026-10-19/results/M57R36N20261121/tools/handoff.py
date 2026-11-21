#!/usr/bin/env python3
"""handoff.py -- move queued jobs of drive.py (cubes/, case A) and drive_b.py (cubes_b/, case B) to drive2.py.

Only jobs with status 'queued' are taken; those drivers can no longer start them (cubes/LANES = 0, NOSTART
files, and drive_b.py is past its start cutoff).  A job id is handed over once (cubes2/handed.json).  B jobs
first, then A jobs, each in the old driver's list order.
"""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
C2 = D + '/cubes2'
os.makedirs(C2, exist_ok=True)
hp = C2 + '/handed.json'
handed = set(json.load(open(hp))) if os.path.exists(hp) else set()
new = []
for sub, case in (('cubes_b', 'B'), ('cubes', 'A')):
    st = json.load(open(os.path.join(D, sub, 'state.json')))
    for j in st['jobs']:
        if j['case'] == case and j['status'] == 'queued' and j['id'] not in handed:
            new.append({'id': j['id'], 'case': case, 'units': j['units'], 'depth': j.get('depth', len(j['units'])), 'from': sub})
inbox = C2 + '/inbox.json'
old = json.load(open(inbox)) if os.path.exists(inbox) else []
ids = {j['id'] for j in old}
old += [j for j in new if j['id'] not in ids]
json.dump(old, open(inbox + '.tmp', 'w'))
os.replace(inbox + '.tmp', inbox)
handed |= {j['id'] for j in new}
json.dump(sorted(handed), open(hp, 'w'))
print('handed over', len(new), 'jobs:', sum(j['case'] == 'B' for j in new), 'B,', sum(j['case'] == 'A' for j in new), 'A')
