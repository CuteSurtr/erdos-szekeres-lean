import sys, json, itertools, time
from multiprocessing import Pool
sys.path.insert(0,'.')
import bfp_cegar2 as B
from modeltest import chi_from_model
if __name__=='__main__':
    chi=chi_from_model(sys.argv[1]); size=int(sys.argv[2]); t0=time.time(); bad=[]
    with Pool(5,initializer=B._init,initargs=(chi,)) as pool:
        for L,r in pool.imap_unordered(B._test,itertools.combinations(range(14),size),chunksize=4):
            if r!='FEAS': bad.append(L); print('bad',L,r,flush=True)
    print('size',size,'bad',len(bad),'of',sum(1 for _ in itertools.combinations(range(14),size)),'%.0fs'%(time.time()-t0),flush=True)
