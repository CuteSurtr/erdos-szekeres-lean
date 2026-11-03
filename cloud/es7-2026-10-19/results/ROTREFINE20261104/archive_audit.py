#!/usr/bin/env python3
"""Audit a stopped campaign archive with streaming hashes and zstd round trips.

Existing compressed artifacts must match their raw files. Missing compressed
copies are created with one compression thread. Changing files or mismatches
stop the audit; this script does not silently repair existing discrepancies.
"""
import argparse, datetime, hashlib, json, subprocess, time
from pathlib import Path
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while data:=f.read(1<<20):h.update(data)
    return h.hexdigest()
def decompressed_sha(path):
    h=hashlib.sha256();proc=subprocess.Popen(['zstd','-q','-dc',str(path)],stdout=subprocess.PIPE)
    try:
        while data:=proc.stdout.read(1<<20):h.update(data)
    finally:
        proc.stdout.close()
    if proc.wait()!=0:raise RuntimeError('decompression failed: '+str(path.name))
    return h.hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True)
    p.add_argument('--summary',type=Path,required=True);a=p.parse_args();root=a.archive.resolve()
    manifest=root/'ARCHIVE_MANIFEST.json';checksum=root/'ARCHIVE_MANIFEST.sha256';start=time.monotonic()
    orphans=[str(x.relative_to(root)) for x in root.rglob('*.zst') if not Path(str(x)[:-4]).exists()]
    if orphans:raise ValueError('compressed-only artifacts need explicit review: '+repr(orphans))
    paths=sorted(x for x in root.rglob('*') if x.is_file() and x.suffix!='.zst' and x not in (manifest,checksum))
    records=[]
    for index,path in enumerate(paths,1):
        if path.is_symlink():raise ValueError('unexpected archive symlink')
        before=path.stat();raw=sha(path);compressed=Path(str(path)+'.zst');created=not compressed.exists()
        if created:subprocess.run(['zstd','-q','-T1',str(path),'-o',str(compressed)],check=True)
        replay=decompressed_sha(compressed)
        if replay!=raw:raise ValueError('raw/compressed mismatch: '+str(path.relative_to(root)))
        after=path.stat()
        if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):raise ValueError('archive file changed during audit')
        records.append({'file':str(path.relative_to(root)),'bytes':after.st_size,'raw_sha256':raw,
            'zstd_sha256':sha(compressed),'compressed_bytes':compressed.stat().st_size,
            'roundtrip_sha256':replay,'compressed_copy_created':created})
        if index%100==0:print(json.dumps({'audited_files':index,'total_files':len(paths)}),flush=True)
    payload={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope':'all raw files present after owned archive writers stopped','records':records}
    manifest.write_text(json.dumps(payload,indent=2)+'\n');digest=sha(manifest)
    checksum.write_text(digest+'  ARCHIVE_MANIFEST.json\n')
    summary={'files':len(records),'raw_bytes':sum(r['bytes'] for r in records),
        'compressed_bytes':sum(r['compressed_bytes'] for r in records),'all_roundtrips_verified':True,
        'manifest_sha256':digest,'elapsed_seconds':round(time.monotonic()-start,3),
        'utc':payload['utc'],'archive':'proof-archives/es8-rot-refine-2026-11-04'}
    a.summary.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
