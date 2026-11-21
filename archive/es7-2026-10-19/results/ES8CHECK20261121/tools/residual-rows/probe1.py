from lp_slices import *
flat=[i for i,s in enumerate(S) if s[0]==s[1]==s[2]==s[3] and s[0]>=1]
second=[S.index(t) for t in [(1,0,0,0),(1,1,0,0),(1,1,1,0),(1,1,1,1)]]
print('flat',[S[i] for i in flat],'second',[S[i] for i in second])
A2=[i for i,s in enumerate(S) if s[3]>=2]
print('A2 size',len(A2), 'A2&Lo',len([i for i in A2 if i in Lo]))
R=base+extra
for T in (19,20,21):
    rows=R+[(T,F),(36-T,Lo)]
    v,x=lp(rows,retx=True)
    holes=[(S[i],round(x[i],3)) for i in range(N) if x[i]>1e-6]
    print('slice',T,'LP',round(v,6),'flat holes sum',round(sum(x[i] for i in flat),3),'second sum',round(sum(x[i] for i in second),3))
    print('  +flat<=5', round(lp(rows,extra_le=[(5,flat)]),6), ' +second<=3', round(lp(rows,extra_le=[(3,second)]),6), ' both', round(lp(rows,extra_le=[(5,flat),(3,second)]),6))
    # max of flat-hole sum on the optimal face
    for nm,Y in (('flat',flat),('second',second)):
        h=highspy.Highs(); h.setOptionValue('output_flag',False); inf=highspy.kHighsInf
        for i in range(N):
            h.addVar(0.0, 0.0 if i==0 else 1.0); h.changeColCost(i, -1.0 if i in Y else 0.0)
        for rhs,sup in rows: h.addRow(float(rhs),inf,len(sup),np.array(sup,dtype=np.int32),np.ones(len(sup)))
        h.addRow(-inf,36.0,N,np.arange(N,dtype=np.int32),np.ones(N))
        h.run(); print('  max',nm,'hole-sum on {sum h<=36}:', -h.getInfo().objective_function_value, ' min:', end=' ')
        for i in range(N): h.changeColCost(i, 1.0 if i in Y else 0.0)
        h.run(); print(h.getInfo().objective_function_value)
