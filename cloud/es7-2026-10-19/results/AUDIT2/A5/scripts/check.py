# A5 independent leaf checker. Usage: check.py sample.jsonl out.jsonl jobs cap
import sys,json,hashlib,subprocess,os,time,threading
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'/opt/a5'); import mk
inp,out,jobs,cap=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
done=set()
if os.path.exists(out):
    for l in open(out): done.add(json.loads(l)['key'])
todo=[json.loads(l) for l in open(inp)]
lock=threading.Lock()
os.makedirs('/opt/a5/w',exist_ok=True)
def run(m):
    key='%s|%s'%(m['case'],json.dumps(m['lits']))
    if key in done: return
    tag=hashlib.sha1(key.encode()).hexdigest()[:12]
    cnf='/opt/a5/w/%s.cnf'%tag; prf='/opt/a5/w/%s.lrat'%tag
    data=mk.build(m['case'],m['lits']); h=hashlib.sha256(data).hexdigest()
    open(cnf,'wb').write(data)
    rec={'key':key,'case':m['case'],'lits':m['lits'],'idx':m['idx'],'cnf_sha256':h}
    t=time.time()
    try:
        p=subprocess.run(['/opt/bin/cadical','-q','--lrat','--no-binary',cnf,prf],capture_output=True,text=True,timeout=cap)
        rec['rc']=p.returncode
    except subprocess.TimeoutExpired:
        rec['rc']='TIMEOUT'
    rec['solve_s']=round(time.time()-t,2)
    rec['cake']=''
    if rec['rc']==20:
        rec['proof_bytes']=os.path.getsize(prf)
        t=time.time()
        q=subprocess.run(['/opt/bin/cake_lpr',cnf,prf],capture_output=True,text=True)
        rec['check_s']=round(time.time()-t,2)
        lines=q.stdout.splitlines()
        rec['cake']='s VERIFIED UNSAT' if 's VERIFIED UNSAT' in lines else (q.stdout+q.stderr)[-200:]
    rec['verdict']='VERIFIED' if rec['cake']=='s VERIFIED UNSAT' else ('SAT' if rec['rc']==10 else 'NOT_VERIFIED')
    for f in (cnf,prf):
        if rec['verdict']=='SAT' and f==cnf: continue
        try: os.remove(f)
        except FileNotFoundError: pass
    with lock:
        with open(out,'a') as f: f.write(json.dumps(rec)+'\n')
with ThreadPoolExecutor(jobs) as ex: list(ex.map(run,todo))
print('DONE')
