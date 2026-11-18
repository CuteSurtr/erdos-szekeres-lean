#!/usr/bin/env python3
"""Same parent exact oracle on the stronger short-cup fixtures."""
import itertools,json,resource
from pathlib import Path
from check_models import inspect,det,sha,HERE,ROOT
def main():
 resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20));resource.setrlimit(resource.RLIMIT_CPU,(18,18))
 summaries=[]
 for n in (6,7,8):
  path=ROOT/f'refined/n{n}-root/real/realized.json';r=json.loads(path.read_text());P=r['P'];m=len(P)
  assert ''.join('+' if det(P,t)>0 else '-' for t in itertools.combinations(range(m),3))==r['signs']
  full=inspect(P,n);old=inspect(P[:-1],n)
  assert full['no_fivecap'] and full['no_ngon'] and not full['longer_cups']
  assert old['long_cups'] and not old['longer_cups'] and all(q['convex'] for q in old['cup_complements'])
  repairs=[]
  for C in old['long_cups']:
   good=[]
   for q in range(m-1):
    if q in C:continue
    D=sorted(set(C)|{q,m-1})
    if not any(all(det(P,t)<0 for t in itertools.combinations(K,3)) for K in itertools.combinations(D,4)):good.append(q)
   repairs.append({'cup':C,'good_added_points':good})
  data={'label':'COMPUTED exact integer exhaustive check','n':n,'P':P,'full':full,'old':old,
        'one_point_cup_augmentations':repairs,'source':str(path),'source_sha256':sha(path)}
  (HERE/f'data/n{n}-refined.json').write_text(json.dumps(data,indent=2)+'\n')
  summaries.append({'n':n,'long_cups':len(old['long_cups']),'safe_count':old['terminal_safe_count'],
                    'safe_delta':old['minimum_terminal_safe_delta'],'rooted':full['minimum_rooted_delta'],
                    'augmentable_cups':sum(bool(x['good_added_points']) for x in repairs)})
 (HERE/'data/refined_checks.json').write_text(json.dumps({'script_sha256':sha(Path(__file__)),
    'oracle_sha256':sha(HERE/'check_models.py'),'outcomes':summaries},indent=2)+'\n')
 print(json.dumps(summaries))
if __name__=='__main__':main()
