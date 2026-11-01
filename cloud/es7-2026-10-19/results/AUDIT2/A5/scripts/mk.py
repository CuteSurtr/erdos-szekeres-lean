# A5 independent CNF builder: F + case cube units + leaf units (one unit clause per literal)
import sys, hashlib, json
F = open('/opt/work/F.cnf','rb').read()
hdr, body = F.split(b'\n',1)
_, _, nv, nc = hdr.split()
nv, nc = int(nv), int(nc)
cubes = {}
_R='/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/Mii-S/'
cases = [json.loads(l) for l in open(_R+'cases.jsonl')]
icnf = [l.split() for l in open(_R+'cases.icnf') if l.startswith('a ')]
assert len(cases)==len(icnf)
for c,a in zip(cases,icnf):
    assert a[-1]=='0'; lits=[int(x) for x in a[1:-1]]
    assert len(lits)==c['nlits'], c['case']
    cubes[c['case']]=lits
def build(case, leaf, variant=0):
    units = cubes[case] + list(leaf)
    if variant==0:
        return b'p cnf %d %d\n' % (nv, nc+len(units)) + body + b''.join(b'%d 0\n'%u for u in units)
if __name__=='__main__':
    ok=bad=0
    for c in cases:
        h=hashlib.sha256(build(c['case'],[])).hexdigest()
        if h==c['cnf_sha256']: ok+=1
        else: bad+=1
    print('case cnf sha match',ok,'mismatch',bad)
