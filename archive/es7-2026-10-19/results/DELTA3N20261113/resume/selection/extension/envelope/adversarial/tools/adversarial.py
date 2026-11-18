"""Integer-grid search in one orientation cell, scored by exact Delta bitsets."""
import argparse
from collections import Counter
from itertools import combinations
import json
import os
from pathlib import Path
import random
import resource
import shutil
import signal
import sys
import time
import traceback

ENVELOPE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ENVELOPE/'tools'))
from exact import determinant,line,build
from search import dump,atomic,sha,run_case,release_cache


def ordinary_family(geometry,m):
    """Truth table in one integer: bit A represents the entire assignment A."""
    size=1<<m;universe=(1<<size)-1;variables=[]
    for v in range(m):
        width=1<<v;bits=((1<<width)-1)<<width;length=2*width
        while length<size:bits|=bits<<length;length*=2
        variables.append(bits)
    keep=universe
    for cap in geometry['caps4']:
        bad=universe
        for v in cap:bad&=variables[v]
        keep&=~bad
    for polygon in geometry['targets']:
        hits=0
        for v in polygon:hits|=variables[v]
        keep&=hits
    masks=[]
    while keep:
        lowest=keep&-keep;masks.append(lowest.bit_length()-1);keep^=lowest
    return masks


class Cell:
    def __init__(self,p,geometry,masks,box):
        self.geometry=geometry;self.masks=masks;self.all=(1<<len(masks))-1
        self.x=[x for x,y in p];self.box=box
        self.triples=list(combinations(range(len(p)),3))
        self.signs=[1 if determinant(p,*t)>0 else -1 for t in self.triples]
        self.affected=[[] for _ in p]
        for t,s in zip(self.triples,self.signs):
            a,b,c=t
            for v,coef in ((a,self.x[c]-self.x[b]),(b,self.x[a]-self.x[c]),(c,self.x[b]-self.x[a])):
                self.affected[v].append((t,s,coef))
        self.ambient=sorted({tuple(t[-2:]) for t in geometry['caps4']})
        self.candidates=sorted({tuple(t[-2:]) for t in geometry['caps3']}-set(self.ambient))
        self.pair_ids={pair:j for j,pair in enumerate(self.candidates)}
        self.cover=[]
        for b,c in self.candidates:
            earlier=sum(1<<a for a,bb,cc in geometry['caps3'] if (bb,cc)==(b,c))
            terminal=(1<<b)|(1<<c);covered=0
            for j,A in enumerate(masks):
                if A&terminal==terminal and A&earlier:covered|=1<<j
            self.cover.append(covered)

    def points(self,y):return [[x,z] for x,z in zip(self.x,y)]

    def valid(self,y):
        p=self.points(y)
        return all(determinant(p,*t)*s>0 for t,s in zip(self.triples,self.signs))

    def bounds(self,y,v):
        p=self.points(y);lo,hi=-self.box,self.box
        for t,s,coef in self.affected[v]:
            d=determinant(p,*t);num=y[v]*coef-d;den=coef
            if den<0:num,den=-num,-den
            if s*coef>0:lo=max(lo,num//den+1)
            else:hi=min(hi,(num-1)//den)
        assert lo<=y[v]<=hi
        return lo,hi

    @staticmethod
    def exposed(q,lines):
        lo_num,lo_den=0,1;hi=None
        for ell in lines:
            ds=q[0]*ell[2]-ell[0]*q[2];dz=q[1]*ell[2]-ell[1]*q[2]
            if ds<=0 and dz<=0:return False
            if ds>0:
                num,den=-dz,ds
                if num*lo_den>lo_num*den:lo_num,lo_den=num,den
            elif ds<0:
                num,den=dz,-ds
                if hi is None or num*hi[1]<hi[0]*den:hi=num,den
            if hi is not None and lo_num*hi[1]>=hi[0]*lo_den:return False
        return True

    def score(self,y):
        p=self.points(y);ambient=[line(p,pair) for pair in self.ambient]
        eliminated=0;exposed=[]
        for j,pair in enumerate(self.candidates):
            if self.exposed(line(p,pair),ambient):exposed.append(j);eliminated|=self.cover[j]
        survivors=self.all^eliminated
        return survivors.bit_count(),survivors,tuple(exposed)

    def check(self,y,result):
        assert self.valid(y)
        report,states=build(self.points(y),self.geometry)
        exposed=tuple(j for j,pair in enumerate(self.candidates) if not states[pair]['safe'])
        eliminated=0
        for j in exposed:eliminated|=self.cover[j]
        survivors=self.all^eliminated
        assert result==(survivors.bit_count(),survivors,exposed)
        return report

    def direct_survivors(self,y,result):
        report=self.check(y,result)
        forbidden=[sum(1<<v for v in t) for t in report['exposed_triples']]
        direct=[A for A in self.masks if all(A&bad!=bad for bad in forbidden)]
        by_bits=[A for j,A in enumerate(self.masks) if result[1]>>j&1]
        assert direct==by_bits
        return direct


def choices(lo,hi,current,rng):
    width=hi-lo
    grid=[lo,lo+1,lo+width//1024,lo+width//32,lo+width//8,lo+width//2,
          hi-width//8,hi-width//32,hi-width//1024,hi-1,hi]
    grid.extend(rng.randint(lo,hi) for _ in range(4))
    return sorted({v for v in grid if lo<=v<=hi and v!=current})


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--binary',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--seconds',type=int,default=3300);ap.add_argument('--max-evals',type=int,default=500000);ap.add_argument('--restarts',type=int,default=256);ap.add_argument('--steps',type=int,default=128);ap.add_argument('--scale',type=int,default=4096);ap.add_argument('--seed',type=int,default=2026111405)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False);start=time.monotonic();rng=random.Random(args.seed)
    (args.out/'source').mkdir();(args.out/'source'/'envelope_tools').mkdir();(args.out/'best').mkdir();(args.out/'patterns').mkdir()
    for file in Path(__file__).parent.iterdir():
        if file.is_file():shutil.copy2(file,args.out/'source'/file.name)
    for name in ('exact.py','search.py','verify.py','geometry.cpp'):shutil.copy2(ENVELOPE/'tools'/name,args.out/'source'/'envelope_tools'/name)
    shutil.copy2(args.binary,args.out/'source'/'geometry');shutil.copy2(args.input,args.out/'original.json')
    original=json.loads(args.input.read_text());base=[[x*args.scale,y*args.scale] for x,y in original['P']]
    assert len(base)==18 and original['n']==7
    origin={'name':'baseline','P':base,'n':7,'source':str(args.input),'source_sha256':sha(args.input),'operation':f'positive coordinate scaling by {args.scale}'}
    initial=run_case(origin,args.out/'baseline',args.binary);assert initial['outcome']=='SAT_EXACT_MODEL_CHECKED'
    geo=json.loads((args.out/'baseline'/'geometry.json').read_text());masks=ordinary_family(geo,len(base));assert len(masks)==8149
    box=16*max(abs(y) for x,y in base);cell=Cell(base,geo,masks,box);base_y=[y for x,y in base]
    initial_score=cell.score(base_y);assert initial_score[0]==4057;cell.direct_survivors(base_y,initial_score)
    family={'ordinary_count':len(masks),'masks':masks,'candidate_pairs':cell.candidates,'ambient_pairs':cell.ambient,'pair_delta_cover_hex':[hex(c) for c in cell.cover],'orientation_signs':cell.signs,'grid_scale':args.scale,'absolute_y_bound':box,'baseline_score':initial_score[0]}
    dump(args.out/'family.json',family);release_cache(args.out/'family.json')
    dump(args.out/'plan.json',{'args':{k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()},'start_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'python':sys.version,'as_limit':resource.getrlimit(resource.RLIMIT_AS),'source_hashes':{str(p.relative_to(args.out/'source')):sha(p) for p in (args.out/'source').rglob('*') if p.is_file()},'input_sha256':sha(args.input),'label':'HEURISTIC search; exact finite scores'})
    best_y=base_y[:];best_result=initial_score;best_rows=[];evaluations=0;accepted=0;restarts_done=0;checks=1;stop='COMPLETE';last_status=0;warm=12
    pattern_stats={};score_histogram=Counter()
    trajectory=(args.out/'trajectory.jsonl').open('x')
    def event(row):
        trajectory.write(json.dumps(row,sort_keys=True)+'\n')
    def status(current=None):
        nonlocal last_status
        atomic(args.out/'status.json',{'stop':stop,'evaluations':evaluations,'accepted_moves':accepted,'accepted_states_checked':checks,'restarts_completed':restarts_done,'current':current,'best_survivors':best_result[0],'strict_improvements':len(best_rows)-1,'exposure_patterns':len(pattern_stats),'elapsed_seconds':time.monotonic()-start})
        trajectory.flush();os.fsync(trajectory.fileno());os.posix_fadvise(trajectory.fileno(),0,0,os.POSIX_FADV_DONTNEED);last_status=time.monotonic()
    def save_best(y,result,reason):
        nonlocal best_y,best_result,stop
        cell.direct_survivors(y,result)
        num=len(best_rows);name=f'best-{num:03d}'
        r={'name':name,'n':7,'P':cell.points(y),'source':str(args.input),'source_sha256':sha(args.input),'orientation_cell':'terminal18','ordinary_delta_count':len(masks),'uniform_delta_count':result[0],'reason':reason,'evaluations':evaluations}
        out=run_case(r,args.out/'best'/name,args.binary)
        if result[0]>0:assert out['outcome']=='SAT_EXACT_MODEL_CHECKED'
        else:assert out['outcome'] in ('UNSAT_UNCERTIFIED_FROZEN','UNKNOWN_SOLVER_TIMEOUT')
        row={'name':name,'survivors':result[0],'exposed_pairs':[cell.candidates[j] for j in result[2]],'evaluations':evaluations,'elapsed_seconds':time.monotonic()-start,'reason':reason,'case_directory':str(args.out/'best'/name),'outcome':out['outcome'],'P':cell.points(y)}
        best_rows.append(row);best_y=y[:];best_result=result;atomic(args.out/'best.json',row);event({'type':'best',**row})
        print(json.dumps({'best':name,'survivors':result[0],'evaluations':evaluations,'elapsed_seconds':row['elapsed_seconds']}),flush=True)
        if result[0]==0:
            stop='NEGATIVE_FROZEN';dump(args.out/'FROZEN_NEGATIVE.json',row)
    def signal_stop(signum,frame):
        nonlocal stop
        stop=f'INTERRUPTED_SIGNAL_{signum}';status();raise SystemExit(128+signum)
    signal.signal(signal.SIGTERM,signal_stop)
    save_best(base_y,initial_score,'baseline');status()
    try:
        for restart in range(args.restarts):
            if stop!='COMPLETE':break
            y=(base_y if restart%4==0 else best_y)[:];current=cell.score(y)
            event({'type':'restart','restart':restart,'y':y,'survivors':current[0]})
            for step in range(args.steps):
                if time.monotonic()-start>=args.seconds:stop='DEADLINE';break
                if evaluations>=args.max_evals:stop='EVALUATION_LIMIT';break
                v=rng.randrange(len(y));lo,hi=cell.bounds(y,v);candidates=choices(lo,hi,y[v],rng)
                if not candidates:continue
                proposals=[]
                for value in candidates:
                    if evaluations>=args.max_evals:break
                    z=y[:];z[v]=value;r=cell.score(z);evaluations+=1
                    score_histogram[r[0]]+=1
                    if r[2] not in pattern_stats:
                        cell.check(z,r);checks+=1
                        name=f'pattern-{len(pattern_stats):04d}.json'
                        sample={'name':name,'n':7,'P':cell.points(z),'survivors':r[0],'exposed_pairs':[cell.candidates[j] for j in r[2]],'first_evaluation':evaluations}
                        dump(args.out/'patterns'/name,sample);release_cache(args.out/'patterns'/name)
                        pattern_stats[r[2]]={'sample':name,'survivors':r[0],'evaluations':0,'exposed_pair_ids':r[2]}
                    pattern_stats[r[2]]['evaluations']+=1
                    proposals.append((z,r))
                    if r[0]<best_result[0]:
                        save_best(z,r,{'restart':restart,'step':step,'vertex':v,'y':value})
                        if stop=='NEGATIVE_FROZEN':break
                if stop=='NEGATIVE_FROZEN':break
                lowest=min(r[0] for z,r in proposals)
                # Early random moves diversify each restart; otherwise choose
                # the best exact survivor score, with rare escape moves.
                if step<warm and restart>0 or rng.randrange(32)==0:
                    z,r=rng.choice(proposals);mode='restart_or_escape'
                elif lowest<=current[0]:
                    z,r=rng.choice([(z,r) for z,r in proposals if r[0]==lowest]);mode='improving_or_neutral'
                else:continue
                cell.check(z,r);checks+=1
                event({'type':'move','restart':restart,'step':step,'vertex':v,'old_y':y[v],'new_y':z[v],'survivors':r[0],'exposed_pair_ids':r[2],'mode':mode,'evaluations':evaluations})
                y,current=z,r;accepted+=1
                if time.monotonic()-last_status>5:status({'restart':restart,'step':step,'survivors':current[0]})
            if stop!='COMPLETE':break
            restarts_done+=1;event({'type':'restart_end','restart':restart,'survivors':current[0]})
            status({'restart':restart,'step':'complete','survivors':current[0]})
    except Exception:
        stop='CHECK_OR_DRIVER_FAILURE'
        (args.out/'failure.txt').write_text(traceback.format_exc())
        dump(args.out/'failure_state.json',{'y':y,'current_score':current[0],'restart':restart,'step':step,'evaluations':evaluations})
        raise
    finally:
        status();trajectory.close();release_cache(args.out/'trajectory.jsonl')
        dump(args.out/'exposure_patterns.json',list(pattern_stats.values()));release_cache(args.out/'exposure_patterns.json')
        dump(args.out/'summary.json',{'label':'HEURISTIC search with exact finite counts','stop':stop,'ordinary_count':len(masks),'baseline_uniform_count':initial_score[0],'best_uniform_count':best_result[0],'evaluations':evaluations,'accepted_moves':accepted,'accepted_states_checked':checks,'restarts_completed':restarts_done,'exposure_patterns':len(pattern_stats),'proposal_score_histogram':dict(score_histogram),'best_trajectory':best_rows,'elapsed_seconds':time.monotonic()-start,'peak_self_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'limitations':['This is one fixed18-point orientation cell and a bounded coordinate grid.','All scores are exact, but the search is not exhaustive.','Positive best count does not exclude a uniform failure elsewhere in the cell.','No ordinary weak Delta counterexample is possible within this fixed cell.']})
        release_cache(args.out/'summary.json')
if __name__=='__main__':main()
