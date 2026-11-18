#!/usr/bin/env python3
"""Bounded Z3 coordinate finder. Only an integer sign replay accepts a witness."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path
import re
import resource
import subprocess
import time


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def formula(signs, seconds):
    triples = list(combinations(range(16), 3))
    anchor = -1 if signs[triples.index((0, 1, 15))] == '+' else 1
    rows = ['(set-logic QF_NRA)', '(set-option :produce-models true)',
            '(set-option :pp.decimal true)', '(set-option :pp.decimal_precision 60)',
            f'(set-option :timeout {int(seconds * 1000)})']
    for i in range(16):
        rows += [f'(declare-const x{i} Real)', f'(declare-const y{i} Real)']
    rows += ['(assert (= x0 0))', '(assert (= y0 0))',
             '(assert (= x15 1))', '(assert (= y15 0))', f'(assert (= y1 {anchor}))']
    for i in range(15):
        rows.append(f'(assert (< x{i} x{i+1}))')
    for (i, j, k), s in zip(triples, signs):
        det = f'(- (* (- x{j} x{i}) (- y{k} y{i})) (* (- y{j} y{i}) (- x{k} x{i})))'
        rows.append(f'(assert ({">" if s == "+" else "<"} {det} 0))')
    rows += ['(check-sat)', '(get-value (' + ' '.join(f'{a}{i}' for i in range(16) for a in ('x', 'y')) + '))']
    return '\n'.join(rows) + '\n'


def sexprs(s):
    tok = re.findall(r'\(|\)|[^\s()]+', s)
    stack = []; result = []
    for t in tok:
        if t == '(':
            new = []
            (stack[-1] if stack else result).append(new)
            stack.append(new)
        elif t == ')':
            if stack: stack.pop()
        else:
            (stack[-1] if stack else result).append(t)
    return result


def number(x):
    if isinstance(x, str): return Fraction(x.rstrip('?'))
    if x[0] == '-' and len(x) == 2: return -number(x[1])
    if x[0] == '/' and len(x) == 3: return number(x[1]) / number(x[2])
    raise ValueError('model number not rational/decimal: ' + repr(x))


def integers_from_output(s, signs):
    expressions = sexprs(s)
    values = {}
    for exp in expressions:
        if isinstance(exp, list):
            for pair in exp:
                if isinstance(pair, list) and len(pair) == 2 and re.fullmatch('[xy][0-9]+', str(pair[0])):
                    values[pair[0]] = number(pair[1])
    if len(values) != 32: return None
    scale = {a: math.lcm(*(values[f'{a}{i}'].denominator for i in range(16))) for a in ('x', 'y')}
    P = [[int(values[f'{a}{i}'] * scale[a]) for a in ('x', 'y')] for i in range(16)]
    if not all(P[i][0] < P[i+1][0] for i in range(15)): return None
    ds = [(P[j][0]-P[i][0])*(P[k][1]-P[i][1])-(P[j][1]-P[i][1])*(P[k][0]-P[i][0])
          for i,j,k in combinations(range(16),3)]
    if not all(d != 0 and (d > 0) == (s == '+') for d,s in zip(ds,signs)): return None
    return {'P':P, 'minimum_absolute_determinant':min(map(abs,ds)), 'integer_signs_checked':560}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--signs', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--seconds', type=int, default=720)
    args = ap.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (600 << 20, 600 << 20))
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    signs = args.signs.read_text().strip()
    assert len(signs) == 560 and set(signs) <= {'+', '-'}
    (args.out/'source.py').write_bytes(Path(__file__).read_bytes())
    (args.out/'orientation.signs').write_bytes(args.signs.read_bytes())
    (args.out/'input.smt2').write_text(formula(signs,args.seconds))
    command = ['/usr/bin/z3','-smt2', '-memory:440',f'-T:{args.seconds+2}',str(args.out/'input.smt2')]
    metadata = {'label':'COMPUTED solver search; exact replay required', 'command':command,
                'started_utc':datetime.now(timezone.utc).isoformat(), 'signs_sha256':sha(args.signs),
                'source_sha256':sha(__file__), 'input_sha256':sha(args.out/'input.smt2'),
                'normalization':'p0=(0,0), p15=(1,0), y1=-sign(0,1,15); x strictly increasing',
                'seconds':args.seconds, 'memory_limit_mib':440,'address_space_mib':600,'threads':1}
    (args.out/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    # Independent controls of serialization/parser and exact acceptance.
    P = [[i, i*i] for i in range(16)]
    fake = 'sat\n(' + ' '.join(f'({a}{i} {P[i][k]})' for i in range(16) for k,a in enumerate(('x','y'))) + ')'
    assert integers_from_output(fake,'+'*560)['integer_signs_checked'] == 560
    assert integers_from_output(fake,'-'+'+'*559) is None
    (args.out/'controls.json').write_text(json.dumps({'exact_positive_control':'16-point parabola',
                                                     'single_flipped_sign_rejected':True},indent=2)+'\n')
    timed_out = False
    with (args.out/'z3.log').open('w') as log:
        try:
            completed = subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=args.seconds+5)
            rc = completed.returncode
        except subprocess.TimeoutExpired:
            timed_out=True;rc=None
    output=(args.out/'z3.log').read_text()
    candidate=None;parse_error=None
    if re.search(r'^sat$',output,re.M):
        try: candidate=integers_from_output(output,signs)
        except Exception as e: parse_error=repr(e)
    if candidate:
        candidate.update(label='COMPUTED exact integer realization',m=16,n=7,method='Z3 rational/decimal model plus integer replay',
                         signs_sha256=sha(args.signs),source_sha256=sha(__file__))
        (args.out/'witness.json').write_text(json.dumps(candidate,indent=2)+'\n')
        (args.out/'witness.points').write_text('16 7\n'+''.join(f'{x} {y}\n' for x,y in candidate['P']))
        print('EXACT_INTEGER_REALIZATION',flush=True)
    done={'status':'EXACT_INTEGER_REALIZATION' if candidate else 'NO_VERIFIED_WITNESS',
          'solver_response':next((s for s in ('sat','unsat','unknown','timeout') if re.search(r'^'+s+r'$',output,re.M)),None),
          'returncode':rc,'outer_timeout':timed_out,'parse_error':parse_error,'seconds':time.monotonic()-start,
          'peak_child_rss_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
          'exact_acceptance':candidate is not None,
          'scope':'Unsuccessful solver search supplies no nonrealizability certificate.'}
    (args.out/'DONE.json').write_text(json.dumps(done,indent=2)+'\n')
    print(json.dumps(done),flush=True)


if __name__ == '__main__': main()
