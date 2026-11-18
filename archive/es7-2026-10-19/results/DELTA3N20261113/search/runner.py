#!/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
"""Build, import pools, run the single-threaded engine, independently audit packets.

No jobs/units/threads are launched in the background. Long invocations are for the
parent scheduler. New artifacts default to the assigned search scratch directory.
"""
import argparse
import collections
import hashlib
import itertools
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/search')
PYTHON = '/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python'
BOUND = 10**15
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
           NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def child_limit(memory_mb):
    def apply():
        ceiling = memory_mb * 1024**2
        resource.setrlimit(resource.RLIMIT_AS, (ceiling, ceiling))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    return apply


def output_dir(path=None):
    path = Path(path) if path else SCRATCH / ('run-' + str(time.time_ns()))
    path.mkdir(parents=True, exist_ok=False)
    return path


def normalize(points):
    if not isinstance(points, list) or len(points) > 64:
        raise ValueError('point list must have at most 64 points')
    for p in points:
        if not isinstance(p, (tuple, list)) or len(p) != 2 or any(type(v) is not int for v in p):
            raise ValueError('coordinates must be JSON integers (no floats/bools)')
        if any(abs(v) > BOUND for v in p):
            raise ValueError('coordinate outside explicit +/-10^15 bound')
    return sorted(map(tuple, points))


def records(path):
    path = Path(path)
    if path.suffix == '.points':
        words = path.read_text().split()
        m = int(words[0])
        if len(words) != 1 + 2*m:
            raise ValueError('bad point-file length')
        yield normalize([[int(words[1+2*i]), int(words[2+2*i])] for i in range(m)])
        return
    objects = [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.suffix == '.jsonl' else [json.loads(path.read_text())]
    for obj in objects:
        if isinstance(obj, dict):
            if 'P' not in obj:
                raise ValueError(f'{path}: record has no coordinates P (certificate indices alone are not input)')
            yield normalize(obj['P'])
        else:
            yield normalize(obj)


def write_points(path, points):
    Path(path).write_text(str(len(points)) + '\n' + ''.join(f'{x} {y}\n' for x, y in points))


def prepare(paths, out):
    sets, seen = [], set()
    for path in paths:
        for p in records(path):
            key = tuple(p)
            if key not in seen:
                sets.append(p)
                seen.add(key)
    if not sets or len(sets) > 4096:
        raise ValueError('pool must contain 1..4096 coordinate sets')
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('x') as f:
        f.write(f'D3POOL 1 {len(sets)}\n')
        for p in sets:
            f.write(str(len(p)) + '\n' + ''.join(f'{x} {y}\n' for x, y in p))
    manifest = {'label': 'COMPUTED', 'sets': len(sets), 'sizes': dict(collections.Counter(map(len, sets))),
                'inputs': {str(p): sha(p) for p in paths}, 'pool_sha256': sha(out)}
    out.with_suffix(out.suffix + '.manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def orient(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])


def hull(points):
    lower, upper = [], []
    for p in points:
        while len(lower) > 1 and orient(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper) > 1 and orient(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1] if len(points) > 1 else points


def chain(p, ids, sign):
    return ids == sorted(set(ids)) and all(orient(p[a], p[b], p[c])*sign > 0 for a, b, c in zip(ids, ids[1:], ids[2:]))


def pair_lengths(p, ids=None):
    """Unbounded Python integers, forward recurrence, no native-library import."""
    m = len(p)
    ids = list(range(m)) if ids is None else sorted(ids)
    cap, cup = [0]*(m*m), [0]*(m*m)
    for start, s in enumerate(ids):
        dc, du = {}, {}
        for jpos in range(start+1, len(ids)):
            j = ids[jpos]
            dc[s, j] = du[s, j] = 2
            bc = bu = 2
            for ipos in range(start+1, jpos):
                i = ids[ipos]
                c = u = 0
                for h in ids[start:ipos]:
                    d = orient(p[h], p[i], p[j])
                    if d < 0 and dc.get((h, i), 0):
                        c = max(c, dc[h, i]+1)
                    if d > 0 and du.get((h, i), 0):
                        u = max(u, du[h, i]+1)
                dc[i, j], du[i, j] = c, u
                bc, bu = max(bc, c), max(bu, u)
            cap[s*m+j], cup[s*m+j] = bc, bu
    return cap, cup


def check_geometry(p, a, n):
    if len({x for x, _ in p}) != len(p) or any(not orient(*q) for q in itertools.combinations(p, 3)):
        raise ValueError('geometry is not general position with distinct x')
    cap, cup = pair_lengths(p)
    if max(cap, default=0) >= a or max((x+y-2 for x, y in zip(cap, cup)), default=0) >= n:
        raise ValueError('counterexample premises are false')
    return cap, cup


def check_model(p, d, a, n, mode):
    cap, cup = check_geometry(p, a, n)
    m = len(p)
    d = set(d)
    if not d <= set(range(m)):
        raise ValueError('model index outside point set')
    inside_c, inside_u = pair_lengths(p, d)
    if max(inside_c, default=0) >= a-1:
        raise ValueError('Delta contains forbidden cap')
    rest = set(range(m)) - d
    rest_c, rest_u = pair_lengths(p, rest)
    for u, v in itertools.combinations(sorted(rest), 2):
        z = u*m+v
        bad = ((mode == 'lower' and cap[z]+rest_u[z] > n) or
               (mode == 'upper' and rest_c[z]+cup[z] > n) or
               (mode == 'ends' and cap[z]+cup[z] == n+1) or
               (mode in ('weak', 'strong') and rest_c[z]+rest_u[z]-2 >= n-1))
        if bad:
            raise ValueError('Delta misses required polygon part')
    if mode == 'strong' and any(inside_c[u*m+v]+inside_u[u*m+v]-2 >= n-1 for u, v in itertools.combinations(sorted(d), 2)):
        raise ValueError('strong Delta contains forbidden polygon')


def audit_packet(path):
    """Checks soundness of every exported clause, not a claim that all hits occur.

    UNSAT of a sound subset of constraints already implies failure. Missing clauses
    can never create a false UNSAT, so no completeness assumption about lazy cuts.
    """
    path = Path(path)
    r = json.loads(path.read_text())
    p = normalize(r['P'])
    if [list(q) for q in p] != r['P']:
        raise ValueError('packet indices require already x-sorted coordinates')
    a, n, mode = r['a'], r['n'], r['mode']
    if mode not in ('lower', 'upper', 'ends', 'weak', 'strong'):
        raise ValueError('unknown packet mode')
    check_geometry(p, a, n)
    m = len(p)
    def ids(xs):
        if not isinstance(xs, list) or xs != sorted(set(xs)) or any(type(i) is not int or not 0 <= i < m for i in xs):
            raise ValueError('invalid clause vertex indices')
        return xs
    def polygon(cap, cup):
        ids(cap); ids(cup)
        if len(cap) < 2 or len(cup) < 2 or (cap[0], cap[-1]) != (cup[0], cup[-1]):
            raise ValueError('witness chains have different endpoints')
        if not chain(p, cap, -1) or not chain(p, cup, 1):
            raise ValueError('wrong witness chain orientation')
        gon = sorted(set(cap) | set(cup))
        if set(cap) & set(cup) != {cap[0], cap[-1]} or len(gon) != n-1 or len(hull([p[i] for i in gon])) != n-1:
            raise ValueError('witness is not an (n-1)-gon')
        return gon
    negative, positive = [], []
    for k in r['cap_clauses']:
        ids(k)
        if len(k) != a-1 or not chain(p, k, -1):
            raise ValueError('unsound negative cap clause')
        negative.append([-(i+1) for i in k])
    for w in r['witness_clauses']:
        gon = polygon(w['cap'], w['cup'])
        ids(w['clause'])
        if w['positive'] is True:
            expected = w['cup'] if mode == 'lower' else w['cap'] if mode == 'upper' else [gon[0], gon[-1]] if mode == 'ends' else gon
            if w['clause'] != expected:
                raise ValueError('positive clause hits wrong polygon part')
            positive.append([i+1 for i in expected])
        elif w['positive'] is False and mode == 'strong' and w['clause'] == gon:
            negative.append([-(i+1) for i in gon])
        else:
            raise ValueError('unsound negative polygon clause')
    for w in r.get('private_cups', []):
        polygon(w['cap'], w['cup'])
        if len(w['vertex']) != 1 or set(w['cup']) & set(r['Delta']) != set(w['vertex']):
            raise ValueError('invalid private cup witness')
    cnf = path.with_suffix('.cnf')
    clauses, pending, header = [], [], None
    for line in cnf.read_text().splitlines():
        if not line or line.startswith('c'):
            continue
        if line.startswith('p '):
            if header is not None:
                raise ValueError('duplicate CNF header')
            h = line.split()
            if len(h) != 4 or h[:2] != ['p', 'cnf']:
                raise ValueError('bad CNF header')
            header = (int(h[2]), int(h[3]))
            continue
        for v in map(int, line.split()):
            if v:
                pending.append(v)
            else:
                clauses.append(pending); pending = []
    if pending or header != (m, len(clauses)) or clauses != negative+positive:
        raise ValueError('CNF differs from geometrically audited clauses')
    if r['status'] == 'OK':
        check_model(p, r['Delta'], a, n, mode)
    return r, {'label': 'COMPUTED', 'audit': 'PASS', 'clauses': len(clauses), 'points': m,
               'packet_sha256': sha(path), 'cnf_sha256': sha(cnf)}


def cake_verdict(stdout):
    return 's VERIFIED UNSAT' in stdout.splitlines()


def certify(args):
    r, evidence = audit_packet(args.packet)
    if r['status'] != 'NO_DELTA_COMPUTED' or r.get('max_delta_bound', -1) != -1:
        raise ValueError('certification requires unbounded exhaustive failure; UNKNOWN/bounded verdicts rejected')
    out = output_dir(args.out)
    cnf = Path(args.packet).with_suffix('.cnf').resolve()
    proof = out / 'proof.lrat'
    start = time.monotonic()
    def run(command, name, timeout):
        try:
            with (out/(name+'.stdout')).open('w') as stdout, (out/(name+'.stderr')).open('w') as stderr:
                proc = subprocess.run(command, stdout=stdout, stderr=stderr, env=ENV,
                                      preexec_fn=child_limit(args.memory_mb), timeout=timeout)
            return proc.returncode, (out/(name+'.stdout')).read_text()
        except subprocess.TimeoutExpired:
            return None, ''
    cmd = [args.cadical, '-q', '-t', str(args.seconds), '--lrat=true', '--binary=false', str(cnf), str(proof)]
    rc, text = run(cmd, 'cadical', args.seconds+2)
    result = dict(evidence, label='COMPUTED', status='INCONCLUSIVE', cadical_exit=rc,
                  solver_command=cmd, packet=str(Path(args.packet).resolve()))
    if 's UNSATISFIABLE' in text.splitlines() and proof.is_file():
        cmd = [str(Path(args.cake).expanduser()), f'--CML_HEAP_SIZE={args.heap_mb}', '--CML_STACK_SIZE=64', str(cnf), str(proof)]
        rc, text = run(cmd, 'cake', args.seconds+2)
        result.update(cake_exit=rc, checker_command=cmd, proof_sha256=sha(proof))
        if cake_verdict(text):
            result.update(label='CERTIFIED', status='UNSAT', checker_verdict='s VERIFIED UNSAT')
    result['wall_seconds'] = time.monotonic()-start
    (out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))
    return 0 if result['label'] == 'CERTIFIED' else 20


def native_options(args):
    result = ['--a', str(args.a), '--n', str(args.n), '--mode', args.mode,
              '--time-ms', str(args.time_ms), '--node-limit', str(args.node_limit),
              '--clause-limit', str(args.clause_limit), '--round-limit', str(args.round_limit)]
    for flag in ('detail', 'min_delta', 'private_witnesses'):
        if getattr(args, flag, False):
            result.append('--'+flag.replace('_', '-'))
    if getattr(args, 'max_delta', None) is not None:
        result += ['--max-delta', str(args.max_delta)]
    return result


def execute(args):
    out = output_dir(args.out)
    if args.command == 'search':
        pool = Path(args.pool).resolve()
        options = ['--input', str(pool), '--seconds', str(args.seconds), '--steps', str(args.steps),
                   '--seed', str(args.seed), '--cache', str(args.cache), '--bank', str(args.bank),
                   '--restart', str(args.restart), '--min-size', str(args.min_size),
                   '--minimize-ms', str(args.minimize_ms)]
        timeout = args.seconds + 5
    else:
        ps = list(records(args.input))
        if len(ps) != 1:
            raise ValueError('check/minimize requires one point set; prepare a search pool for JSONL')
        pool = out/'input.points'
        write_points(pool, ps[0])
        options = ['--input', str(pool)]
        if args.command == 'minimize':
            options += ['--minimize-ms', str(args.minimize_ms)]
        timeout = (args.time_ms+getattr(args, 'minimize_ms', 0))/1000 + 5
    cmd = [str(Path(args.binary).resolve()), args.command, '--out', str(out)] + options + native_options(args)
    manifest = {'label': 'COMPUTED', 'command': cmd, 'memory_mb': args.memory_mb, 'threads': 1,
                'engine_sha256': sha(args.binary), 'source_sha256': sha(HERE/'delta_search.cpp'),
                'input_sha256': sha(pool), 'started_unix': time.time()}
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    start = time.monotonic()
    try:
        with (out/'stdout.jsonl').open('w') as stdout, (out/'stderr.log').open('w') as stderr:
            proc = subprocess.run(cmd, stdout=stdout, stderr=stderr, env=ENV,
                                  preexec_fn=child_limit(args.memory_mb), timeout=timeout)
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        rc = 20
        manifest['wrapper_timeout'] = True
    manifest.update(exit=rc, wall_seconds=time.monotonic()-start)
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print((out/'stdout.jsonl').read_text(), end='')
    print(json.dumps({'output': str(out), 'exit': rc, 'wall_seconds': manifest['wall_seconds']}))
    if rc not in (0, 10, 11, 20, 30, 31):
        print((out/'stderr.log').read_text(), file=sys.stderr)
    return rc


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='command', required=True)
    p = sub.add_parser('build')
    p.add_argument('--binary', default=str(SCRATCH/'delta_search'))
    p.add_argument('--sanitize', action='store_true')
    p = sub.add_parser('prepare')
    p.add_argument('--out', required=True)
    p.add_argument('inputs', nargs='+')
    p = sub.add_parser('audit')
    p.add_argument('packet')
    p = sub.add_parser('controls')
    p.add_argument('--binary', default=str(SCRATCH/'delta_search'))
    p.add_argument('--out')
    p = sub.add_parser('certify')
    p.add_argument('packet')
    p.add_argument('--out')
    p.add_argument('--seconds', type=int, default=60)
    p.add_argument('--memory-mb', type=int, default=1536)
    p.add_argument('--heap-mb', type=int, default=512)
    p.add_argument('--cadical', default='/usr/bin/cadical')
    p.add_argument('--cake', default='~/.local/bin/cake_lpr')
    for command in ('check', 'search', 'minimize'):
        p = sub.add_parser(command)
        p.add_argument('--binary', default=str(SCRATCH/'delta_search'))
        p.add_argument('--out')
        p.add_argument('--a', type=int, default=5)
        p.add_argument('--n', type=int, default=8)
        p.add_argument('--mode', choices=['lower', 'upper', 'ends', 'weak', 'strong'], default='lower')
        p.add_argument('--time-ms', type=int, default=2000)
        p.add_argument('--node-limit', type=int, default=2000000)
        p.add_argument('--clause-limit', type=int, default=1000000)
        p.add_argument('--round-limit', type=int, default=10000)
        p.add_argument('--memory-mb', type=int, default=1536)
        p.add_argument('--min-delta', action='store_true')
        p.add_argument('--private-witnesses', action='store_true')
        p.add_argument('--detail', action='store_true')
        if command == 'search':
            p.add_argument('--pool', required=True)
            p.add_argument('--seconds', type=float, required=True)
            p.add_argument('--steps', type=int, default=100000000)
            p.add_argument('--seed', type=int, default=1)
            p.add_argument('--cache', type=int, default=20000)
            p.add_argument('--bank', type=int, default=32)
            p.add_argument('--restart', type=int, default=128)
            p.add_argument('--min-size', type=int, default=0)
        else:
            p.add_argument('--input', required=True)
        if command == 'check':
            p.add_argument('--max-delta', type=int)
        if command in ('search', 'minimize'):
            p.add_argument('--minimize-ms', type=int, default=5000)
    args = ap.parse_args()
    SCRATCH.mkdir(parents=True, exist_ok=True)
    (SCRATCH/'tmp').mkdir(exist_ok=True)
    ENV['TMPDIR'] = str(SCRATCH/'tmp')
    if args.command == 'build':
        flags = ['-O1', '-g', '-fsanitize=undefined', '-fno-sanitize-recover=all'] if args.sanitize else ['-O3', '-DNDEBUG']
        # Atomic replacement leaves any centrally scheduled running binary intact.
        temporary = str(Path(args.binary).with_name(Path(args.binary).name+'.build-'+str(os.getpid())))
        cmd = ['g++', '-std=c++20', '-Wall', '-Wextra', '-Wshadow', '-Werror']+flags+[str(HERE/'delta_search.cpp'), '-o', temporary]
        subprocess.run(cmd, check=True, env=ENV, timeout=20)
        os.replace(temporary, args.binary)
        print(json.dumps({'label': 'COMPUTED', 'binary': args.binary, 'sha256': sha(args.binary)}))
        return 0
    if args.command == 'prepare':
        print(json.dumps(prepare(args.inputs, args.out)))
        return 0
    if args.command == 'audit':
        print(json.dumps(audit_packet(args.packet)[1]))
        return 0
    if args.command == 'certify':
        return certify(args)
    if args.command == 'controls':
        import controls
        return controls.run(Path(args.binary), output_dir(args.out))
    return execute(args)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(2)
