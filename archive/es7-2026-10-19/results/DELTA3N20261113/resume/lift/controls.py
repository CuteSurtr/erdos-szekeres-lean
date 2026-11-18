#!/usr/bin/env python3
"""Bounded independent controls for new embedding clauses and exact geometry.

No imports from the old encoder, old geometry audit, or old model checker.
The new CNF under test is evaluated literally using audit_extension.py.
"""
import argparse
from itertools import combinations, product
import json
from pathlib import Path
import resource
import subprocess
import time

from audit_extension import check_clauses, digest, geometry, load_source, orientations

HERE = Path(__file__).resolve().parent
SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/resume/lift')
SOURCE = HERE/'../../coordinator/data/cup15/realized.json'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--binary', type=Path, default=SCRATCH/'extension_cnf')
    args = ap.parse_args()
    if not args.out.resolve().is_relative_to(SCRATCH):
        raise ValueError('output outside assigned scratch')
    args.out.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    result = {'label': 'COMPUTED', 'status': 'STARTED', 'controls': {}}

    def save():
        (args.out/'report.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')

    def encode(name, old_signs, old_m, added, base_only=False):
        old_file = args.out/(name+'.signs')
        old_file.write_text(old_signs+'\n')
        cnf = args.out/(name+'.cnf')
        command = [str(args.binary),'--old-signs',str(old_file),'--old-size',str(old_m),
                   '--add',str(added),'--n','7',
                   '--base-only' if base_only else '--embedding-only','--out',str(cnf)]
        run = subprocess.run(command,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=8)
        (args.out/(name+'.stdout')).write_text(run.stdout)
        (args.out/(name+'.stderr')).write_text(run.stderr)
        if run.returncode:
            raise ValueError(f'encoder failed for {name}')
        meta = json.loads(run.stdout)
        return cnf, meta

    def assignment(meta, signs, positions):
        vals = bytearray([1])*(meta['variables']+1)
        for i,s in enumerate(signs,1):
            vals[i] = 2 if s == '+' else 1
        for i,pos in enumerate(positions):
            vals[meta['selector_ids'][i][pos-i]] = 2
        return vals

    def accepted(cnf, vals):
        try:
            check_clauses(cnf,vals)
            return True
        except ValueError as exc:
            if str(exc).startswith('unsatisfied clause'):
                return False
            raise

    save()
    try:
        # Exhaust every possible orientation assignment and every valid old
        # embedding, independent of signotope realizability. 10,240 cases.
        cnf, meta = encode('small-exhaustive','-',3,2)
        triples = list(combinations(range(5),3))
        tri_id = {q:i for i,q in enumerate(triples)}
        placements = list(combinations(range(5),3))
        checks = accepts = 0
        for row in product('+-',repeat=len(triples)):
            signs = ''.join(row)
            for positions in placements:
                actual = accepted(cnf,assignment(meta,signs,positions))
                expected = row[tri_id[positions]] == '-'
                if actual != expected:
                    raise ValueError('embedding clauses disagree with literal old triple')
                checks += 1
                accepts += actual
        # Invalid selector rows: missing, double, and order reversal.
        vals = assignment(meta,'-'*10,(0,1,2))
        bad = []
        absent = bytearray(vals); absent[meta['selector_ids'][0][0]]=1; bad.append(absent)
        double = bytearray(vals); double[meta['selector_ids'][0][1]]=2; bad.append(double)
        reverse = assignment(meta,'-'*10,(2,1,2)); bad.append(reverse)
        if any(accepted(cnf,x) for x in bad):
            raise ValueError('bad selector accepted')
        result['controls']['exhaustive_embedding'] = {
            'checks': checks,'accepted':accepts,'rejected':checks-accepts,
            'invalid_selector_cases_rejected':len(bad),'cnf_sha256':digest(cnf)}
        save()

        # Actual integer parabola points; every placement of four old points
        # is a copy of the fixed all-positive four-point order type.
        points = [[i,i*i] for i in range(7)]
        signs, margin = orientations(points)
        cnf, meta = encode('parabola7','++++',4,3)
        count = 0
        for positions in combinations(range(7),4):
            check_clauses(cnf,assignment(meta,signs,positions))
            count += 1
        result['controls']['integer_parabola_all_gaps'] = {
            'P':points,'embeddings':count,'minimum_abs_determinant':margin,
            'cnf_sha256':digest(cnf)}
        save()

        old, old_signs, margin = load_source(SOURCE)
        (args.out/'cup15.signs').write_text(old_signs+'\n')
        original = geometry(old_signs,15,6,'cup',old)
        if (original['fourcaps'], original['fivecaps'], original['convex_ngons'],
            original['target_polygons'],original['targets'],original['working_deltas']) != (80,0,0,216,103,0):
            raise ValueError('source geometry differs from recorded facts')
        result['controls']['original_exact_geometry'] = {
            **original,'source_sha256':digest(SOURCE),'minimum_abs_determinant':margin}
        save()

        # A valid real extension: duplicate the left extreme in a very low
        # direction. This tests the actual n7 base plus all embedding clauses,
        # with all clause values determined by integer coordinates.
        E = 1 << 256
        one_added = [[x*E,y*E] for x,y in old]+[[1,-10**16]]
        one_added.sort()
        osigns, omargin = orientations(one_added)
        opositions = [0]+list(range(2,16))
        cnf, meta = encode('valid-source16',old_signs,15,1,base_only=True)
        literal_check = check_clauses(cnf,assignment(meta,osigns,opositions))
        og = geometry(osigns,16,7,'cup',one_added)
        if not og['valid'] or not og['targets'] or not og['working_deltas']:
            raise ValueError('source16 extension not a nonvacuous positive control')
        (args.out/'valid-source16.json').write_text(json.dumps({
            'P':one_added,'m':16,'n':7,'signs':osigns,'old_positions':opositions},indent=2)+'\n')
        result['controls']['valid_real_one_insertion_base'] = {
            'geometry':og,'literal_clause_check':literal_check,
            'minimum_abs_determinant':omargin,'old_positions':opositions,
            'cnf_sha256':digest(cnf),'fixture_sha256':digest(args.out/'valid-source16.json')}
        save()

        # An exact interacting secant tie embedded in the source. D is chosen
        # large; all claims below are checked, not assumed from its magnitude.
        D = 1 << 128
        scale = D**3
        length = old[-1][0]
        tagged = [(tuple(scale*c for c in p),('old',i)) for i,p in enumerate(old)]
        tagged += [((length*D*D,length),('new','p1')),
                   ((length*(scale+D*D),length*D*D),('new','q1')),
                   ((2*length*scale,3*length*scale),('new','nonlocal'))]
        tagged.sort()
        P = [list(p) for p,tag in tagged]
        positions = [next(j for j,(_,tag) in enumerate(tagged) if tag==('old',i)) for i in range(15)]
        (args.out/'secant-input.json').write_text(json.dumps({'P':P,'old_positions':positions},indent=2)+'\n')
        signs, new_margin = orientations(P)
        lookup = dict(zip(combinations(range(18),3),signs))
        p0 = positions[0]
        p1 = next(j for j,(_,tag) in enumerate(tagged) if tag==('new','p1'))
        q0 = positions[14]
        q1 = next(j for j,(_,tag) in enumerate(tagged) if tag==('new','q1'))
        if (lookup[p0,p1,q0],lookup[p0,p1,q1]) != ('-','+'):
            raise ValueError('aligned signs did not split')
        cnf, meta = encode('secant-source18',old_signs,15,3)
        clause_counts = check_clauses(cnf,assignment(meta,signs,positions))
        retrieved = ''.join(lookup[tuple(positions[i] for i in t)] for t in combinations(range(15),3))
        if retrieved != old_signs:
            raise ValueError('source copy changed')
        # Check every representative choice for triples of distinct old fibers.
        fibers = [[v] for v in positions]
        fibers[0].append(p1); fibers[14].append(q1)
        representative_triples = 0
        for tri, old_sign in zip(combinations(range(15),3),old_signs):
            for reps in product(*(fibers[i] for i in tri)):
                if lookup[tuple(reps)] != old_sign:
                    raise ValueError('distinct-fiber orientation changed')
                representative_triples += 1
        secant_geometry = geometry(signs,18,7,'cup',P)
        fixture = {'P':P,'m':18,'n':7,'signs':signs,'old_positions':positions,
                   'D':str(D),'p_pair':[p0,p1],'q_pair':[q0,q1],
                   'label':'COMPUTED','purpose':'scope control, not a counterexample'}
        (args.out/'secant-source18.json').write_text(json.dumps(fixture,indent=2)+'\n')
        result['controls']['interacting_secant_exact_integers'] = {
            'old_positions':positions,'pair_third_signs':['-','+'],
            'minimum_abs_determinant':new_margin,'distinct_fiber_triples_checked':representative_triples,
            'literal_clause_check':clause_counts,'geometry':secant_geometry,
            'cnf_sha256':digest(cnf),'fixture_sha256':digest(args.out/'secant-source18.json')}

        # Nonvacuous exact control of the five-insertion weak-n8 theorem:
        # A has a four-cap, but deleting one of its vertices removes it.
        A = [[0,0],[1,-1],[2,-4],[3,-9],[4,100]]
        old5 = [[x,10000*(x-4)**2+100] for x in range(10,15)]
        Q = A+old5
        qs, qmargin = orientations(Q)
        qt = dict(zip(combinations(range(10),3),(s=='+' for s in qs)))
        def cap(s):
            return all(not qt[t] for t in combinations(s,3))
        if not cap((0,1,2,3)) or any(cap(s) for s in combinations(range(10),5)):
            raise ValueError('five-insertion control does not have intended caps')
        R = next(s for s in combinations(range(5),4) if not cap(s))
        heptagons = []
        for g in combinations(range(10),7):
            if all(qt[a,b,c] == qt[a,b,d] and qt[a,c,d] == qt[b,c,d]
                   for a,b,c,d in combinations(g,4)):
                if len(set(g)&set(range(5)))<2 or not set(g)&set(R):
                    raise ValueError('weak-n8 theorem control failed')
                heptagons.append(list(g))
        if not heptagons:
            raise ValueError('vacuous weak-n8 control')
        result['controls']['weak_n8_five_insertion_theorem'] = {
            'P':Q,'old_indices':list(range(5,10)),'added_indices':list(range(5)),
            'fourcap_in_added':[0,1,2,3],'weak_delta':list(R),
            'fivecaps':0,'old_hexagons':0,'heptagons_checked':len(heptagons),
            'minimum_abs_determinant':qmargin}
        result['status'] = 'PASSED'
    except Exception as exc:
        result['status'] = 'FAILED'
        result['error'] = repr(exc)
        raise
    finally:
        result['elapsed_seconds'] = round(time.monotonic()-started,3)
        result['max_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        save()
    print(json.dumps({'status':result['status'],'report':str(args.out/'report.json')}))


if __name__ == '__main__':
    main()
