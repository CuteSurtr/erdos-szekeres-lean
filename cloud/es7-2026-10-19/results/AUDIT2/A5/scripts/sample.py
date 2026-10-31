import json,random
M=[json.loads(l) for l in open('/opt/work/M.jsonl')]
rng=random.Random(20261021)
quota={'U_L2':70,'U3_L':60,'U_L7':50}
S=[]
for c,q in quota.items():
    S+=rng.sample([m for m in M if m['case']==c],q)
S+=rng.sample([m for m in M if m['case'] not in quota],140)
rng.shuffle(S)
with open('/opt/a5/sample.jsonl','w') as f:
    for m in S: f.write(json.dumps({'idx':m['idx'],'case':m['case'],'lits':m['lits']})+'\n')
print(len(S),len({m['case'] for m in S}),'cases')
