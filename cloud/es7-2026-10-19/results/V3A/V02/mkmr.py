import json,sys
acc=set()
for i,l in enumerate(open(sys.argv[1])):
    f=l.rstrip('\n').split('\t')
    if i==0: assert f[0]=='case' and f[7]=='result'; continue
    if f[7]=='ACCEPTED': acc.add(f[0])
out=[];cases=set();rm=0
for l in open('/opt/work/M.jsonl'):
    r=json.loads(l)
    if r['case'] in acc: rm+=1; continue
    r['idx']=len(out); out.append(r); cases.add(r['case'])
with open('/opt/work/Mr.jsonl','w') as f:
    for r in out: f.write(json.dumps(r)+'\n')
print('accepted cases',len(acc),'removed records',rm,'n',len(out),'cases',len(cases))
