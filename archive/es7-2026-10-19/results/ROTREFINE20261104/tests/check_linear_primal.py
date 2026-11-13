#!/usr/bin/env python3
"""Independently check a rational orientation lift via seed polynomials.

The search coefficient table is not imported. Extract dot/cross coefficients
from direct oblique-coordinate triangle determinants and reconstruct every
polynomial before evaluating the supplied rational lift.
"""
import argparse, hashlib, importlib.util, itertools, json
from fractions import Fraction as F
from pathlib import Path
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--primal',type=Path,required=True)
    ap.add_argument('--model',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();w=json.loads(a.primal.read_text());raw=a.model.read_bytes();positive=set(json.loads(raw))
    if hashlib.sha256(raw).hexdigest()!=w['model_sha256']:raise ValueError('model hash')
    spec=importlib.util.spec_from_file_location('polynomials',Path(__file__).with_name('check_linear_symbolic.py'))
    p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
    values={tuple(key):F(val) for key,val in w['lift']};t=10
    expected={('D',i,j) for i in range(t) for j in range(i,t)}|{('E',i,j) for i in range(t) for j in range(i+1,t)}
    if set(values)!=expected:raise ValueError('lift variables')
    basis={}
    for key in expected:
        kind,i,j=key
        if i==j:basis[key]={(2*i,2*i):F(1),(2*i,2*i+1):F(1),(2*i+1,2*i+1):F(1)}
        elif kind=='D':basis[key]={(2*i,2*j):F(1),(2*i,2*j+1):F(1,2),(2*i+1,2*j):F(1,2),(2*i+1,2*j+1):F(1)}
        else:basis[key]={(2*i,2*j+1):F(1,2),(2*i+1,2*j):F(-1,2)}
    orbits={}
    for q in itertools.combinations(range(6*t),3):
        c=p.canon(q,6)
        if c not in orbits:orbits[c]=len(orbits)+1
    margins=[]
    for q,var in orbits.items():
        poly=p.orient(q,6);coefficients={}
        for i in range(t):
            coefficients[('D',i,i)]=F(poly.get((2*i,2*i),0))
            for j in range(i+1,t):
                d=F(poly.get((2*i,2*j),0));e=2*F(poly.get((2*i,2*j+1),0))-d
                coefficients[('D',i,j)]=d;coefficients[('E',i,j)]=e
        residual=dict(poly)
        for key,co in coefficients.items():residual=p.add(residual,{m:-co*c for m,c in basis[key].items()})
        if residual:raise ValueError('lift does not reconstruct triangle polynomial')
        margin=sum(co*values[key] for key,co in coefficients.items())*(1 if var in positive else -1)
        if margin<=0:raise ValueError('orientation inequality')
        margins.append(margin)
    radius=[values['D',i,i] for i in range(t)]
    if not all(radius[i]>radius[i+1]>0 for i in range(t-1)):raise ValueError('radius ordering')
    # A negative 2x2 Hermitian principal minor suffices to reject this lift.
    # The imaginary part is sqrt(3)*E, so this test uses rational arithmetic.
    negative_minor=None
    for i,j in itertools.combinations(range(t),2):
        minor=values['D',i,i]*values['D',j,j]-values['D',i,j]**2-3*values['E',i,j]**2
        if minor<0:
            negative_minor={'orbits':[i,j],'determinant':str(minor)};break
    if negative_minor is None:raise ValueError('no negative 2x2 minor; this checker has no PSD conclusion')
    out={'model_sha256':w['model_sha256'],'primal_sha256':hashlib.sha256(a.primal.read_bytes()).hexdigest(),
        'method':'independent direct seed polynomials, exact rational lift evaluation',
        'orientation_inequalities_verified':len(margins),'minimum_exact_margin':str(min(margins)),
        'strict_positive_radius_order':True,'this_lift_is_not_psd':True,
        'exact_negative_hermitian_principal_minor':negative_minor,
        'scope':'excludes zero-identity separation of this model; indefiniteness concerns this lift only, not every lift'}
    a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
