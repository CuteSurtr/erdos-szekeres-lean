#!/usr/bin/env python3
"""Compress copies of finished traces; retain the uncompressed originals.

SAT and UNKNOWN traces are explicitly not UNSAT certificates. In-progress
files are excluded. This script is run in a bounded, one-CPU research unit.
"""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path('/home/jay/research/data/delta3-codex-20261113')


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for data in iter(lambda: f.read(1 << 20), b''):
            h.update(data)
    return h.hexdigest()


items = []
for p in sorted((ROOT/'encoder').glob('*/result.json')):
    r = json.loads(p.read_text())
    if r.get('status') in ('STARTED', 'GENERATED', 'ENCODER_FAILED'):
        continue
    proof = p.parent/'case.lrat'
    if proof.is_file():
        items.append((proof, r.get('status'), r.get('hashes', {}).get('case.lrat')))
for sub in ('coordinator/cup15', 'coordinator/minimized/counterexample'):
    for proof in (ROOT/sub).glob('*.lrat'):
        items.append((proof, 'CERTIFIED_SMALL_FIXED_INSTANCE', None))
manifest_path = ROOT/'coordinator'/'archives.json'
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
already = {entry['file']: entry for entry in manifest}
for proof, status, expected in items:
    compressed = proof.with_suffix(proof.suffix+'.zst')
    if str(proof) in already:
        old = already[str(proof)]
        assert old['original_bytes'] == proof.stat().st_size
        assert old['compressed_bytes'] == compressed.stat().st_size
        assert not expected or old['original_sha256'] == expected
        continue  # Finished artifacts are immutable; the prior roundtrip is retained.
    if not compressed.exists():
        subprocess.run(['/usr/bin/zstd', '-q', '-T1', '-3', '-k', str(proof), '-o', str(compressed)], check=True)
    original_sha = sha(proof)
    if expected:
        assert original_sha == expected
    # Check decompressed bytes against the recorded original hash.
    h = hashlib.sha256()
    with subprocess.Popen(['/usr/bin/zstd', '-q', '-d', '-c', str(compressed)], stdout=subprocess.PIPE) as p:
        for data in iter(lambda: p.stdout.read(1 << 20), b''):
            h.update(data)
        assert p.wait() == 0
    assert h.hexdigest() == original_sha
    entry = dict(file=str(proof), status=status, original_bytes=proof.stat().st_size,
                 original_sha256=original_sha, compressed=str(compressed),
                 compressed_bytes=compressed.stat().st_size, compressed_sha256=sha(compressed),
                 roundtrip_checked=True, original_retained=True)
    manifest.append(entry)
    print(json.dumps(entry), flush=True)
manifest_path.write_text(json.dumps(manifest, indent=2)+'\n')
