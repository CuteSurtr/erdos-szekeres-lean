#!/usr/bin/env python3
"""Rank-aware export of coupled-core semantics as kernel-checked Lean terms.

Adapted from the repository's frozen export_omission_coupled_sized.py at
SHA-256 8a0a6390d289d243750a88609413c1d14288ed32b9b6c54396401345dbde6c14.
The sibling remains byte-frozen for existing certificate provenance. This
version conditionally imports CoupledDomain only for source_cup clauses;
without such clauses it reproduces the older export byte for byte.

The source_cup detail is [i,j] for distinct local owner indices. It excludes
chronological i-before-j with cup coordinate at least source height plus two.
The literal threshold and direction are checked by Lean's covered_clause.

The JSON is untrusted input. Each emitted clause is checked against a generic
geometric necessity lemma, and the literal CNF/LRAT refutation is independently
checked by Mathlib's proof-term builder. No solver result is assumed.
"""
import argparse,json,re
from pathlib import Path

LEGACY_EXPORTER_SHA256='8a0a6390d289d243750a88609413c1d14288ed32b9b6c54396401345dbde6c14'

def export(source, output, namespace, artifact, stem):
 if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", namespace):
  raise ValueError("Invalid Lean namespace")
 if not re.fullmatch(r"[A-Za-z0-9_-]+", artifact) or not re.fullmatch(r"[A-Za-z0-9_-]+", stem):
  raise ValueError("Invalid artifact path")
 d=json.loads(source.read_text());S=d['support'];size=len(S)
 if not 8 <= size <= 154 or len(set(S)) != size or any(type(x) is not int or not 0 <= x < 154 for x in S):
  raise ValueError("Expected 8 to 154 distinct residual states")
 rank_clauses=any(c['kind']=='source_cup' for c in d['clauses'])
 for c in d['clauses']:
  if c['kind']=='source_cup':
   q=c['detail']
   if not isinstance(q,list) or len(q)!=2 or any(type(i) is not int or not 0<=i<size for i in q) or q[0]==q[1]:
    raise ValueError('source_cup detail must contain two distinct local owner indices')
 raw='import ErdosSzekeres.Omission.CoupledLrat\nimport ErdosSzekeres.Omission.CoupledSemantics\n'
 if rank_clauses:raw+='import CoupledDomain\n'
 raw+='\n'
 raw+='namespace ErdosSzekeres.Omission.CoupledCore13\nopen Coupled\nset_option maxRecDepth 100000\nset_option maxHeartbeats 100000000\n\n'
 raw+='lrat_raw cnf_refutation\n  (include_str "../../experiments/omission-coupled-core-2026-10-10/core13.cnf")\n  (include_str "../../experiments/omission-coupled-core-2026-10-10/core13.lrat")\n\n'
 raw+='def support : List (Fin 154) := ['+', '.join(map(str,S))+']\n\ndef states : Fin 13 → Fin 154 := support.get\n\n'
 def atom(v):
  names={'before':'before','cap_ge':'capGe','cup_ge':'cupGe','orientation':'positive','convex_four':'convex'}
  return '.'+names[v[0]]+' '+' '.join(map(str,v[1:]))
 raw+='def atoms : List (Atom 13) := [\n  '+',\n  '.join(atom(v) for v in d['variables'])+']\n\n'
 def clause(c):return '['+', '.join(('.pos ' if x>0 else '.neg ')+str(abs(x)-1) for x in c['literals'])+']'
 for i,c in enumerate(d['clauses']):raw+=f'private def clause{i:03d} : Sat.Clause := {clause(c)}\n'
 raw+='\nprivate def clauses : Sat.Fmla := [\n  '+', '.join(f'clause{i:03d}' for i in range(len(d['clauses'])))+']\n\n'
 raw+='private theorem formula_eq : cnf_refutation.formula = clauses := by rfl\n\n'
 raw+='variable {n : ℕ} (C : Context 13 n states)\n\n'
 for i,c in enumerate(d['clauses']):
  kind=c['kind'];q=c['detail'];n3=' '.join(map(str,q[:3]));n4=' '.join(map(str,q[:4]));dc='(by decide)';kc='(by decide +kernel)'
  if kind=='empty_direction':proof=f'C.empty_clause {q[0]} {q[1]} {dc} {kc}'
  elif kind=='domain':proof=f'C.domain_clause {q[0]} {q[1]} {dc} {q[2]} {q[3]} {kc}'
  elif kind=='source_cup':proof=f'C.source_cup_clause {q[0]} {q[1]} {dc}'
  elif kind=='order_transitive':proof=f'C.transitive_clause {n3} {dc} {dc} {dc}'
  elif kind=='growth':proof=f'C.growth_clause {str(q[0]=="cup").lower()} '+ ' '.join(map(str,q[1:4]))+f' {dc} {dc} {dc} {q[4]}'
  elif kind=='fixed_sign':proof=f'C.fixed_{"positive" if q[3] else "negative"} {n3} {dc} {dc} {dc} {kc}'
  elif kind in ['packet','convex_four']:
   proof=f'C.{"packet" if kind=="packet" else "convex"}_clause {n4} '+ ' '.join([dc]*6)+' '+' '.join(str(x).lower() for x in q[4:])
   if kind=='packet':proof+=' '+kc
  elif kind=='no_octagon':proof=None
  else:raise ValueError(kind)
  raw+=f'-- Clause {i+1}: {kind}; source clause {c["original_id"]}.\n'
  raw+=f'private theorem sound{i:03d} : C.clause (decodeClause atoms clause{i:03d}) := by\n'
  if proof:raw+=f'  exact C.covered_clause _ _ ({proof}) {kc}\n\n'
  else:raw+='  exact C.no_octagon_clause {'+', '.join(map(str,q))+'} '+kc+' _ '+kc+'\n\n'
 raw+='private theorem all_sound : List.Forall (fun cl => C.clause (decodeClause atoms cl)) clauses := by\n'
 raw+='  exact '+''.join(f'And.intro (sound{i:03d} C) (' for i in range(len(d['clauses'])-1))+f"sound{len(d['clauses'])-1:03d} C"+')'*(len(d['clauses'])-1)+'\n\n'
 raw+='''theorem context_impossible (C : Context 13 n states) : False := by
  have h : (C.valuation atoms).satisfies_fmla cnf_refutation.formula := by
    rw [formula_eq]
    constructor
    intro cl hc
    exact C.satisfies_of_clause atoms cl ((List.forall_iff_forall_mem.mp (all_sound C)) cl hc)
  exact cnf_refutation (C.valuation atoms) h

#print axioms context_impossible
end ErdosSzekeres.Omission.CoupledCore13
'''
 raw=raw.replace('CoupledCore13', namespace)
 raw=raw.replace('Fin 13', f'Fin {size}').replace('Atom 13', f'Atom {size}').replace('Context 13', f'Context {size}')
 raw=raw.replace('omission-coupled-core-2026-10-10', artifact).replace('core13.cnf', stem+'.cnf').replace('core13.lrat', stem+'.lrat')
 output.write_text(raw)

if __name__ == '__main__':
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--source',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True)
 p.add_argument('--namespace',required=True)
 p.add_argument('--artifact',required=True)
 p.add_argument('--stem',required=True)
 a=p.parse_args();export(a.source,a.output,a.namespace,a.artifact,a.stem)
