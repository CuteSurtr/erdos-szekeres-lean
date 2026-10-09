#!/usr/bin/env python3
"""Exploratory LP pruning of the existing tree using the 21 additional rows.
Run from the repository root with optional highspy/numpy installed. Candidate
closures require a positive exact integer margin, but this script is not a
Lean proof. Fixed bounds: 240 seconds, 30,000 LPs, subtrees >=64 leaves.
Output stays under .cache/; existing output there is replaced.
"""
import sys,json,gzip,time
from pathlib import Path
sys.path.insert(0,'scripts')
from omission_row_probe import read_rows
from omission_tree import leaf_margin
from omission_tree_compact import compact_leaf
import highspy,numpy as np
n,old=read_rows(json.loads(gzip.decompress(Path('experiments/omission-residual-geometry-2026-10-09/row-source.json.gz').read_bytes())))
extra=json.loads(Path('experiments/omission-additional-rows-2026-10-10.json').read_text())
rows=old+[(C,1) for C in extra['cycles']]+[(extra['block']['support'],6)]
tree=json.loads(gzip.decompress(Path('experiments/omission-residual-30-2026-10-05.json.gz').read_bytes()))
nodes=tree['nodes']; counts={}
def size(i):
    if i not in counts:
        node=nodes[i];counts[i]=size(node['zero'])+size(node['one']) if node['type']=='branch' else 1
    return counts[i]
size(tree['root'])
h=highspy.Highs();h.setOptionValue('output_flag',False);h.setOptionValue('threads',1)
x=[h.addVariable(lb=0,ub=1,obj=1) for _ in range(n)]
for R,d in rows:h.addConstr(h.qsum(x[v] for v in R)>=d)
stack=[(tree['root'],frozenset(),frozenset())]; found=[]; processed=0;start=time.monotonic()
while stack and time.monotonic()-start<240 and processed<30000:
    i,M,O=stack.pop();node=nodes[i]
    if node['type']!='branch' or counts[i]<64:continue
    h.changeColsBounds(n,np.arange(n,dtype=np.int32),np.array([float(v in M) for v in range(n)]),np.array([float(v not in O) for v in range(n)]))
    h.setOptionValue('time_limit',h.getRunTime()+10);h.run();processed+=1
    sol=h.getSolution();closed=False
    if h.getModelStatus()==highspy.HighsModelStatus.kOptimal and sol.dual_valid:
        for scale in [10**6,10**9]:
            leaf={'type':'weighted','capacity':scale,'weights':[[r,round(w*scale)] for r,w in enumerate(sol.row_dual) if round(w*scale)>0]}
            if leaf_margin(n,rows,30,M,O,leaf)>0:
                leaf=compact_leaf(n,rows,30,M,O,leaf)
                entry={'node':i,'replaced_leaves':counts[i],'leaf':leaf,'missing':sorted(M),'occupied':sorted(O),'margin':leaf_margin(n,rows,30,M,O,leaf),'uses_new_rows':any(r>=len(old) for r,w in leaf['weights'])}
                found.append(entry);closed=True;print('prune',i,counts[i],entry['uses_new_rows'],flush=True);break
    if not closed:
        v=node['vertex'];stack.extend([(node['zero'],M,O|{v}),(node['one'],M|{v},O)])
report={'scope':'Exploratory exact integer checks; not yet a Lean-checked tree','processed_lp_nodes':processed,'seconds':time.monotonic()-start,'remaining_stack':len(stack),'minimum_subtree_leaves':64,'saved_leaves':sum(f['replaced_leaves']-1 for f in found),'prunes':found}
Path('.cache/new-row-lp-pruning-2026-10-10.json').write_text(json.dumps(report,indent=2)+'\n')
print({k:v for k,v in report.items() if k!='prunes'},flush=True)
