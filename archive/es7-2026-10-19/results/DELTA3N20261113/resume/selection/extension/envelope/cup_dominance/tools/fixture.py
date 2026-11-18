"""Retain both uniform and cup-protected membership tests for a new fixture."""
import argparse
import json
from pathlib import Path
import shutil
from probe import E,probe
from search import dump,sha,run_case,release_cache


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--binary',type=Path,required=True);ap.add_argument('--n',type=int,required=True);ap.add_argument('--name',required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False);(args.out/'source').mkdir()
    for f in Path(__file__).parent.iterdir():
        if f.is_file():shutil.copy2(f,args.out/'source'/f.name)
    for name in ('exact.py','search.py','verify.py'):shutil.copy2(E/'tools'/name,args.out/'source'/name)
    shutil.copy2(args.input,args.out/'source_input.json')
    original=json.loads(args.input.read_text());r={'name':args.name,'n':args.n,'P':original['P'],'source':str(args.input),'source_sha256':sha(args.input)}
    uniform=run_case(r,args.out/'uniform',args.binary)
    if uniform['outcome']=='UNSAT_UNCERTIFIED_FROZEN':
        dump(args.out/'FROZEN_UNIFORM_NEGATIVE.json',uniform)
        summary={'label':'COMPUTED','uniform':uniform,'cup':'not run after uniform negative'}
    elif uniform['outcome']=='SAT_EXACT_MODEL_CHECKED':
        cup=probe(r,args.out/'cup',args.binary,args.out/'uniform'/'geometry.json')
        if cup['outcome']=='UNSAT_UNCERTIFIED_FROZEN':dump(args.out/'FROZEN_CUP_NEGATIVE.json',cup)
        summary={'label':'COMPUTED','uniform':uniform,'cup':cup}
    else:summary={'label':'COMPUTED','uniform':uniform,'cup':'not run after failed/unknown uniform test'}
    dump(args.out/'summary.json',summary);release_cache(args.out/'summary.json')
    print(json.dumps({k:({'outcome':v['outcome'],'A':v.get('A')} if isinstance(v,dict) else v) for k,v in summary.items()}))
if __name__=='__main__':main()
