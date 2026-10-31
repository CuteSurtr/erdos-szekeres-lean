import sys,json,time
sys.path.insert(0,'/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools')
import close_tree, os
os.makedirs(close_tree.WORK, exist_ok=True)
n=sys.argv[1]; t=time.time()
r=close_tree.solve(('/opt/work/base.cnf', n, 300, '/opt/work/models', ['--sat']))
r['base_sha256']=close_tree.sha('/opt/work/base.cnf'); r['recheck_alone']=True
open('/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C13/recheck.jsonl','a').write(json.dumps(r)+'\n')
print(json.dumps(r))
