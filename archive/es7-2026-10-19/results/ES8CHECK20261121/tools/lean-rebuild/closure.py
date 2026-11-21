import os,re,sys
root=sys.argv[1]; mods=sys.argv[2:]
def path(m): return os.path.join(root,*m.split('.'))+'.lean'
seen={};order=[]
def visit(m):
    if m in seen: return
    seen[m]=1
    p=path(m)
    if not os.path.exists(p): return
    imps=[]
    for line in open(p,encoding='utf-8'):
        s=line.strip()
        if s.startswith('import '):
            imps+=s.split()[1:]
        elif s and not s.startswith('--') and not s.startswith('/-') and not s.startswith('import') and not s.startswith('module') and not s.startswith('prelude'):
            pass
    for i in imps:
        if i.startswith('ErdosSzekeres'): visit(i)
    order.append((m,os.path.getsize(p)))
for m in mods: visit(m)
tot=0
for m,s in order: tot+=s; print(m,s)
print('count',len(order),'bytes',tot)
