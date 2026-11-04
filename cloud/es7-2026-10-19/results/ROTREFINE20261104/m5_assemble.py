#!/usr/bin/env python3
"""Append hash-bound verified fivefold cut families and explicitly named cube units."""
import argparse,hashlib,json,shutil
from pathlib import Path
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True)
    p.add_argument('--family',type=Path,action='append',default=[])
    p.add_argument('--cube',choices=('none','H1','d111111'),default='none')
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    meta=json.loads(a.base.with_name(a.base.name+'.json').read_text());assert meta['m']==5
    units=[]
    if a.cube!='none':units.append(meta['H']['1'])
    if a.cube=='d111111':units.extend(meta['Y'][s] for s in ('1,2','1,3','1,4','2,3','2,4','3,4'))
    families=[];count=0
    for f in a.family:
        m=json.loads(f.with_suffix(f.suffix+'.json').read_text())
        assert m['family_sha256']==sha(f) and m['target_layers']==meta['t']
        assert m['direct_exact56_clause_tests']>0 and m['complete_template_tests']['forbidden_matches']==0
        actual=0
        for line in f.read_text().splitlines():
            values=list(map(int,line.split()));assert values[-1]==0
            assert all(0<abs(l)<=meta['ntriple'] for l in values[:-1]);actual+=1
        assert actual==m['clauses'];count+=actual
        families.append({'file':f.name,'sha256':sha(f),'metadata_sha256':sha(f.with_suffix(f.suffix+'.json')),'clauses':actual})
    with a.base.open('rb') as inp,a.out.open('wb') as out:
        inp.readline();out.write(f"p cnf {meta['nv']} {meta['ncl']+count+len(units)}\n".encode())
        shutil.copyfileobj(inp,out)
        for f in a.family:
            with f.open('rb') as stream:shutil.copyfileobj(stream,out)
        for l in units:out.write(f'{l} 0\n'.encode())
    record={'base_sha256':sha(a.base),'base_metadata_sha256':sha(a.base.with_name(a.base.name+'.json')),
            'm':5,'layers':meta['t'],'cube':a.cube,'units':units,'families':families,
            'variables':meta['nv'],'clauses':meta['ncl']+count+len(units),'cnf_sha256':sha(a.out)}
    a.out.with_name(a.out.name+'.assembly.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record),flush=True)
if __name__=='__main__':main()
