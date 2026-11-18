"""One bounded audit process: certify appended rows, reuse exact context receipts.

A receipt transfers only to an identical subtree and path over an ordered
superset of its original rows. New subtrees always call check_tree at34.
Master/row epochs are frozen in the audit scratch before replay.
"""
import datetime as dt
import gc
import hashlib
import json
from pathlib import Path
import re
import resource
import time

import audit_followup_rows_v2 as audit_batch_rows  # v4
import replay34_v2 as base  # v4: labels need not be 0..n-1
import replay_adaptive as versions
from pool_audit import sha,dump
from residual_encoder import Geometry,static

ROOT,WORK,AUDIT=base.ROOT,base.WORK,base.AUDIT
import sys
# v3: packet folder = argv[3], extra prior replay folders = argv[4:]. v2 (14 Nov 2026 evening): deadline and output folder from argv; prior incremental receipts carried (re-validated below).
OUT=AUDIT/sys.argv[2]
SCRATCH=WORK/'audit'/sys.argv[2]
BB0=WORK/'runs/s20/bb'  # v3: historical v1-v3 bindings name files in the original packet
BB=WORK/'runs/s20'/sys.argv[3];assert BB.parent==BB0.parent and BB.is_dir()
END=dt.datetime.fromisoformat(sys.argv[1]);assert END.tzinfo is not None
PRIORS=[AUDIT/'incremental']+[AUDIT/d for d in sys.argv[4:]]  # v3: earlier replay folders


def now():return dt.datetime.now(dt.timezone(dt.timedelta(hours=9)))


def event(kind,**details):
    r={'time':now().isoformat(),'event':kind,**details}
    with (OUT/'events.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
    print(json.dumps(r),flush=True)


def digest_rows(rows):
    h=hashlib.sha256()
    for support,demand in rows:
        h.update((str(demand)+':'+','.join(map(str,support))+'\n').encode())
    return h.hexdigest()


def state_limit(mib):
    _,hard=resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS,(mib*1048576,hard))


def audit_pending_batches():
    candidates=[]
    for p in WORK.glob('cuts-v*/result.json'):
        m=re.fullmatch(r'cuts-v([0-9]+)',p.parent.name)
        if m and (p.parent/'accepted.json').exists():candidates.append((int(m[1]),p.parent.name[5:]))
    for _,tag in sorted(candidates):
        summary=AUDIT/f'cuts-{tag}/summary.json'
        if summary.exists():continue
        if now()>=END:break
        event('ROW_AUDIT_START',batch=tag)
        audit_batch_rows.audit(tag)
        s=base.read_json(summary)
        assert s['own_encoder_matches']==s['fresh_cake_acceptances']==s['rows']
        Geometry.positive.cache_clear();static.cache_clear();gc.collect();state_limit(1000)
        event('ROW_AUDIT_PASS',batch=tag,rows=s['rows'],summary_sha256=sha(summary))


def initial_receipts(pool):
    """Import our own earlier exact checks, validating their historical bindings."""
    done={};evidence=[]
    for version,directory,ledger_name,binding_name in [
        (3,AUDIT/'s20-v3','contexts.jsonl','binding.json'),
        (2,AUDIT/'s20-v2','contexts.jsonl','binding.json'),
        (1,AUDIT,'s20-contexts.jsonl','s20-binding.json')]:
        lp=directory/ledger_name;bp=directory/binding_name
        if not lp.exists() or not bp.exists():continue
        bind=base.read_json(bp);resolved={}
        for name,h in bind['input_sha256'].items():
            p=Path(name)
            if p.name in ('master.json','contexts.json') and p.parent==BB0:
                replacement=Path(str(p)+f'.v{version}-snapshot')
                if replacement.exists() and sha(replacement)==h:p=replacement
            assert p.exists() and sha(p)==h,(version,'historical binding mismatch',str(p))
            resolved[name]=str(p)
        oldmaster=base.read_json(Path(resolved[str(BB0/'master.json')]))
        oldpaths=base.frontier(oldmaster)
        source=base.read_json(WORK/'inputs/source-2650.json.gz')
        oldextra=base.read_json(Path(oldmaster['extra']))
        oldrows=[(r['support'],r['rhs']) for r in source['constraints']+oldextra]
        rd=digest_rows(oldrows);lh=sha(lp)
        with lp.open() as f:
            for line_number,line in enumerate(f,1):
                r=json.loads(line);c=r['context']
                assert c in oldpaths and r['path']==[list(z) for z in oldpaths[c]]
                assert r['internal_pending']==0 and (r['minimum_margin'] is None or r['minimum_margin']>=1)
                assert all(type(i)is int and 0<=i<len(oldrows) for i in r['used_rows'])
                p=BB/f'ctx-{c}.json.gz'
                if c in done or not p.exists() or base.sha_drop(p)!=r['context_sha256']:continue
                record={**r,'origin_version':version,'origin_kind':'prior own exact check',
                        'origin_ledger':str(lp),'origin_ledger_sha256':lh,'origin_line':line_number,
                        'origin_line_sha256':hashlib.sha256(line.encode()).hexdigest(),
                        'original_row_count':len(oldrows),'original_rows_sha256':rd,
                        'max_used_row':max(r['used_rows'],default=-1)}
                done[c]=record
        evidence.append({'version':version,'ledger':str(lp),'ledger_sha256':lh,
                         'binding_sha256':sha(bp),'resolved_input_paths':resolved})
    dump(OUT/'carry_sources.json',evidence)
    with (OUT/'carried.jsonl').open('x') as f:
        for c,r in sorted(done.items()):f.write(json.dumps(r)+'\n')
    event('CARRIED_PREVIOUS_CONTEXTS',contexts=len(done),nodes=sum(r['nodes'] for r in done.values()))
    return done


def pin_epoch(name,pool):
    t,rows,source,extra,pins,provenance=versions.version_rows(name,pool)
    assert t==20
    master_raw=(BB/'master.json').read_bytes();master=json.loads(master_raw)
    if Path(master['extra'])!=extra:return None
    assert master['budget']==34 and type(master['budget'])is int and Path(master['source'])==source
    paths=base.frontier(master)
    description_raw=(BB/'contexts.json').read_bytes();descriptions=json.loads(description_raw)
    assert len(descriptions)==len(paths) and {d['context'] for d in descriptions}==set(paths)
    for d in descriptions:base.descriptor(d,d['context'],paths[d['context']])
    mh=hashlib.sha256(master_raw).hexdigest();epoch=f'{name}-{mh[:16]}'
    folder=SCRATCH/epoch;folder.mkdir(exist_ok=True)
    for filename,data in [('master.json',master_raw),('contexts.json',description_raw)]:
        p=folder/filename
        if p.exists():assert p.read_bytes()==data
        else:p.write_bytes(data)
        pins[str(p)]=sha(p)
    for p in (Path(__file__),Path(base.__file__),Path(versions.__file__),ROOT/'scripts/omission_tree.py',ROOT/'scripts/omission_row_probe.py'):
        pins[str(p)]=sha(p)
    wrapped,used=base.envelope(master['nodes'],master['root'],((0,0),),master=True)
    top=base.check_tree(154,rows,34,wrapped,0,allow_pending=True);del wrapped
    assert top['pending']==len(paths)+1
    result={'name':name,'epoch':epoch,'rows':rows,'master':master,'master_sha256':mh,'paths':paths,
            'input_sha256':pins,'provenance':provenance,'top':top,'used':used,'row_digest':digest_rows(rows)}
    small={k:v for k,v in result.items() if k not in ('rows','master','paths','used')}
    dump(folder/'epoch.json',small)
    event('PINNED_EPOCH',version=name,rows=len(rows),contexts=len(paths),master_sha256=mh)
    return result


def prefix_valid(record,epoch,cache):
    count=record['original_row_count']
    if count not in cache:cache[count]=digest_rows(epoch['rows'][:count])
    return (count<=len(epoch['rows']) and cache[count]==record['original_rows_sha256']
            and record['max_used_row']<count)


def checkpoint(epoch,done):
    paths=epoch['paths'];covered={};cache={};used=set(epoch['used'])
    present={int(p.name[4:-8]):p for p in BB.glob('ctx-*.json.gz')}
    assert set(present)<=set(paths)
    for c,r in done.items():
        if c not in paths or c not in present:continue
        if r['path']!=[list(z) for z in paths[c]]:continue
        if not prefix_valid(r,epoch,cache):continue
        if base.sha_drop(present[c])!=r['context_sha256']:continue
        covered[c]=r;used.update(r['used_rows'])
    pending=sorted(set(paths)-set(covered))
    nodes=len(epoch['master']['nodes'])+2-len(covered)+sum(r['nodes'] for r in covered.values())
    leaves=epoch['top']['leaves']-len(covered)+sum(r['leaves'] for r in covered.values())
    margins=[r['minimum_margin'] for r in covered.values() if r['minimum_margin']is not None]
    if epoch['top']['minimum_margin']is not None:margins.append(epoch['top']['minimum_margin'])
    same_master=sha(BB/'master.json')==epoch['master_sha256']
    assert all(sha(p)==h for p,h in epoch['input_sha256'].items()),'frozen epoch input changed'
    closed=not pending and same_master
    if closed:assert set(present)==set(paths) and margins and min(margins)>=1
    result={'label':'EXACT TREE' if closed else 'PARTIAL EXACT REPLAY; NO EXCLUSION',
            'input_version':epoch['name'],'epoch':epoch['epoch'],'budget':34,'capacity_demands':[20,14],
            'rows':len(epoch['rows']),'contexts_total':len(paths),'contexts_replayed':len(covered),
            'contexts_pending':pending,'global_pending':1+len(pending),'nodes':nodes,'leaves':leaves,
            'minimum_margin':min(margins,default=None),'sole_pending_state0_missing':closed,
            'master_still_current':same_master,'master_sha256':epoch['master_sha256'],
            'input_sha256':epoch['input_sha256'],'appended_provenance':epoch['provenance'],
            'used_row_indices':sorted(used),'contexts_transferred':sum(r['origin_version']!=int(epoch['name'].split('-v')[1]) for r in covered.values()),
            'finished_local':now().isoformat(),'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    dump(OUT/f'{epoch["name"]}-summary.json',result);dump(OUT/'latest-summary.json',result)
    event('TREE_CHECKPOINT',version=epoch['name'],contexts=len(covered),total=len(paths),nodes=nodes,
          pending=result['global_pending'],minimum_margin=result['minimum_margin'],label=result['label'])
    return result,covered


def main():
    OUT.mkdir(exist_ok=True);SCRATCH.mkdir(exist_ok=True)
    assert now()<END
    assert not (OUT/'carried.jsonl').exists(),'exclusive controller attempt required'
    state_limit(1000);pool,_=base.evidence();done=initial_receipts(pool);epoch=None
    prior=[]
    for name in [d/n for d in PRIORS for n in ('carried.jsonl','new-contexts.jsonl')]:
        p=name;prior.append({'file':str(p),'sha256':sha(p)})
        with p.open() as f:
            for line in f:
                r=json.loads(line)
                if r['context'] not in done:done[r['context']]=r  # used only after path, row-prefix and file-hash checks
    dump(OUT/'carried_incremental.json',{'sources':prior,'contexts_now_known':len(done)})
    event('CARRIED_INCREMENTAL_RECEIPTS',contexts=len(done))
    original_checker=sha(ROOT/'scripts/omission_tree.py')
    ledger=OUT/'new-contexts.jsonl';last_summary=None
    with ledger.open('x') as out:
        while now()<END:
            audit_pending_batches()
            assert sha(ROOT/'scripts/omission_tree.py')==original_checker
            current=base.read_json(BB/'master.json');name=Path(current['extra']).parent.name
            if epoch is None or epoch['name']!=name or sha(BB/'master.json')!=epoch['master_sha256']:
                epoch=pin_epoch(name,pool)
                if epoch is None:continue
            present={int(p.name[4:-8]):p for p in BB.glob('ctx-*.json.gz')}
            assert set(present)<=set(epoch['paths'])
            cache={};tick=time.monotonic();new_count=0
            for c,p in sorted(present.items()):
                if now()>=END or time.monotonic()-tick>=25:break
                if sha(BB/'master.json')!=epoch['master_sha256']:break
                r=done.get(c)
                if (r and r['path']==[list(z) for z in epoch['paths'][c]] and prefix_valid(r,epoch,cache)
                        and base.sha_drop(p)==r['context_sha256']):continue
                if p.stat().st_size*40+80*1048576>900*1048576:
                    event('CONTEXT_DEFERRED',context=c,reason='estimated memory exceeds900MiB');continue
                h=base.sha_drop(p);sub=base.read_json(p);base.descriptor(sub,c,epoch['paths'][c])
                assert base.natural(sub['root']) and sub['root']<len(sub['nodes'])
                wrapped,u=base.envelope(sub['nodes'],sub['root'],epoch['paths'][c])
                try:res=base.check_tree(154,epoch['rows'],34,wrapped,0,allow_pending=True)
                except (ValueError,AssertionError):
                    if sha(BB/'master.json')!=epoch['master_sha256']:
                        del sub,wrapped;break
                    raise
                assert res['pending']==len(epoch['paths'][c]) and h==base.sha_drop(p)
                r={'context':c,'context_sha256':h,'nodes':len(sub['nodes']),
                   'leaves':res['leaves']-len(epoch['paths'][c]),'minimum_margin':res['minimum_margin'],
                   'internal_pending':0,'used_rows':sorted(u),'max_used_row':max(u,default=-1),
                   'path':[list(z) for z in epoch['paths'][c]],'origin_kind':'fresh exact check',
                   'origin_version':int(name.split('-v')[1]),'origin_epoch':epoch['epoch'],
                   'original_row_count':len(epoch['rows']),'original_rows_sha256':epoch['row_digest']}
                out.write(json.dumps(r)+'\n');out.flush();done[c]=r;new_count+=1
                del sub,wrapped,res
            last_summary,_=checkpoint(epoch,done)
            if last_summary['sole_pending_state0_missing']:break
            gc.collect()
            if not new_count and now()<END:time.sleep(min(8,max(0,(END-now()).total_seconds())))
        if epoch is not None:last_summary,_=checkpoint(epoch,done)
    dump(OUT/'finished.json',{'finished_local':now().isoformat(),'label':last_summary['label'] if last_summary else 'NO TREE REPLAY',
         'last_version':last_summary['input_version'] if last_summary else None,'carried_sha256':sha(OUT/'carried.jsonl'),
         'new_contexts_sha256':sha(ledger),'latest_summary_sha256':sha(OUT/'latest-summary.json') if last_summary else None,
         'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
    event('FINISHED',version=last_summary['input_version'] if last_summary else None)


if __name__=='__main__':
    try:main()
    except BaseException as e:
        if OUT.exists():dump(OUT/'failure.json',{'exception':repr(e),'time':now().isoformat(),'label':'NOT CONFIRMED'})
        raise
