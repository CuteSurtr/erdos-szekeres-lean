#!/usr/bin/env python3
"""Retain proof artifacts and verify compressed round trips in the campaign archive."""
import argparse,hashlib,importlib.util,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
def main():
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True)
    p.add_argument('files',type=Path,nargs='+');a=p.parse_args();a.archive.mkdir(parents=True,exist_ok=True)
    prior=Path(__file__).resolve().parent.parent/'C6C7REVIEW/m5_pilot.py'
    s=importlib.util.spec_from_file_location('archive_helper',prior);h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
    manifest=a.archive/'m5_proof_artifacts.json'
    rows=json.loads(manifest.read_text()) if manifest.exists() else []
    for path in a.files:
        try:relative=path.resolve().relative_to(a.archive.resolve())
        except ValueError:
            target=a.archive/path.name
            if target.exists() and target.read_bytes()!=path.read_bytes():
                raise ValueError('artifact basename already has different contents')
            shutil.copyfile(path,target);path=target;relative=Path(path.name)
        row=h.archived(path);row['file']=str(relative);rows.append(row)
        print(json.dumps(row),flush=True)
    manifest.write_text(json.dumps(rows,indent=2)+'\n')
if __name__=='__main__':main()
