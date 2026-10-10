#!/usr/bin/env python3
"""Resumable exact omission-tree search; numerical LP never closes a leaf."""
import argparse, collections, gzip, json, math, os, signal, sys, time
for env_key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[env_key]='1'
from pathlib import Path
sys.path.insert(0, str(Path('scripts').resolve()))
from omission_row_probe import read_rows, valid_holes
from omission_opb import sha256
from omission_tree import leaf_margin, contexts
import highspy
import numpy as np

p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('seed',type=Path);p.add_argument('output',type=Path);p.add_argument('--seconds',type=float,default=18000);p.add_argument('--budget',type=int,default=31);p.add_argument('--strategy',choices=['fraction','pseudocost'],default='fraction');p.add_argument('--max-scale',type=int,default=1000000);p.add_argument('--strong-candidates',type=int,default=8);a=p.parse_args()
source=json.loads(a.source.read_text());n,rows=read_rows(source);masks=[sum(1<<i for i in s) for s,d in rows];demands=[d for s,d in rows];allmask=(1<<n)-1
with (gzip.open(a.seed,'rt') if a.seed.suffix=='.gz' else a.seed.open()) as f:seed=json.load(f)
assert seed.get('source_sha256')==sha256(a.source)
initial_missing=set(seed['missing']);initial_occupied=set(seed['occupied']);assert not initial_missing & initial_occupied
nodes=seed['nodes'];root=seed['root'];budget=a.budget;started=time.monotonic();lastlog=started;lastsave=started;stopping=False
signal.signal(signal.SIGTERM,lambda *_:globals().__setitem__('stopping',True));signal.signal(signal.SIGINT,lambda *_:globals().__setitem__('stopping',True))

def margin(missing,occupied,node):
    lower=0;loads=[0]*n;cap=node['capacity'];free=allmask^missing^occupied
    for r,w in node['weights']:
        lower+=w*max(0,demands[r]-(masks[r]&missing).bit_count())
        for i in rows[r][0]:loads[i]+=w
    excess=sum(max(0,loads[i]-cap) for i in range(n) if free>>i&1)
    return lower-cap*(budget-missing.bit_count())-excess

pending=[];leaves=contexts(n,nodes,root)
for i,missing,occupied in leaves:
    assert not (missing | occupied) & (initial_missing | initial_occupied)
    missing=set(missing)|initial_missing;occupied=set(occupied)|initial_occupied
    m=sum(1<<j for j in missing);o=sum(1<<j for j in occupied);node=nodes[i]
    if m.bit_count()>budget:nodes[i]={'type':'over_budget'}
    elif node.get('type')=='weighted' and node['capacity']<=a.max_scale and margin(m,o,node)>0:pass
    else:
        assert node.get('type') in ['pending','weighted','over_budget'];nodes[i]={'type':'pending'};pending.append((i,m,o,None,None,None,None))
del leaves
pending.reverse()  # Continue the frozen pending-context order, after applying its five exact cuts.
started=time.monotonic();lastlog=started;lastsave=started  # Bound actual search separately from source/tree verification.
initial_pending=len(pending);initial_nodes=len(nodes);processed=closed=branches=forced=lp_resets=0;failures=collections.Counter();scale_counts=collections.Counter();pseudo=[[1.,1.,1.,1.] for _ in range(n)];model=None

def make_model():
    h=highspy.Highs();h.setOptionValue('output_flag',False);h.setOptionValue('threads',1);h.setOptionValue('solver','simplex');h.setOptionValue('presolve','off');h.setOptionValue('simplex_iteration_limit',10000);h.setOptionValue('time_limit',1e9)
    v=[h.addVariable(lb=0,ub=1,obj=1) for _ in range(n)]
    for s,d in rows:h.addConstr(h.qsum(v[i] for i in s)>=d)
    return h
model=make_model();indices=np.arange(n,dtype=np.int32)

def status(final=False):
    return {'scope':'Exact integer weighted tree; Python replay only until Lean export and geometric transfer are checked','source':str(a.source),'source_sha256':sha256(a.source),'seed_tree':str(a.seed),'seed_tree_sha256':sha256(a.seed),'script_sha256':sha256(Path(__file__)),'solver':'HiGHS '+model.version(),'strategy':a.strategy,'maximum_weight_scale':a.max_scale,'strong_candidates':a.strong_candidates,'strong_lookahead_depth':8,'hole_budget':budget,'root':root,'original_node':seed['original_node'],'missing':sorted(initial_missing),'occupied':sorted(initial_occupied),'initial_pending':initial_pending,'initial_nodes':initial_nodes,'seconds':time.monotonic()-started,'processed_lp_nodes':processed,'new_exact_leaves':closed,'new_branches':branches,'forced_branches':forced,'lp_resets':lp_resets,'lp_failures':dict(failures),'leaf_scales':dict(scale_counts),'nodes_count':len(nodes),'pending_count':len(pending),'status':'conditionally_unsat' if not pending else 'unknown','complete':not pending,'final':final}

def save(final=False):
    global lastsave
    record=status(final);print(json.dumps(record),flush=True);record['nodes']=nodes
    tmp=a.output.with_suffix(a.output.suffix+'.tmp')
    with gzip.open(tmp,'wt',compresslevel=1) as f:json.dump(record,f,separators=(',',':'))
    os.replace(tmp,a.output);a.output.with_suffix('.summary.json').write_text(json.dumps({k:v for k,v in record.items() if k!='nodes'},indent=2)+'\n');lastsave=time.monotonic()

print(json.dumps(status()),flush=True)
while pending and not stopping and time.monotonic()-started<a.seconds:
    index,missing,occupied,parent_obj,parent_var,parent_dir,parent_delta=pending.pop();nm=missing.bit_count();free=allmask^missing^occupied
    if nm>budget:nodes[index]={'type':'over_budget'};closed+=1;continue
    impossible=None;force=None
    for r,mask in enumerate(masks):
        rem=demands[r]-(mask&missing).bit_count();available=mask&free
        if rem>available.bit_count():impossible=r;break
        if rem and rem==available.bit_count() and force is None:force=(available&-available).bit_length()-1
    if impossible is not None:
        leaf={'type':'weighted','capacity':0,'weights':[[impossible,1]]};assert margin(missing,occupied,leaf)>0;nodes[index]=leaf;closed+=1;continue
    obj=None;sol=None;variable=force
    if force is not None:forced+=1
    else:
        lower=np.fromiter((float(missing>>i&1) for i in range(n)),dtype=float,count=n);upper=np.fromiter((float(not(occupied>>i&1)) for i in range(n)),dtype=float,count=n)
        model.changeColsBounds(n,indices,lower,upper);model.run();processed+=1;verdict=model.getModelStatus()
        if verdict!=highspy.HighsModelStatus.kOptimal:
            failures[str(verdict)]+=1;model.clearSolver();lp_resets+=1;model.setOptionValue('simplex_strategy',4 if lp_resets%2 else 1);model.run();processed+=1;verdict=model.getModelStatus()
        if verdict==highspy.HighsModelStatus.kOptimal:
            sol=model.getSolution();assert sol.value_valid and sol.dual_valid;obj=model.getObjectiveValue()
            if parent_obj is not None and parent_delta:
                gain=max(1e-6,obj-parent_obj)/parent_delta;row=pseudo[parent_var];row[parent_dir*2]+=gain;row[parent_dir*2+1]+=1
            if obj>budget+1e-8:
                dual=sol.row_dual;certified=False
                for scale in (10,32,100,256,1000,10000,100000,1000000):
                    if scale>a.max_scale:continue
                    weights=[[r,max(0,round(scale*x))] for r,x in enumerate(dual) if x>0.5/scale]
                    leaf={'type':'weighted','capacity':scale,'weights':[[r,w] for r,w in weights if w]}
                    if margin(missing,occupied,leaf)>0:nodes[index]=leaf;closed+=1;scale_counts[scale]+=1;certified=True;break
                if certified:continue
            candidate=[i for i,x in enumerate(sol.col_value) if x>0.5]
            if len(candidate)<=budget and valid_holes(n,rows,budget,candidate):
                pending.append((index,missing,occupied,parent_obj,parent_var,parent_dir,parent_delta));a.output.with_suffix('.witness.json').write_text(json.dumps({'holes':candidate,'exact_rows_checked':True})+'\n');print('EXACT_WITNESS',candidate,flush=True);break
            available=[i for i in range(n) if free>>i&1];fractional=[i for i in available if 1e-7<sol.col_value[i]<1-1e-7]
            if fractional:
                if a.strategy=='fraction':variable=min(fractional,key=lambda i:(abs(sol.col_value[i]-.5),i))
                else:
                    def score(i):
                        x=sol.col_value[i];q=pseudo[i];lo=x*q[0]/q[1];hi=(1-x)*q[2]/q[3]
                        return (min(lo,hi)*max(lo,hi), min(x,1-x),-i)
                    variable=max(fractional,key=score)
                    # Numerical look-ahead chooses a branch only. Every final
                    # leaf still requires the independent exact integer margin.
                    candidate_count=a.strong_candidates if (missing|occupied).bit_count()<8 else 0
                    strong=sorted(fractional,key=score,reverse=True)[:candidate_count]
                    best=None
                    for trial in strong:
                        gains=[]
                        for direction in (0,1):
                            lo=lower.copy();hi=upper.copy();lo[trial]=direction;hi[trial]=direction
                            model.changeColsBounds(n,indices,lo,hi);model.run();processed+=1
                            st=model.getModelStatus()
                            gain=max(0.0,model.getObjectiveValue()-obj) if st==highspy.HighsModelStatus.kOptimal else max(1.0,budget+1-obj) if st==highspy.HighsModelStatus.kInfeasible else 0.0
                            gains.append(gain)
                        key=((min(gains)+.02)*(max(gains)+.02),min(gains),-trial)
                        if best is None or key>best[0]:best=(key,trial)
                    if best is not None:variable=best[1]
                    model.changeColsBounds(n,indices,lower,upper)
            else:variable=min(available)
        else:
            failures[str(verdict)]+=1
            if verdict==highspy.HighsModelStatus.kInfeasible:
                status_ray,exists,ray=model.getDualRay()
                if exists:
                    for scale in (1000,1000000,1000000000):
                        leaf={'type':'weighted','capacity':0,'weights':[[r,max(0,round(scale*x))] for r,x in enumerate(ray) if x>0.5/scale]}
                        if margin(missing,occupied,leaf)>0:nodes[index]=leaf;closed+=1;break
                    else:leaf=None
                    if leaf is not None:continue
            # A failed numerical calculation can only choose a branch, never prove it.
            variable=max((i for i in range(n) if free>>i&1),key=lambda i:sum(1 for mask in masks if mask>>i&1))
    assert variable is not None and free>>variable&1
    zero,one=len(nodes),len(nodes)+1;nodes.extend([{'type':'pending'},{'type':'pending'}]);nodes[index]={'type':'branch','vertex':variable,'zero':zero,'one':one};branches+=1
    x=sol.col_value[variable] if sol is not None else .5
    pending.extend([(zero,missing,occupied|(1<<variable),obj,variable,0,x),(one,missing|(1<<variable),occupied,obj,variable,1,1-x)])
    now=time.monotonic()
    if now-lastlog>30:print(json.dumps(status()),flush=True);lastlog=now
    if now-lastsave>900:save()  # Keep this bounded 600-second chunk to one final checkpoint write.
save(True)
# The independent original validator replays every leaf with unbounded integers.
checked_leaves=contexts(n,nodes,root);margins=[];open_count=0
for index,M,O in checked_leaves:
    assert not (M|O)&(initial_missing|initial_occupied)
    M=set(M)|initial_missing;O=set(O)|initial_occupied;node=nodes[index]
    if node['type']=='pending':open_count+=1
    elif node['type']=='over_budget':assert len(M)>budget
    else:
        assert node['type']=='weighted'
        exact_margin=leaf_margin(n,rows,budget,M,O,node);assert exact_margin>0
        margins.append(exact_margin)
checked={'nodes':len(nodes),'leaves':len(checked_leaves),'pending':open_count,'complete_under_context':open_count==0,'minimum_margin':min(margins,default=None),'missing':sorted(initial_missing),'occupied':sorted(initial_occupied)}
a.output.with_suffix('.replay.json').write_text(json.dumps(checked,indent=2)+'\n');print('INDEPENDENT_REPLAY',json.dumps(checked),flush=True)
