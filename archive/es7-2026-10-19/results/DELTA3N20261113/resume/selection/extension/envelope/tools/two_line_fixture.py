"""Extract and directly verify a small real two-support necessity fixture."""
from fractions import Fraction as Q
from itertools import combinations as C
import argparse
import json
from pathlib import Path


def det(p,a,b,c):
    return (p[b][0]-p[a][0])*(p[c][1]-p[a][1])-(p[c][0]-p[a][0])*(p[b][1]-p[a][1])


def ell(p,pair):
    a,b=pair;s=Q(p[b][1]-p[a][1],p[b][0]-p[a][0])
    return s,p[b][1]+s*(p[-1][0]-p[b][0])


def hullsize(p,ids):
    count=0
    for order in (ids,tuple(reversed(ids))):
        h=[]
        for i in order:
            while len(h)>1 and det(p,h[-2],h[-1],i)<=0:h.pop()
            h.append(i)
        count+=len(h)-1
    return count


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    case=args.run/'cases'/'n8-i107';original=json.loads((case/'input.json').read_text())['P']
    cert=next(c for c in json.loads((case/'certificates.json').read_text()) if len(c['supports'])==2)
    ids=sorted(set(cert['triple']+[len(original)-1]+[v for item in cert['supports'] for v in item['fourcap']]))
    p=[original[i] for i in ids];translate={v:i for i,v in enumerate(ids)}
    triple=[translate[v] for v in cert['triple']]
    support=[{'fourcap':[translate[v] for v in item['fourcap']],'weight':item['weight']} for item in cert['supports']]
    assert all(p[i][0]<p[i+1][0] for i in range(len(p)-1)) and all(det(p,*t) for t in C(range(len(p)),3))
    assert det(p,*triple)<0 and not any(all(det(p,*t)<0 for t in C(c,3)) for c in C(range(len(p)),5))
    assert not any(hullsize(p,c)==8 for c in C(range(len(p)),8))
    c4=[c for c in C(range(len(p)),4) if all(det(p,*t)<0 for t in C(c,3))]
    q=ell(p,triple[-2:]);lines={c[-2:]:ell(p,c[-2:]) for c in c4}
    assert all(not(s>=q[0] and z>=q[1]) for s,z in lines.values())
    slope=height=weight=Q(0)
    for item in support:
        c=tuple(item['fourcap']);assert c in c4
        s,z=ell(p,c[-2:]);w=Q(item['weight']);assert 0<w<1
        item['line']=list(map(str,(s,z)));slope+=w*s;height+=w*z;weight+=w
    assert weight==1 and slope==q[0] and height>=q[1]
    out={'label':'COMPUTED exact geometric two-line necessity','P':p,'n':8,'m':len(p),'source_case':'n8-i107','source_original_indices':ids,'triple':triple,'line':list(map(str,q)),'supports':support,'height_margin':str(height-q[1]),'fourcaps':len(c4),'ambient_lines':len(lines),'no_fivecap':True,'no_eightgon':True,'no_single_line_dominates':True,'all_ambient_lines':[{'pair':list(pair),'line':list(map(str,line))} for pair,line in lines.items()],'scope':'This cap triple is uniformly dominated but no individual ambient four-cap terminal line dominates it; not a universal selection result.'}
    with args.out.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({k:out[k] for k in ('m','triple','fourcaps','ambient_lines','height_margin','no_single_line_dominates')}))
if __name__=='__main__':main()
