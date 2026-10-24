# Compare cover.py obligation CNFs with an independent construction from the soundness note.
import sys, subprocess, os; sys.path.insert(0,'/opt/audit'); import mycube as M
from itertools import combinations
S='/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/Mii-S/scripts'
F='/opt/work/F/m33k7int.sub.cnf'; NC=515121
UPS=[()]+[(a,) for a in range(2,17)]+list(combinations(range(2,17),2))
CASES=M.cases()
assert len(UPS)==121 and len(CASES)==450 and len(set(CASES))==450
# every case appears in the obligation of its own U, and UPS covers every case's U
assert all(tuple(sorted(U)) in UPS for U,L in CASES)
from collections import Counter
cnt=Counter(U for U,L in CASES); print("cases per |U|:", Counter(len(U) for U,L in CASES), "obligations with 0 cases:", [U for U in UPS if cnt[U]==0])
obs=['root']+['up:'+','.join(map(str,U)) for U in UPS]
listed=subprocess.run(['python3',S+'/cover.py','list'],capture_output=True,text=True).stdout.split()
assert listed==obs, "obligation list differs"
tmp='/opt/work/ob.cnf'; bad=0
for ob in obs:
    subprocess.run(['python3',S+'/cover.py','cnf',F,ob,tmp],check=True)
    with open(tmp) as f:
        hdr=f.readline().split(); lines=f.read().split('\n')
    if lines[-1]=='': lines.pop()
    tail=[frozenset(map(int,l.split()[:-1])) for l in lines[NC:]]
    assert all(l.split()[-1]=='0' for l in lines[NC:])
    if ob=='root': exp=[frozenset(-x for x in M.UP(U)) for U in UPS]
    else:
        U=tuple(int(x) for x in ob[3:].split(',') if x)
        exp=[frozenset([x]) for x in M.UP(U)]+[frozenset(-x for x in M.cube(U2,L)) for U2,L in CASES if U2==U]
    ok = int(hdr[2])==47002 and int(hdr[3])==len(lines) and Counter(tail)==Counter(exp)
    if not ok: bad+=1; print("BAD", ob, hdr, len(lines), len(tail), len(exp))
print("obligations checked:", len(obs), "bad:", bad)
