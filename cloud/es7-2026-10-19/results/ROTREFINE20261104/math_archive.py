#!/usr/bin/env python3
"""Compress retained math evidence with raw/compressed hashes and round trips."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while block:=f.read(1<<20):h.update(block)
    return h.hexdigest()


def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);a=ap.parse_args();records=[]
    for p in sorted(a.root.rglob('*')):
        if not p.is_file() or p.suffix=='.zst' or p.name=='math_archive_manifest.json':continue
        z=Path(str(p)+'.zst')
        raw=digest(p)
        subprocess.run(['zstd','-q','-f','-T1',str(p),'-o',str(z)],check=True)
        h=hashlib.sha256();proc=subprocess.Popen(['zstd','-q','-dc',str(z)],stdout=subprocess.PIPE)
        while block:=proc.stdout.read(1<<20):h.update(block)
        assert proc.wait()==0 and h.hexdigest()==raw
        records.append({'file':str(p.relative_to(a.root)),'raw_sha256':raw,'zstd_sha256':digest(z),
                        'raw_bytes':p.stat().st_size,'compressed_bytes':z.stat().st_size,'roundtrip':True})
    (a.root/'math_archive_manifest.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps({'files':len(records),'raw_bytes':sum(r['raw_bytes'] for r in records),'compressed_bytes':sum(r['compressed_bytes'] for r in records),'all_roundtrips':True}))


if __name__=='__main__':main()
