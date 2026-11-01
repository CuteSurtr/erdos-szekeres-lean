# C3LEAN: a Lean check of the threefold 33-point composition

Local runs on an Apple M5 Pro, 1 November 2026 (UTC), over the run records on `es7-cloud` at 9cf4949a5.

**Statement (Lean-checked).** Each of the 910 depth-2 roots of the reduced threefold case split is covered by the
73,567 leaves named in `C3Cover.lean`, through layer splits and σ-splits. The roots are computed in Lean from the
definitions of the split, with the reductions of Lemma 5 (below H3) and Lemma H6M (below H6(a, s)).

**Status.**
- The statement is the theorem `all_roots_covered`: core Lean 4.24.0, no imports, `decide +kernel`, axioms `propext`
  and `Quot.sound`.
- Lean does not know which nodes are certified. That every leaf names a certified record is checked in Python by two
  separate scripts, and the CNF hash of every such record is re-derived from the base formula (§4). These checks are
  exact computations, outside Lean. The verdicts themselves are record fields and are not replayed.
- That the splits are exhaustive, and that the reflection maps of Lemma 5 and Lemma H6M are the right maps, are
  written proofs, reviewed, not Lean-checked (§6). The 90 H3 and 720 H6 second-layer options that the two reductions
  drop are not in the file.
- An independent review (§5) found no blocking error.
- This checks the composition step of `C3FINAL` again. No SAT problem was solved.

## 1. The Lean file (`C3Cover.lean`)

`tools/gen_c3lean.py` writes it from the 280 record files of `C3FINAL/compose_files.txt` (128,803 records) and the
root column of `C3FINAL/C3FINAL_mirrorh6_roots.tsv`. It has 1,340,345 bytes and SHA-256 `4b64293d…`.

**The split** (`tools/prelude.lean`, definition by definition after `C3U2/tools/hullcase.py`).
- A node is a list of convex layers, top layer first, and a σ cube (pairs of a residue and a σ value). The residues
  are 0..10 (m = 11 orbits).
- 11 top cases: H3 (layer `0s0`) and H6(a, s) (layer `0s0-<a>s<s>`), a = 1..5, s = 0, 1.
- Second layers: every one-orbit layer, and every two-orbit layer b < c with each of the 4 values of (σ_b, σ_c), on
  the unused residues. An option O is kept if key(O) ≤ key(refl O).
  - Below H3, refl is the mirror map of Lemma 5: (r, σ) ↦ ((m − r) mod m, 1 − σ).
  - Below H6(a, s), refl is φ_{a,s} of Lemma H6M: (r, σ) ↦ ((a − r) mod m, σ ⊕ [r < a] ⊕ [s = 0]).
- A layer split has as children every next layer on the unused residues that does not contradict the cube.
- A σ-split on K bits has as children all 2^K values of σ on the K smallest free residues (residues 1..10 in no layer
  and not in the cube).

**Covered.** `Covered S` is an inductive predicate with three rules:
- the node is in S;
- it has at least 2 layers, at least one layer child, and every layer child is covered;
- it has at least 2 layers and, for some 1 ≤ K ≤ (number of free residues), all 2^K σ-children are covered.

**Certificates.** There is one per root.
- It holds decision digits in depth-first order (0 = leaf, 1 = layer split, 1 + K = σ-split on K bits), packed in
  base 16 with the first decision least significant, and the keys of the leaves.
- `checkRoot` computes every child itself. A certificate only chooses the split at each node (a layer split, or a
  σ-split on K bits) and names the leaves. The children are never read from it. The stream must be used up exactly.
- A leaf must be equal, as a node, to its decoded key (`beqNode_eq`). No injectivity of the key encoding is used.
- `run_sound` proves that a passing check gives `Covered`.
- The certificates encode the cover tree that `tools/cover.py` rebuilds from the records with the rules of
  `compose.py` (`covered2`, `--mirror-h6`). That this is the tree of `compose.py` is argued from the code and the equal
  σ-split count (below), not shown. Lean re-checks the tree it is given, so the theorem does not depend on this.

**Theorems.**
- `reflection_facts_H3` and the ten `reflection_facts_H6_a_s`: H3 has 190 options and each H6(a, s) has 153, all valid
  and distinct. refl maps options to options and is an involution. It fixes 10 (H3) or 9 (H6) options. 100 or 81
  options are kept. Of each pair {O, refl O} at least one is kept, and both only if O = refl O. These facts are
  Boolean computations, proved equal to the values listed (§5, finding 4).
- `topCases_eq`, `strata`: per top case, 5 one-orbit and 95 (H3) or 76 (H6) two-orbit kept options.
- `roots_match`, `roots_codes_match`, `roots_eq_tsv`: `roots`, computed in Lean, has 910 distinct elements. In order,
  they are the roots of the 910 certificates. As a set, their codes are the 910 codes of `tsvRootCodes`. That
  `tsvRootCodes` is the root column of the TSV is checked in Python (§4).
- 127 batch theorems check the 910 certificates, and `all_checked` joins them. A batch has at most 800 cover nodes,
  except that a larger root gets a batch of its own (the largest has 849).
- `all_roots_covered : ∀ ρ ∈ roots, Covered (fun n => ∃ k ∈ certifiedKeys, decodeKey k = n) ρ`, where
  `certifiedKeys` is the list of all keys of the certificates.

**Counts** (`c3cover_summary.json`). 76,256 cover nodes: 73,567 leaves, 1,747 σ-splits and 942 layer splits. The
1,747 σ-splits equal `sigma_splits_used` of `compose.py` in `C3FINAL/run_final.log`.

**Axioms and resources** (`logs/compile.log`).
- `all_roots_covered`, `run_sound`, `checkRoot_sound`: `propext` and `Quot.sound`. The other theorems: `propext` or
  none. No `sorry`, no `native_decide`, no `Classical.choice`.
- With `set_option Elab.async false` (in the file) and `lean -j1`: 253 s wall (235 s user, 9 s system), peak RSS
  1.14 GB. No errors or warnings.

## 2. Controls

**In the file (Lean-checked).**
- `control_missing_record`: root 0 (`0s0_1`) with its fourth key removed fails. Despite the name, this removes a key
  from the stream. It does not test an uncertified record (§4).
- `control_missing_sigma_child`: root 0 without the subtree of the last child of its first σ-split (73 decisions,
  64 keys) fails.
- `control_swapped_keys`: root 0 with two adjacent keys swapped fails.
- `control_missing_layer_child`: root 100 (`0s0-1s0_2`, a layer split into leaves) without the key of its last child
  fails.
- `control_wrong_root`: the certificate of root 0 does not cover root 1.
- `control_strict_reduction`: with a strict < (fixed options dropped) only 810 roots remain, not 910.
- `control_phi_mutant`: φ without its [s = 0] term keeps options below H6(1, 0) that are not roots of the TSV.

**Must-fail files.** `Control_record.lean` and `Control_sibling.lean` state the first two mutated certificates as
`= true`. Both fail with "Tactic `decide` proved that the proposition … is false" (`logs/control_record.log`,
`logs/control_sibling.log`). The unmodified certificate of root 0 passes in `batch0`.

## 3. The definitions against `hullcase.py`

- **Python children** (`tools/xcheck_hullcase.py`, rerun by the review; exact computation at every split node of the
  tree). At all 942 layer splits and 1,747 σ-splits of the cover tree, the children from `tools/c3tree.py` equal those
  of `hullcase.py` (`cube_layer_children`, `sigma_children`, `free_residues`), in content and order. 0 mismatches
  (`review/logs/xcheck.log`).
- **Lean's own output** (`review/difftest.py`, by the review; exact computation on the inputs below, computational
  evidence beyond them). Lean evaluates its definitions with `#eval` on 304 nodes: 300 from random walks below the
  roots (seed 20261101) and 4 edge cases. The output is compared with `hullcase.py`: 304 layer-children lists,
  304 free-residue lists, 627 σ-children lists (K = 1..3), the 910 roots in order, and the kept options of all 11 top
  cases. 0 mismatches (`review/logs/difftest_cmp.json`). This comparison was rerun on the saved Lean output
  `review/logs/revdiff.log` when this directory was prepared.

## 4. Certification of the leaves (checked by exact computation, outside Lean)

**Lean does not check it.** In `all_roots_covered` the leaf set is the set of nodes named by `certifiedKeys`, and
`certifiedKeys` is only the certificates' own key list. The theorem would also hold with an uncertified leaf. The
review shows this in `review/RevCtrl_pass.lean` (`rev_uncertified_leaf_passes`): root 0, with an inner σ-split
collapsed into one leaf, still passes. That leaf is the parent node `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0`, which has no
certified record.

**Two Python checks.** A record counts as certified by the criterion of `compose.py`: `certified` true, lrat_check
`c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.
- `tools/audit_keys.py` reads only the Lean text, the TSV and the records, with its own decoder (rerun by the review).
  - All 73,567 keys decode to distinct names of certified records, each under the root of its certificate.
  - The certificate roots are the 910 roots of the TSV, and `tsvRootCodes` is the TSV root column in file order.
  - 0 failures (`review/logs/audit_keys_orig.log`).
  - On the review's file with the uncertified leaf it fails and names that node (`review/logs/audit_keys_uncert.log`).
- `review/indep_audit.py` is the review's own code. It imports `C3U2/tools/hullcase.py` and `C3a/c3cnf.py`, and none
  of the files in `tools/`.
  - It reruns all 910 certificates with a literal Python transcription of the Lean checker: 942 layer splits,
    1,747 σ-splits, 73,567 distinct leaves, 0 failures.
  - It computes the roots with `hullcase.tree_children`: the 910 roots of the TSV, in certificate order.
  - It streams the base CNF (`gen_case.py 11 7 none`, SHA-256 `bf0e502e…`) and re-derives the CNF SHA-256 of every
    leaf from `hullcase.node_units`, as `compose.py` does.
  - **All 73,707 certified records behind the 73,567 leaves match, 0 mismatches** (`review/logs/indep_audit.json`;
    21 s, 1.39 GB). `compose.py` had matched all 116,883 certified records in `C3FINAL`.
- **Inputs unchanged.** The git blob ids of the 280 record files are the same at f788780c (the `C3FINAL` snapshot), at
  9cf4949a5 and in the checkout. `C3U2/tools/compose.py`, `C3U2/tools/hullcase.py` and `C3a/c3cnf.py` are the same at
  cad4e050 (the `compose.py` version that `C3FINAL` ran), f788780c and 9cf4949a5.

**What a certified record says.** Each one records that both checkers accepted its proof when it was solved. The
proofs were not kept. 26,436 of the 116,883 certified records carry the proof's SHA-256 (`C3FINAL/run_final.log`). So
the leaves rest on recorded verdicts "certificate accepted by both checkers". They are not replayed here.

## 5. Independent review (1 November 2026)

An adversarial review, run separately with its own scripts (`review/`), checked the file and the claims. It ran no
SAT solver or proof checker. **No blocking error.**

**Checked and found correct.**
- Recompile of the same file (SHA-256 `4b64293d…`): exit 0, 265 s, peak RSS 1.14 GB, no errors or warnings, the same
  axioms (`review/logs/main_compile.log`).
- The file has no imports, and no `#exit`, `#eval`, notation, attributes, `local` or `scoped` commands, or debug
  options. The 127 batch theorems cover the 910 certificates, and `certs` is `certs0` … `certs126` in order.
- The two must-fail files fail again (`review/logs/control_record.log`, `review/logs/control_sibling.log`).
- Eight more mutated certificates are all proved `= false` (`review/RevCtrl_mut.lean`, `review/logs/revctrl_mut.log`):
  σ-split arity K − 1 and K + 1; a σ-split read as a layer split, and the reverse; a leaf key replaced by the key of
  its parent; a duplicated leaf; rotated keys; an extra key. The file has a ninth theorem (finding 6).
- The comparisons of §3 and the audits of §4.

**Findings and their resolution.**
1. *Minor*: certification is not part of the Lean statement, and `control_missing_record` tests a missing key, not a
   missing record. Both are stated here (§2, §4). The Lean file is unchanged, so its hash is the one compiled and
   reviewed.
2. *Note*: the key encoding is not injective. A key with value bits outside the cube mask decodes to the same node
   (`rev_noncanonical_key_passes` in `review/RevCtrl_pass.lean`), and `audit_keys.py` ignores the same bits. This is
   harmless, because the leaf set is defined through `decodeKey`. A key with a zero layer digit decodes differently in
   Lean and in `audit_keys.py`, but in Lean it decodes to a node with a lower layer `[(0, 0)]`, which the checker never
   generates (residue 0 is in the top layer of every node it generates). `indep_audit.py` audits, at each leaf, the
   node that its transcription of the checker matched, that is, the Lean leaf itself.
3. *Note*: Lean's `Covered` allows a layer split of a cube node without a layer-split record, which `compose.py`
   requires. This is more permissive than `compose.py`, but still exhaustive by rule 3 of `C3U2/sigma_split.md`.
4. *Note*: `reflection_facts_*`, `strata` and `roots_eq_tsv` are Boolean computations. The corollary "of each pair
   {O, refl O} at least one is kept, and both only if O = refl O" is read off them. It is not stated as a proposition.
5. *Note*: the 90 H3 options removed by Lemma 5 are outside the file, like the 720 H6 options removed by Lemma H6M.
6. *Note* (found when this directory was prepared): the ninth mutation theorem, `rev_extra_decision`, has the same
   certificate as `rev_extra_key`. The added decision is a leaf digit 0, and a trailing 0 does not change the base-16
   number. So no control tests an extra non-zero decision; the checker's final test `ds == 0` rejects one by its
   definition.

## 6. What is not checked

- **The SAT verdicts.** They are record fields (§4). `C3SPOT` re-solved 2,120 randomly drawn certified pieces (σ-cube
  records were not in its population), with fresh proofs accepted by both checkers (computational evidence, not
  exhaustive).
- **The CNF encoding** (`C3a`): computational evidence (cross-checks against `C3b` and `symcnf.py`, random and
  mutation tests). `C3AUDIT` calls it "tested, not proved".
- **The geometry.** These are written proofs, reviewed, not Lean-checked. The reviews are `C3AUDIT` (Lemmas 1–5 and
  the cover theorem), `C3AUDIT2` and `C3H6M` (Lemma H6M) and `C3AUDIT3` (rules 2 and 3).
  - That a layer split and a σ-split lose no set of the class (Lemmas 1–4 and the cover theorem of
    `C3-S/soundness.md`, its version for the reduced cut in `C3H6M/soundness_h6m.md`, rules 2 and 3 of
    `C3U2/sigma_split.md`).
  - That refl is the action of the reflection on layer paths (Lemma 5 of `C3-S/soundness.md`, Lemma H6M of
    `C3H6M/soundness_h6m.md`).
  - That the units `hullcase.node_units` adds to the base for a node hold for every set the node contains (Lemma 3 of
    `C3-S/soundness.md`, and "Containment" in `C3U2/sigma_split.md`). The hash check of §4 shows only that each
    record's CNF is the base plus these units.
- **The removed options.** The 90 H3 and 720 H6 second-layer options removed by the reductions are not roots of the
  file. By the facts Lean computes (§1), each one is refl of a kept option. That the reflected set is again in the
  class, in the same top case, is Lemma 5 or Lemma H6M.
- **Keys and record names in Lean.** Lean only decodes keys into nodes. The match with record names is §4.
- **Other certified nodes.** `certifiedKeys` holds only the 73,567 leaves used, out of 116,741 certified nodes.

## 7. Place in the proof

Theorem 1 of `WRITEUP/SYMMETRIC.md` (threefold, 33 points) uses the composition of `C3FINAL`. This directory checks
that step again. The bookkeeping is Lean-checked. That every leaf names a certified record, and that the recorded CNF
hashes match the base formula, are exact computations in Python. The verdicts themselves are record fields. The rest of
the trust base of Theorem 1 (§3 there) is unchanged. `WRITEUP` itself is not changed here.

## Files

- `C3Cover.lean`, `Control_record.lean`, `Control_sibling.lean`, `c3cover_summary.json`: written by
  `tools/gen_c3lean.py`.
- `tools/`: `gen_c3lean.py` with `prelude.lean` (the Lean definitions and proofs), `c3tree.py` (the split in Python),
  `cover.py` (the cover tree from the records), `audit_keys.py` and `xcheck_hullcase.py`.
- `logs/`: the compile log and the two must-fail logs.
- `review/`: the review's `indep_audit.py`; `difftest.py` with `RevDiff.lean` and `diff_samples.json`; `mk_controls.py`
  with `RevCtrl_mut.lean`, `RevCtrl_pass.lean` and `controls.json`; its logs in `review/logs/`. The header comment of
  the two `RevCtrl` files names the generator by its path during the review, `c3review/tools/mk_controls.py`; here it
  is `review/mk_controls.py`.
- Not included:
  - `c3cover_keys.tsv`, one row per leaf (root index and name, key, node, CNF SHA-256, and the file and line of each
    certified record of the node): 11,355,163 bytes, SHA-256 `70acadec…`. It is over 5 MB, and `gen_c3lean.py` writes
    it again.
  - The review's `C3Cover_uncert.lean` (SHA-256 `99a6796d…`). `mk_controls.py` writes it again.
- In the logs, file names are given without the machine-specific directory. Most logs also hold `/usr/bin/time -l`
  output and lines from wrappers that sample the peak RSS or wait for free memory.

## Reproduction

From `cloud/es7-2026-10-19/results`, with Python 3 and Lean 4.24.0 (no Mathlib needed); `OUT` is any empty directory:

```sh
python3 -B C3LEAN/tools/gen_c3lean.py . OUT 9cf4949a5    # OUT/C3Cover.lean has SHA-256 4b64293d…
lean -j1 C3LEAN/C3Cover.lean                             # 253 s and 1.14 GB here
lean C3LEAN/Control_record.lean                          # must fail
lean C3LEAN/Control_sibling.lean                         # must fail
python3 -B C3LEAN/tools/audit_keys.py C3LEAN/C3Cover.lean .
python3 -B C3LEAN/tools/xcheck_hullcase.py .
python3 -B C3U2/tools/gen_case.py 11 7 none -o BASE.cnf  # p cnf 168399 4154921, 109,924,548 bytes, SHA-256 bf0e502e…
python3 -B C3LEAN/review/indep_audit.py C3LEAN/C3Cover.lean . BASE.cnf indep_audit.json
python3 -B C3LEAN/review/mk_controls.py C3LEAN/C3Cover.lean C3LEAN/tools/prelude.lean OUT
lean OUT/RevCtrl_mut.lean
lean OUT/RevCtrl_pass.lean
python3 -B C3LEAN/tools/audit_keys.py OUT/C3Cover_uncert.lean .     # must fail
python3 -B C3LEAN/review/difftest.py gen . C3LEAN/tools/prelude.lean OUT/RevDiff.lean OUT/diff_samples.json 300 20261101
lean OUT/RevDiff.lean > OUT/revdiff.log
python3 -B C3LEAN/review/difftest.py cmp . OUT/diff_samples.json OUT/revdiff.log
```

`mk_controls.py` and `difftest.py gen` write the files in `review/` again, byte for byte.
