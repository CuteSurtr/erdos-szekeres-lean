"""Collect the completed audit without touching source packets or prior records."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess

from pool_audit import RECORD as R,WORK,sha,dump


def main():
    p=argparse.ArgumentParser();p.add_argument('--final',action='store_true');args=p.parse_args()
    s19=json.loads((R/'s19-summary.json').read_text())
    s20=json.loads((R/'incremental/latest-summary.json').read_text())
    pool=json.loads((R/'pool_summary.json').read_text())
    batches=[];count=pool['rows'];support_seen=set()
    for line in (R/'pool_replay.jsonl').open():
        x=json.loads(line);key=tuple(x['support']);assert key not in support_seen;support_seen.add(key)
    for sp in sorted(R.glob('cuts-*/summary.json')):
        s=json.loads(sp.read_text());rp=sp.with_name('replay.jsonl')
        assert s['fresh_cake_acceptances']==s['own_encoder_matches']==s['rows']
        assert sha(rp)==s['replay_sha256']
        for line in rp.open():
            x=json.loads(line);key=tuple(x['support']);assert key not in support_seen;support_seen.add(key)
            log=Path(x['fresh_cake_stdout']);assert sha(log)==x['fresh_cake_sha256']
            assert 's VERIFIED UNSAT' in log.read_text().splitlines()
        count+=s['rows'];batches.append({'batch':sp.parent.name,'rows':s['rows'],'summary_sha256':sha(sp)})
    assert len(support_seen)==count
    unit='nov13c-vfy-308-audit-incremental'
    state=subprocess.run(['systemctl','--user','show',unit,'-p','ActiveState','-p','Result','-p','ExecMainStatus'],capture_output=True,text=True).stdout
    if args.final:assert 'ActiveState=active' not in state and 'ActiveState=activating' not in state
    finished=R/'incremental/finished.json'
    if not finished.exists():finished=R/'incremental/finished-by-control.json'
    failure=R/'incremental/failure.json'
    result={'label':'INDEPENDENT AUDIT SNAPSHOT' if not args.final else 'INDEPENDENT AUDIT COMPLETE FOR THIS PASS',
            'collected_local':dt.datetime.now().astimezone().isoformat(),
            'all_certified_coupled_rows':count,'original_rows':pool['rows'],'additional_batches':batches,
            'slice19':{k:s19[k] for k in ('label','contexts_total','contexts_replayed','nodes','leaves','minimum_margin','global_pending')},
            'slice20':{k:s20[k] for k in ('label','input_version','rows','contexts_total','contexts_replayed','nodes','leaves','minimum_margin','global_pending','master_still_current')},
            'both_required_slices_exact':s19['sole_pending_state0_missing'] and s20['sole_pending_state0_missing'],
            'remaining_frontier_contexts':len(s20['contexts_pending']),
            'slice19_summary_sha256':sha(R/'s19-summary.json'),
            'slice20_summary_sha256':sha(R/'incremental/latest-summary.json'),
            'worker_finished_packet':str(finished) if finished.exists() else None,
            'worker_failure_packet':str(failure) if failure.exists() else None,
            'unit_state':state,'trust_boundary':'Written geometry and prior N5/N66 audits inherited; fresh row certificates and exact integer tree checks here; no Lean theorem claimed.'}
    path=R/('final-audit.json' if args.final else 'audit-snapshot.json');dump(path,result)
    print(json.dumps(result,indent=2))
    if args.final:
        entries={}
        for q in sorted(R.rglob('*')):
            if q.is_file() and q.name not in ('final-manifest.json',) and '__pycache__' not in q.parts:
                entries[str(q.relative_to(R))]={'sha256':sha(q),'bytes':q.stat().st_size}
        dump(R/'final-manifest.json',{'created_local':dt.datetime.now().astimezone().isoformat(),'files':entries})


if __name__=='__main__':main()
