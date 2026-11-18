#!/usr/bin/env python3
"""Analyze subsets of an abstract model; no coordinate or realizability claim."""
import argparse,hashlib,itertools,json,resource,time
from pathlib import Path
from protection_signs import analyze
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--signs',type=Path,required=True);ap.add_argument('--m',type=int,required=True);ap.add_argument('--size',type=int,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(150<<20,150<<20));resource.setrlimit(resource.RLIMIT_CPU,(25,25));start=time.monotonic();a.out.mkdir(parents=True,exist_ok=False)
 signs=a.signs.read_text().strip();tr=list(itertools.combinations(range(a.m),3));assert len(signs)==len(tr);table=dict(zip(tr,signs));results=[]
 for case,old in enumerate(itertools.combinations(range(a.m),a.size)):
  sub=''.join(table[t] for t in itertools.combinations(old,3));report,_=analyze(sub,a.size,7)
  row=dict(case=case,local_to_original=old,**report);results.append(row)
  if not report['families']['terminal']['count']:
   (a.out/(str(case)+'.signs')).write_text(sub+'\n')
 result={'label':'COMPUTED abstract restrictions; realizability unknown','m':a.m,'size':a.size,'cases':results,'failures':{k:[r['case'] for r in results if not r['families'][k]['count']] for k in ['terminal','cup','forced']},'seconds':time.monotonic()-start,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'signs_sha256':hashlib.sha256(a.signs.read_bytes()).hexdigest()}
 (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='cases'}))
if __name__=='__main__':main()
