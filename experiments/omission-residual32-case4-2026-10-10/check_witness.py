#!/usr/bin/env python3
"""Check the fixed-catalog 32-hole witness using Python integer arithmetic only.

This checks a necessary-inequality relaxation, not geometric realizability.
"""
import argparse,collections,gzip,hashlib,json
from pathlib import Path
SOURCE_SHA='f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909'
def check(source_bytes,witness):
    if hashlib.sha256(source_bytes).hexdigest()!=SOURCE_SHA:raise ValueError('Source hash mismatch')
    source=json.loads(source_bytes);n=len(source['states']);rows=source['constraints']
    if n!=154 or len(rows)!=2469:raise ValueError('Source dimensions mismatch')
    if witness['source_uncompressed_sha256']!=SOURCE_SHA:raise ValueError('Witness source mismatch')
    holes=witness['holes']
    if not isinstance(holes,list) or len(holes)!=32 or len(set(holes))!=32:raise ValueError('Expected 32 distinct holes')
    if not all(type(i) is int and 0<=i<n for i in holes):raise ValueError('Invalid hole index')
    H=set(holes)
    if 54 not in H or 43 in H or 67 in H:raise ValueError('Case 4 context mismatch')
    if 0 in H:raise ValueError('Required state zero is not occupied')
    slacks=[]
    for i,row in enumerate(rows):
        support=row['support'];rhs=row['rhs']
        if type(rhs) is not int or rhs<0 or len(set(support))!=len(support):raise ValueError('Malformed row')
        if not all(type(j) is int and 0<=j<n for j in support):raise ValueError('Invalid row index')
        slack=sum(j in H for j in support)-rhs
        if slack<0:raise ValueError(f'Unsatisfied row {i}')
        slacks.append(slack)
    return {'source_rows':len(rows),'states':n,'holes':len(H),'occupied':n-len(H),'minimum_slack':min(slacks),'tight_rows':slacks.count(0),'slack_histogram':dict(sorted(collections.Counter(slacks).items())),'case4_context_satisfied':True,'state_zero_occupied':True,'geometric_realizability_checked':False,'scope':'Exact feasible assignment to the frozen 2469-row Boolean relaxation only'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--bundle',type=Path,default=Path(__file__).resolve().parent);a=p.parse_args()
    witness=json.loads((a.bundle/'witness.json').read_text());raw=gzip.decompress((a.bundle/witness['source_reference']).read_bytes())
    print(json.dumps(check(raw,witness),indent=2))
