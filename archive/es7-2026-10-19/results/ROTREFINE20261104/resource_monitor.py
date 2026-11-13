#!/usr/bin/env python3
"""Record total active+wired+compressed memory during a bounded research window.
Stop by creating the --stop-file. This monitor never signals unrelated processes.
Workers enforce their own memory/deadline guards; warnings here prompt review.
"""
import argparse, datetime, json, re, subprocess, time
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--stop-file',required=True,type=Path)
p.add_argument('--deadline',required=True);a=p.parse_args()
deadline=datetime.datetime.fromisoformat(a.deadline);peak=0;count=0
a.out.parent.mkdir(parents=True,exist_ok=True)
with a.out.open('a',buffering=1) as f:
    while not a.stop_file.exists() and datetime.datetime.now(datetime.timezone.utc)<deadline:
        raw=subprocess.check_output(['vm_stat'],text=True)
        page=int(re.search(r'page size of (\d+) bytes',raw)[1])
        fields=dict((k,int(v)) for k,v in re.findall(r'^([^:\n]+):\s+(\d+)',raw,re.M))
        total=page*sum(fields[k] for k in ('Pages active','Pages wired down','Pages occupied by compressor'))
        peak=max(peak,total);count+=1
        rec={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'total_bytes':total}
        f.write(json.dumps(rec)+'\n')
        if total>=29_000_000_000: print('MEMORY_WARNING '+json.dumps(rec),flush=True)
        time.sleep(10)
    f.write(json.dumps({'event':'monitor_stopped','samples':count,'peak_total_bytes':peak})+'\n')
print(json.dumps({'monitor_stopped':True,'samples':count,'peak_total_bytes':peak}),flush=True)
