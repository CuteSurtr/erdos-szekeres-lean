#!/usr/bin/env python3
"""Bounded fivefold orientation-split pilot and exact cyclotomic validation.

Use --prepare before --run. Inputs and generated CNFs remain in --archive.
No solving occurs in --prepare. No proof verdict is certified by this pilot.
"""
import argparse
import collections
import functools
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
LOG = HERE / 'logs'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def archived(path):
    raw = sha(path)
    compressed = path.with_name(path.name + '.zst')
    subprocess.run(['zstd', '-q', '-T1', '-f', str(path), '-o', str(compressed)], check=True)
    p = subprocess.Popen(['zstd', '-q', '-d', '-c', str(compressed)], stdout=subprocess.PIPE)
    h = hashlib.sha256()
    while chunk := p.stdout.read(1 << 20):
        h.update(chunk)
    if p.wait() or h.hexdigest() != raw:
        raise RuntimeError('archive round trip failed')
    return {'file': path.name, 'bytes': path.stat().st_size, 'sha256': raw,
            'zst_sha256': sha(compressed), 'roundtrip_sha256': h.hexdigest()}


def clauses(path):
    with path.open() as f:
        f.readline()
        for line in f:
            yield [int(x) for x in line.split()[:-1]]


def append_units(base, dest, units):
    with base.open() as f, dest.open('w') as g:
        _, _, nv, nc = f.readline().split()
        g.write('p cnf %s %d\n' % (nv, int(nc) + len(units)))
        while chunk := f.read(1 << 20):
            g.write(chunk)
        for lit in units:
            g.write('%d 0\n' % lit)


# Integer arithmetic in Z[zeta_5]. The sign predicate is the one proved in
# SYMMAX/verify5.py; that script is not imported because it has top-level writes.
def sign5(a, b):
    if a >= 0 and b >= 0:
        return int(a > 0 or b > 0)
    if a <= 0 and b <= 0:
        return -int(a < 0 or b < 0)
    d = a*a - 5*b*b
    return (int(d > 0) - int(d < 0)) * (1 if a > 0 else -1)


def norm(w):
    w = list(w) + [0] * (5-len(w))
    return tuple(x-w[4] for x in w[:4]) + (0,)


def mul(a, b):
    w = [0]*5
    for i in range(5):
        for j in range(5):
            w[(i+j) % 5] += a[i]*b[j]
    return norm(w)


def conj(a):
    return norm([a[(-i) % 5] for i in range(5)])


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def imag(a):
    return sign5(2*(a[1]-a[4])-(a[2]-a[3]), a[2]-a[3])


def real(a):
    return sign5(4*a[0]-(a[1]+a[4])-(a[2]+a[3]),
                 (a[1]+a[4])-(a[2]+a[3]))


def cross(a, b):
    return imag(mul(conj(a), b))


def orient(a, b, c):
    return cross(sub(b, a), sub(c, a))


ONE = (1, 0, 0, 0, 0)
ZERO = (0, 0, 0, 0, 0)
ZETA = (0, 1, 0, 0, 0)
HALF = (0, 0, 0, -1, 0)  # -zeta^3, angle +pi/5
FOLD = (0, 0, -1, 0, 0)  # -zeta^2, angle -pi/5


def normalized_layers(points):
    remaining = set(points) - {ZERO}
    orbits = []
    for p in points:
        if p not in remaining:
            continue
        orbit = [p]
        for _ in range(4):
            orbit.append(mul(orbit[-1], ZETA))
        if len(set(orbit)) != 5 or not set(orbit) <= remaining:
            raise ValueError('not a disjoint fivefold orbit')
        remaining.difference_update(orbit)
        orbits.append(orbit)
    radius = lambda p: mul(conj(p), p)
    orbits.sort(key=functools.cmp_to_key(lambda a, b: -real(sub(radius(a[0]), radius(b[0])))))
    for a, b in zip(orbits, orbits[1:]):
        assert real(sub(radius(a[0]), radius(b[0]))) > 0
    normalizer = conj(orbits[0][0])
    answer = []
    phase = []
    halves = []
    for i, orbit in enumerate(orbits):
        adjusted = [mul(p, normalizer) for p in orbit]
        if i == 0:
            p = adjusted[0]
            assert imag(p) == 0 and real(p) > 0
        else:
            choices = [p for p in adjusted if cross(ONE, p) > 0 and cross(p, ZETA) > 0]
            assert len(choices) == 1, 'sector boundary or label ambiguity'
            p = choices[0]
        row = [p]
        for _ in range(4):
            row.append(mul(row[-1], ZETA))
        assert set(row) == set(adjusted)
        answer.extend(row)
        h = cross(p, HALF) > 0
        assert cross(p, HALF) != 0
        folded = p if h else mul(p, FOLD)
        if i:
            assert cross(ONE, folded) > 0 and cross(folded, HALF) > 0
        phase.append(folded)
        halves.append(h)
    for i, j in itertools.combinations(range(len(orbits)), 2):
        assert cross(phase[i], phase[j]) != 0
    return answer, phase, halves


def exact56(E11, path, selected):
    source = ROOT / 'ES8SYM/sets3/c5_56pts_11layers_centre.pts'
    points = [norm([int(x) for x in l.split()]) for l in source.read_text().splitlines()
              if l.strip() and not l.startswith('#')]
    assert len(points) == 56 and len(set(points)) == 56 and points.count(ZERO) == 1
    assert all(mul(p, ZETA) in set(points) for p in points)
    oracle = load('horn_oracle', HERE / 'tests/adversarial.py')
    records = []
    for label, data in [('original', points), ('mirror', [conj(p) for p in points])]:
        P, phase, halves = normalized_layers(data)
        assert len(P) == 55
        nonzero = 0
        for a, b, c in itertools.combinations(range(55), 3):
            assert orient(P[a], P[b], P[c]) != 0, 'collinearity'
            nonzero += 1
        for i in range(11):
            for k in range(5):
                assert all(orient(P[5*i+k], P[5*i+(k+1) % 5], P[x]) > 0
                           for x in range(5*(i+1), 55))
        fixed = {v: orient(P[a], P[b], P[c]) > 0 for (a, b, c), v in E11.tvar.items()}
        fixed.update({v: cross(phase[i], phase[j]) > 0 for (i, j), v in E11.Y.items()})
        fixed.update({v: halves[i] for i, v in E11.H.items()})
        bad = oracle.horn_test(clauses(path), fixed, set(fixed))
        assert bad == (0, 0), bad
        routes = []
        for item in selected:
            tri = tuple(item['triple'])
            sign = orient(*(P[x] for x in tri))
            assert sign in (-1, 1)
            lit11 = E11.o(*tri)
            assert fixed[abs(lit11)] == ((sign > 0) == (lit11 > 0))
            routes.append({'triple': tri, 'pilot_var': item['var'], 'sign': sign,
                           'eleven_layer_literal': lit11})
        record = {'set': label, 'nonzero_triples': nonzero, 'clauses': 1630243,
                  'geometry_violations': bad[0], 'chain_violations': bad[1],
                  'H1': halves[1], 'd111111': all(cross(phase[i], phase[j]) > 0
                            for i, j in itertools.combinations(range(1, 5), 2)),
                  'split_routes': routes}
        records.append(record)
        print(json.dumps({'exact56': record}), flush=True)
    assert records[0]['H1'] != records[1]['H1']
    return {'source_sha256': sha(source), 'arithmetic': 'integer cyclotomic signs, no floating comparisons',
            'records': records, 'H1_toggle': True}


def select_variables(E, path, common):
    E.fam_order(); E.fam_angle(); E.fam_nest()
    geometric = E.cls
    fixed = {}
    for lit in common:
        fixed[abs(lit)] = lit > 0
    changed = True
    while changed:
        changed = False
        for cl in geometric:
            if any(abs(l) in fixed and fixed[abs(l)] == (l > 0) for l in cl):
                continue
            rem = [l for l in cl if abs(l) not in fixed]
            if not rem:
                raise RuntimeError('geometric propagation conflict')
            if len(rem) == 1:
                fixed[abs(rem[0])] = rem[0] > 0
                changed = True
    candidate = {v: c for c, v in E.tvar.items()
                 if max(c)//5 <= 3 and len({x//5 for x in c}) == 3 and v not in fixed}
    pos = collections.Counter(); neg = collections.Counter()
    for cl in clauses(path):
        if any(abs(l) in fixed and fixed[abs(l)] == (l > 0) for l in cl):
            continue
        for lit in cl:
            if abs(lit) in candidate:
                (pos if lit > 0 else neg)[abs(lit)] += 1
    rank = sorted(candidate, key=lambda v: (-min(pos[v], neg[v]), -(pos[v]+neg[v]), v))
    chosen = []
    for v in rank[:2]:
        chosen.append({'var': v, 'triple': candidate[v], 'positive_occurrences': pos[v],
                       'negative_occurrences': neg[v], 'score': min(pos[v], neg[v])})
    if len(chosen) != 2:
        raise RuntimeError('too few orientation candidates')
    return {'method': 'balanced residual occurrence, after geometric-family unit propagation',
            'candidate_count': len(candidate), 'fixed_geometric_variables': len(fixed),
            'selected': chosen, 'top_ten': [{'var': v, 'triple': candidate[v], 'positive': pos[v],
                                          'negative': neg[v]} for v in rank[:10]]}


def prepare(args):
    archive = args.archive
    archive.mkdir(parents=True, exist_ok=True); args.scratch.mkdir(parents=True, exist_ok=True)
    LOG.mkdir(parents=True, exist_ok=True)
    generated = []
    for t in (13, 11):
        path = archive / ('m5K8t%d.cnf' % t)
        proc = subprocess.run([sys.executable, '-I', str(ROOT / 'C7UPPER/gen.py'), '5', '8', str(t), str(path)],
                              text=True, capture_output=True, check=True)
        (LOG / ('m5_generate_t%d.log' % t)).write_text(proc.stdout)
        generated.append(archived(path))
        print(json.dumps({'generated': generated[-1]}), flush=True)
    gen = load('m5_source', ROOT / 'C7UPPER/gen.py')
    E = gen.Enc(5, 8, 13)
    common = [E.H[1]] + [E.Y[i, j] for i, j in itertools.combinations(range(1, 5), 2)]
    choice = select_variables(E, archive / 'm5K8t13.cnf', common)
    print(json.dumps({'selection': choice}), flush=True)
    E11 = gen.Enc(5, 8, 11)
    validation = exact56(E11, archive / 'm5K8t11.cnf', choice['selected'])
    v = choice['selected'][0]['var']
    jobs = [('baseline', common), ('split_positive', common+[v]), ('split_negative', common+[-v])]
    job_records = []
    for name, units in jobs:
        path = archive / (name+'.cnf')
        append_units(archive/'m5K8t13.cnf', path, units)
        info = archived(path)
        generated.append(info)
        job_records.append({'name': name, 'units': units, 'file': path.name, 'sha256': info['sha256']})
    report = {'schema': 1, 'common_cube': 'd111111 + H(1)', 'common_units': common,
              'selection': choice, 'exact56': validation, 'jobs': job_records, 'archives': generated,
              'generator_sha256': sha(ROOT/'C7UPPER/gen.py'), 'script_sha256': sha(Path(__file__))}
    save(LOG/'m5_prepare.json', report); save(archive/'manifest.json', report)
    print(json.dumps({'preparation': 'PASS', 'jobs': job_records}), flush=True)


def memory_bytes():
    out = subprocess.run(['vm_stat'], capture_output=True, text=True, check=True).stdout
    size = int(re.search(r'page size of (\d+)', out).group(1))
    values = [int(re.search(re.escape(k)+r':\s*(\d+)', out).group(1))
              for k in ('Pages active', 'Pages wired down', 'Pages occupied by compressor')]
    return size*sum(values)


def sanitize(text):
    lines = []
    in_banner = True
    for line in text.splitlines():
        if in_banner:
            if '[ limit ]' in line:
                in_banner = False
            else:
                continue
        if '/Users/' in line or '/private/' in line or 'Darwin ' in line or 'compiled ' in line:
            continue
        if line.startswith('v '):
            continue
        lines.append(line)
    return '\n'.join(lines)+'\n'


def run_one(args, job, deadline):
    raw = args.scratch/(job['name']+'.raw.log')
    start = time.monotonic(); peak = 0; reason = None; ru = None
    with raw.open('w') as output:
        proc = subprocess.Popen([str(args.bin/'cadical'), '-t', str(args.seconds), job['file']],
                                cwd=args.archive, stdout=output, stderr=subprocess.STDOUT, start_new_session=True)
        save(args.scratch/'active.json', {'pid': proc.pid, 'job': job['name']})
        try:
            while True:
                pid, status, usage = os.wait4(proc.pid, os.WNOHANG)
                if pid:
                    proc.returncode = os.waitstatus_to_exitcode(status); ru = usage
                    break
                used = memory_bytes(); peak = max(peak, used)
                if used >= args.memory_limit:
                    reason = 'memory_guard'
                if time.monotonic() >= min(deadline, start+args.seconds+15):
                    reason = 'wall_guard'
                if reason:
                    os.killpg(proc.pid, signal.SIGTERM)
                    time.sleep(2)
                    pid, status, usage = os.wait4(proc.pid, os.WNOHANG)
                    if not pid:
                        os.killpg(proc.pid, signal.SIGKILL)
                        pid, status, usage = os.wait4(proc.pid, 0)
                    proc.returncode = os.waitstatus_to_exitcode(status); ru = usage
                    break
                time.sleep(3)
        finally:
            if proc.returncode is None:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
            (args.scratch/'active.json').unlink(missing_ok=True)
    raw_content = raw.read_text()
    content = sanitize(raw_content)
    log = LOG/('m5_'+job['name']+'.log'); log.write_text(content)
    result = {'job': job['name'], 'exit_code': proc.returncode, 'seconds_limit': args.seconds,
              'wall_seconds': round(time.monotonic()-start, 3), 'guard': reason,
              'system_memory_peak_bytes': peak, 'cnf_sha256': sha(args.archive/job['file']),
              'log_sha256': sha(log), 'child_stopped': True,
              'verdict': ('UNSAT_REQUIRES_PROOF' if proc.returncode==20 else
                    'SAT_ABSTRACT' if proc.returncode==10 else 'UNKNOWN')}
    if ru:
        result.update(cpu_seconds=round(ru.ru_utime+ru.ru_stime, 3), peak_rss_bytes=ru.ru_maxrss)
    if proc.returncode == 10:
        witness = '\n'.join(line for line in raw_content.splitlines() if line.startswith('v '))+'\n'
        if not witness.strip():
            raise RuntimeError('SAT verdict without an assignment')
        witness_file = args.archive/(job['name']+'.model.txt')
        witness_file.write_text(witness)
        result['sat_model_file'] = witness_file.name
        result['sat_model_sha256'] = sha(witness_file)
    for key in ('conflicts', 'decisions', 'propagations', 'restarts'):
        hits = re.findall(r'^c\s+'+key+r':\s+([\d,]+)', content, re.M)
        if hits:
            result[key] = int(hits[-1].replace(',', ''))
    raw.unlink()
    print(json.dumps(result), flush=True)
    return result


def run(args):
    prepared = json.loads((LOG/'m5_prepare.json').read_text())
    deadline = time.monotonic()+1500
    results = []
    for job in prepared['jobs']:
        if sha(args.archive/job['file']) != job['sha256']:
            raise RuntimeError('prepared CNF hash mismatch')
        result = run_one(args, job, deadline)
        results.append(result)
        save(LOG/'m5_runs.json', {'solver_sha256': sha(args.bin/'cadical'), 'runs': results,
                                'completed_children_stopped': True, 'campaign_state': 'running'})
        if result['guard'] or time.monotonic() >= deadline:
            break
    final = {'solver_sha256': sha(args.bin/'cadical'), 'runs': results,
             'all_children_stopped': True,
             'campaign_state': 'complete' if len(results)==len(prepared['jobs']) else 'stopped_by_guard'}
    save(LOG/'m5_runs.json', final)
    save(args.archive/'pilot_runs.json', final)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--prepare', action='store_true'); p.add_argument('--run', action='store_true')
    p.add_argument('--bin', type=Path); p.add_argument('--scratch', required=True, type=Path)
    p.add_argument('--archive', required=True, type=Path); p.add_argument('--seconds', type=int, default=300)
    p.add_argument('--memory-limit', type=int, default=29000000000)
    args = p.parse_args()
    if args.prepare == args.run:
        p.error('choose exactly one of --prepare or --run')
    if args.run and args.bin is None:
        p.error('--run requires --bin')
    prepare(args) if args.prepare else run(args)


if __name__ == '__main__':
    main()
