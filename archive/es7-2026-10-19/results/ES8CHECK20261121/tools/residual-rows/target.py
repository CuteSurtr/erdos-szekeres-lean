from lp_slices import *
R=base+extra
FA2=[i for i,s in enumerate(S) if s[0]>=5 and s[3]>=2]
F4=[i for i,s in enumerate(S) if s[0]>=5 and s[3]>=4]
print('|F&A2|',len(FA2),'|F&f4>=4|',len(F4))
for T in (19,20,21):
    rows=R+[(T,F),(36-T,Lo)]
    out=[]
    for d in (10,11,12,13):
        out.append((d, round(lp(rows+[(d,FA2)]),4)))
    print('slice',(T,36-T),'LP with h(F&A2)>=d:',out)
