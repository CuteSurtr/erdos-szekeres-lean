"""Check that the 3,131 constraints of balanced-v2-source.json are exactly the Lean rows, in order:
rows 0..2684 = OmissionBalanced.support/demand (BalancedProof/Catalog.lean, arrays rowsK of (support, demand, _)),
rows 2685..3130 = BalancedCoverCutsV2.support/demand (support0..support445, `def demand : Fin 446 → ℕ := ![...]`)."""
import json, re, sys, hashlib
SRC = '/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-compact-checker-2026-11-05/build/chain311/src/'
J = '/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'
raw = open(J, 'rb').read(); assert hashlib.sha256(raw).hexdigest().startswith('acaf6323')
cons = json.loads(raw)['constraints']; assert len(cons) == 3131
cat = open(SRC + 'BalancedProof/Catalog.lean').read()
# rows arrays in file order; each entry "({a, b, ...}, demand, big)"
blocks = re.findall(r'def rows(\d+) : Array \(Finset \(Fin 252\) × ℕ × ℕ\) := #\[(.*?)\n\]', cat, re.S)
lean = []
for start, body in sorted(blocks, key=lambda b: int(b[0])):
    assert int(start) == len(lean), (start, len(lean))
    for s, d in re.findall(r'\(\{([0-9, ]*)\}, (\d+), \d+\)', body):
        lean.append((sorted(int(x) for x in s.split(',')), int(d)))
# how OmissionBalanced.support/demand index the arrays
tail = cat[cat.rfind('def rows'):]
print('rows parsed', len(lean)); print([l for l in cat.splitlines() if re.match(r'^(noncomputable )?def (row|support|demand)\b', l)][:6])
cut = open(SRC + 'BalancedCoverCutsV2.lean').read()
sup = {int(k): sorted(int(x) for x in v.split(',')) for k, v in re.findall(r'^def support(\d+) : Finset \(Fin 252\) := \{([0-9, ]*)\}', cut, re.M)}
dem = [int(x) for x in re.search(r'^def demand : Fin 446 → ℕ := !\[([0-9, ]*)\]', cut, re.M).group(1).split(',')]
assert len(sup) == 446 and len(dem) == 446
for k in range(446): lean.append((sup[k], dem[k]))
assert len(lean) == 3131, len(lean)
bad = [i for i, (c, (s, d)) in enumerate(zip(cons, lean)) if sorted(c['support']) != s or c['rhs'] != d]
print('mismatches', len(bad), bad[:10])
sys.exit(1 if bad else 0)
