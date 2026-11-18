#!/usr/bin/env python3
"""Archive attemptA and repair optional child-IO telemetry for a fresh replay."""
import hashlib,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'data/attemptA';A.mkdir(exist_ok=False)
source=R/'tools/replay.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(source)=='f7a38556968ee3d32b49c88055d1379b5b682b485346b47a4e09707fdea20dcf'
shutil.copyfile(source,A/'replay.py')
shutil.copytree(R/'data/replay',A/'replay')
for name in ('unit.stderr','unit.stdout','unit-start.txt','unit-attempt1-final.txt','unit-attempt1-journal.txt','unit-released.txt'):
 shutil.copyfile(R/'data'/name,A/name)
original=source.read_text();text=original
changes=[("D=R/'data/replay'","D=R/'data/retryB'"),
 ('nov13c-vfy-delta6-low16-independent','nov13c-vfy-delta6-low16-retryb'),
 ('except (FileNotFoundError,ProcessLookupError):rchar=lastchar',
  'except (FileNotFoundError,ProcessLookupError,PermissionError):rchar=lastchar')]
for before,after in changes:
 assert text.count(before)==1,(before,text.count(before));text=text.replace(before,after)
compile(text,str(R/'tools/replay_retryB.py'),'exec')
with (R/'tools/replay_retryB.py').open('x') as f:f.write(text)
files=sorted(p for p in A.rglob('*') if p.is_file())
with (A/'SHA256SUMS').open('x') as f:
 for p in files:f.write(f'{sha(p)}  {p.relative_to(A)}\n')
receipt={'status':'PASS','attemptA_source_sha256':sha(source),'attemptA_manifest_sha256':sha(A/'SHA256SUMS'),
 'retryB_source_sha256':sha(R/'tools/replay_retryB.py'),'changes':changes,
 'proof_access_or_checker_logic_changed':False,'fresh_replay_required':True,
 'attemptA_status':'checker printed accepted line; wrapper failed on optional telemetry; original records preserved',
 'prior_posthash_recovery':'supplemental only, not the requested final clean retryB receipt'}
with (R/'data/retryB-preparation.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(receipt))
