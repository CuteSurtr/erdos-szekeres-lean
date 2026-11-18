#!/usr/bin/env python3
"""Generate the twelve-point finite fixture and proof templates from frozen adapters."""
from pathlib import Path
from itertools import combinations
import json
import re

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / 'lean_geometry'
P = json.loads((ROOT / 'data/T12-coordinates.json').read_text())['P']
assert len(P) == 12 and all(P[i][0] < P[i+1][0] for i in range(11))
def save(name, text):
    assert name.startswith('T12')
    (ROOT / name).write_text(text)
def adapt(text):
    text = text.replace('Delta3.Balanced15', 'Delta3.Terminal12')
    return re.sub(r'^import (\w+)$', lambda m: 'import T12' + m[1], text, flags=re.M)
text = adapt((OLD / 'FiniteModel.lean').read_text())
text = text.replace('Fin 15', 'Fin 12')
block = '  match i.val with\n' + '\n'.join(
    f'  | {i if i < 11 else "_"} => ({x}, {y})' for i,(x,y) in enumerate(P)) + '\n\n'
text = re.sub(r'  match i.val with\n.*?\n\ndef det', block + 'def det', text, flags=re.S)
text = re.sub(r'def indices : List Index := \[[^\n]+\]', 'def indices : List Index := [' +
              ', '.join(map(str,range(12))) + ']', text)
text = text.replace('six-tuple','five-tuple').replace('HitsSix','HitsFive')
text = text.replace('a b c d e f : Index', 'a b c d e : Index')
text = text.replace(' → e < f', '').replace('[a, b, c, d, e, f]', '[a, b, c, d, e]')
text = text.replace(' ∨ A f', '')
save('T12FiniteModel.lean', text)
save('T12FiniteFacts.lean', adapt((OLD / 'FiniteFacts.lean').read_text()))
save('T12IndexHelpers.lean', adapt((OLD / 'real_bridge/IndexHelpers.lean').read_text()))
save('T12PredicateSemantics.lean', adapt((OLD / 'PredicateSemantics.lean').read_text()))

def det(a,b,c):
    x,y=P[a];u,v=P[b];w,z=P[c]
    return (u-x)*(z-y)-(v-y)*(w-x)
values=[det(*t) for t in combinations(range(12),3)]
assert all(values)
text = 'import T12FiniteModel\n\nset_option maxRecDepth 32768\n\nnamespace Delta3.Terminal12\n\n'
text += '/-- Exact determinants in lexicographic order of the 220 increasing triples. -/\n'
text += 'def expectedDeterminants : List Int := [\n'
text += ',\n'.join('  '+', '.join(map(str,values[i:i+12])) for i in range(0,len(values),12))+'\n]\n\n'
text += '''def computedDeterminants : List Int := (choose 3 indices).map fun s =>
  match s with
  | [a, b, c] => det a b c
  | _ => 0

theorem exact_determinant_table : computedDeterminants = expectedDeterminants := by decide +kernel
theorem triple_count : (choose 3 indices).length = 220 := by decide +kernel
theorem five_count : (choose 5 indices).length = 792 := by decide +kernel
theorem six_count : (choose 6 indices).length = 924 := by decide +kernel

#print axioms exact_determinant_table
#print axioms triple_count
#print axioms five_count
#print axioms six_count

end Delta3.Terminal12
'''
save('T12Determinants.lean',text)
sets=list(combinations(range(12),6))
for n,start in enumerate(range(0,len(sets),512)):
    block=sets[start:start+512]
    name=f'sixBlock{n:02}'
    text='import T12FiniteModel\n\nset_option maxRecDepth 32768\n\nnamespace Delta3.Terminal12\n\n'
    text+=f'def {name} : List (List Index) := [\n'
    text+=',\n'.join('  ['+', '.join(map(str,s))+']' for s in block)+'\n]\n\n'
    text+=f'theorem no_six_block_{n:02} : {name}.all (fun s => !signConvex s) = true := by\n  decide +kernel\n\n'
    text+=f'#print axioms no_six_block_{n:02}\n\nend Delta3.Terminal12\n'
    save(f'T12SixBlock{n:02}.lean',text)
    text=f'''import T12SixBlock{n:02}

set_option maxRecDepth 32768

namespace Delta3.Terminal12

theorem six_cover_{n:02} :
    ((choose 6 indices).drop {start}).take 512 = sixBlock{n:02} := by
  decide +kernel

#print axioms six_cover_{n:02}

end Delta3.Terminal12
'''
    save(f'T12SixCover{n:02}.lean',text)
old=adapt((OLD/'SevenAggregate.lean').read_text())
helper=old[old.index('theorem all_of_take_drop'):old.index('theorem no_seven_sign_convex')]
text='import T12SixCover00\nimport T12SixCover01\nimport T12Determinants\n\nnamespace Delta3.Terminal12\n\n'+helper
text+='''theorem no_six_sign_convex : (choose 6 indices).all (fun s => !signConvex s) = true := by
  have he : (choose 6 indices).drop 1024 = [] :=
    List.drop_eq_nil_iff.mpr (by rw [six_count]; decide)
  have h2 : ((choose 6 indices).drop 1024).all (fun s => !signConvex s) = true := by
    rw [he]
    rfl
  have h1 : ((choose 6 indices).drop 512).all (fun s => !signConvex s) = true :=
    all_of_take_drop (choose 6 indices) (fun s => !signConvex s) 512 512
      (by rw [six_cover_01]; exact no_six_block_01) h2
  have h0 : ((choose 6 indices).drop 0).all (fun s => !signConvex s) = true :=
    all_of_take_drop (choose 6 indices) (fun s => !signConvex s) 0 512
      (by rw [six_cover_00]; exact no_six_block_00) h1
  exact h0

#print axioms all_of_take_drop
#print axioms no_six_sign_convex

end Delta3.Terminal12
'''
save('T12SixAggregate.lean',text)
text=adapt((OLD/'SubsequenceFacts.lean').read_text()).replace('Seven','Six').replace('seven','six')
text=re.sub(r'\b7\b','6',text)
save('T12SubsequenceFacts.lean',text)
print(json.dumps({'points':len(P),'triples':len(values),'min_abs_det':min(map(abs,values)),
                  'six_subsets':len(sets),'generated_modules':11},indent=2))

