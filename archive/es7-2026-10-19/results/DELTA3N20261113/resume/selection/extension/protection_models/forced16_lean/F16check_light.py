#!/usr/bin/env python3
"""One bounded Lean CLI check; writes logs only to the authorized scratch directory."""
import json
import hashlib
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

REPO = Path('/home/jay/research/lean/erdos-szekeres-lean')
SCRATCH = Path(__file__).resolve().parent / 'work'
LEAN = Path('/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean')
SOURCE = Path(sys.argv[1]).resolve()
assert SOURCE.stem.startswith('F16'), 'all source module names must start F16'
TAG = sys.argv[2] if len(sys.argv) > 2 else SOURCE.stem
if not TAG.replace('-', '').replace('_', '').isalnum():
    raise SystemExit('invalid log tag')
env = os.environ.copy()
env['LEAN_PATH'] = str(SCRATCH)
env['MIMALLOC_ARENA_RESERVE'] = '33554432'
env['MALLOC_ARENA_MAX'] = '1'


def limits():
    os.setsid()
    os.sched_setaffinity(0, {4})
    resource.setrlimit(resource.RLIMIT_AS, (3 * 1024**3, 3 * 1024**3))
    resource.setrlimit(resource.RLIMIT_CPU, (18, 19))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


cmd = [str(LEAN), '-j1', '-s16384', '-M200', f'--root={SOURCE.parent}']
if len(sys.argv) > 3 and sys.argv[3] == '--export':
    cmd.extend(['-o', str(SCRATCH / f'{SOURCE.stem}.olean')])
cmd.append(str(SOURCE))
started = time.monotonic()
peaks = {}
stop_reason = None
with (SCRATCH / f'{TAG}.log').open('w') as output:
    child = subprocess.Popen(cmd, cwd=REPO, env=env, stdout=output,
                             stderr=subprocess.STDOUT, preexec_fn=limits)
    while child.poll() is None:
        try:
            for line in Path(f'/proc/{child.pid}/status').read_text().splitlines():
                key, _, value = line.partition(':')
                if key in ('VmPeak', 'VmSize', 'VmRSS', 'VmHWM', 'RssAnon', 'RssFile',
                           'VmSwap', 'Threads'):
                    peaks[key] = max(peaks.get(key, 0), int(value.split()[0]))
        except (FileNotFoundError, ProcessLookupError):
            pass
        if peaks.get('VmRSS', 0) > 480 * 1024:
            stop_reason = 'RSS guard at 480 MiB'
        elif peaks.get('VmSwap', 0) > 0:
            stop_reason = 'nonzero swap'
        elif time.monotonic() - started > 18:
            stop_reason = '18-second wall deadline'
        if stop_reason:
            os.killpg(child.pid, signal.SIGTERM)
            try:
                child.wait(timeout=1)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
            break
        time.sleep(0.01)
    rc = child.wait()
record = dict(command=cmd, exit_code=rc, stop_reason=stop_reason,
              source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              elapsed_seconds=round(time.monotonic() - started, 3),
              proc_status_peaks_kib_except_threads=peaks,
              rusage_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              as_limit_bytes=3 * 1024**3, rss_guard_mib=480, lean_heap_mib=200,
              cpu_affinity=[4], wall_deadline_seconds=18)
(SCRATCH / f'{TAG}.json').write_text(json.dumps(record, indent=2) + '\n')
print((SCRATCH / f'{TAG}.log').read_text(), end='')
print('CHECK ' + json.dumps({k: record[k] for k in
      ('exit_code', 'stop_reason', 'elapsed_seconds', 'rusage_maxrss_kib', 'source_sha256')}))
raise SystemExit(rc if 0 <= rc <= 255 else 128 - rc)
