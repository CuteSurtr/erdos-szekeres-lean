#!/usr/bin/env python3
"""FV302 (24 Nov 2026): generate CompactChecker/FcatZZs16.lean and CompactChecker/BridgeZZs16.lean.

fcatZZs16 = fcat62 (the 3,131 rows of balanced-v2-source.json, sha256 acaf6323...) with two rows added:
row 3131 = the Z-row (support OmissionZRow.zIndices, demand 16) and row 3132 = the Z*-row (support
OmissionZStarRow.zsIndices, demand 16). As in FV304's FcatZ, every subtree off the two new paths is fcat62's own
constant, so wf follows from fcat62_wf plus a kernel check of the two new rows, and get r = fcat62.get r for r < 3131
follows level by level (eq lemmas). The bridge turns the zero-side root exclusion over fcatZZs16 into
OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 b.
Usage: python3 -I gen_fcatzzs16.py FCAT62.lean ZINDICES ZSINDICES OUTDIR
"""
import re, sys

F62, ZI, ZSI, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
DEPTH = 12                       # indices < 4096, LSB-first trie
NEW = {3131: ('Z', ZI), 3132: ('Zs', ZSI)}
node, row = {}, set()
for line in open(F62):
    m = re.match(r'noncomputable def (fcat62(?:_\w+)?) : FCat := FCat\.node (\w+) (\w+)', line)
    if m: node[m.group(1)] = (m.group(2), m.group(3)); continue
    m = re.match(r'noncomputable def (fcat62_r\d+) : FCat := FCat\.row', line)
    if m: row.add(m.group(1))
assert 'fcat62' in node and len(row) == 3131, (len(row),)


def bits(i): return [(i >> d) & 1 for d in range(DEPTH)]


# The walk of one new index through fcat62: the old node at each depth, until the old trie collapses to a row.
def walk(i):
    b = bits(i); cur, out = 'fcat62', []
    for d in range(DEPTH):
        if cur in row: return out, d, cur          # collapsed: an old row stands where the path continues
        out.append((d, cur)); cur = node[cur][b[d]]
    raise AssertionError('index %d already present' % i)


defs, wf_lines, eq_thms = [], [], []
newname = {}                                     # path string -> new constant name
for i, (tag, lst) in NEW.items():
    defs.append('noncomputable def fcatZZs16_r%d : FCat := FCat.row %s 16 (codeL 4194304 %s)' % (i, lst, lst))
roots_children = {}
paths = {}
for i in NEW:
    steps, dcol, oldrow = walk(i)
    b = bits(i)
    # old row index at the collapse point: its remaining bits are 0 (it is the bit-0 side at depth dcol);
    # the new index continues with bit b[dcol] = 1 here (both new indices: last bit set)
    assert b[dcol] == 1 and all(x == 0 for x in bits(int(oldrow[len('fcat62_r'):]))[dcol:]), (i, dcol, oldrow)
    paths[i] = (steps, dcol, oldrow, b)

# build new nodes bottom-up for each path (the two paths share only the root)
shared_root = []
for i, (steps, dcol, oldrow, b) in paths.items():
    p = ''.join(str(x) for x in b[:dcol])
    leaf = 'fcatZZs16_n%s' % p                   # new node at the collapse point: (old row, new row)
    defs.append('noncomputable def %s : FCat := FCat.node %s fcatZZs16_r%d' % (leaf, oldrow, i))
    child = leaf
    for d, old in reversed(steps):
        l, r = node[old]
        nm = 'fcatZZs16' if d == 0 else 'fcatZZs16_n' + ''.join(str(x) for x in b[:d])
        if d == 0:
            shared_root.append((b[0], child)); continue
        nl, nr = (child, r) if b[d] == 0 else (l, child)
        defs.append('noncomputable def %s : FCat := FCat.node %s %s' % (nm, nl, nr))
        child = nm
# root: both children new (the paths start with different bits)
rc = dict(shared_root)
assert set(rc) == {0, 1}
defs.append('noncomputable def fcatZZs16 : FCat := FCat.node %s %s' % (rc[0], rc[1]))

# well-formedness: decompose fcat62_wf along both paths, recompose along the new nodes
wf = ['theorem FCat.wf_node2 {n b : ℕ} {l r : FCat} :', '    (FCat.node l r).wf n b = true ↔ l.wf n b = true ∧ r.wf n b = true := by',
      '  simp [FCat.wf]', '']
for i in NEW: wf.append('theorem fcatZZs16_r%d_wf : fcatZZs16_r%d.wf 252 4194304 = true := by decide +kernel' % (i, i))
wf.append('')
wf.append('theorem fcatZZs16_wf : fcatZZs16.wf 252 4194304 = true := by')
wf.append('  have h0 := FCat.wf_node2.mp (show (FCat.node %s %s).wf 252 4194304 = true from fcat62_wf)' % node['fcat62'])
have = {'fcat62_n0': 'h0.1', 'fcat62_n1': 'h0.2'}  # wf proof term of old constants along the paths
k = 0
for i, (steps, dcol, oldrow, b) in paths.items():
    for d, old in steps[1:]:
        l, r = node[old]; k += 1
        wf.append('  have a%d := FCat.wf_node2.mp (show (FCat.node %s %s).wf 252 4194304 = true from %s)' % (k, l, r, have[old]))
        have[l] = 'a%d.1' % k; have[r] = 'a%d.2' % k
for i, (steps, dcol, oldrow, b) in paths.items():
    p = ''.join(str(x) for x in b[:dcol])
    k += 1; leaf = 'fcatZZs16_n%s' % p
    wf.append('  have b%d : %s.wf 252 4194304 = true := FCat.wf_node2.mpr ⟨%s, fcatZZs16_r%d_wf⟩' % (k, leaf, have[oldrow], i))
    child, cproof = leaf, 'b%d' % k
    for d, old in reversed(steps):
        if d == 0: have['new%d' % b[0]] = cproof; continue
        l, r = node[old]; k += 1
        nm = 'fcatZZs16_n' + ''.join(str(x) for x in b[:d])
        pl, pr = (cproof, have[r]) if b[d] == 0 else (have[l], cproof)
        wf.append('  have b%d : %s.wf 252 4194304 = true := FCat.wf_node2.mpr ⟨%s, %s⟩' % (k, nm, pl, pr))
        child, cproof = nm, 'b%d' % k
wf.append('  exact FCat.wf_node2.mpr ⟨%s, %s⟩' % (have['new0'], have['new1']))

hdr = ('import CompactChecker.Fcat62\nnamespace CompactChecker\n'
       '-- FV302 (24 Nov 2026): fcatZZs16 = fcat62 (3,131 rows of balanced-v2-source.json, sha256 acaf6323...) with row\n'
       '-- 3131 = Z-row (OmissionZRow.zIndices, demand 16) and row 3132 = Z*-row (OmissionZStarRow.zsIndices, demand 16).\n'
       '-- Generated by gen_fcatzzs16.py; every subtree off the two new paths is fcat62\'s own constant.\n')
open(OUT + '/FcatZZs16.lean', 'w').write(hdr + '\n'.join(defs) + '\n\n' + '\n'.join(wf) + '\n\n#print axioms fcatZZs16_wf\nend CompactChecker\n')

# bridge: eq lemmas along both paths, then the rows lemma and the root bridge
E = []
def P(s): E.append(s)
P('-- FV302 (24 Nov 2026): the bridge from the compact check over fcatZZs16 to ExcludesHoleBudgetZZsN 16. Generated.')
P('import CompactChecker.Path\nimport CompactChecker.FcatZZs16\nimport CompactChecker.Bridge311Bal\nimport LemmaZ\nimport LemmaZStar\nimport BalancedBudgetsZZsN\n')
P('open ErdosSzekeres.OmissionCertificates\nopen scoped BigOperators\n\nnamespace CompactChecker.BridgeZZs16\n')
P('theorem node_get_even {l r : FCat} {k : ℕ} (h : k % 2 = 0) : (FCat.node l r).get k = l.get (k / 2) := by')
P('  show (bif Nat.beq (k % 2) 0 then l.get (k / 2) else r.get (k / 2)) = l.get (k / 2)\n  rw [h]; rfl\n')
P('theorem node_get_odd {l r : FCat} {k : ℕ} (h : k % 2 = 1) : (FCat.node l r).get k = r.get (k / 2) := by')
P('  show (bif Nat.beq (k % 2) 0 then l.get (k / 2) else r.get (k / 2)) = r.get (k / 2)\n  rw [h]; rfl\n')
for i, (steps, dcol, oldrow, b) in paths.items():
    p = ''.join(str(x) for x in b[:dcol])
    leaf = 'fcatZZs16_n%s' % p
    # at the collapse level: index 0 of the new node is the old row
    P('theorem eq_%d_%d : ∀ k, k < 2 → k ≠ 1 → %s.get k = %s.get k := by' % (i, dcol, leaf, oldrow))
    P('  intro k hk hne\n  obtain rfl : k = 0 := by omega\n  rfl\n')
    prev = 'eq_%d_%d' % (i, dcol); child_new = leaf
    for d, old in reversed(steps[1:]):
        l, r = node[old]
        nm = 'fcatZZs16_n' + ''.join(str(x) for x in b[:d])
        size, excl = 2 ** (DEPTH - d), i >> d
        newl, newr = (child_new, r) if b[d] == 0 else (l, child_new)
        P('theorem eq_%d_%d : ∀ k, k < %d → k ≠ %d → %s.get k = %s.get k := by' % (i, d, size, excl, nm, old))
        P('  intro k hk hne')
        P('  show (FCat.node %s %s).get k = (FCat.node %s %s).get k' % (newl, newr, l, r))
        P('  rcases Nat.mod_two_eq_zero_or_one k with h | h')
        if b[d] == 0:
            P('  · rw [node_get_even h, node_get_even h]\n    exact %s (k / 2) (by omega) (by omega)\n  · rw [node_get_odd h, node_get_odd h]\n' % prev)
        else:
            P('  · rw [node_get_even h, node_get_even h]\n  · rw [node_get_odd h, node_get_odd h]\n    exact %s (k / 2) (by omega) (by omega)\n' % prev)
        prev, child_new = 'eq_%d_%d' % (i, d), nm
    paths[i] = paths[i] + (prev, child_new)
# root: k even -> path of 3132 (bit 0), k odd -> path of 3131 (bit 1)
c0, c1 = node['fcat62']
p0 = [paths[i] for i in NEW if bits(i)[0] == 0][0]; p1 = [paths[i] for i in NEW if bits(i)[0] == 1][0]
P('theorem eq0 : ∀ k, k < 4096 → k ≠ 3131 → k ≠ 3132 → fcatZZs16.get k = fcat62.get k := by')
P('  intro k hk h1 h2')
P('  show (FCat.node %s %s).get k = (FCat.node %s %s).get k' % (p0[5], p1[5], c0, c1))
P('  rcases Nat.mod_two_eq_zero_or_one k with h | h')
P('  · rw [node_get_even h, node_get_even h]\n    exact %s (k / 2) (by omega) (by omega)' % p0[4])
P('  · rw [node_get_odd h, node_get_odd h]\n    exact %s (k / 2) (by omega) (by omega)\n' % p1[4])
P('theorem get_eq (r : ℕ) (hr : r < 3131) : fcatZZs16.get r = fcat62.get r := eq0 r (by omega) (by omega) (by omega)\n')
P('theorem zlist : (fcatZZs16.get 3131).1 = OmissionZRow.zIndices := by decide +kernel')
P('theorem zdem : fcatZZs16.dem 3131 = 16 := by decide +kernel')
P('theorem zslist : (fcatZZs16.get 3132).1 = OmissionZStarRow.zsIndices := by decide +kernel')
P('theorem zsdem : fcatZZs16.dem 3132 = 16 := by decide +kernel\n')
P('theorem zsupp : fsupp fcatZZs16 252 3131 = OmissionZRow.Z := by\n  ext i\n  rw [OmissionZRow.Z_eq]\n  simp only [fsupp, Finset.mem_filter, Finset.mem_univ, true_and, zlist]\n')
P('theorem zssupp : fsupp fcatZZs16 252 3132 = OmissionZStarRow.Zs := by\n  ext i\n  rw [OmissionZStarRow.Zs_eq]\n  simp only [fsupp, Finset.mem_filter, Finset.mem_univ, true_and, zslist]\n')
P('''/-- Every row of `fcatZZs16` holds for a 0/1 vector that satisfies the 2,685 base rows and both Z-rows at 16. -/
theorem fcatZZs16_rows (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤ ∑ i ∈ OmissionBalanced.support r, holes i)
    (hz : 16 ≤ ∑ i ∈ OmissionZRow.Z, holes i) (hzs : 16 ≤ ∑ i ∈ OmissionZStarRow.Zs, holes i) :
    ∀ r : Fin 3133, fcatZZs16.dem r.val ≤ ∑ i ∈ fsupp fcatZZs16 252 r.val, holes i := by
  intro ⟨r, hr⟩
  by_cases h : r < 3131
  · have h62 := CompactChecker.Bridge311Bal.fcat62_rows holes hbool hrows ⟨r, h⟩
    have hd : fcatZZs16.dem r = fcat62.dem r := by unfold FCat.dem; rw [get_eq r h]
    have hs : fsupp fcatZZs16 252 r = fsupp fcat62 252 r := by unfold fsupp; rw [get_eq r h]
    show fcatZZs16.dem r ≤ ∑ i ∈ fsupp fcatZZs16 252 r, holes i
    rw [hd, hs]
    exact h62
  · by_cases h' : r = 3131
    · subst h'
      show fcatZZs16.dem 3131 ≤ ∑ i ∈ fsupp fcatZZs16 252 3131, holes i
      rw [zsupp, zdem]
      exact hz
    · have e : r = 3132 := by omega
      subst e
      show fcatZZs16.dem 3132 ≤ ∑ i ∈ fsupp fcatZZs16 252 3132, holes i
      rw [zssupp, zsdem]
      exact hzs

/-- The bridge: the zero-side root exclusion of the compact export over `fcatZZs16` (state 0 occupied) gives
`OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 budget`. -/
theorem zzsn16_of_root {budget : ℕ}
    (h : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 budget (pmask (zerosF 252) [(0, 2)]) holes) :
    OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 budget := by
  rintro ⟨holes, h0, _, hb, hr, _, hz, hzs, hc⟩
  refine h ⟨holes, hb, fcatZZs16_rows holes hb hr hz hzs, hc, fun i hi => ?_, fun i hi => ?_⟩
  · rcases mem_mset_zero_occupied 1 i hi with ⟨_, h12⟩ | h10
    · exact absurd h12 (by decide)
    · exact absurd h10 (by decide)
  · rcases mem_mset_zero_occupied 2 i hi with ⟨hi0, _⟩ | h20
    · have : i = 0 := Fin.ext hi0
      subst this
      exact h0
    · exact absurd h20 (by decide)

#print axioms get_eq
#print axioms zsupp
#print axioms zssupp
#print axioms fcatZZs16_rows
#print axioms zzsn16_of_root

end CompactChecker.BridgeZZs16''')
open(OUT + '/BridgeZZs16.lean', 'w').write('\n'.join(E) + '\n')
print('wrote', OUT + '/FcatZZs16.lean', OUT + '/BridgeZZs16.lean', 'paths', {i: (paths[i][1], paths[i][2]) for i in NEW})
