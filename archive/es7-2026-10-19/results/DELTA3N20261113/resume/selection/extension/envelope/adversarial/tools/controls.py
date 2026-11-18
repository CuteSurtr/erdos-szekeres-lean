"""Direct full truth-table, strict-grid-bound and rational exposure controls."""
import argparse
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path
import random
from adversarial import Cell,ordinary_family


def exact_exposed(q,lines):
    low=Q(0);high=None
    a,b,c=q;qs,qz=Q(a,c),Q(b,c)
    for a,b,c in lines:
        ds=qs-Q(a,c);dz=qz-Q(b,c)
        if not ds:
            if dz<=0:return False
        elif ds>0:low=max(low,-dz/ds)
        else:high=-dz/ds if high is None else min(high,-dz/ds)
    return high is None or low<high


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    p=json.loads((args.run/'baseline'/'input.json').read_text())['P'];g=json.loads((args.run/'baseline'/'geometry.json').read_text())
    masks=ordinary_family(g,len(p));caps=[sum(1<<v for v in row) for row in g['caps4']];targets=[sum(1<<v for v in row) for row in g['targets']]
    direct=[A for A in range(1<<len(p)) if all(A&C!=C for C in caps) and all(A&H for H in targets)]
    assert masks==direct and len(masks)==8149
    cell=Cell(p,g,masks,16*max(abs(y) for x,y in p));y=[z for x,z in p];score=cell.score(y);assert score[0]==4057
    assert len(cell.direct_survivors(y,score))==4057
    boundary_checks=[]
    for v in range(len(p)):
        lo,hi=cell.bounds(y,v)
        for endpoint in (lo,hi):
            z=y[:];z[v]=endpoint;assert cell.valid(z);cell.check(z,cell.score(z))
        if lo>-cell.box:
            z=y[:];z[v]=lo-1;assert not cell.valid(z)
        if hi<cell.box:
            z=y[:];z[v]=hi+1;assert not cell.valid(z)
        boundary_checks.append({'vertex':v,'low':lo,'high':hi})
    rng=random.Random(2026111409)
    for _ in range(1000):
        q=(rng.randrange(-20,21),rng.randrange(-20,21),rng.randrange(1,10))
        lines=[(rng.randrange(-20,21),rng.randrange(-20,21),rng.randrange(1,10)) for _ in range(rng.randrange(0,9))]
        assert Cell.exposed(q,lines)==exact_exposed(q,lines)
    out={'label':'COMPUTED exact controls','all_passed':True,'truth_table_assignments':1<<len(p),'ordinary_delta_count':len(masks),'uniform_baseline':score[0],'strict_boundary_checks':boundary_checks,'random_rational_line_families':1000}
    with args.out.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({k:out[k] for k in ('all_passed','truth_table_assignments','ordinary_delta_count','uniform_baseline','random_rational_line_families')}))
if __name__=='__main__':main()
