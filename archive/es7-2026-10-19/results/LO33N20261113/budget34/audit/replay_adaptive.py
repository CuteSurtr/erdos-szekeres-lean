"""Versioned append-only input audit and exact replay, preserving v1 receipts.

Reuses only this audit's frozen traversal/envelope helpers and the trusted
integer checker. Each version gets its own binding, receipts and summary.
"""
import argparse
import datetime as dt
import gc
import json
from pathlib import Path
import re
import resource
import time

import replay34 as base
from pool_audit import sha,dump

ROOT,WORK,AUDIT=base.ROOT,base.WORK,base.AUDIT


def version_rows(name,pool):
    match=re.fullmatch(r's(19|20)-v([2-9]|[1-9][0-9]+)',name)
    assert match,'expected an explicit versioned folder'
    t=int(match[1]);folder=WORK/'inputs'/name
    rows,source,oldextra,pins=base.input_rows(t,pool)
    chain=[];seen=set();cur=folder
    while cur!=oldextra.parent:
        assert cur.parent==WORK/'inputs' and cur.name.startswith(f's{t}-v') and cur not in seen
        seen.add(cur);manifest=base.read_json(cur/'manifest.json')
        chain.append((cur,manifest));cur=Path(manifest['previous'])
    previous=oldextra.parent
    extra=base.read_json(oldextra)
    provenance=[]
    for d,m in reversed(chain):
        assert Path(m['previous'])==previous
        assert sha(previous/'extra.json')==m['previous_extra_sha256']
        assert sha(previous/'rows.txt')==m['previous_rows_sha256']
        accepted=Path(m['accepted_source']);assert accepted.is_relative_to(WORK) and accepted.suffix=='.json'
        assert sha(accepted)==m['accepted_source_sha256']
        accepted_rows=base.read_json(accepted)
        assert len(m['bindings'])==len(accepted_rows)==m['appended_rows']
        batches={}
        new=[]
        for a,b in zip(accepted_rows,m['bindings']):
            receipt=Path(b['acceptance_receipt'])
            assert receipt.name=='receipt.json' and receipt.parent.parent.parent==WORK
            batch=receipt.parent.parent.name
            assert batch.startswith('cuts-') and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',batch[5:])
            if batch not in batches:
                summary_path=AUDIT/batch/'summary.json';rs=base.read_json(summary_path)
                replay_path=AUDIT/batch/'replay.jsonl';original_accepted=WORK/batch/'accepted.json'
                assert rs['accepted_sha256']==sha(original_accepted) and rs['replay_sha256']==sha(replay_path)
                checked=[json.loads(l) for l in replay_path.read_text().splitlines()]
                assert rs['rows']==rs['fresh_cake_acceptances']==rs['own_encoder_matches']==len(checked)
                assert len({tuple(r['support']) for r in checked})==len(checked)
                batches[batch]={tuple(r['support']):r for r in checked}
                for p in (summary_path,replay_path,original_accepted):pins[str(p)]=sha(p)
            r=batches[batch][tuple(a['support'])]
            assert a['support']==r['support']==b['support'] and a['rhs']==r['rhs']==1
            base.strict_set(r['support'])
            assert r['independent_encoder_sha256']==r['cnf_sha256']==b['cnf_sha256']==base.sha_drop(r['cnf'])
            assert r['lrat_sha256']==b['lrat_sha256']==base.sha_drop(r['lrat'])
            assert Path(b['acceptance_receipt'])==Path(r['parent_receipt'])
            assert sha(r['parent_receipt'])==r['parent_receipt_sha256']
            assert sha(r['parent_cake_log'])==b['cake_log_sha256']==r['parent_cake_sha256']
            assert 's VERIFIED UNSAT' in Path(r['parent_cake_log']).read_text().splitlines()
            assert sha(r['fresh_cake_stdout'])==r['fresh_cake_sha256']
            assert 's VERIFIED UNSAT' in Path(r['fresh_cake_stdout']).read_text().splitlines()
            new.append({'support':r['support'],'rhs':1})
        assert not {tuple(x['support']) for x in new}&{tuple(x['support']) for x in extra}
        expected=extra+new
        assert base.read_json(d/'extra.json')==expected,'not a strict ordered row extension'
        assert sha(d/'extra.json')==m['extra_sha256'] and sha(d/'rows.txt')==m['rows_sha256']
        assert m['rows']==2650+len(expected)
        text=(d/'rows.txt').read_text().splitlines();nrows=m['rows']
        assert text[:8]==['FASTBB-ROWS 1',f'source {source}',f'source_sha256 {sha(source)}',
            f'extra {d/"extra.json"}',f'extra_sha256 {sha(d/"extra.json")}','states 154','base_rows 2650',f'rows {nrows}']
        expected_rows=rows+[(r['support'],r['rhs']) for r in new]
        assert len(text[8:])==len(expected_rows)==nrows
        for line,(support,demand) in zip(text[8:],expected_rows):
            vals=list(map(int,line.split()));assert vals==[demand,len(support),*support]
        rows=expected_rows;extra=expected;previous=d
        for p in (d/'manifest.json',d/'extra.json',d/'rows.txt',accepted):
            pins[str(p)]=sha(p)
        provenance.append({'input_folder':str(d),'append_count':len(new),
                           'batch_audits':{batch:sha(AUDIT/batch/'summary.json') for batch in batches}})
    pins[str(Path(__file__))]=sha(Path(__file__))
    return t,rows,source,folder/'extra.json',pins,provenance


def replay(name,pool,until,preflight=False):
    t,rows,source,extra,pins,provenance=version_rows(name,pool)
    outdir=AUDIT/name;outdir.mkdir(exist_ok=True)
    folder=WORK/f'runs/s{t}/bb';mp=folder/'master.json';dp=folder/'contexts.json'
    master=base.read_json(mp);assert master['budget']==34 and type(master['budget'])is int
    assert Path(master['source'])==source and Path(master['extra'])==extra,'master not on requested frozen version'
    paths=base.frontier(master);desc=base.read_json(dp)
    assert len(desc)==len(paths) and {x['context'] for x in desc}==set(paths)
    for d in desc:base.descriptor(d,d['context'],paths[d['context']])
    for p in (mp,dp,Path(base.__file__),ROOT/'scripts/omission_tree.py',ROOT/'scripts/omission_row_probe.py'):
        pins[str(p)]=sha(p)
    wrapped,used=base.envelope(master['nodes'],master['root'],((0,0),),master=True)
    top=base.check_tree(154,rows,34,wrapped,0,allow_pending=True);del wrapped
    assert top['pending']==len(paths)+1
    present={int(p.name[4:-8]):p for p in folder.glob('ctx-*.json.gz')}
    assert set(present)<=set(paths)
    if preflight:
        result={'label':'PREFLIGHT; no tree exclusion','input_folder':name,'rows':len(rows),
                'coupled_rows':len(rows)-2652,'capacity_demands':[t,34-t],
                'contexts_total':len(paths),'contexts_present':len(present),'master_check':top,
                'input_sha256':pins,'appended_provenance':provenance}
        dump(outdir/'preflight.json',result);return result
    bp=outdir/'binding.json';ledger=outdir/'contexts.jsonl'
    bind={'input_sha256':pins,'pool_summary_sha256':sha(AUDIT/'pool_summary.json')}
    if bp.exists():assert base.read_json(bp)==bind,'version inputs changed'
    else:dump(bp,bind)
    done={}
    if ledger.exists():
        for line in ledger.open():
            r=json.loads(line);c=r['context'];assert c not in done and c in paths and c in present
            assert r['context_sha256']==base.sha_drop(present[c])
            done[c]=r
    deferred=[]
    with ledger.open('a') as out:
        for c,p in sorted(present.items()):
            if c in done:continue
            if time.monotonic()>=until:
                deferred.append({'context':c,'reason':'time budget'});break
            if p.stat().st_size*40+80*1048576>900*1048576:
                deferred.append({'context':c,'reason':'estimated memory >900MiB'});continue
            h=base.sha_drop(p);sub=base.read_json(p);base.descriptor(sub,c,paths[c])
            assert base.natural(sub['root']) and sub['root']<len(sub['nodes'])
            begin=time.monotonic();wrapped,u=base.envelope(sub['nodes'],sub['root'],paths[c])
            rr=base.check_tree(154,rows,34,wrapped,0,allow_pending=True)
            assert rr['pending']==len(paths[c])
            assert h==base.sha_drop(p)
            result={'context':c,'context_sha256':h,'nodes':len(sub['nodes']),
                    'leaves':rr['leaves']-len(paths[c]),'minimum_margin':rr['minimum_margin'],
                    'used_rows':sorted(u),'internal_pending':0,'path':[list(z) for z in paths[c]],
                    'seconds':round(time.monotonic()-begin,4)}
            out.write(json.dumps(result)+'\n');out.flush();done[c]=result
            del sub,wrapped,rr
            if len(done)%100==0:
                print(json.dumps({'version':name,'replayed':len(done),'total':len(paths)}),flush=True);gc.collect()
    nodes=len(master['nodes'])+2-len(done);leaves=top['leaves']-len(done)
    margins=[top['minimum_margin']] if top['minimum_margin']is not None else []
    for r in done.values():
        nodes+=r['nodes'];leaves+=r['leaves'];used.update(r['used_rows'])
        if r['minimum_margin']is not None:margins.append(r['minimum_margin'])
    pending=sorted(set(paths)-set(done));final={int(p.name[4:-8]):p for p in folder.glob('ctx-*.json.gz')}
    assert set(final)<=set(paths)
    for c,r in done.items():assert c in final and base.sha_drop(final[c])==r['context_sha256']
    assert all(sha(p)==h for p,h in pins.items()),'frozen inputs or master changed during pass'
    closed=not pending
    if closed:assert set(final)==set(paths) and margins and min(margins)>=1
    result={'label':'EXACT TREE' if closed else 'PARTIAL EXACT REPLAY; NO EXCLUSION',
            'input_folder':name,'budget':34,'capacity_demands':[t,34-t],'rows':len(rows),
            'contexts_total':len(paths),'contexts_replayed':len(done),'contexts_pending':pending,
            'global_pending':1+len(pending),'sole_pending_state0_missing':closed,
            'nodes':nodes,'leaves':leaves,'minimum_margin':min(margins,default=None),
            'used_row_indices':sorted(used),'coupled_rows_used':sum(i>=2652 for i in used),
            'input_sha256':pins,'appended_provenance':provenance,'deferred':deferred,
            'contexts_sha256':sha(ledger),'pool_summary_sha256':sha(AUDIT/'pool_summary.json'),
            'finished_local':dt.datetime.now().astimezone().isoformat(),
            'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    dump(outdir/'summary.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('contexts_pending','used_row_indices','input_sha256','appended_provenance')}),flush=True)
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--input-folder',required=True);p.add_argument('--watch',action='store_true')
    p.add_argument('--preflight',action='store_true');p.add_argument('--seconds',type=int,default=1700)
    args=p.parse_args();assert 1<=args.seconds<=2400
    if args.preflight:
        pool=base.read_json(WORK/'inputs/pool812.json');assert sha(WORK/'inputs/pool812.json')==base.POOL_SHA
    else:pool,_=base.evidence()
    now=dt.datetime.now().astimezone();stop=now.replace(hour=10,minute=53,second=0,microsecond=0)
    assert now.date()==dt.date(2026,11,14) and now<stop
    deadline=time.monotonic()+min(args.seconds,(stop-now).total_seconds())
    while time.monotonic()<deadline:
        r=replay(args.input_folder,pool,min(deadline,time.monotonic()+120),args.preflight)
        if args.preflight or not args.watch or r.get('sole_pending_state0_missing'):break
        if time.monotonic()<deadline:time.sleep(min(20,deadline-time.monotonic()))


if __name__=='__main__':main()
