#!/usr/bin/env python3
"""Exact-checker regression and rejection tests; no solver dependency."""
import copy,gzip,importlib.util,json
from pathlib import Path
from conditional_check import replay
ROOT=Path(__file__).resolve().parents[2]
def load(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
old=load(ROOT/'experiments/omission-residual32-resume-2026-10-10/check.py','old_checker')
source=json.loads(gzip.decompress((ROOT/'experiments/omission-residual32-research-2026-10-10/source.json.gz').read_bytes()))
rows=[(r['support'],r['rhs']) for r in source['constraints']];n=len(source['states'])
passed=0
for node in [492357,29,485519,492355,485517,24]:
    proof=json.loads(gzip.decompress((ROOT/f'experiments/omission-residual32-resume-2026-10-10/closed-context-{node}.json.gz').read_bytes()))
    ctx={'missing':proof['missing'],'occupied':proof['occupied']}
    expected=old.replay(proof,rows,n,ctx);got=replay(proof,rows,n,ctx)
    assert got==dict(expected,pending=0,complete=True)
    passed+=1
base=proof;ctx={'missing':base['missing'],'occupied':base['occupied']}
def rejected(p):
    global passed
    try:replay(p,rows,n,ctx)
    except (ValueError,KeyError):passed+=1;return
    raise AssertionError('Accepted bad proof')
p=copy.deepcopy(base);p['missing']=[];rejected(p)
p=copy.deepcopy(base);p['hole_budget']=31;rejected(p)
p=copy.deepcopy(base);p['nodes'].append({'type':'pending'});rejected(p)
p=copy.deepcopy(base);p['nodes'][p['root']]={'type':'over_budget'};rejected(p)
p=copy.deepcopy(base);next(x for x in p['nodes'] if x['type']=='weighted')['weights']=[];rejected(p)
p=copy.deepcopy(base);q=next(x for x in p['nodes'] if x['type']=='branch');q['zero']=q['one'];rejected(p)
p=copy.deepcopy(base);q=next(x for x in p['nodes'] if x['type']=='branch');q['vertex']=p['missing'][0];rejected(p)
seed=json.loads((Path(__file__).parent/'seed.json').read_text());ctx={'missing':[54],'occupied':[43,67]}
assert replay(seed,rows,n,ctx,allow_pending=True)['pending']==1;passed+=1
rejected(seed)
from check_witness import check as witness_check
w=json.loads((Path(__file__).parent/'witness.json').read_text())
source_bytes=gzip.decompress((ROOT/'experiments/omission-residual32-research-2026-10-10/source.json.gz').read_bytes())
assert witness_check(source_bytes,w)['tight_rows']==588;passed+=1
def bad_witness(v,raw=source_bytes):
    global passed
    try:witness_check(raw,v)
    except ValueError:passed+=1;return
    raise AssertionError('Accepted bad witness')
v=copy.deepcopy(w);v['holes'][0]=v['holes'][1];bad_witness(v)
v=copy.deepcopy(w);v['holes'][0]=0;bad_witness(v)
v=copy.deepcopy(w);v['holes'].remove(54);v['holes'].append(6);bad_witness(v)
v=copy.deepcopy(w);v['source_uncompressed_sha256']='0'*64;bad_witness(v)
bad_witness(w,source_bytes+b' ')
v=copy.deepcopy(w);v['holes'][0]=6;bad_witness(v)
print(json.dumps({'passed':passed,'closed_certificates_crosschecked':6,'scope':'Exact Python checker tests, no Lean claim'}))
