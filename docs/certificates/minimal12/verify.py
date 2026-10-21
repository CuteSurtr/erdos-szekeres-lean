#!/usr/bin/env python3
"""Offline exact proof replay for certificate.json.

Python standard library only; no external programs or packages are required. All 220 orientation signs come from coordinate overlaps.
"""
from pathlib import Path
from collections import Counter
import argparse,copy,hashlib,itertools,json

class InvalidCertificate(ValueError):
    pass

def require(condition,message):
    if not condition:
        raise InvalidCertificate(message)

def determinant(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def parity(t):
    return -1 if sum(t[i]>t[j] for i in range(3) for j in range(i+1,3))%2 else 1

def gp_terms(a,b,c,d,e):
    return [((a,b,c),(a,d,e),1),
            ((a,b,d),(a,c,e),-1),
            ((a,b,e),(a,c,d),1)]

def verify(data):
    V=tuple(data['labels']);ground=set(V)
    require(len(V)==12 and len(ground)==12 and list(V)==sorted(V),'Need 12 distinct sorted labels.')
    require(all(type(v) is int for v in V),'Labels must be integers.')
    triples=list(itertools.combinations(V,3));derived={};witnesses=[];comparisons=0
    supplied=data['deletion_witnesses']
    require(len(supplied)==4 and len({w['omitted'] for w in supplied})==4,'Need 4 distinct deletion witnesses.')
    for witness in supplied:
        omitted=witness['omitted'];rows=witness['points']
        require(omitted in ground and len(rows)==11,'Invalid omitted label or witness size.')
        require(all(len(r)==3 and all(type(x) is int for x in r) for r in rows),'Coordinates must be integer triples label,x,y.')
        coords={r[0]:(r[1],r[2]) for r in rows}
        require(len(coords)==11 and set(coords)==ground-{omitted},'Wrong deletion labels.')
        margin=None
        for t in itertools.combinations(sorted(coords),3):
            value=determinant(*(coords[v] for v in t))
            require(value!=0,'A coordinate witness has a collinear triple.')
            s=1 if value>0 else -1
            require(t not in derived or derived[t]==s,'Coordinate witnesses disagree on an overlapping triple.')
            derived[t]=s;comparisons+=1
            margin=abs(value) if margin is None else min(margin,abs(value))
        witnesses.append({'omitted':omitted,'coordinates':coords,'minimum_absolute_determinant':margin})
    require(set(derived)==set(triples),'The coordinate overlaps do not cover all 220 triples.')
    def chi(t):
        return 0 if len(set(t))<3 else parity(t)*derived[tuple(sorted(t))]

    # Build and verify the supplied permutations without any original model.
    sym=data['symmetries'];tau=dict(zip(V,sym['c3_images']));rho=dict(zip(V,sym['reflection_images']))
    require(len(sym['c3_images'])==12 and set(tau.values())==ground,'Invalid C3 permutation.')
    require(len(sym['reflection_images'])==12 and set(rho.values())==ground,'Invalid reflection permutation.')
    identity={v:v for v in V}
    def compose(p,q):return {v:p[q[v]] for v in V}
    tau2=compose(tau,tau)
    require(compose(tau2,tau)==identity and all(tau[v]!=v for v in V),'C3 must be free of order 3.')
    require(compose(rho,rho)==identity and rho!=identity,'Reflection must be a nontrivial involution.')
    require(compose(compose(rho,tau),rho)==tau2,'The dihedral relation fails.')
    for t in triples:
        require(chi(tuple(tau[v] for v in t))==chi(t),'C3 does not preserve the derived signs.')
        require(chi(tuple(rho[v] for v in t))==-chi(t),'Reflection does not reverse the derived signs.')
    powers=[identity,tau,tau2];group=[p for k in powers for p in (k,compose(k,rho))]
    keys={tuple(g[v] for v in V) for g in group}
    require(len(keys)==6,'Need six distinct group elements.')
    require(all(tuple(compose(g,h)[v] for v in V) in keys for g in group for h in group),'Group closure fails.')

    # Explicitly realize every one-point deletion by relabeling a supplied column.
    deletions={};translated_checks=0
    for witness in witnesses:
        for phase,p in enumerate(powers):
            omitted=p[witness['omitted']]
            coords={p[v]:xy for v,xy in witness['coordinates'].items()}
            require(omitted not in deletions and set(coords)==ground-{omitted},'Deletion orbit coverage fails.')
            values=[chi(t)*determinant(*(coords[v] for v in t)) for t in itertools.combinations(sorted(coords),3)]
            require(len(values)==165 and min(values)>0,'A relabeled deletion fails an orientation.')
            translated_checks+=len(values)
            deletions[omitted]={'omitted':omitted,'source_omitted':witness['omitted'],'phase':phase,
                'coordinates':[[v,*coords[v]] for v in sorted(coords)],'minimum_signed_determinant':min(values)}
    require(set(deletions)==ground,'Not all twelve deletions are covered.')

    # Full rank-three exchange axiom. Repeated triples have chi=0 and are automatic.
    # Swapping i2,i3 or permuting j multiplies every exchange term by a common
    # sign, so increasing i2<i3 and increasing j cover all remaining cases.
    cache={t:chi(t) for t in itertools.product(V,repeat=3)};exchange_checks=0
    for i1 in V:
        for i2,i3 in itertools.combinations([v for v in V if v!=i1],2):
            for j in triples:
                terms=[-cache[i1,i2,i3]*cache[j]]
                for k in range(3):
                    replaced=list(j);replaced[k]=i1
                    terms.append(cache[j[k],i2,i3]*cache[tuple(replaced)])
                require(set(terms)-{0}=={-1,1},'Rank-three chirotope exchange axiom fails.')
                exchange_checks+=1

    circuits={};nonconvex={}
    for q in itertools.combinations(V,4):
        a,b,c,d=q;signs=(-cache[b,c,d],cache[a,c,d],-cache[a,b,d],cache[a,b,c])
        require(len(set(signs))==2,'A positive circuit violates acyclicity.')
        circuits[q]=signs
        if signs.count(1)!=2:
            minority=1 if signs.count(1)==1 else -1
            nonconvex[q]=q[signs.index(minority)]
    seven_checks=0
    for seven in itertools.combinations(V,7):
        require(any(q in nonconvex for q in itertools.combinations(seven,4)),'An abstract convex seven exists.')
        seven_checks+=1
    six=tuple(sorted(data['convex_six_witness']))
    require(len(six)==6 and len(set(six))==6 and set(six)<=ground,'Invalid convex-six witness.')
    require(all(q not in nonconvex for q in itertools.combinations(six,4)),'The six-point witness is not convex.')

    # Four seed GP inequalities, each lifted through the six permutations.
    seeds=data['gp_seeds'];require(len(seeds)==4,'Need the four seed inequalities.')
    upper=Counter();lower=Counter();lifted=[];sign_brackets=set()
    for seed in seeds:
        labels=(seed['anchor'],*seed['others'])
        require(len(labels)==5 and len(set(labels))==5 and set(labels)<=ground,'Invalid GP relation labels.')
        big,small=seed['larger_term'],seed['smaller_term']
        require(big in range(3) and small in range(3) and big!=small,'Invalid GP term indices.')
        original=gp_terms(*labels)
        for g in group:
            terms=[(tuple(g[v] for v in t),tuple(g[v] for v in u),c) for t,u,c in original]
            signs=[c*chi(t)*chi(u) for t,u,c in terms]
            require(len(set(signs))==2 and signs.count(signs[big])==1 and signs[small]!=signs[big],
                    'A proposed strict comparison lacks the required minority sign.')
            lhs=[tuple(sorted(t)) for t in terms[big][:2]]
            rhs=[tuple(sorted(t)) for t in terms[small][:2]]
            upper.update(lhs);lower.update(rhs)
            for t,u,c in terms:sign_brackets.update((tuple(sorted(t)),tuple(sorted(u))))
            lifted.append({'larger_absolute_brackets':lhs,'smaller_absolute_brackets':rhs,'gp_term_signs':signs})
    require(upper==lower and sum(upper.values())>0,'The product factors do not cancel individually.')
    require(set().union(*(set(t) for t in upper))==ground,'The proof support differs from the twelve labels.')
    sign_table=[[*t,derived[t]] for t in triples]
    sign_hash=hashlib.sha256(json.dumps(sign_table,separators=(',',':')).encode()).hexdigest()
    return {'verified':True,'coordinate_overlap_comparisons':comparisons,'derived_orientation_triples':len(derived),
        'derived_sign_table_sha256':sign_hash,'derived_chirotope':sign_table,
        'representative_margins':[[w['omitted'],w['minimum_absolute_determinant']] for w in witnesses],
        'all_twelve_deletions':[deletions[v] for v in V],'translated_deletion_determinants':translated_checks,
        'rank3_exchange_checks':exchange_checks,'acyclic_circuits_checked':len(circuits),
        'seven_subsets_checked':seven_checks,'abstract_convex_sevens':0,'convex_six_witness':six,
        'group_size':len(group),'gp_seed_inequalities':len(seeds),'lifted_gp_inequalities':len(lifted),
        'distinct_product_brackets':len(upper),'factors_on_each_side':sum(upper.values()),
        'individual_sign_brackets_used':len(sign_brackets),'exact_individual_factor_cancellation':True,
        'lifted_inequalities':lifted,
        'theorem':'A uniform acyclic rank-three twelve-point oriented matroid with no convex seven is nonrealizable, while every proper restriction is realized by integer coordinates. Every proper minor is realizable as well: any minor involving a contraction has rank at most 2.'}

def negative_controls(data):
    mutants=[]
    duplicate=copy.deepcopy(data)
    duplicate['deletion_witnesses'][0]['points'][0][1:]=duplicate['deletion_witnesses'][0]['points'][1][1:]
    mutants.append(('duplicate_coordinate',duplicate))
    reflection=copy.deepcopy(data)
    for row in reflection['deletion_witnesses'][0]['points']:row[2]=-row[2]
    mutants.append(('reflect_one_witness',reflection))
    changed=copy.deepcopy(data);seed=changed['gp_seeds'][0]
    seed['smaller_term']=next(i for i in range(3) if i not in (seed['larger_term'],seed['smaller_term']))
    mutants.append(('change_one_GP_comparison',changed))
    outcomes=[]
    for name,mutant in mutants:
        try:verify(mutant)
        except InvalidCertificate as error:outcomes.append({'mutation':name,'rejected':True,'reason':str(error)})
        else:raise InvalidCertificate('Negative control was accepted: '+name)
    return outcomes

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate',type=Path,nargs='?',default=Path(__file__).with_name('certificate.json'))
    parser.add_argument('--out',type=Path,help='Optional complete replay report, including the derived sign table.')
    parser.add_argument('--self-test',action='store_true',help='Also reject three deliberately corrupted certificates.')
    args=parser.parse_args();raw=args.certificate.read_bytes();data=json.loads(raw);report=verify(data)
    report['portable_certificate_sha256']=hashlib.sha256(raw).hexdigest()
    if args.self_test:report['negative_controls']=negative_controls(data)
    if args.out:args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('derived_chirotope','all_twelve_deletions','lifted_inequalities')},indent=2))

if __name__=='__main__':main()
