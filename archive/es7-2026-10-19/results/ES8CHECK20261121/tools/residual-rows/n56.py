from lp_slices import *
R=base+extra
U5=[i for i,s in enumerate(S) if s[0]<=5]; F6=[i for i,s in enumerate(S) if s[0]==6]
print('|f1<=5|',len(U5),'|f1=6|',len(F6))
for c in range(93,101):
    a=lp(base+[(15,Lo),(126-c,U5)]); b=lp(R+[(15,Lo),(126-c,U5)]); d=lp(R+[(15,Lo),(19,F),(126-c,U5)]); e=lp(base+[(126-c,U5)])
    print(f'N56<={c}: LP 2650+row {e:.4f} | 2650+Lo15+row {a:.4f} | +extra {b:.4f} | +extra+F19 {d:.4f}')
