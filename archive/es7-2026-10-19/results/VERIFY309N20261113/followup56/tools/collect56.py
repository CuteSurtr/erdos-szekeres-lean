"""Collect small audit evidence; never replay or hash the large main LRAT.
Rerun after the parent row jobs to refresh data/audit_status.json.
"""
import datetime
import hashlib
import json
import pathlib
import shutil
from model import D, OLD, HERE, WORK

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):
            h.update(b)
    return h.hexdigest()

def copy(source,dest):
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,dest)

def main():
    data=HERE/'data'
    for name in ('compile.out','compile.err','compile2.out','compile2.err',
                 'rows-probe.out','rows-probe.err','tail-probe.out','tail-probe.err',
                 'recognize-probe.err','reconstruct-probe.out','reconstruct-probe.err',
                 'real-probe.out','real-probe.err','negative-probe.out','negative-probe.err',
                 'negative.stdout','negative.stderr'):
        copy(WORK/name,data/'probes'/name)
    copy(WORK/'recognize-probe.json',data/'clause_families.json')
    for i in range(4):
        for ext in ('out','err'):
            copy(WORK/f'generate{i}.{ext}',data/'probes'/f'generate{i}.{ext}')
    for name in ('cake_attempts.json','cake.out','cake.err','cert.json','verify.json'):
        copy(D/name,data/'original'/name)
    for name in ('result.json','cake.out','cake.time'):
        copy(WORK/'replay_existing'/name,data/'main_replay'/name)
    replay=json.loads((data/'main_replay/result.json').read_text())
    assert replay['status']=='VERIFIED' and replay['verdict']=='s VERIFIED UNSAT'
    assert 's VERIFIED UNSAT' in (data/'main_replay/cake.out').read_text().splitlines()
    assert replay['cnf_sha256']=='8d4b9099cf045ca72ba5ac56e8ecea00a73a44652d5a9f3d100f63f1f10bc151'
    assert replay['lrat_sha256']=='ff79c2ef3805255b18917dc0769c5088cca0ee8106c5eefb78b8f212fa487296'
    assert sha(data/'main_replay/cake.out')==replay['cake_output_sha256']
    rows=json.loads((data/'rows.json').read_text())
    clauses=json.loads((data/'clause_families.json').read_text())
    reconstruction=json.loads((data/'reconstruction.json').read_text())
    real=json.loads((data/'real.json').read_text())
    assert rows['rows']==6775 and rows['kinds']['cycle']==51 and rows['cycle_triples_checked']==2856
    assert rows['inherited']==620 and rows['new_certificates_needed']==4
    assert clauses['clauses']==319611 and clauses['unrecognized']==0
    assert clauses['families']['sb']['distinct']==56
    assert reconstruction['trim_sha256']==replay['cnf_sha256']
    obligations=json.loads((data/'new_certificates.json').read_text())
    certified=[]; pending=[]; failed=[]; generated=[]
    for i,item in enumerate(obligations):
        h=item['record']['cnf_sha256']; dest=WORK/'new_rows'/h
        generation=json.loads((dest/'generation.json').read_text())
        assert generation['hash_matches'] and generation['full_sha256']==h
        generated.append(generation)
        copy(dest/'generation.json',data/'new_rows'/h/'generation.json')
        successes=[]
        for attempt in sorted(dest.glob('attempt-*')):
            stages=attempt/'stages.jsonl'
            if stages.exists():
                copy(stages,data/'new_rows'/h/attempt.name/'stages.jsonl')
                entries=[json.loads(l) for l in stages.read_text().splitlines()]
                failed.extend({'index':i,'attempt':str(attempt),'stage':s} for s in entries
                              if s.get('result')=='UNKNOWN TIMEOUT' or
                              (s.get('returncode') not in (0,20,None)))
            receipt=attempt/'receipt.json'
            if not receipt.exists():
                continue
            r=json.loads(receipt.read_text())
            assert r['result']=='CERTIFIED' and r['full_sha256']==h
            assert sha(attempt/'selected.cnf')==r['sub_sha256']
            assert sha(attempt/'selected.lrat')==r['lrat_sha256']
            assert 's VERIFIED UNSAT' in (attempt/'cake.log').read_text().splitlines()
            for file in ('receipt.json','cake.log','sub-solve.log','full-solve.log'):
                copy(attempt/file,data/'new_rows'/h/attempt.name/file)
            successes.append(r)
        if successes:
            certified.append(successes[-1])
        else:
            pending.append({'index':i,'kind':item['kind'],'cnf_sha256':h})
    (data/'new_row_generations.json').write_text(json.dumps(generated,indent=2)+'\n')
    inputs=[D/'layout.json',D/'used_rows.json',D/'used_ids.txt',D/'tcert/justification.json',
            D/'tcert/template_certs.jsonl',D/'tcert/core_certs.jsonl',OLD/'tcert/template_certs.jsonl',
            OLD/'tcert/core_certs.jsonl',HERE.parent/'tools/audit_mono.py',HERE.parent/'tools/rows66.py',
            HERE.parent/'tools/coupled66_independent.py',HERE.parent/'tools/real_geometry.py',
            HERE.parent/'logs/n66-row-certificates.jsonl',WORK/'recognize56',WORK/'independent-tail.txt',
            pathlib.Path('/usr/bin/cadical'),pathlib.Path('/home/jay/.local/bin/cake_lpr')]
    (data/'input_hashes.json').write_text(json.dumps({str(p):sha(p) for p in inputs},indent=2)+'\n')
    status={'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'status':'INDEPENDENTLY CONFIRMED' if not pending else 'FOUR-ROW COVERAGE FOLLOW-UP',
            'main_certificate':'CERTIFIED: retained LRAT independently replayed',
            'geometric_bound_confirmed':not pending,'fresh_main_solve':False,
            'all_trimmed_clauses_recognized':True,'trimmed_bytes_reconstructed':True,
            'sb_retained':56,'cycles':51,'rows':6775,'inherited_cnfs':620,
            'fresh_row_certificates':certified,'pending_row_certificates':pending,
            'failed_or_unknown_stages':failed,'real_controls':{k:real[k] for k in
                ('sets_including_reflections','row_evaluations','full_sb_clause_evaluations','states_seen')},
            'limits':'Written soundness + exact computations + cake_lpr; not Lean-checked; parent review required before earlier-record changes.'}
    (data/'audit_status.json').write_text(json.dumps(status,indent=2)+'\n')
    with (data/'status_history.jsonl').open('a') as f:
        f.write(json.dumps(status)+'\n')
    # Manifest covers the current small record, including this history.
    paths=sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='SHA256SUMS'
                 and '__pycache__' not in p.parts)
    (HERE/'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.relative_to(HERE)}\n' for p in paths))
    print(json.dumps({'status':status['status'],'fresh_rows':len(certified),'pending_rows':len(pending),
                      'failed_or_unknown_stages':len(failed),'files_in_manifest':len(paths)}),flush=True)

if __name__=='__main__':
    main()
