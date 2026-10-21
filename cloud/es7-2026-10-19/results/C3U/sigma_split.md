# Soundness of σ-cube splitting (C3U)

Line numbers are for `results/C3U/tools/` as committed with this note. The notation is that of
`results/C3-S/soundness.md`: S is a set of the class (m = 11, k = 7) with its canonical
labelling (Lemma 2), α is the true assignment of the base variables for S, and σ_r = α(E.sig(r))
is the σ bit of label r (σ_0 = 0, σ_{r+m} = 1 − σ_r, σ_{r+2m} = σ_r). So the bits σ_1 … σ_{m−1}
are well defined for every S, whatever its layers are.

**Containment.** A layer node L *contains* S if L is a prefix of S's layer path (Lemmas 3, 4):
then α satisfies the base and all units of `layer_clauses(L)` (the Theorem of soundness.md). A
cube node `L__C` contains S if L contains S and σ_r = v for every (r, v) in C. Its CNF
(`node_units`, `hullcase.py:239`) is the CNF of L followed by `cube_units(C)` (`hullcase.py:235`):
the literal E.sig(r) for v = 1 and −E.sig(r) for v = 0. These are the same σ literals that
`layer_clauses` already uses for two-orbit layers (`hullcase.py:125-128`). So α satisfies the CNF
of `L__C` exactly when S is contained in `L__C` (and α satisfies the CNF of L). An UNSAT
certificate for `L__C` therefore refutes every S contained in `L__C`, and no other set.

**Adding units never loses a set of the class.** The units of C say nothing about the sets that
are not contained in `L__C`. Those sets have some σ_r ≠ v for an (r, v) in C. They are the
responsibility of the siblings (rule 2) or of other branches of the tree; the unit never claims
them. The only claim attached to a node is "no S is contained in it". Below we show that each
split's children together contain every S that the parent contains. Then induction on the
covered tree (as in the Theorem of soundness.md) shows: if the root is covered, every S of the
class is contained in a certified node, which is impossible. So the class is empty, up to the
same trusted parts as before (base encoding, Lemmas 1–5, the checkers).

## Rule 2: the cube children cover the parent

`sigma_children(m, L, C, K)` (`hullcase.py:244-252`) takes bits b_1 < … < b_K, the K smallest
free residues. Free means in 1..m−1, in no layer of L, and not in C (`free_residues`,
`hullcase.py:229`). It returns the 2^K nodes `L__C'`, where C' = C ∪ {(b_j, v_j)}, sorted by
residue, for every vector (v_1 … v_K) ∈ {0,1}^K (the loop at `hullcase.py:249` runs over all
2^K vectors i). Let S be contained in `L__C`. The vector (σ_{b_1}, …, σ_{b_K}) of S is one of
the 2^K vectors, and the b_j are not in C, so C' has no contradictory duplicates. S is contained
in exactly that child. Hence the children exhaust the assignments of the K bits and cover the
parent.

Neither soundness nor this argument needs the bits to be the *smallest* free ones. Any K
residues outside C would do. "Smallest" fixes the children's names, so `compose.py` can rebuild
them: it requires `sigma_bits` to be exactly the K smallest free residues (`compose.py:153`), and
for the records of `sigma_cubes.py` it requires the same of the cube residues (`compose.py:160`).
It then requires all 2^K children to be covered (`compose.py:218`).

**Why never at depth 1.** Lemma 5 (H3 mirror) and Lemma H6M (`--mirror-h6`) reduce the
children of a depth-1 node. They do not keep every set. They keep S *or* its mirror image M(S),
and M flips σ (Lemma 5: σ' = 1 − σ, residues r ↦ m − r). So the mirror image of a set in a cube
`L__C` need not lie in `L__C`. A cube placed at depth 1 whose layer children were then reduced
would lose sets. So both tools refuse σ-splits of nodes with fewer than 2 layers
(`close_tree.py:188`, `compose.py:153` and `compose.py:160`). Every cube node is made by a σ-split of a node with
at least 2 layers, and layer splits only add layers. So every cube node has at least 2 layers. For
such L, `tree_children` applies no reduction: the H3 branch needs `layers == [[(0, 0)]]`
(`hullcase.py:192`), the H6 branch needs `len(layers) == 1` (`hullcase.py:194`), and otherwise
it returns all of `layer2_options` on the unused residues (`hullcase.py:198-199`).

## Rule 3: the layer children of a cube node cover it

`cube_layer_children(m, k, L, C)` (`hullcase.py:261-264`) returns `(L', C)` for every L' in
`tree_children(L)` except those where `conflicts(L'[-1], C)` holds (`hullcase.py:255`). That is
the case when the newest layer of L' gives a residue r of C an explicit σ different from C's
value. Let S be contained in `L__C`, where L has at least 2 layers.

- If S's layer path ends at L (no residue is left), S has no child. `tree_children(L)` is then
  empty. `compose.py` never counts a cube node with no layer children as covered
  (`compose.py:226`), so S must be refuted by the certificate of `L__C` itself.
- Otherwise S has a next layer L_{j+1} on the unused residues. By Lemma 4 it is one of
  `layer2_options` and, since there is no reduction at depth ≥ 2, `L' = L + [L_{j+1}]` is in
  `tree_children(L)`, and L' contains S. The explicit σ values of L_{j+1} are S's true σ values,
  and so are C's values (S is in `L__C`). So L_{j+1} agrees with C on every residue they share:
  L' is not dropped, and S is contained in the child `L'__C`.
  A one-orbit layer carries no σ (`None`) and never conflicts.

The dropped L' are exactly the ones that contradict C. No S contained in `L__C` lies in them,
because they would need some σ_r = s ≠ v = σ_r. So the kept children cover `L__C`.

## What compose.py checks

A node is covered (`compose.py`, `covered2`) if one of these holds:
- it has a certified record whose `cnf_sha256` equals the sha256 re-derived from the name
  (`compose.py:173-175`, with BASE pinned);
- it has a σ-split (a checked record, or an implied one: all 2^K `sigma_cubes.py` cubes on its
  K smallest free residues are certified) and all 2^K children are covered;
- it is a layer node and all its `tree_children` are covered. This is the C3T rule, unchanged.
- it is a cube node with a layer split record, at least one layer child, and all children of
  rule 3 covered.

Every split it accepts is one of the two splits above, and the base case is a certified CNF. So
covered(root) implies that every S of the class is contained in a certified node.
