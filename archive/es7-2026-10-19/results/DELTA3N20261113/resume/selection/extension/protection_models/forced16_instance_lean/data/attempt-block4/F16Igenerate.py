#!/usr/bin/env python3
"""Transcribe fixed inputs; Lean independently reduces every claimed finite fact."""
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / 'forced16_realization/data'
cert_bytes = (INPUT / 'certificate.json').read_bytes()
sign_bytes = (INPUT / 'orientation.signs').read_bytes()
assert hashlib.sha256(cert_bytes).hexdigest() == 'cfe42cec6041709b2ed7ac18ee16b13e57f091239ac19b8e5257aac46d2a326d'
assert hashlib.sha256(sign_bytes).hexdigest() == 'b21664b06887c4019d75023025b1cd80582064a0b06f53698d2a70bc8fc49067'
cert = json.loads(cert_bytes)
signs = sign_bytes.decode().strip()
triples = list(itertools.combinations(range(16), 3))
assert len(signs) == len(triples) == 560
assert set(signs) == {'+', '-'}
CHUNK = 4
rows = cert['rows']
assert len(rows) == 387

header = '''import F16Cancellation

namespace Delta3.Forced16Instance

open Delta3.Forced16Algebra

structure Triple where
  a : Nat
  b : Nat
  c : Nat
  deriving BEq, DecidableEq, Repr

structure Row where
  a : Nat
  b : Nat
  c : Nat
  d : Nat
  e : Nat
  largeSlot : Nat
  smallSlot : Nat
  otherSlot : Nat
  large1 : Nat
  large2 : Nat
  small1 : Nat
  small2 : Nat
  weight : Nat
  deriving BEq, DecidableEq, Repr

'''
def lean_list(xs):
    return '[\n' + ',\n'.join('  ' + x for x in xs) + '\n]'
data = header
data += 'def triples : List Triple := ' + lean_list(['⟨%d, %d, %d⟩' % t for t in triples]) + '\n\n'
data += 'def signs : List Bool := ' + lean_list(['true' if s == '+' else 'false' for s in signs]) + '\n\n'
row_terms = []
reconstructed = []
for r in rows:
    a = r['root']
    b, c, d, e = r['other']
    pairs = [((a,b,c),(a,d,e)), ((a,b,d),(a,c,e)), ((a,b,e),(a,c,d))]
    large, small = r['large'], r['small']
    other = 3 - large - small
    large_ids = [triples.index(tuple(sorted(t))) for t in pairs[large]]
    small_ids = [triples.index(tuple(sorted(t))) for t in pairs[small]]
    assert large_ids == r['positive_brackets']
    assert small_ids == r['negative_brackets']
    fields = [a,b,c,d,e,large,small,other,*large_ids,*small_ids,r['weight']]
    row_terms.append('⟨' + ', '.join(map(str, fields)) + '⟩')
    reconstructed.append(fields)
data += 'def rows : List Row := ' + lean_list(row_terms) + '\n\n'
data += '''def vars : List Nat := List.range 560

def canonical (t : Triple) : Triple :=
  if t.a ≤ t.b then
    if t.b ≤ t.c then t else if t.a ≤ t.c then ⟨t.a, t.c, t.b⟩ else ⟨t.c, t.a, t.b⟩
  else
    if t.a ≤ t.c then ⟨t.b, t.a, t.c⟩
    else if t.b ≤ t.c then ⟨t.b, t.c, t.a⟩ else ⟨t.c, t.b, t.a⟩

def oddPermutation (t : Triple) : Bool :=
  if t.a ≤ t.b then
    if t.b ≤ t.c then false else if t.a ≤ t.c then true else false
  else
    if t.a ≤ t.c then true else if t.b ≤ t.c then false else true

def canonicalPositive (t : Triple) : Bool := signs[triples.idxOf t]?.getD false

def orderedPositive (t : Triple) : Bool :=
  if oddPermutation t then !canonicalPositive (canonical t)
  else canonicalPositive (canonical t)

def rawFactors (r : Row) (slot : Nat) : Triple × Triple :=
  match slot with
  | 0 => (⟨r.a, r.b, r.c⟩, ⟨r.a, r.d, r.e⟩)
  | 1 => (⟨r.a, r.b, r.d⟩, ⟨r.a, r.c, r.e⟩)
  | _ => (⟨r.a, r.b, r.e⟩, ⟨r.a, r.c, r.d⟩)

def termPositive (r : Row) (slot : Nat) : Bool :=
  let fs := rawFactors r slot
  let same := orderedPositive fs.1 == orderedPositive fs.2
  if slot == 1 then !same else same

def boundPair (r : Row) (slot i j : Nat) : Bool :=
  let fs := rawFactors r slot
  decide (triples[i]? = some (canonical fs.1)) &&
    decide (triples[j]? = some (canonical fs.2))

def rowValid (r : Row) : Bool :=
  decide ([r.a, r.b, r.c, r.d, r.e].Nodup) &&
    [r.a, r.b, r.c, r.d, r.e].all (fun i => i < 16) &&
    decide (canonical ⟨r.largeSlot, r.smallSlot, r.otherSlot⟩ = ⟨0, 1, 2⟩) &&
    decide (0 < r.weight) && boundPair r r.largeSlot r.large1 r.large2 &&
    boundPair r r.smallSlot r.small1 r.small2 &&
    [0, 1, 2].all (fun slot =>
      let fs := rawFactors r slot
      triples.contains (canonical fs.1) && triples.contains (canonical fs.2)) &&
    (termPositive r r.largeSlot != termPositive r r.smallSlot) &&
    (termPositive r r.largeSlot != termPositive r r.otherSlot)

def smallExp (r : Row) (j : Nat) : Nat :=
  (if j = r.small1 then 1 else 0) + (if j = r.small2 then 1 else 0)

def largeExp (r : Row) (j : Nat) : Nat :=
  (if j = r.large1 then 1 else 0) + (if j = r.large2 then 1 else 0)

def balanced (j : Nat) : Bool :=
  decide (natTotal rows (fun r => smallExp r j * r.weight) =
    natTotal rows (fun r => largeExp r j * r.weight))

end Delta3.Forced16Instance
'''
(HERE / 'F16IData.lean').write_text(data)
modules = ['F16IData']
for kind, count, predicate, source in [('Rows',387,'rowValid','rows'),('Columns',560,'balanced','vars')]:
    for block, start in enumerate(range(0, count, CHUNK)):
        name = f'F16I{kind}{block:02d}'
        theorem = f'{kind.lower()}_{block:02d}'
        text = f'''import F16IData

namespace Delta3.Forced16Instance

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem {theorem} : (({source}.drop {start}).take {CHUNK}).all {predicate} = true := by
  decide +kernel

#print axioms {theorem}

end Delta3.Forced16Instance
'''
        (HERE / (name + '.lean')).write_text(text)
        modules.append(name)
aggregate = ''.join(f'import {m}\n' for m in modules[1:])
aggregate += '''
namespace Delta3.Forced16Instance

open Delta3.Forced16Algebra

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem all_of_take_drop {α : Type} (xs : List α) (p : α → Bool) (start size : Nat)
    (hb : ((xs.drop start).take size).all p = true)
    (ht : (xs.drop (start + size)).all p = true) : (xs.drop start).all p = true := by
  have h := (congrArg (fun ys => ys.all p) (List.take_append_drop size (xs.drop start))).symm
  rw [List.all_append, List.drop_drop, hb, ht] at h
  exact h

theorem rows_count : rows.length = 387 := by decide +kernel
theorem variables_count : vars.length = 560 := by decide +kernel
theorem triples_count : triples.length = 560 := by decide +kernel
theorem signs_count : signs.length = 560 := by decide +kernel
theorem positive_weights : rows.all (fun r => decide (0 < r.weight)) = true := by
  decide +kernel

'''
for kind,count,predicate,source in [('Rows',387,'rowValid','rows'),('Columns',560,'balanced','vars')]:
    n = (count+CHUNK-1)//CHUNK
    aggregate += f'theorem all_{kind.lower()} : {source}.all {predicate} = true := by\n'
    aggregate += f'  have h{n} : ({source}.drop {CHUNK*n}).all {predicate} = true := by decide +kernel\n'
    for block in reversed(range(n)):
        aggregate += f'  have h{block} : ({source}.drop {CHUNK*block}).all {predicate} = true :=\n'
        aggregate += f'    all_of_take_drop {source} {predicate} {CHUNK*block} {CHUNK} {kind.lower()}_{block:02d} h{block+1}\n'
    aggregate += '  exact h0\n\n'
aggregate += '''theorem every_weight_positive (r : Row) (hr : r ∈ rows) : 0 < r.weight := by
  exact of_decide_eq_true (List.all_eq_true.mp positive_weights r hr)

theorem every_exponent_balanced (j : Nat) (hj : j ∈ vars) :
    natTotal rows (fun r => smallExp r j * r.weight) =
      natTotal rows (fun r => largeExp r j * r.weight) := by
  exact of_decide_eq_true (List.all_eq_true.mp all_columns j hj)

theorem every_row_valid (r : Row) (hr : r ∈ rows) : rowValid r = true :=
  List.all_eq_true.mp all_rows r hr

open Lean.Grind Std

/-- The fixed 387 inequalities admit no positive assignment of the 560 bracket magnitudes.
This statement still assumes the strict monomial inequalities; coordinate semantics is separate. -/
theorem no_positive_monomial_assignment {K : Type u} [CommRing K] [LE K] [LT K]
    [LawfulOrderLT K] [IsLinearOrder K] [OrderedRing K]
    (x : Nat → K) (hx : ∀ j ∈ vars, 0 < x j)
    (hlt : ∀ r ∈ rows, monomial vars x (smallExp r) < monomial vars x (largeExp r)) :
    False := by
  exact cancelling_certificate_contradiction rows (by decide +kernel) vars x
    smallExp largeExp Row.weight hx every_weight_positive hlt every_exponent_balanced

#print axioms all_of_take_drop
#print axioms rows_count
#print axioms variables_count
#print axioms triples_count
#print axioms signs_count
#print axioms positive_weights
#print axioms all_rows
#print axioms all_columns
#print axioms every_weight_positive
#print axioms every_exponent_balanced
#print axioms every_row_valid
#print axioms no_positive_monomial_assignment

end Delta3.Forced16Instance
'''
(HERE / 'F16IAggregate.lean').write_text(aggregate)
modules.append('F16IAggregate')
(HERE / 'data/generation.json').write_text(json.dumps({
    'certificate_sha256':hashlib.sha256(cert_bytes).hexdigest(),
    'signs_sha256':hashlib.sha256(sign_bytes).hexdigest(),
    'row_count':len(rows), 'variable_count':len(triples),
    'modules':modules, 'reconstructed_rows':reconstructed,
    'status':'Generated sources; kernel verification required.'},indent=2)+'\n')
print(json.dumps({'generated_modules':len(modules),'rows':len(rows),'vars':len(triples)}))
