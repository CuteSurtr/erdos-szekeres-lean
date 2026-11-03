#!/usr/bin/env python3
"""Bounded sound lifts of a negative-definite determinant obstruction.

Injective orbit maps and arbitrary offsets substitute invertible rotations in
the source quadratic form. Reversing sector direction must also reverse all
required signs: this substitutes conjugated seeds and preserves negativity.
Each emitted canonical clause is tested exactly on original/mirrored known54
embeddings. This is a finite partial family, not all orbit maps or shifts.
"""
import argparse
import hashlib
import importlib.util
import itertools as it
import json
from pathlib import Path
import random
import resource
import shutil
import time

def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--witness',type=Path,required=True);p.add_argument('--verified',type=Path,required=True);p.add_argument('--model',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--shifts',type=int,default=128);p.add_argument('--incoming',type=Path);p.add_argument('--index',type=int,default=1006);p.add_argument('--independent',type=Path);a=p.parse_args();start=time.monotonic();a.out.mkdir(parents=True,exist_ok=True)
 w=json.loads(a.witness.read_text());v=json.loads(a.verified.read_text());assert v['status']=='PASS' and v['exact_negative_definite'] and v['coupled_reflection_congruence'] and v['exact54_tests']>=100
 assert sha(a.witness)==v['witness_sha256'];assert sha(a.model)==w['model_sha256']==v['model_sha256'];pos=set(json.loads(a.model.read_text()))
 if a.incoming:
  assert a.independent is not None,'independent instance check required before queueing'
  independent=json.loads(a.independent.read_text());assert independent['negative_definite'] and independent['all_weights_positive']
  assert independent['witness_sha256']==sha(a.witness) and independent['model_sha256']==sha(a.model)
 V=load('verify',Path(__file__).parent/'tests/verify_sdp.py');G=load('encoder',V.ROOT/'C7UPPER/gen.py');E=G.Enc(6,8,w['t']);reverse={value:key for key,value in E.tvar.items()};source,pts=V.known54()
 layers=w['source_layers'];n=len(layers);assert n<=9
 rng=random.Random(20261104);shifts={(0,)*(n-1)}
 while len(shifts)<min(a.shifts,6**(n-1)):shifts.add(tuple(rng.randrange(6) for _ in range(n-1)))
 clauses=set();count=0;tests=0;violated=0;mintrue=len(w['records']);maxsum=None
 records=a.out/'family_records.jsonl';clausepath=a.out/'family.clauses'
 with records.open('w') as out,clausepath.open('w') as cf:
  for targets in it.combinations(range(w['t']),n):
   target_to_known=dict(zip(targets,range(n)))
   for offsets in sorted(shifts):
    for direction in (1,-1):
     mapping=dict(zip(layers,zip(targets,(0,)+offsets)));mapped=[]
     for r in w['records']:
      q=[6*mapping[x//6][0]+(direction*(x%6)+mapping[x//6][1])%6 for x in r['triple']]
      lit=E.o(*q);sg=r['required_sign']*direction*(1 if lit>0 else -1)
      mapped.append((abs(lit),sg,r['weight'],q,1 if lit>0 else -1))
     clause=tuple(sorted((-var*sg for var,sg,weight,q,par in mapped),key=abs));assert len(set(clause))==len(clause) and not any(-x in clause for x in clause)
     if clause in clauses:continue
     clauses.add(clause);count+=1;bad=all((x>0)!=(abs(x) in pos) for x in clause);violated+=bad
     for mirror in (1,-1):
      pp=V.mirrored_ccw(pts,mirror)
      def point(x):return pp[6*target_to_known[x//6]+x%6]
      total=0;truecount=0
      for var,sg,weight,q,par in mapped:
       value=V.det(*(point(x) for x in reverse[var]));assert value
       assert value*par==V.det(*(point(x) for x in q)),'canonicalization mismatch'
       total+=value*sg*weight;truecount+=(value>0)!=(sg>0)
      assert total<0 and truecount>0;tests+=1;mintrue=min(mintrue,truecount);maxsum=total if maxsum is None else max(maxsum,total)
     cf.write(' '.join(map(str,clause))+' 0\n');out.write(json.dumps({'targets':targets,'offsets':(0,)+offsets,'direction_and_sign':direction,'clause':clause,'violated_by_source_model':bad},separators=(',',':'))+'\n')
 assert tuple(w['candidate_clause']) in clauses and violated>0
 result={'status':'PASS','kind':'sixfold negative-definite quadratic obstruction family','source_witness_sha256':sha(a.witness),'source_verified_sha256':sha(a.verified),'source_model_sha256':w['model_sha256'],'family_sha256':sha(clausepath),'records_sha256':sha(records),'unique_clauses':count,'source_model_violated_clauses':violated,'orbit_injections':'order-preserving only','relative_shift_patterns':len(shifts),'direction_and_sign':'coupled +/+ or -/- only','coverage':'finite partial family; not exhaustive','exact54_sha256':sha(source),'exact54_tests':tests,'exact54_test_scope':'each emitted canonical clause on original and mirrored CCW injective embeddings','exact54_forbidden_matches':0,'exact54_min_true_literals':mintrue,'exact54_largest_weighted_sum':maxsum,'elapsed_seconds':round(time.monotonic()-start,3),'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 if a.independent:result['independent_verification_sha256']=sha(a.independent)
 evidence=a.out/'family_verified.json';evidence.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
 if a.incoming:
  assert a.index>=1000;dest=a.incoming/f'psd{a.index:04d}';dest.mkdir(exist_ok=False)
  for src in (a.witness,a.verified,evidence,clausepath):shutil.copyfile(src,dest/src.name)
  shutil.copyfile(a.independent,dest/'independent_verified.json')
  approval={'approved':True,'kind':result['kind'],'clauses':'family.clauses','sha256':result['family_sha256'],'approval_scope':'standing authorization after exact direct-polynomial and rational definiteness proofs, independent checker instance pass, finite exact54 regression tests','evidence':['sdp_witness.json','verified.json','family_verified.json','independent_verified.json']}
  pending=dest/'approved.pending';pending.write_text(json.dumps(approval,indent=2)+'\n');pending.replace(dest/'approved.json')
  receipt={'queue_folder':dest.name,'family_sha256':result['family_sha256'],'source_model_sha256':w['model_sha256'],'clauses':count};(a.out.parent/'queue_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True)
if __name__=='__main__':main()
