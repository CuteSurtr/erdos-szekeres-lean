#!/usr/bin/env python3
"""Read-only research-cgroup snapshot, appended to this record's evidence."""
import datetime
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = Path('/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice')


def key_values(path):
    return {line.split()[0]: int(line.split()[1]) for line in path.read_text().splitlines()}


def integer_or_text(path):
    value = path.read_text().strip()
    return int(value) if value.isdigit() else value


units = []
for directory in sorted(ROOT.glob('nov13c-*.service')):
    try:
        stat = key_values(directory / 'memory.stat')
        row = {'unit': directory.name, 'anon_bytes': stat['anon'],
               'file_bytes': stat['file'], 'current_bytes': integer_or_text(directory / 'memory.current'),
               'peak_bytes': integer_or_text(directory / 'memory.peak'),
               'swap_bytes': integer_or_text(directory / 'memory.swap.current'),
               'kernel_memory_max': integer_or_text(directory / 'memory.max'),
               'memory_high': integer_or_text(directory / 'memory.high'),
               'memory_events': key_values(directory / 'memory.events'),
               'cpu_max': (directory / 'cpu.max').read_text().strip(),
               'cpu_stat': key_values(directory / 'cpu.stat')}
    except FileNotFoundError:
        continue
    units.append(row)
snapshot = {
    'time': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(),
    'unit_count': len(units), 'research_anon_plus_swap_bytes': sum(r['anon_bytes'] + r['swap_bytes'] for r in units),
    'research_current_bytes_including_file_cache': sum(r['current_bytes'] for r in units),
    'research_swap_bytes': sum(r['swap_bytes'] for r in units),
    'memory_pressure': Path('/proc/pressure/memory').read_text(),
    'cpu_pressure': Path('/proc/pressure/cpu').read_text(),
    'units': units,
    'scope': 'Live nov13c cgroups only; short independently capped CLI probes are budgeted separately. Historical disappeared cgroups are not covered.'}
with (HERE / 'data/resource-snapshots.jsonl').open('a') as output:
    output.write(json.dumps(snapshot) + '\n')
print(json.dumps({k: snapshot[k] for k in ['time', 'unit_count', 'research_anon_plus_swap_bytes', 'research_current_bytes_including_file_cache', 'research_swap_bytes']}))
