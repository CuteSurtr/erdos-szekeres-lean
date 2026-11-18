"""Exact fixed-coordinate analysis; no imports from prior geometry tools."""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
from itertools import combinations as C
import json
import os
from pathlib import Path
import resource
import shutil
import time


def dump(path,obj):
    with path.open('x') as f:
        json.dump(obj,f,indent=2,sort_keys=True);f.write('\n')
        f.flush();os.fsync(f.fileno())
        os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)


def det(p,a,b,c):
    return (p[b][0]-p[a][0])*(p[c][1]-p[a][1])-(p[c][0]-p[a][0])*(p[b][1]-p[a][1])


def convex(p,ids):
    chains=[]
    for order in (ids,ids[::-1]):
        chain=[]
        for v in order:
            while len(chain)>1 and det(p,chain[-2],chain[-1],v)<=0:chain.pop()
            chain.append(v)
        chains.append(chain)
    return len(chains[0])+len(chains[1])-2==len(ids)


def geometry(p):
    m=len(p);ids=range(m)
    assert m==15 and all(type(z)is int for pt in p for z in pt)
    assert all(p[i][0]<p[i+1][0] for i in range(m-1))
    determinants=[det(p,*t) for t in C(ids,3)];assert all(determinants)
    signs=''.join('+' if d>0 else '-' for d in determinants)
    caps={k:[list(s) for s in C(ids,k) if all(det(p,*t)<0 for t in C(s,3))] for k in (3,4,5)}
    polygons={k:[list(s) for s in C(ids,k) if convex(p,s)] for k in (6,7)}
    assert not caps[5] and not polygons[7]
    return {'m':m,'n':7,'signs':signs,'minimum_absolute_determinant':min(map(abs,determinants)),
            'caps3':caps[3],'caps4':caps[4],'caps5':caps[5],
            'targets':polygons[6],'ngons':polygons[7]}


def cup(p,q,r):
    b,c=q;u,v=r
    return q==r or (u>=b and v>=c and all(det(p,*t)>0 for t in C(sorted(set(q+r)),3)))


def forced(p,q,r):
    b,c=q;u,v=r
    return v>=c and (v==c or det(p,b,c,v)>0) and (u<=b or det(p,b,u,v)>0) and (u>=b or det(p,u,b,c)<0)


def line(p,pair):
    a,b=pair;s=Q(p[b][1]-p[a][1],p[b][0]-p[a][0])
    return s,Q(p[a][1])+s*(p[-1][0]-p[a][0])


def exposure(q,ambient):
    low=Q(0);high=None;lower=upper=None
    s,z=q
    for pair,(u,w) in ambient.items():
        ds,dz=s-u,z-w
        if ds<=0 and dz<=0:return {'safe':True,'supports':[(pair,Q(1))]}
        if ds>0:
            bound=-dz/ds
            if bound>low:low,lower=bound,pair
        elif ds<0:
            bound=-dz/ds
            if high is None or bound<high:high,upper=bound,pair
    if high is not None and low>=high:
        assert lower is not None and upper is not None
        u,w=ambient[lower];v,h=ambient[upper]
        weight=(v-s)/(v-u)
        assert 0<weight<1 and weight*w+(1-weight)*h>=z
        return {'safe':True,'supports':[(lower,weight),(upper,1-weight)]}
    t=low+1 if high is None else (low+high)/2
    assert t>0 and all(s*t+z>u*t+w for u,w in ambient.values())
    return {'safe':False,'exposure_interval':[str(low),None if high is None else str(high)],'witness_t':str(t)}


def mask(s):return sum(1<<v for v in s)
def verts(a,m=15):return [v for v in range(m) if a>>v&1]
def describe(masks):
    minimum=min((a.bit_count() for a in masks),default=None)
    mins=[a for a in masks if a.bit_count()==minimum]
    return {'count':len(masks),'minimum':minimum,'size_counts':dict(sorted(Counter(a.bit_count() for a in masks).items())),
            'minimum_count':len(mins),'minimum_masks':mins,'one_minimum':min(mins) if mins else None}


def inspect_case(name,p,g,out):
    out.mkdir();dump(out/'geometry.json',g)
    cap_for={}
    for c in g['caps4']:cap_for.setdefault(tuple(c[-2:]),c)
    ambient={pair:line(p,pair) for pair in cap_for}
    covered={key:[] for key in ('terminal','cup','forced','uniform')}
    rows=[];by_pair={}
    for pair in C(range(15),2):
        q=line(p,pair);state=exposure(q,ambient)
        terminal=pair in ambient;cs=[r for r in ambient if cup(p,pair,r)];fs=[r for r in ambient if forced(p,pair,r)]
        flags={'terminal':terminal,'cup':bool(cs),'forced':bool(fs),'uniform':state['safe']}
        assert not flags['cup'] or flags['forced']
        assert not flags['forced'] or flags['uniform']
        row={'pair':list(pair),'cap_triples':[t for t in g['caps3'] if t[-2:]==list(pair)],
             'query_line':{'slope':str(q[0]),'height_at_max_x':str(q[1])},'protected':flags,
             'cup_support_pairs':cs,'forced_support_pairs':fs,'safe':state['safe']}
        if state['safe']:
            ss=hh=Q(0);supports=[]
            for r,w in state['supports']:
                u,h=ambient[r];ss+=w*u;hh+=w*h
                supports.append({'fourcap':cap_for[r],'tail_pair':r,'weight':str(w),'slope':str(u),'height_at_max_x':str(h)})
            row.update(supports=supports,slope_difference=str(ss-q[0]),height_difference=str(hh-q[1]))
            assert ss>=q[0] and hh>=q[1]
        else:row.update({k:v for k,v in state.items() if k!='safe'})
        rows.append(row);by_pair[pair]=row
        for key,value in flags.items():
            if value:covered[key].append(pair)
    bad={key:[t for t in g['caps3'] if not by_pair[tuple(t[-2:])]['protected'][key]] for key in covered}
    c4=[mask(c) for c in g['caps4']];targets=[mask(t) for t in g['targets']]
    weak=[a for a in range(1<<15) if all(a&c!=c for c in c4) and all(a&t for t in targets)]
    family={'weak':weak}
    for key,triples in bad.items():
        blockers=[mask(t) for t in triples]
        family[key]=[a for a in weak if all(a&t!=t for t in blockers)]
    description={k:describe(v) for k,v in family.items()}
    dump(out/'memberships.json',family);dump(out/'pairs.json',{'max_x':p[-1][0],'ambient_fourcaps':list(cap_for.values()),'pairs':rows})
    dump(out/'bad_triples.json',bad)
    witness=None
    if family['uniform']:
        a=description['uniform']['one_minimum'];A=verts(a)
        witness={'name':name,'n':7,'P':p,'A':A,'mask':a,'certificates':[
            {'triple':t,'line_certificate':by_pair[tuple(t[-2:])]} for t in g['caps3'] if mask(t)&a==mask(t)]}
        dump(out/'positive.json',witness)
        with (out/'model.txt').open('x') as f:f.write('v '+' '.join(str(i+1 if a>>i&1 else -i-1) for i in range(15))+' 0\n')
    with (out/'uniform.cnf').open('x') as f:
        f.write(f'p cnf 15 {len(g["caps4"])+len(g["targets"])+len(bad["uniform"])}\n')
        for family_,sgn in ((g['targets'],1),(g['caps4'],-1),(bad['uniform'],-1)):
            for row in family_:f.write(' '.join(str(sgn*(v+1)) for v in row)+' 0\n')
    report={'name':name,'label':'COMPUTED exact fixed-coordinate enumeration',
            'geometry':{k:len(g[k]) for k in ('caps3','caps4','caps5','targets','ngons')},
            'minimum_absolute_determinant':g['minimum_absolute_determinant'],'ambient_terminal_pairs':len(ambient),
            'covered_pairs':{k:len(v) for k,v in covered.items()},
            'covered_cap_terminal_pairs':{k:sum(bool(row['cap_triples']) and row['protected'][k] for row in rows) for k in covered},
            'cap_terminal_pairs':sum(bool(row['cap_triples']) for row in rows),'bad_triples':{k:len(v) for k,v in bad.items()},
            'families':description,'one_uniform_minimum':None if witness is None else witness['A'],
            'one_uniform_minimum_cap_triples':None if witness is None else [c['triple'] for c in witness['certificates']],
            'exposed_pairs':[row['pair'] for row in rows if not row['safe']],
            'exposed_cap_terminal_pairs':[row['pair'] for row in rows if not row['safe'] and row['cap_triples']]}
    dump(out/'report.json',report)
    return report,family,rows


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--original',type=Path,required=True);ap.add_argument('--balanced',type=Path,required=True)
    ap.add_argument('--parent-semantics',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    shutil.copy2(__file__,args.out/'analyze.py');inputs=args.out/'inputs';inputs.mkdir()
    manifest={};raws={}
    for name,path in [('original',args.original),('balanced',args.balanced),('parent_semantics',args.parent_semantics)]:
        raw=path.read_bytes();(inputs/(name+'.json')).write_bytes(raw);raws[name]=json.loads(raw)
        manifest[name]={'path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
    dump(args.out/'input_manifest.json',manifest)
    report=[];families={};pairrows={};reference=None
    for name in ('original','balanced'):
        raw=raws[name];g=geometry(raw['P']);assert g['signs']==raw['orientation_signs']
        if reference is None:reference=g['signs']
        assert reference==g['signs']
        r,f,rows=inspect_case(name,raw['P'],g,args.out/name);report.append(r);families[name]=f;pairrows[name]=rows
    a,b=map(set,(families['original']['uniform'],families['balanced']['uniform']))
    differences={'common_uniform_count':len(a&b),'original_only_uniform_masks':sorted(a-b),'balanced_only_uniform_masks':sorted(b-a),
                 'pair_safety_changes':[{'pair':x['pair'],'original_safe':x['safe'],'balanced_safe':y['safe']} for x,y in zip(pairrows['original'],pairrows['balanced']) if x['safe']!=y['safe']]}
    dump(args.out/'differences.json',differences)
    parent=raws['parent_semantics'];checks=[]
    for r in report:
        for key in ('caps4','caps5','targets','ngons'):assert r['geometry'][key]==parent[key]
        assert r['ambient_terminal_pairs']==parent['ambient_terminal_pairs']
        for key in ('terminal','cup','forced'):
            assert r['covered_pairs'][key]==parent['covered_pairs'][key] and r['bad_triples'][key]==parent['bad_triples'][key]
        for key in ('weak','terminal','cup','forced'):
            for field in ('count','minimum','one_minimum'):assert r['families'][key][field]==parent['families'][key][field]
            assert {str(k):v for k,v in r['families'][key]['size_counts'].items()}==parent['families'][key]['size_counts']
        checks.append({'name':r['name'],'parent_semantics_agreement':True})
    summary={'label':'COMPUTED exact finite comparison','cases':report,'differences':differences,'parent_comparisons':checks,
             'same_ordered_orientation_type':True,'seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'scope':'These two fixed realizations only. No coordinate search, general existence claim, or certified UNSAT claim.'}
    dump(args.out/'summary.json',summary)
    print(json.dumps({'cases':[{k:r[k] for k in ('name','covered_pairs','bad_triples','one_uniform_minimum')}|{'families':{k:{field:v[field] for field in ('count','minimum','minimum_count')} for k,v in r['families'].items()}} for r in report],
                      'differences':{k:v for k,v in differences.items() if not k.endswith('_masks')},'seconds':summary['seconds'],'peak_rss_kib':summary['peak_rss_kib']}))


if __name__=='__main__':main()
