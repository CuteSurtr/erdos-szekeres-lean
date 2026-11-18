"""Exactly enumerate two fixed uniform families from one cached geometry."""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
from itertools import combinations as C
import json
from pathlib import Path
import resource
import shutil
import sys
import time

ENVELOPE=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ENVELOPE/'tools'))
from exact import build,certificate,determinant
from verify import maxima,replay
from search import dump,sha,release_cache


def mask(row):return sum(1<<i for i in row)
def vertices(a,m=15):return [i for i in range(m) if a>>i&1]
def distribution(masks):return dict(sorted(Counter(a.bit_count() for a in masks).items()))


def independent_pair_checks(p,g,states):
    """Use all ambient-line intersections, zero and the final slope."""
    def ell(pair):
        a,b=pair;s=Q(p[b][1]-p[a][1],p[b][0]-p[a][0]);return s,p[a][1]+s*(p[-1][0]-p[a][0])
    lines={tuple(c[-2:]):ell(c[-2:]) for c in g['caps4']}
    tests={Q(0)}
    for (s,z),(u,w) in C(lines.values(),2):
        if s!=u:
            t=(w-z)/(s-u)
            if t>0:tests.add(t)
    envelope={t:max(s*t+z for s,z in lines.values()) for t in tests} if lines else {}
    for pair,row in states.items():
        s,z=ell(pair)
        safe=bool(lines) and s<=max(u for u,w in lines.values()) and all(s*t+z<=height for t,height in envelope.items())
        assert safe==row['safe']
        if not safe:
            t=Q(row['witness_t']);assert t>0 and all(s*t+z>u*t+w for u,w in lines.values())
    return {'terminal_pairs_checked':len(states),'common_exact_tests':len(tests),'all_classifications_agree':True}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--original',type=Path,required=True);ap.add_argument('--balanced',type=Path,required=True);ap.add_argument('--cached-case',type=Path,required=True);ap.add_argument('--weak-witnesses',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False);(args.out/'source').mkdir();start=time.monotonic()
    shutil.copy2(Path(__file__),args.out/'source'/Path(__file__).name)
    for name in ('exact.py','verify.py','search.py'):shutil.copy2(ENVELOPE/'tools'/name,args.out/'source'/name)
    input_paths={'original':args.original,'balanced':args.balanced,'cached_geometry':args.cached_case/'geometry.json','cached_input':args.cached_case/'input.json','parent_weak_witnesses':args.weak_witnesses}
    dump(args.out/'input_manifest.json',{name:{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for name,p in input_paths.items()})
    original=json.loads(args.original.read_text());balanced=json.loads(args.balanced.read_text());g=json.loads(input_paths['cached_geometry'].read_text())
    assert json.loads(input_paths['cached_input'].read_text())['P']==original['P'] and g['m']==15 and g['n']==7
    shutil.copy2(input_paths['cached_geometry'],args.out/'geometry.json')
    caps=[mask(c) for c in g['caps4']];targets=[mask(h) for h in g['targets']]
    ordinary=[a for a in range(1<<15) if all(a&c!=c for c in caps) and all(a&h for h in targets)]
    assert len(ordinary)==4805
    ordinary3=[vertices(a) for a in ordinary if a.bit_count()==3]
    parent=json.loads(args.weak_witnesses.read_text())['ordinary_triples']
    assert len(ordinary3)==4 and sorted(ordinary3)==sorted(parent)
    assert all(t in g['caps3'] for t in ordinary3)
    dump(args.out/'ordinary_masks.json',ordinary)
    reference_signs=None;reports=[];survivors={};bad_sets={}
    for name,raw in [('original',original),('balanced',balanced)]:
        case=args.out/name;case.mkdir();dump(case/'coordinates.json',raw)
        p=raw['P'];assert len(p)==15 and all(type(x)is int for pt in p for x in pt)
        assert all(p[i][0]<p[i+1][0] for i in range(14))
        dets=[determinant(p,*t) for t in C(range(15),3)];assert all(dets)
        signs=''.join('+' if d>0 else '-' for d in dets)
        if reference_signs is None:reference_signs=signs
        assert signs==reference_signs==raw['orientation_signs']
        premise=maxima(p,range(15));assert premise['maxcap']<5 and premise['maxgon']<7
        envelope,states=build(p,g);dump(case/'exposure.json',envelope)
        comparison=independent_pair_checks(p,g,states)
        bad=[mask(t) for t in envelope['exposed_triples']]
        accepted=[a for a in ordinary if all(a&b!=b for b in bad)]
        survivors[name]=set(accepted);bad_sets[name]={tuple(t) for t in envelope['exposed_triples']}
        dump(case/'uniform_masks.json',accepted)
        minimum=min(a.bit_count() for a in accepted);min_masks=[a for a in accepted if a.bit_count()==minimum]
        minimum_rows=[]
        for a in min_masks:
            A=vertices(a);cert=certificate(p,g,states,A);checked=replay(p,7,A,cert)
            minimum_rows.append({'A':A,'mask':a,'certificates':cert,'geometric_replay':checked})
        dump(case/'minimum_witnesses.json',minimum_rows)
        triples=[]
        for A in ordinary3:
            pair=tuple(A[-2:]);s=states[pair]
            row={'A':A,'is_cap':determinant(p,*A)<0,'terminal_pair':pair,'uniform':s['safe']}
            if s['safe']:row['certificates']=certificate(p,g,states,A)
            else:row.update(exposure_interval=s['interval'],exposure_witness_t=s['witness_t'])
            triples.append(row)
        dump(case/'ordinary_size3.json',triples)
        cnf=case/'uniform.cnf'
        with cnf.open('x') as f:
            f.write(f'p cnf 15 {len(g["targets"])+len(g["caps4"])+len(bad)}\n')
            for family,sgn in ((g['targets'],1),(g['caps4'],-1),(envelope['exposed_triples'],-1)):
                for row in family:f.write(' '.join(str(sgn*(v+1)) for v in row)+' 0\n')
        report={'name':name,'P':p,'label':'COMPUTED exact finite enumeration','ordinary_count':len(ordinary),'ordinary_size_distribution':distribution(ordinary),'uniform_count':len(accepted),'uniform_size_distribution':distribution(accepted),'minimum_uniform_size':minimum,'minimum_uniform_count':len(min_masks),'minimum_uniform_As':[r['A'] for r in minimum_rows],'ordinary_size3':triples,'exposed_triple_count':len(bad),'exposed_pairs':[list(pair) for pair,s in states.items() if not s['safe']],'premises':premise,'minimum_absolute_determinant':min(map(abs,dets)),'signs_sha256':hashlib.sha256(signs.encode()).hexdigest(),'independent_pair_checks':comparison,'cnf_sha256':sha(cnf)}
        dump(case/'report.json',report);reports.append(report);release_cache(case)
    common=survivors['original']&survivors['balanced'];original_only=survivors['original']-survivors['balanced'];balanced_only=survivors['balanced']-survivors['original']
    differences={'common_uniform_count':len(common),'original_only_uniform_count':len(original_only),'balanced_only_uniform_count':len(balanced_only),'original_only_uniform_masks':sorted(original_only),'balanced_only_uniform_masks':sorted(balanced_only),'original_only_exposed_triples':sorted(bad_sets['original']-bad_sets['balanced']),'balanced_only_exposed_triples':sorted(bad_sets['balanced']-bad_sets['original'])}
    dump(args.out/'differences.json',differences)
    summary={'label':'COMPUTED exact fixed-realization comparison','same_ordered_orientation_type':True,'ordinary_count':len(ordinary),'ordinary_size_distribution':distribution(ordinary),'cases':reports,'differences':{k:v for k,v in differences.items() if not k.endswith('_masks')},'seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Exactly these two fixed coordinate sets; no coordinate search or claim that the uniform optimum/count is constant across their orientation cell.'}
    dump(args.out/'summary.json',summary);release_cache(args.out/'summary.json')
    print(json.dumps({'ordinary':len(ordinary),'cases':[{k:r[k] for k in ('name','uniform_count','minimum_uniform_size','minimum_uniform_count','exposed_triple_count')} for r in reports],'differences':summary['differences'],'seconds':summary['seconds'],'peak_rss_kib':summary['peak_rss_kib']}))
if __name__=='__main__':main()
