#!/usr/bin/env python3
"""Retain the short audit results and both parent checker outcomes in scope."""
import audit_pool as audit  # Also installs this control's resource limits.
import hashlib
import json
from pathlib import Path
import subprocess

out = audit.HERE / 'results'
out.mkdir(exist_ok=True)
manifest = {}


def retain(source, relative):
    need = audit.need
    raw = source.read_bytes()
    need(len(raw) < 2_000_000, 'unexpectedly large audit artifact')
    target = out / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    manifest[str(relative)] = dict(source=str(source), bytes=len(raw),
                                  sha256=hashlib.sha256(raw).hexdigest())
    return raw


for mode in ('geometry', 'edges', 'exports', 'input7', 'input8'):
    record = json.loads(retain(audit.SCRATCH / (mode + '.json'), mode + '.json'))
    audit.need(record['checker_sha256'] == audit.sha(audit.HERE / 'audit_pool.py'),
               'checker source changed')
    audit.need(record['driver_sha256'] == audit.sha(audit.DRIVER), 'driver changed')
for n in (7, 8):
    for name in ('pool.json', 'result.json'):
        retain(audit.SCRATCH / f'n{n}m16-{name}', f'interim/n{n}m16-{name}')
for name in ('base.cnf', 'final.cnf', 'result.json', 'pool.json', 'events.jsonl'):
    retain(audit.SCRATCH / 'tiny-n6m8' / name, 'own-tiny/' + name)

parent = audit.SCRATCH.parent / 'pool/control-n6m8'
for name in ('final.cnf', 'result.json', 'pool.json', 'events.jsonl',
             'cert/certify.jsonl', 'cert/final.cadical.log',
             'cert/final.cake.out', 'cert/cake-stack32.out',
             'cert/final.lrat', 'cert/final.lrat.zst'):
    retain(parent / name, 'parent-tiny/' + name)
cert = out / 'parent-tiny/cert'
entry = json.loads((cert / 'certify.jsonl').read_text().strip())
audit.need(audit.sha(out / 'parent-tiny/final.cnf') == entry['cnf_sha256'], 'certificate CNF hash')
audit.need(audit.sha(cert / 'final.lrat') == entry['lrat_sha256'], 'certificate proof hash')
p = subprocess.run(['zstd', '-d', '-c', str(cert / 'final.lrat.zst')],
                   capture_output=True, timeout=3)
audit.need(p.returncode == 0 and p.stdout == (cert / 'final.lrat').read_bytes(),
           'retained compressed proof mismatch')
failure = (cert / 'final.cake.out').read_text()
success = (cert / 'cake-stack32.out').read_text()
audit.need('s VERIFIED UNSAT' not in failure.splitlines(), 'unexpected initial success')
audit.need('cannot allocate the heap and stack' in failure, 'unexpected initial failure')
audit.need('s VERIFIED UNSAT' in success.splitlines(), 'missing exact acceptance line')
certificate = dict(
    status='PARENT_CERTIFICATE_LOGS_AND_HASHES_CONFIRMED',
    independently_replayed_here=False,
    cnf_sha256=entry['cnf_sha256'], lrat_sha256=entry['lrat_sha256'],
    initial_helper_verdict=entry['verdict'], initial_checker_output=failure,
    successful_replay_output=success,
    replay_heap_mib_reported_by_parent=128, replay_stack_mib_reported_by_parent=32,
    process_as_mib_reported_by_parent=400,
    note='The original allocation failure is retained separately; it is not an OOM kill or a mathematical proof rejection.')
(out / 'certificate.json').write_text(json.dumps(certificate, indent=2, sort_keys=True)+'\n')
(out / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n')
print(json.dumps(dict(status='SAVED', files=len(manifest),
                     total_bytes=sum(v['bytes'] for v in manifest.values()),
                     certificate=certificate), sort_keys=True))
