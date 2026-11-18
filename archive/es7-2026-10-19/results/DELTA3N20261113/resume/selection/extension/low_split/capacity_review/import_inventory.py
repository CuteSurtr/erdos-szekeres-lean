#!/usr/bin/env python3
"""Read-only source-header/cache-size inventory. No Lean or build tool is invoked."""
from pathlib import Path
import json,hashlib,re
R=Path('/home/jay/research/lean/erdos-szekeres-lean')
T=Path('/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0')
roots=[(R,R/'.lake/build/lib/lean')]
roots += [(p,p/'.lake/build/lib/lean') for p in sorted((R/'.lake/packages').iterdir()) if p.is_dir()]
roots += [(T/'src/lean',T/'lib/lean')]
def strip_comments(text):
 out=[];i=0;depth=0
 while i<len(text):
  if text[i:i+2]=='/-':depth+=1;i+=2;continue
  if depth and text[i:i+2]=='-/':depth-=1;i+=2;continue
  if not depth and text[i:i+2]=='--':
   j=text.find('\n',i);i=len(text) if j<0 else j;continue
  if not depth:out.append(text[i])
  elif text[i]=='\n':out.append('\n')
  i+=1
 return ''.join(out)
def imports(p):
 # Stop at the first declaration. Commented examples never become imports.
 text=strip_comments(p.read_text())
 out=[]
 for line in text.splitlines():
  line=line.strip()
  if not line or line in ['prelude','module']:continue
  m=re.fullmatch(r'(?:(?:public|private)\s+)?import\s+([\w. ]+)',line)
  if not m:break
  names = m[1].split()
  if names and names[0] == 'all': names = names[1:]
  out += names
 return out
pending=['ErdosSzekeres.Omission.BaekGeometry'];seen={};missing=[]
while pending:
 module=pending.pop()
 if module in seen:continue
 rel=module.replace('.','/')
 located=None
 for src,cache in roots:
  path=src/(rel+'.lean')
  if path.exists():located=(path,cache/(rel+'.olean'));break
 if located is None:
  seen[module]=None;missing.append(module);continue
 p,o=located;im=imports(p)
 seen[module]={'source':str(p),'imports':im,'olean':str(o),'olean_bytes':o.stat().st_size if o.exists() else None}
 pending.extend(im)
known={m:x for m,x in seen.items() if x}
large=sorted(known,key=lambda m:known[m]['olean_bytes'] or 0,reverse=True)[:10]
summary=dict(status='static source-header inventory only; no Lean replay or RSS measurement',
 root='ErdosSzekeres.Omission.BaekGeometry',modules=len(known),
 main_olean_bytes=sum(x['olean_bytes'] or 0 for x in known.values()),
 full_mathlib_import='Mathlib' in known,
 mathlib_tactic_import='Mathlib.Tactic' in known,
 missing_source=missing,
 missing_olean=[m for m,x in known.items() if x['olean_bytes'] is None],
 largest_oleans=[dict(module=m,bytes=known[m]['olean_bytes']) for m in large],
 caveat='Does not estimate anonymous heap, all private/server companion mappings, or live resident memory.')
out=Path(__file__).resolve().parent
(out/'import-inventory.json').write_text(json.dumps(summary,indent=2)+'\n')
(out/'import-closure.json').write_text(json.dumps(known,indent=2)+'\n')
print(json.dumps(summary,indent=2))

