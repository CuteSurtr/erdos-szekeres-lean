#!/usr/bin/env python3
"""Sequential capacity-specialization checks, with independent RSS/swap stops.

Allocate the selected RSS guard before launching (default3000MiB). This driver is not a memory reservation.
Use a nov13c-vfy unit, CPU100%, Swap0, Runtime240s, MemoryMax at least RSS/0.8.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parent
REPO = Path('/home/jay/research/lean/erdos-szekeres-lean')
LEAN = Path('/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean')
SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/extension/capacity-lean')
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
EXPECTED = {
    'Capacity16': {'four_cap_or_seven_gon', 'hasNGon_real', 'geometric_capacity16'},
    'Capacity11': {'four_cap_or_six_gon', 'geometric_capacity11'},
}


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def local_dependencies():
    pending = ['ErdosSzekeres.Omission.BaekGeometry']
    seen = {}
    while pending:
        name = pending.pop()
        if name in seen:
            continue
        source = REPO / (name.replace('.', '/') + '.lean')
        if not source.is_file():
            continue
        olean = REPO / '.lake/build/lib/lean' / (name.replace('.', '/') + '.olean')
        assert olean.is_file(), olean
        seen[name] = {'source': str(source), 'source_sha256': sha(source),
                      'olean': str(olean), 'olean_sha256': sha(olean)}
        for line in source.read_text().splitlines():
            if line.startswith('import '):
                pending.extend(line[7:].split('--')[0].split())
    return seen


def limits():
    os.setsid()
    os.sched_setaffinity(0, {4})
    resource.setrlimit(resource.RLIMIT_AS, (6 << 30, 6 << 30))
    resource.setrlimit(resource.RLIMIT_CPU, (27, 28))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prefix', required=True)
    parser.add_argument('--rss-mib', type=int, default=3000)
    args = parser.parse_args()
    assert re.fullmatch('[a-zA-Z0-9_-]+', args.prefix)
    assert 2000 <= args.rss_mib <= 4500
    out = SCRATCH / args.prefix
    out.mkdir(parents=True, exist_ok=False)
    env = os.environ.copy()
    env['LEAN_PATH'] = ':'.join([str(out), str(REPO / '.lake/build/lib/lean')] +
        [str(p) for p in sorted((REPO / '.lake/packages').glob('*/.lake/build/lib/lean'))])
    env['MIMALLOC_ARENA_RESERVE'] = '33554432'
    env['MALLOC_ARENA_MAX'] = '1'
    before = local_dependencies()
    records = []
    status = 'FAIL'
    try:
        for stem, expected in EXPECTED.items():
            source = ROOT / (stem + '.lean')
            digest = sha(source)
            assert not re.search(r'\b(sorry|admit|native_decide|ofReduceBool|axiom)\b',
                                 '\n'.join(l for l in source.read_text().splitlines()
                                           if not l.startswith('#print axioms')))
            cmd = [str(LEAN), '-j1', '-s16384', '-M1000', f'--root={ROOT}',
                   '-o', str(out / (stem + '.olean')), str(source)]
            peaks = {}
            stop = None
            start = time.monotonic()
            with (out / (stem + '.log')).open('x') as log:
                child = subprocess.Popen(cmd, cwd=REPO, env=env, stdout=log,
                    stderr=subprocess.STDOUT, preexec_fn=limits)
                while child.poll() is None:
                    try:
                        for line in Path(f'/proc/{child.pid}/status').read_text().splitlines():
                            key, _, val = line.partition(':')
                            if key in {'VmPeak', 'VmSize', 'VmRSS', 'VmHWM',
                                       'RssAnon', 'RssFile', 'VmSwap', 'Threads'}:
                                peaks[key] = max(peaks.get(key, 0), int(val.split()[0]))
                    except FileNotFoundError:
                        pass
                    if peaks.get('VmRSS', 0) > args.rss_mib * 1024:
                        stop = f'RSS exceeds {args.rss_mib}MiB'
                    elif peaks.get('VmSwap', 0):
                        stop = 'nonzero swap'
                    elif time.monotonic() - start > 27:
                        stop = '27-second deadline'
                    if stop:
                        os.killpg(child.pid, signal.SIGTERM)
                        try:
                            child.wait(timeout=1)
                        except subprocess.TimeoutExpired:
                            os.killpg(child.pid, signal.SIGKILL)
                        break
                    time.sleep(.01)
                rc = child.wait()
            logtext = (out / (stem + '.log')).read_text()
            audits = {name: [v.strip() for v in raw.split(',') if v.strip()]
                      for name, raw in re.findall(
                          r"'([^']+)' depends on axioms: \[([^]]*)\]", logtext)}
            audits.update({name: [] for name in re.findall(
                r"'([^']+)' does not depend on any axioms", logtext)})
            row = dict(source=str(source), source_sha256=digest, command=cmd,
                       exit_code=rc, stop_reason=stop, peaks=peaks,
                       seconds=round(time.monotonic()-start, 3), axiom_reports=audits,
                       as_bytes=6<<30, rss_guard_mib=args.rss_mib, lean_heap_mib=1000)
            records.append(row)
            (out / (stem + '.json')).write_text(json.dumps(row, indent=2)+'\n')
            print(json.dumps(row), flush=True)
            assert rc == 0 and stop is None, logtext
            assert sha(source) == digest
            assert not re.search(r'\b(error|warning)(?:\(|:)', logtext), logtext
            assert set(audits) == {'Delta3.LowSplitCapacity.'+n for n in expected}, audits
            assert all(set(a) <= ALLOWED for a in audits.values()), audits
        assert local_dependencies() == before
        status = 'PASS'
    finally:
        receipt = dict(status=status, checks=records, dependencies=before,
                       lean_sha256=sha(LEAN), driver_sha256=sha(Path(__file__)),
                       lean_toolchain=(REPO/'lean-toolchain').read_text().strip())
        (out/'result.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(status, flush=True)


if __name__ == '__main__':
    main()
