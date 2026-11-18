#!/usr/bin/env python3
"""Deliberately invalid exact inputs exercise this track's independent checker."""
from copy import deepcopy
from fractions import Fraction
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource

from verify import check, orientation

HERE=Path(__file__).resolve().parent


def main():
    resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
    resource.setrlimit(resource.RLIMIT_CPU,(18,18))
    raw=json.loads((HERE/'data/simple11.candidate.json').read_text())
    results=[]
    def rejected(name,case):
        case.pop('signs',None)
        try:check(case)
        except (AssertionError,StopIteration) as e:
            results.append({'name':name,'status':'EXPECTED_REJECTION','exception':type(e).__name__})
        else:raise AssertionError(f'bad input accepted: {name}')
    case=deepcopy(raw);case['P']=[[i,i*i] for i in range(11)]
    rejected('eleven_cup_has_seven_gons',case)
    case=deepcopy(raw);case['P'][1]=case['P'][0][:]
    rejected('duplicate_point',case)
    for label,t in (('family_lower_endpoint',Fraction(-1)),('family_upper_endpoint',Fraction(8,61))):
        case=deepcopy(raw);d=t.denominator
        case['P']=[[x*d,y*d] for x,y in case['P']];case['P'][5][1]+=t.numerator
        rejected(label,case)
    facts=json.loads((HERE/'data/simple11.verify.json').read_text())['result']
    targets=facts['all_convex_six_subsets'];caps=facts['all_four_caps']
    first=targets[0]
    case=deepcopy(raw);case['terminal_delta']=[i for i in range(11) if i not in first][:3]
    rejected('selected_triple_misses_a_target',case)
    for A in combinations(range(11),3):
        if orientation(raw['P'],*A)>=0:continue
        if any(tuple(q[-2:])==A[-2:] for q in caps):continue
        if not all(set(A)&set(t) for t in targets):continue
        case=deepcopy(raw);case['terminal_delta']=list(A)
        rejected('ordinary_delta_triple_is_not_terminal_safe',case)
        break
    else:raise AssertionError('missing negative terminal control')
    # The previously checked boundary example admits a pair; it must not
    # satisfy this new fixture check even though its ambient premises hold.
    path=HERE.parent.parent/'boundary/audit/data/n7-root.json'
    old=json.loads(path.read_text());case={'P':old['P'][:old['old_m']],'n':7,'terminal_delta':[0,1,3]}
    # Use an actual cup triple meeting every target, to reach the pair check.
    P=case['P']
    from verify import convex_hull
    old_targets=[t for t in combinations(range(11),6) if len(convex_hull(P,t))==6]
    case['terminal_delta']=list(next(A for A in combinations(range(11),3)
        if orientation(P,*A)>0 and all(set(A)&set(t) for t in old_targets)))
    rejected('valid_boundary_set_admits_a_pair',case)
    out={'label':'COMPUTED exact negative controls','status':'PASS','controls':results,
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'checker_sha256':hashlib.sha256((HERE/'verify.py').read_bytes()).hexdigest(),
         'boundary_control_source':str(path),'boundary_control_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    with (HERE/'data/controls.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({'status':'PASS','expected_rejections':len(results)}))


if __name__=='__main__':main()
