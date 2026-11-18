"""No search imports: replay all moves' geometry and sampled exact scores."""
import argparse
from fractions import Fraction as Q
from itertools import combinations as C
import json
import os
from pathlib import Path
import time


def det(x,y,t):
    a,b,c=t
    return x[a]*(y[b]-y[c])+x[b]*(y[c]-y[a])+x[c]*(y[a]-y[b])


def exposure_pair(x,y,pair,ambient):
    def line(pair):
        a,b=pair;s=Q(y[b]-y[a],x[b]-x[a]);return s,y[a]+s*(x[-1]-x[a])
    s,z=line(pair);lower=Q(0);upper=None
    for other in ambient:
        u,w=line(other);slope=s-u;height=z-w
        if slope==0:
            if height<=0:return False
        elif slope>0:lower=max(lower,-height/slope)
        else:upper=-height/slope if upper is None else min(upper,-height/slope)
    return upper is None or lower<upper


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--sample-every',type=int,default=257)
    args=ap.parse_args();start=time.monotonic()
    base=json.loads((args.run/'baseline'/'input.json').read_text())['P'];x=[p[0] for p in base];original_y=[p[1] for p in base];m=len(x)
    triples=list(C(range(m),3));signs={t:1 if det(x,original_y,t)>0 else -1 for t in triples}
    caps3=[t for t in triples if signs[t]<0]
    caps4=[s for s in C(range(m),4) if all(signs[t]<0 for t in C(s,3))]
    ambient=sorted({c[-2:] for c in caps4});pairs=sorted({c[-2:] for c in caps3}-set(ambient))
    fam=json.loads((args.run/'family.json').read_text());masks=fam['masks'];assert len(masks)==8149
    y=None;moves=restarts=orientation_tests=0;checks=[]
    def check_score(y,expected,where):
        exposed={pair for pair in pairs if exposure_pair(x,y,pair,ambient)}
        bad=[sum(1<<i for i in t) for t in caps3 if t[-2:] in exposed]
        count=sum(all(mask&b!=b for b in bad) for mask in masks)
        assert count==expected
        checks.append({'where':where,'score':count,'exposed_pairs':sorted(exposed)})
    with (args.run/'trajectory.jsonl').open() as f:
        for line in f:
            row=json.loads(line)
            if row['type']=='restart':
                y=row['y'];assert all(det(x,y,t)*signs[t]>0 for t in triples);orientation_tests+=len(triples);restarts+=1
            elif row['type']=='move':
                assert y is not None
                v=row['vertex'];assert y[v]==row['old_y'];y[v]=row['new_y']
                # Every unaffected determinant is identical to the previous
                # valid state, so affected triples suffice for full replay.
                affected=[t for t in triples if v in t]
                assert all(det(x,y,t)*signs[t]>0 for t in affected);orientation_tests+=len(affected);moves+=1
                if moves%args.sample_every==0:check_score(y,row['survivors'],{'move':moves})
            elif row['type']=='best':
                p=row['P'];assert [a for a,b in p]==x
                check_score([b for a,b in p],row['survivors'],{'best':row['name']})
            elif row['type']=='restart_end':
                assert y is not None
            else:raise ValueError(row['type'])
        os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
    summary=json.loads((args.run/'summary.json').read_text())
    assert moves==summary['accepted_moves'] and restarts==summary['restarts_completed']
    out={'label':'COMPUTED separate within-track trajectory replay','verdict':'PASS','all_accepted_moves_geometry_checked':moves,'restart_geometries_checked':restarts,'exact_orientation_tests':orientation_tests,'score_samples_checked':len(checks),'score_checks':checks,'seconds':time.monotonic()-start,'scope':'Every accepted move preserves all orientations by affected-triple replay; independently recomputed scores only at the retained bests and the listed samples, not every proposal.'}
    with args.out.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({k:out[k] for k in ('verdict','all_accepted_moves_geometry_checked','restart_geometries_checked','exact_orientation_tests','score_samples_checked','seconds')}))
if __name__=='__main__':main()
