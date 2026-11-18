#!/usr/bin/env python3
"""Reproduce the checked numeric tables and seven-subset blocks in scratch."""
from pathlib import Path
from itertools import combinations
import json

ROOT = Path(__file__).resolve().parent
OUT = Path('/home/jay/research/data/delta3-codex-20261113/extension/lean/geometry-generated')
OUT.mkdir(exist_ok=True)
points = json.loads((ROOT / 'data/balanced-witness.json').read_text())['P']


def determinant(a, b, c):
    x, y = points[a]
    u, v = points[b]
    w, z = points[c]
    return (u - x) * (z - y) - (v - y) * (w - x)


def save(name, source):
    (OUT / name).write_text(source)
    assert source == (ROOT / name).read_text(), name


values = [determinant(*triple) for triple in combinations(range(15), 3)]
source = '''import FiniteModel

set_option maxRecDepth 32768

namespace Delta3.Balanced15

/-- Exact integer determinant values in the lexicographic order of the 455 triples. -/
def expectedDeterminants : List Int := [
'''
source += '\n'.join('  ' + ', '.join(map(str, values[i:i+15])) +
                    (',' if i + 15 < len(values) else '') for i in range(0, len(values), 15))
source += '''
]

def computedDeterminants : List Int := (choose 3 indices).map fun s =>
  match s with
  | [a,b,c] => det a b c
  | _ => 0

theorem exact_determinant_table : computedDeterminants = expectedDeterminants := by decide +kernel

theorem triple_count : (choose 3 indices).length = 455 := by decide +kernel

theorem five_count : (choose 5 indices).length = 3003 := by decide +kernel

theorem seven_count : (choose 7 indices).length = 6435 := by decide +kernel

#print axioms exact_determinant_table
#print axioms triple_count
#print axioms five_count
#print axioms seven_count

end Delta3.Balanced15
'''
save('Determinants.lean', source)
sets = list(combinations(range(15), 7))
for n, start in enumerate(range(0, len(sets), 512)):
    block = sets[start:start+512]
    name = f'sevenBlock{n:02}'
    source = 'import FiniteModel\n\nset_option maxRecDepth 32768\n\nnamespace Delta3.Balanced15\n\n'
    source += f'def {name} : List (List Index) := [\n'
    source += '\n'.join('  [' + ', '.join(map(str, s)) + ']' +
                        (',' if k + 1 < len(block) else '') for k, s in enumerate(block)) + '\n]\n\n'
    source += f'theorem no_seven_block_{n:02} : {name}.all (fun s => !signConvex s) = true := by\n'
    source += f'  decide +kernel\n\n#print axioms no_seven_block_{n:02}\n\nend Delta3.Balanced15\n'
    save(f'SevenBlock{n:02}.lean', source)
    source = f'''import SevenBlock{n:02}

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem seven_cover_{n:02} :
    ((choose 7 indices).drop {512*n}).take 512 = sevenBlock{n:02} := by
  decide +kernel

#print axioms seven_cover_{n:02}

end Delta3.Balanced15
'''
    save(f'SevenCover{n:02}.lean', source)
print('All 27 generated fixture sources reproduce the checked repository bytes.')
