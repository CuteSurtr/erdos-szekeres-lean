import json,re,sys
acc=set()
for i,l in enumerate(open(sys.argv[1])):
    f=l.rstrip('\n').split('\t')
    if i>0 and f[-1]=='ACCEPTED': acc.add(f[0])
out=open('/opt/work/Mr.jsonl','w'); n=0; cases=set(); drop=0
for l in open('/opt/work/M.jsonl'):
    r=json.loads(l)
    if r['case'] in acc: drop+=1; continue
    m=re.match(r'^\{"idx": \d+, ',l); assert m
    nl='{"idx": %d, '%n + l[m.end():]
    r2=json.loads(nl); r['idx']=n; assert r2==r
    out.write(nl); n+=1; cases.add(r['case'])
print("accepted cases",len(acc),"records dropped",drop,"n",n,"cases",len(cases))
