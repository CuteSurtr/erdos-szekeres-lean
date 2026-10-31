import sys,json,hashlib,subprocess,random,os
sys.path.insert(0,'/opt/a5'); import cover, mk
nontriv=[c for c,r in cover.cov.items() if 'cnf_sha256' in r]
triv=[c for c,r in cover.cov.items() if 'cnf_sha256' not in r]
# hash comparison for every case
bad=[]
for c,r in cover.cov.items():
    if len(cover.L[c])!=r['nleaves'] or cover.lsha(c)['manifest-json']!=r['leaves_sha256']: bad.append(('leaves',c))
    if c in nontriv:
        d=dict(cover.variants(c))[('47002','manifest',False)]
        if hashlib.sha256(d).hexdigest()!=r['cnf_sha256']: bad.append(('cnf',c))
    else:
        if cover.L[c]!=[[]]: bad.append(('triv-not-empty',c))
print('covers',len(cover.cov),'nontrivial',len(nontriv),'trivial',len(triv),'hash mismatches',bad)
print('cases in covers == cases in manifest:', set(cover.cov)==set(cover.L))
rng=random.Random(20261021)
pick=sorted(nontriv) if len(sys.argv)>1 else ['U_L2','U3_L','U_L7']+rng.sample(sorted(set(nontriv)-{'U_L2','U3_L','U_L7'}),17)
os.makedirs('/opt/a5/cw',exist_ok=True)
with open('/opt/a5/covers_all.jsonl' if len(sys.argv)>1 else '/opt/a5/covers_out.jsonl','w') as f:
    for c in pick:
        d=dict(cover.variants(c))[('47002','manifest',False)]
        p='/opt/a5/cw/c.cnf'; open(p,'wb').write(d)
        s=subprocess.run(['/opt/bin/cadical','-q','--lrat','--no-binary',p,p+'.lrat'],capture_output=True)
        k=subprocess.run(['/opt/bin/cake_lpr',p,p+'.lrat'],capture_output=True,text=True) if s.returncode==20 else None
        v='s VERIFIED UNSAT' in (k.stdout.splitlines() if k else [])
        rec={'kind':'cover','case':c,'nleaves':len(cover.L[c]),'cnf_sha256':hashlib.sha256(d).hexdigest(),'v3_cnf_sha256':cover.cov[c]['cnf_sha256'],'rc':s.returncode,'cake':'s VERIFIED UNSAT' if v else '','verdict':'VERIFIED' if v else 'NOT_VERIFIED'}
        f.write(json.dumps(rec)+'\n'); print(c,rec['nleaves'],rec['verdict'],rec['cnf_sha256']==rec['v3_cnf_sha256'])
