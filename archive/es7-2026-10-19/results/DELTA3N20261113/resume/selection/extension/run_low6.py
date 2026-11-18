#!/usr/bin/env python3
"""Sequential bounded n6 left-size checks; use the stated systemd unit."""
import json,subprocess,sys
from pathlib import Path
E=Path(__file__).resolve().parent
W=Path('/home/jay/research/data/delta3-codex-20261113/extension')
rows=[]
for m in (10,11):
 out=W/f'low{m}-n6-a'
 cmd=[sys.executable,'-B',str(E/'run_binary.py'),'--cnf',str(W/f'low{m}-n6.cnf'),'--out',str(out),'--seconds','120','--cake-seconds','120','--as-mib','300','--heap','128']
 p=subprocess.run(cmd,check=False,timeout=360)
 assert p.returncode==0
 r=json.loads((out/'result.json').read_text());assert r.get('finished')
 rows.append({'left_m':m,'command':cmd,'status':r['status'],'label':r['label'],'seconds':r['seconds'],'result':str(out/'result.json')})
(W/'low6-queue-result.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows))
