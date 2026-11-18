"""Independent, resumable exact replay of the two *new* budget34 trees.

The finder and its verification scripts are never imported. This wrapper
re-derives master paths, checks all bindings and coverage, and delegates
every weighted/over-budget leaf to scripts/omission_tree.check_tree.
Its only admissible global pending branch is exactly state0 missing.
"""
import argparse
import datetime as dt
import gc
import gzip
import hashlib
import json
import os
import resource
from pathlib import Path
import sys
import time

ROOT=Path('/home/jay/research/lean/erdos-szekeres-lean')
WORK=Path('/home/jay/research/data/es308-20261114')
AUDIT=ROOT/'cloud/es7-2026-10-19/results/LO33N20261113/budget34/audit'
sys.path.insert(0,str(ROOT/'scripts'))
from omission_tree import check_tree
from omission_row_probe import read_rows
from pool_audit import sha, dump, POOL_SHA, SOURCE_RAW_SHA


def sha_drop(path):
    """Hash a read-only large packet and advise away its file cache afterwards."""
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):
            h.update(b)
        os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
    return h.hexdigest()


def natural(x):
    return type(x) is int and x>=0


def strict_set(xs):
    assert isinstance(xs,list) and all(natural(x) and x<154 for x in xs)
    assert xs==sorted(set(xs))
    return set(xs)


def read_json(path):
    if path.suffix=='.gz':
        with gzip.open(path,'rt') as f:
            return json.load(f)
    return json.loads(path.read_text())


def evidence():
    """A summary label or the old ledgers alone cannot admit an extra row."""
    poolpath=WORK/'inputs/pool812.json'
    assert sha(poolpath)==POOL_SHA
    pool=read_json(poolpath)
    assert len(pool)==812
    summary=read_json(AUDIT/'pool_summary.json')
    assert summary['rows']==812 and summary['accepted_retained_lrats']==812
    assert summary['pool_sha256']==POOL_SHA
    assert sha(AUDIT/'pool_replay.jsonl')==summary['replay_sha256']
    assert sha(AUDIT/'pool_inventory.json')==summary['inventory_sha256']
    recs=[json.loads(x) for x in (AUDIT/'pool_replay.jsonl').read_text().splitlines()]
    assert len(recs)==812
    inv=read_json(AUDIT/'pool_inventory.json')
    assert len(inv['rows'])==812
    for i,(row,rec,prior) in enumerate(zip(pool,recs,inv['rows'])):
        assert rec['pool_index']==i and prior['pool_index']==i
        assert row=={'support':rec['support'],'rhs':rec['rhs']}
        assert row=={'support':prior['support'],'rhs':prior['rhs']}
        assert rec['rhs']==1 and type(rec['rhs']) is int
        strict_set(rec['support'])
        assert rec['independent_encoder_sha256']==rec['cnf_sha256']==prior['cnf_sha256']
        assert rec['lrat_sha256']==prior['lrat_sha256']
        stdout=Path(rec['cake_stdout'])
        assert sha(stdout)==rec['cake_stdout_sha256']
        assert 's VERIFIED UNSAT' in stdout.read_text().splitlines()
        assert all(sha_drop(p)==h for p,h in rec['compressed_inputs_sha256'].items())
    return pool,summary


def input_rows(t,pool):
    assert t in (19,20)
    inp=WORK/'inputs';source=inp/'source-2650.json.gz';extra=inp/f's{t}/extra.json'
    manifest=read_json(inp/'input-manifest.json')
    assert manifest['budget']==34 and manifest['states']==154 and manifest['base_rows']==2650
    assert manifest['coupled_rows']==812 and manifest['pool_sha256']==POOL_SHA
    assert sha(source)==manifest['source_sha256']
    raw=gzip.decompress(source.read_bytes())
    assert hashlib.sha256(raw).hexdigest()==SOURCE_RAW_SHA
    catalog=json.loads(raw); assert len(catalog['states'])==154 and len(catalog['constraints'])==2650
    states=catalog['states'];F=[i for i,s in enumerate(states) if s[0]>=5];Lo=[i for i,s in enumerate(states) if s[0]<=4]
    assert len(F)==84 and len(Lo)==70 and set(F).isdisjoint(Lo) and set(F)|set(Lo)==set(range(154))
    extras=read_json(extra)
    assert extras==[{'support':F,'rhs':t},{'support':Lo,'rhs':34-t}]+pool
    assert sha(extra)==manifest['slices'][str(t)]['extra_sha256']
    n,rows=read_rows({'states':states,'constraints':catalog['constraints']+extras})
    assert n==154 and len(rows)==3464
    rowsfile=inp/f's{t}/rows.txt'
    assert sha(rowsfile)==manifest['slices'][str(t)]['rows_sha256']
    text=rowsfile.read_text().splitlines()
    assert text[:8]==['FASTBB-ROWS 1',f'source {source}',f'source_sha256 {sha(source)}',
                     f'extra {extra}',f'extra_sha256 {sha(extra)}','states 154','base_rows 2650','rows 3464']
    parsed=[]
    for line in text[8:]:
        a=list(map(int,line.split())); demand,k,*support=a
        assert k==len(support)
        parsed.append((support,demand))
    assert len(parsed)==len(rows)
    assert all(list(s)==a and d==b for (s,d),(a,b) in zip(rows,parsed))
    pins={str(p):sha(p) for p in (source,extra,rowsfile,inp/'input-manifest.json',inp/'pool812.json')}
    return rows,source,extra,pins


def frontier(master):
    """Own full traversal; never trust stored context descriptions."""
    nodes=master['nodes'];assert isinstance(nodes,list) and nodes
    root=master['root'];assert natural(root) and root<len(nodes)
    paths={};seen=set();stack=[(root,((0,0),))];ordinary=0
    while stack:
        i,path=stack.pop()
        assert natural(i) and i<len(nodes) and i not in seen
        seen.add(i);nd=nodes[i];assert isinstance(nd,dict)
        kind=nd.get('type')
        if kind=='branch':
            v=nd['vertex'];assert natural(v) and v<154 and v not in {v for v,b in path}
            stack.extend([(nd['zero'],path+((v,0),)),(nd['one'],path+((v,1),))])
        elif kind=='context':
            c=nd['context'];assert natural(c) and c not in paths
            paths[c]=path
        else:
            assert kind in ('weighted','over_budget'), 'uncertified master leaf'
            ordinary+=1
    assert len(seen)==len(nodes), 'unreachable master nodes'
    # v2: --split-open numbers new contexts after the old maximum, so labels need not be 0..n-1. Distinct labels
    # (asserted above), their count (next line) and closure = files exactly match labels keep the bijection.
    assert all(natural(c) for c in paths), 'context identifiers must be natural numbers'
    assert master['contexts']==len(paths) and type(master['contexts']) is int
    assert master['master_leaves']==ordinary
    return paths


def envelope(nodes,root,path,master=False):
    """Attach a complete branch path with explicit artificial pending siblings."""
    assert path
    k=len(path);out=[]
    for j,(v,b) in enumerate(path):
        onward=j+1 if j+1<k else k+root
        sibling=k+len(nodes)+j
        out.append({'type':'branch','vertex':v,'zero':onward if b==0 else sibling,
                    'one':onward if b==1 else sibling})
    used=set()
    for nd in nodes:
        kind=nd['type']
        if kind=='branch':
            out.append(dict(nd,zero=nd['zero']+k,one=nd['one']+k))
        elif kind=='context' and master:
            out.append({'type':'pending'})
        else:
            assert kind in ('weighted','over_budget'), 'unfinished context subtree'
            if kind=='weighted':
                for r,w in nd['weights']:
                    if type(w) is int and w>0:
                        used.add(r)
            out.append(nd)
    out.extend({'type':'pending'} for _ in path)
    return out,used


def descriptor(rec,c,path):
    assert type(rec['context']) is int and rec['context']==c
    assert strict_set(rec['missing'])=={v for v,b in path if b==1}
    assert strict_set(rec['occupied'])=={v for v,b in path if b==0}


def replay_slice(t,pool,pool_summary,until=None,preflight=False):
    rows,source,extra,pins=input_rows(t,pool)
    folder=WORK/f'runs/s{t}/bb';mpath=folder/'master.json';desc=folder/'contexts.json'
    master=read_json(mpath);assert master['budget']==34 and type(master['budget']) is int
    assert Path(master['source'])==source and Path(master['extra'])==extra
    paths=frontier(master)
    ds=read_json(desc);assert isinstance(ds,list) and len(ds)==len(paths)
    assert len({d['context'] for d in ds})==len(ds)
    assert {d['context'] for d in ds}==set(paths)
    for d in ds:
        descriptor(d,d['context'],paths[d['context']])
    pins.update({str(mpath):sha(mpath),str(desc):sha(desc),
                 str(ROOT/'scripts/omission_tree.py'):sha(ROOT/'scripts/omission_tree.py'),
                 str(ROOT/'scripts/omission_row_probe.py'):sha(ROOT/'scripts/omission_row_probe.py'),
                 str(Path(__file__)):sha(Path(__file__))})
    # All master leaves are checked at the *new* budget, even during preflight.
    top,used=envelope(master['nodes'],master['root'],((0,0),),master=True)
    result=check_tree(154,rows,34,top,0,allow_pending=True)
    assert result['pending']==len(paths)+1
    del top
    present={int(p.name[4:-8]):p for p in folder.glob('ctx-*.json.gz')}
    assert set(present)<=set(paths), 'extra context files outside master frontier'
    sizes=[p.stat().st_size for p in present.values()]
    estimate={'slice':t,'status':'PREFLIGHT ONLY','budget':34,'capacities':[t,34-t],
              'contexts_total':len(paths),'contexts_present':len(present),
              'largest_gzip_bytes':max(sizes,default=0),
              'estimated_largest_context_mib':round(max(sizes,default=0)*40/1048576+80,1),
              'master_exact_check':result,'input_sha256':pins,'pool_sha256':POOL_SHA}
    if preflight:
        dump(AUDIT/f's{t}-preflight.json',estimate)
        return estimate
    receipts=AUDIT/f's{t}-contexts.jsonl';binding=AUDIT/f's{t}-binding.json'
    binding_data={'input_sha256':pins,'pool_summary_sha256':sha(AUDIT/'pool_summary.json')}
    if binding.exists():
        assert read_json(binding)==binding_data, 'replay inputs changed since checkpoint'
    else:
        dump(binding,binding_data)
    done={}
    if receipts.exists():
        for line in receipts.read_text().splitlines():
            r=json.loads(line);c=r['context']
            assert c not in done and c in paths and c in present
            assert r['context_sha256']==sha_drop(present[c]), 'already-replayed subtree changed'
            done[c]=r
    deferred=[]
    with receipts.open('a') as out:
        for c,p in sorted(present.items()):
            if c in done:
                continue
            if until is not None and time.monotonic()>=until:
                deferred.append({'context':c,'reason':'time budget'});break
            # Refuse an unsafe full JSON load. An unverified large context stays pending.
            if p.stat().st_size*40+80*1048576 > 900*1048576:
                deferred.append({'context':c,'reason':'estimated memory >900MiB'});continue
            h=sha_drop(p);sub=read_json(p);descriptor(sub,c,paths[c])
            assert natural(sub['root']) and sub['root']<len(sub['nodes'])
            started=time.monotonic()
            wrapped,local_used=envelope(sub['nodes'],sub['root'],paths[c])
            rr=check_tree(154,rows,34,wrapped,0,allow_pending=True)
            assert rr['pending']==len(paths[c]), 'pending subtree leaf'
            assert h==sha_drop(p), 'context changed during replay'
            r={'context':c,'context_sha256':h,'nodes':len(sub['nodes']),
               'leaves':rr['leaves']-len(paths[c]),'minimum_margin':rr['minimum_margin'],
               'used_rows':sorted(local_used),'internal_pending':0,
               'path':[list(z) for z in paths[c]],'seconds':round(time.monotonic()-started,4)}
            out.write(json.dumps(r)+'\n');out.flush();done[c]=r
            del wrapped,sub,rr
            if len(done)%100==0:
                print(json.dumps({'slice':t,'replayed':len(done),'contexts':len(paths)}),flush=True)
                gc.collect()
    nodes=len(master['nodes'])+2-len(done)
    leaves=result['leaves']-len(done)
    margins=[result['minimum_margin']] if result['minimum_margin'] is not None else []
    for r in done.values():
        nodes+=r['nodes'];leaves+=r['leaves'];used.update(r['used_rows'])
        if r['minimum_margin'] is not None:
            margins.append(r['minimum_margin'])
    pending_contexts=sorted(set(paths)-set(done))
    # Check coverage again, including appeared or mutated files. New files wait for the next pass.
    final_present={int(p.name[4:-8]):p for p in folder.glob('ctx-*.json.gz')}
    assert set(final_present)<=set(paths)
    for c,r in done.items():
        assert c in final_present and sha_drop(final_present[c])==r['context_sha256']
    assert all(sha(p)==h for p,h in pins.items()), 'master or frozen input changed'
    closed=not pending_contexts
    if closed:
        assert set(final_present)==set(paths), 'master frontier not covered'
        assert margins and min(margins)>=1
    summary={'slice':t,'budget':34,'capacity_demands':[t,34-t],
             'label':'EXACT TREE' if closed else 'PARTIAL EXACT REPLAY; NO EXCLUSION',
             'contexts_total':len(paths),'contexts_replayed':len(done),'contexts_pending':pending_contexts,
             'nodes':nodes,'leaves':leaves,'minimum_margin':min(margins,default=None),
             'global_pending':1+len(pending_contexts),
             'sole_pending_state0_missing':closed,'used_row_indices':sorted(used),
             'coupled_rows_used':sum(r>=2652 for r in used),'deferred':deferred,
             'input_sha256':pins,'pool_summary_sha256':sha(AUDIT/'pool_summary.json'),
             'contexts_receipts_sha256':sha(receipts),'finished_local':dt.datetime.now().astimezone().isoformat(),
             'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    dump(AUDIT/f's{t}-summary.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k not in ('contexts_pending','used_row_indices','input_sha256')}),flush=True)
    return summary


def main():
    p=argparse.ArgumentParser();p.add_argument('--slice',type=int,choices=(19,20));p.add_argument('--preflight',action='store_true')
    p.add_argument('--watch',action='store_true');p.add_argument('--seconds',type=int,default=2100)
    args=p.parse_args();assert 1<=args.seconds<=2400
    if args.preflight:
        # Before row proofs finish this checks structural inputs only and makes no claim of certification.
        pool=read_json(WORK/'inputs/pool812.json');assert sha(WORK/'inputs/pool812.json')==POOL_SHA
        for t in ((args.slice,) if args.slice else (19,20)):
            replay_slice(t,pool,None,preflight=True)
        return
    pool,summary=evidence()
    local=dt.datetime.now().astimezone()
    hard_stop=local.replace(hour=10,minute=54,second=0,microsecond=0)
    assert local.date()==dt.date(2026,11,14) and local<hard_stop
    deadline=time.monotonic()+min(args.seconds,(hard_stop-local).total_seconds())
    slices=(args.slice,) if args.slice else (19,20)
    finished=set()
    while time.monotonic()<deadline and len(finished)<len(slices):
        for t in slices:
            if t in finished or time.monotonic()>=deadline:
                continue
            result=replay_slice(t,pool,summary,until=min(deadline,time.monotonic()+120))
            if result['sole_pending_state0_missing']:
                finished.add(t)
        if not args.watch:
            break
        if len(finished)<len(slices) and time.monotonic()<deadline:
            time.sleep(min(20,deadline-time.monotonic()))
    print(json.dumps({'closed_slices':sorted(finished),'required_slices':list(slices),'all_closed':len(finished)==len(slices)}),flush=True)


if __name__=='__main__':
    main()
