#!/usr/bin/env python3
"""Bounded joint-coordinate realization search; exact integers alone accept.

Distinct from the parent's fixed-random-x LP: anchored relaxed LPs,
alternating x/y LPs, joint SLSQP and smooth-gap L-BFGS-B are combined.
"""
import os
os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
import argparse
from datetime import datetime,timezone
from fractions import Fraction
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path
import resource
import signal
import time
import traceback
import warnings

class StopSearch(Exception):pass


def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def determinant(P,a,b,c):
    return (P[b][0]-P[a][0])*(P[c][1]-P[a][1])-(P[b][1]-P[a][1])*(P[c][0]-P[a][0])


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--signs',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--seconds',type=float,default=2100)
    parser.add_argument('--until',default='2026-11-13T22:44:00+00:00')
    parser.add_argument('--trials',type=int,default=100000)
    parser.add_argument('--seed',type=int,default=202611140707)
    parser.add_argument('--controls',action='store_true')
    args=parser.parse_args()
    resource.setrlimit(resource.RLIMIT_AS,(600<<20,600<<20))
    args.out.mkdir(parents=True,exist_ok=False)
    (args.out/'source.py').write_bytes(Path(__file__).read_bytes())
    (args.out/'orientation.signs').write_bytes(args.signs.read_bytes())
    start=time.monotonic();wall_start=time.time()
    absolute=datetime.fromisoformat(args.until).timestamp()
    cutoff=min(start+args.seconds,start+max(0,absolute-wall_start))
    def deadline(*unused):
        if time.monotonic()>=cutoff:raise StopSearch('driver deadline')
    def stopped(sig,frame):raise StopSearch(f'signal {sig}')
    signal.signal(signal.SIGTERM,stopped)
    import numpy as np
    import scipy
    from scipy.optimize import linprog,minimize,OptimizeWarning
    warnings.filterwarnings('ignore',category=OptimizeWarning)
    m=16;triples=list(combinations(range(m),3));ta=np.array(triples,dtype=int)
    I,J,K=ta.T
    signs=args.signs.read_text().strip();assert len(signs)==len(triples)==560 and set(signs)<={'+','-'}
    S=np.array([1. if s=='+' else -1. for s in signs]);rng=np.random.default_rng(args.seed)
    best={'bad':561,'margin':-1e99};attempts=0;witness=None;accepted_method=None
    metadata={'label':'HEURISTIC search until exact integer acceptance','signs_sha256':digest(args.signs),
              'source_sha256':digest(__file__),'scipy':scipy.__version__,'numpy':np.__version__,
              'seed':args.seed,'started_utc':datetime.now(timezone.utc).isoformat(),
              'seconds_budget':max(0,cutoff-start),'address_space_mib':600,'threads':1,
              'methods':['anchored relaxed LP','alternating x/y LP','joint SLSQP','softmax-gap L-BFGS-B'],
              'scope':'No numerical outcome proves infeasibility or nonrealizability.'}
    (args.out/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    def unpack(z,anchor):
        x=np.r_[0.,z[:14],1.];y=np.zeros(m)
        free=[i for i in range(1,m-1) if i!=anchor]
        y[anchor]=-S[triples.index((0,anchor,m-1))]
        y[free]=z[14:27]
        return x,y,free
    def pack(x,y,anchor,rho=0.):
        free=[i for i in range(1,m-1) if i!=anchor]
        return np.r_[x[1:-1],y[free],rho]
    def vals_jac(x,y,normalized=True):
        d=(x[J]-x[I])*(y[K]-y[I])-(y[J]-y[I])*(x[K]-x[I])
        span=x[K]-x[I]
        scale=np.maximum(span,1e-10) if normalized else np.ones(len(triples))
        values=S*d/scale
        gx=np.zeros((len(triples),m));gy=np.zeros_like(gx);rows=np.arange(len(triples))
        gx[rows,I]=S*(y[J]-y[K])/scale
        gx[rows,J]=S*(y[K]-y[I])/scale
        gx[rows,K]=S*(y[I]-y[J])/scale
        if normalized:
            extra=np.where(span>1e-10,S*d/(scale*scale),0.)
            gx[rows,I]+=extra;gx[rows,K]-=extra
        gy[rows,I]=S*(x[K]-x[J])/scale
        gy[rows,J]=S*(x[I]-x[K])/scale
        gy[rows,K]=S*(x[J]-x[I])/scale
        return values,gx,gy
    def exact(x,y,method,trial):
        nonlocal witness,accepted_method
        if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):return False
        if not np.all(np.diff(x)>0):return False
        for scale in (10**5,10**7,10**9,10**11,10**13,10**15,10**17):
            P=[[int(round(float(a)*scale)),int(round(float(b)*scale))] for a,b in zip(x,y)]
            if not all(P[i][0]<P[i+1][0] for i in range(m-1)):continue
            ds=[determinant(P,*t) for t in triples]
            if all(d and (d>0)==(s=='+') for d,s in zip(ds,signs)):
                xg=math.gcd(*(p[0] for p in P));yg=math.gcd(*(p[1] for p in P))
                P=[[a//max(1,xg),b//max(1,yg)] for a,b in P]
                ds=[determinant(P,*t) for t in triples]
                assert all(d and (d>0)==(s=='+') for d,s in zip(ds,signs))
                witness={'label':'COMPUTED exact integer realization','P':P,'m':m,'n':7,
                         'orientation_signs':signs,'minimum_absolute_determinant':min(map(abs,ds)),
                         'method':method,'trial':trial,'scale':scale,'seconds':time.monotonic()-start,
                         'signs_sha256':digest(args.signs),'source_sha256':digest(__file__)}
                (args.out/'witness.json').write_text(json.dumps(witness,indent=2)+'\n')
                (args.out/'witness.points').write_text('16 7\n'+''.join(f'{a} {b}\n' for a,b in P))
                accepted_method=method
                print(json.dumps({'status':'EXACT_INTEGER_REALIZATION','method':method,'trial':trial,'seconds':witness['seconds']}),flush=True)
                return True
        return False
    def observe(x,y,method,trial,extra=None):
        nonlocal best
        values,_,_=vals_jac(x,y)
        bad=int(np.sum(values<=0));margin=float(np.min(values));ordered=bool(np.all(np.diff(x)>0))
        score=(bad,-margin)
        rec={'trial':trial,'method':method,'bad_signs':bad,'height_margin':margin,
             'ordered_x':ordered,'seconds':round(time.monotonic()-start,3)}
        if extra:rec.update(extra)
        with (args.out/'attempts.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
        if ordered and score<(best['bad'],-best['margin']):
            best={'bad':bad,'margin':margin,'x':x.tolist(),'y':y.tolist(),'trial':trial,'method':method,
                  'seconds':time.monotonic()-start}
            (args.out/'best.json').write_text(json.dumps(best,indent=2)+'\n')
            print(json.dumps({'status':'IMPROVED','bad':bad,'margin':margin,'method':method,'trial':trial}),flush=True)
        return exact(x,y,method,trial)
    def y_lp(x,anchor):
        deadline();span=np.maximum(x[K]-x[I],1e-10)
        A=np.zeros((len(triples),m+1));rows=np.arange(len(triples))
        A[rows,I]=-S*(x[K]-x[J])/span;A[rows,J]=S*(x[K]-x[I])/span;A[rows,K]=-S*(x[J]-x[I])/span
        A[:,-1]=1.;c=np.zeros(m+1);c[-1]=-1
        bounds=[(-1.,1.)]*m+[(-4.,1.)];bounds[0]=bounds[m-1]=(0.,0.)
        v=-S[triples.index((0,anchor,m-1))];bounds[anchor]=(v,v)
        answer=linprog(c,A_ub=A,b_ub=np.zeros(len(triples)),bounds=bounds,method='highs',
                       options={'threads':1,'parallel':False,'time_limit':1.})
        if answer.x is None:return None,answer.status
        return answer.x[:m],answer.status
    def x_lp(x,y,gap):
        deadline();span=np.maximum(x[K]-x[I],1e-10)
        A=np.zeros((len(triples)+m-1,m+1));rows=np.arange(len(triples))
        A[rows,I]=-S*(y[J]-y[K])/span;A[rows,J]=-S*(y[K]-y[I])/span;A[rows,K]=-S*(y[I]-y[J])/span
        A[:len(triples),-1]=1.;b=np.zeros(len(A))
        for i in range(m-1):A[len(triples)+i,i]=1;A[len(triples)+i,i+1]=-1;b[len(triples)+i]=-gap
        c=np.zeros(m+1);c[-1]=-1;bounds=[(0.,1.)]*m+[(-4.,1.)];bounds[0]=(0.,0.);bounds[m-1]=(1.,1.)
        answer=linprog(c,A_ub=A,b_ub=b,bounds=bounds,method='highs',
                       options={'threads':1,'parallel':False,'time_limit':1.})
        if answer.x is None:return None,answer.status
        return answer.x[:m],answer.status
    def slsqp(x,y,anchor,gap,trial):
        normalized=trial%4!=3
        def constraints(z):
            xx,yy,free=unpack(z,anchor);v,_,_=vals_jac(xx,yy,normalized)
            return np.r_[v-z[-1],np.diff(xx)-gap]
        def jacobian(z):
            xx,yy,free=unpack(z,anchor);v,gx,gy=vals_jac(xx,yy,normalized)
            out=np.zeros((len(triples)+m-1,28));out[:len(triples),:14]=gx[:,1:-1]
            out[:len(triples),14:27]=gy[:,free];out[:len(triples),-1]=-1
            for i in range(m-1):
                if i>0:out[len(triples)+i,i-1]=-1
                if i<m-2:out[len(triples)+i,i]=1
            return out
        z=pack(x,y,anchor);z[-1]=float(np.min(constraints(z)[:len(triples)]))-1e-5
        objective=np.zeros(28);objective[-1]=-1
        ans=minimize(lambda zz:-zz[-1],z,jac=lambda zz:objective,method='SLSQP',
                     constraints=[{'type':'ineq','fun':constraints,'jac':jacobian}],
                     bounds=[(0.,1.)]*14+[(-1.,1.)]*13+[(-4.,1.)],callback=deadline,
                     options={'maxiter':300 if trial%3 else 700,'ftol':1e-12,'disp':False})
        xx,yy,_=unpack(ans.x,anchor)
        return xx,yy,{'numeric_status':int(ans.status),'iterations':int(ans.nit),'objective_margin':float(ans.x[-1])}
    def smooth(x,y,anchor,trial):
        free=[i for i in range(1,m-1) if i!=anchor]
        gaps=np.maximum(np.diff(x),1e-10);gaps/=np.sum(gaps)
        z=np.r_[np.log(gaps[:-1]/gaps[-1]),y[free]]
        target=(.03,.003,.0003)[trial%3]
        def function(zz):
            lg=np.r_[zz[:14],0.];gg=np.exp(lg-np.max(lg));gg/=np.sum(gg)
            xx=np.r_[0.,np.cumsum(gg)];yy=np.zeros(m);yy[free]=zz[14:]
            yy[anchor]=-S[triples.index((0,anchor,m-1))]
            vv,gx,gy=vals_jac(xx,yy)
            residual=np.minimum(vv-target,0.)
            loss=float(np.dot(residual,residual));dx=2*residual@gx;dy=2*residual@gy
            correction=float(dx@xx)
            dlog=np.array([gg[h]*(np.sum(dx[h+1:])-correction) for h in range(14)])
            return loss,np.r_[dlog,dy[free]]
        ans=minimize(function,z,method='L-BFGS-B',jac=True,bounds=[(-14.,14.)]*14+[(-1.,1.)]*13,
                     callback=deadline,options={'maxiter':1200,'ftol':1e-15,'gtol':1e-10,'maxls':40})
        zz=ans.x;lg=np.r_[zz[:14],0.];gg=np.exp(lg-np.max(lg));gg/=np.sum(gg)
        xx=np.r_[0.,np.cumsum(gg)];yy=np.zeros(m);yy[free]=zz[14:];yy[anchor]=-S[triples.index((0,anchor,m-1))]
        return xx,yy,{'numeric_status':int(ans.status),'iterations':int(ans.nit),'loss':float(ans.fun),'target':target}
    def controls():
        xx=np.r_[0.,np.cumsum(np.arange(1,16,dtype=float))];xx/=xx[-1]
        yy=rng.uniform(-1,1,m);yy[[0,-1]]=0
        errors=[]
        for normalized in (False,True):
            vv,gx,gy=vals_jac(xx,yy,normalized)
            for axis in (0,1):
                for i in range(1,m-1):
                    xp=xx.copy();xm=xx.copy();yp=yy.copy();ym=yy.copy();h=1e-7
                    if axis==0:xp[i]+=h;xm[i]-=h
                    else:yp[i]+=h;ym[i]-=h
                    vp,_,_=vals_jac(xp,yp,normalized);vm,_,_=vals_jac(xm,ym,normalized)
                    error=float(np.max(np.abs((vp-vm)/(2*h)-(gx[:,i] if axis==0 else gy[:,i]))))
                    assert error<1e-5,error;errors.append(error)
        return {'analytic_jacobian_tests':len(errors),'max_absolute_error':max(errors)}
    status='NO_VERIFIED_WITNESS';stopreason=None
    try:
        control=controls();(args.out/'controls.json').write_text(json.dumps(control,indent=2)+'\n')
        for trial in range(args.trials):
            deadline();attempts=trial+1;anchor=1+trial%14;gap=(1e-6,1e-8,1e-10)[(trial//14)%3]
            if trial%5==4 and 'x' in best:
                x=np.array(best['x']);y=np.array(best['y'])
                anchor=int(np.argmax(np.abs(y[1:-1])))+1;y=y/max(1e-12,abs(y[anchor]))
                if trial%10==9:
                    gg=np.maximum(np.diff(x),1e-10)*np.exp(rng.normal(0,.3,15));x=np.r_[0.,np.cumsum(gg)/np.sum(gg)]
            else:
                gg=np.ones(15) if trial<14 else np.exp(rng.normal(0,1+(trial//14)%5,15))
                x=np.r_[0.,np.cumsum(gg)/np.sum(gg)];y,code=y_lp(x,anchor)
                if y is None:continue
            if observe(x,y,'anchored-LP-start',trial):status='EXACT_INTEGER_REALIZATION';break
            if trial%2==0:
                for j in range(3):
                    xx,code=x_lp(x,y,gap)
                    if xx is None:break
                    yy,code=y_lp(xx,anchor)
                    if yy is None:break
                    x,y=xx,yy
                if observe(x,y,'alternating-LP',trial):status='EXACT_INTEGER_REALIZATION';break
            if trial%3==1:
                x,y,info=smooth(x,y,anchor,trial)
                if observe(x,y,'softmax-gap-LBFGS',trial,info):status='EXACT_INTEGER_REALIZATION';break
            x,y,info=slsqp(x,y,anchor,gap,trial)
            if observe(x,y,'joint-SLSQP',trial,info):status='EXACT_INTEGER_REALIZATION';break
            (args.out/'status.json').write_text(json.dumps({'status':'SEARCHING','trials':attempts,'seconds':time.monotonic()-start,'best':best})+'\n')
    except StopSearch as e:stopreason=str(e)
    except BaseException:
        status='FAILED';stopreason=traceback.format_exc();raise
    finally:
        out={'status':status,'label':'COMPUTED exact coordinates' if witness else 'HEURISTIC unresolved',
             'trials':attempts,'seconds':time.monotonic()-start,'best':best,'stop_reason':stopreason,
             'exact_acceptance':witness is not None,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'scope':'No infeasibility or nonrealizability conclusion from failed numerics.'}
        (args.out/'DONE.json').write_text(json.dumps(out,indent=2)+'\n')
        print(json.dumps(out),flush=True)


if __name__=='__main__':main()
