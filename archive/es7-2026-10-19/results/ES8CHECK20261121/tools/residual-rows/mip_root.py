import sys, time
from lp_slices import *
T=int(sys.argv[1]); tl=float(sys.argv[2])
rows=base+extra+[(T,F),(36-T,Lo)]
h=highspy.Highs(); h.setOptionValue('output_flag',False); inf=highspy.kHighsInf
h.setOptionValue('threads',1); h.setOptionValue('time_limit',tl); h.setOptionValue('random_seed',1)
for i in range(N):
    h.addVar(0.0, 0.0 if i==0 else 1.0); h.changeColCost(i,1.0); h.changeColIntegrality(i, highspy.HighsVarType.kInteger)
for rhs,sup in rows: h.addRow(float(rhs),inf,len(sup),np.array(sup,dtype=np.int32),np.ones(len(sup)))
h.addRow(-inf,36.0,N,np.arange(N,dtype=np.int32),np.ones(N))   # feasibility at budget 36
t0=time.time(); h.run(); info=h.getInfo()
print('slice',(T,36-T),'status',h.modelStatusToString(h.getModelStatus()),'dual_bound',info.mip_dual_bound,'primal',info.objective_function_value,'nodes',info.mip_node_count,'time',round(time.time()-t0,1))
