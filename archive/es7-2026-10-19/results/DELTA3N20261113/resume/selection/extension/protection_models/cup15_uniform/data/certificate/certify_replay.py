"""Replay the retained binary LRAT on the independently audited CNF."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path,obj):
    with path.open('x') as f:
        json.dump(obj,f,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
        os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--audit',type=Path,required=True)
    ap.add_argument('--source-certificate',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    match=json.loads((args.audit/'cup_clause_match.json').read_text())
    assert match['status']=='PASS' and match['complete_clause_multiset_equal']
    assert json.loads((args.audit/'summary.json').read_text())['status']=='PASS'
    audited=args.audit/'parent_membership.cnf';assert sha(audited)==match['input_sha256']
    assert audited.read_bytes()==(args.source_certificate/'input.cnf').read_bytes()
    shutil.copy2(audited,args.out/'input.cnf');shutil.copy2(__file__,args.out/'certify_replay.py')
    shutil.copy2(args.audit/'cup_clause_match.json',args.out/'cup_clause_match.json')
    for name in ('proof.blrat','proof.blrat.zst'):shutil.copy2(args.source_certificate/name,args.out/name)
    decoded=subprocess.run(['/usr/bin/zstd','-q','-d','-c',str(args.out/'proof.blrat.zst')],capture_output=True,check=True,timeout=5).stdout
    assert decoded==(args.out/'proof.blrat').read_bytes()
    cake=Path('/home/jay/.local/bin/cake_lpr')
    command=['/usr/bin/time','-v','-o',str(args.out/'cake.time'),'/usr/bin/timeout','--kill-after=1','15',str(cake),
             '--CML_HEAP_SIZE=64','--CML_STACK_SIZE=32',str(args.out/'input.cnf'),str(args.out/'proof.blrat')]
    initial={'status':'STARTED','source_certificate':str(args.source_certificate),'audited_geometry':str(args.audit),
             'command':command,'limits':{'address_space_mib':400,'cpu_count':1,'external_seconds':20,'cake_seconds':15,'heap_mib':64,'stack_mib':32},
             'hashes':{name:sha(args.out/name) for name in ('input.cnf','proof.blrat','proof.blrat.zst','certify_replay.py','cup_clause_match.json')},
             'cake_lpr_sha256':sha(cake),'compressed_roundtrip_verified':True}
    save(args.out/'STARTED.json',initial)
    with (args.out/'cake.log').open('x') as f:proc=subprocess.run(command,stdout=f,stderr=subprocess.STDOUT,timeout=18)
    lines=(args.out/'cake.log').read_text().splitlines()
    accepted=proc.returncode==0 and 's VERIFIED UNSAT' in lines
    result=initial|{'status':'UNSAT_CERTIFIED' if accepted else 'REJECTED_OR_INCOMPLETE',
                    'label':'CERTIFIED' if accepted else 'COMPUTED','checker_exit':proc.returncode,
                    'exact_acceptance_line':'s VERIFIED UNSAT' if accepted else None,'seconds':time.monotonic()-start}
    result['hashes']=initial['hashes']|{name:sha(args.out/name) for name in ('cake.log','cake.time')}
    save(args.out/'result.json',result)
    for path in args.out.iterdir():
        if path.is_file():
            with path.open('rb') as f:
                os.fsync(f.fileno());os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
    print(json.dumps({'status':result['status'],'exact_acceptance_line':result['exact_acceptance_line'],'seconds':result['seconds'],'hashes':result['hashes']}))
    if not accepted:raise SystemExit(1)


if __name__=='__main__':main()
