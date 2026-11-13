#!/usr/bin/env python3
"""Bind the frozen 2598-row source tail to the checked Sixth and Fourth families."""
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / 'experiments/omission-residual32-2598-primal-2026-10-10/source-2598.json.gz'
OLD = ROOT / 'experiments/omission-residual32-research-2026-10-10/source.json.gz'
FOURTH = ROOT / 'experiments/omission-residual32-fourth-global-variants-2026-10-10'
SIXTH = ROOT / 'experiments/omission-residual32-witness-coupled-2026-10-10'
EXPECTED = '01d4fde13ae0ca43427540a3d529e7e29b875936332af2cc4ef7d423edee469b'
OLD_EXPECTED = 'f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    raw = gzip.decompress(SOURCE.read_bytes())
    old_raw = gzip.decompress(OLD.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == EXPECTED
    assert hashlib.sha256(old_raw).hexdigest() == OLD_EXPECTED
    source, old = json.loads(raw), json.loads(old_raw)
    assert source['states'] == old['states'] and len(source['constraints']) == 2598
    assert source['constraints'][:2469] == old['constraints']
    tail = source['constraints'][2469:]
    family = json.loads((FOURTH / 'row-bindings.json').read_bytes())['rows']
    core = json.loads((SIXTH / 'core13.json').read_bytes())['support']
    assert tail[0] == {'support': core, 'rhs': 1}
    assert tail[1:] == [{'support': r['support'], 'rhs': r['rhs']} for r in family]
    assert all(r['rhs'] == 1 and len(r['support']) == len(set(r['support'])) == 13 for r in tail)
    literals = ',\n'.join('  [' + ', '.join(map(str, r['support'])) + '].toFinset' for r in tail)
    lean = '''import Geometry
import FourthGlobalProof.Root

/-! Exact ordered 129-row suffix of the frozen 2598-row source.
The first 2469 rows remain covered by the separate frozen transfer. -/
namespace ErdosSzekeres.Omission.Residual32AddedRows
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

def literalSupports : Array (Finset (Fin 154)) := #[
''' + literals + '''
]

def support (r : Fin 129) : Finset (Fin 154) := literalSupports[r.val]!

def familySupport (r : Fin 129) : Finset (Fin 154) :=
  if h : r.val = 0 then CoupledCoreSixth.support.toFinset
  else CoupledFourthGlobalVariants.support ⟨r.val - 1, by omega⟩

theorem literal_binding : ∀ r : Fin 129, support r = familySupport r := by
  decide +kernel

/-- All 129 ordered demand-one additions hold for actual configurations. -/
theorem all_rows {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∀ r : Fin 129, 1 ≤
      (support r \\ c.residualOccupied noCap noOctagon noJunction).card := by
  intro r
  rw [literal_binding]
  unfold familySupport
  split
  · exact CoupledCoreSixth.hole_bound c noCap noOctagon noJunction
  · exact CoupledFourthGlobalVariants.all_rows c noCap noOctagon noJunction _

#print axioms literal_binding
#print axioms all_rows
end ErdosSzekeres.Omission.Residual32AddedRows
'''
    (HERE / 'AddedRows.lean').write_text(lean)
    dependencies = [SOURCE, OLD, FOURTH / 'manifest.json', FOURTH / 'row-bindings.json',
                    SIXTH / 'core13.json', SIXTH / 'core13.cnf', SIXTH / 'core13.lrat',
                    SIXTH / 'LeanCore.lean', SIXTH / 'Geometry.lean',
                    ROOT / 'experiments/omission-residual32-case4-2026-10-10/Witness.lean',
                    ROOT / 'experiments/omission-residual32-context-certificates-2026-10-10/Residual32ContextsProof/Catalog.lean']
    dependencies += sorted((FOURTH / 'FourthGlobalProof').glob('*.lean'))
    manifest = {
        'scope': 'Literal geometric validity of the ordered129 additions only; no global32-hole exclusion or improved planar bound.',
        'source': str(SOURCE.relative_to(ROOT)), 'source_uncompressed_sha256': EXPECTED,
        'old_source': str(OLD.relative_to(ROOT)), 'old_source_uncompressed_sha256': OLD_EXPECTED,
        'prefix_rows': 2469, 'source_rows': 2598, 'new_rows': 129,
        'row_order': 'local0/global2469 is Sixth core; local(k+1)/global(2470+k) is Fourth family k, for0≤k<128.',
        'namespace': 'ErdosSzekeres.Omission.Residual32AddedRows',
        'external_inputs': {str(p.relative_to(ROOT)): sha(p) for p in dependencies},
        'files': {'AddedRows.lean': sha(HERE / 'AddedRows.lean'), 'generate.py': sha(Path(__file__))},
        'bindings': [{'local_row': i, 'source_row': i + 2469, **r} for i, r in enumerate(tail)],
    }
    (HERE / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    main()
