# C3H6M: integration of the H6 mirror reduction (`--mirror-h6`)

Task: `TASK.md` (commit 8d13deee), H = 1.75 h, one 4-core VM (`env.txt`). Started 05:27 UTC on
2026-10-21 from commit **b05b8ba7**. Paths are relative to `cloud/es7-2026-10-19/`.

## Verdict: accept, with conditions

The cut with `--mirror-h6`, as `results/C3T/tools` implements it at commit ff9b09ee, is **sound
and correctly implemented**. C3AUDIT2 set conditions (1) to (3); (1) and (2) hold in the code, and
(3) is met by the addendum `soundness_h6m.md` and by the second composer `tools/mycompose.py --h6m`.
I found no defect that affects soundness. The remaining conditions concern use, not code:

1. Any claim that rests on the reduced cut must cite `results/C3H6M/soundness_h6m.md` together
   with `results/C3-S/soundness.md`. `soundness.md:78–79` still says the mirror map is not used for
   H6. That file is outside my directory, so I did not edit it; it should get a pointer to the
   addendum.
2. The cut claim must come from `results/C3T/tools/compose.py --mirror-h6` at ff9b09ee or later,
   and it must agree with `results/C3H6M/tools/mycompose.py --h6m`. A node marked `no` may leave
   the work lists only on that basis.
3. Do not add a second S-or-M(S) reduction inside an H6 subtree. The σ-cubes of C3U are not one:
   they are an exhaustive split, and C3U allows them only at depth ≥ 2 (see finding 5).

## Findings, most serious first (none breaks soundness)

1. **Weakens the trust base, minor (existing behaviour, not caused by H6M).**
   `results/C3T/tools/compose.py:142–152` (`covered2`), like `results/C3-S/tools/compose.py:77–87`
   and `results/C3AUDIT/tools/mycompose.py` (`all([])`), counts a node as covered when it is in
   `prefixes` and has no children. A node with no children has all 11 residues used. It can reach
   `prefixes` only if some certified record's name extends it, and such a name would repeat a
   residue. In the current records this does not happen: of the 45,827 certified records, 0 have a
   repeated residue, 0 have a non-normal name, 0 are outside the unreduced tree, the maximum depth
   is 4, and 0 prefixes have no children. A guard (`if not ch: missing.append(name); return False`)
   would remove the case.
2. **Cosmetic, but misleading in reduced mode.** With `--mirror-h6`, `compose.py:155` reports
   `certified_nodes` = every certified record name, including names outside the reduced tree.
   On set T it prints 45,824, but only 28,721 of them are leaves of the reduced cut. The other
   17,103 lie under the 720 dropped H6 options. Only `class_covered` and the frontier count matter,
   and both are right.
3. **Cosmetic.** The docstring of `compose.py:6–8` still says the children come from
   `tree_children` "with the H3 mirror reduction"; only line 21 mentions `--mirror-h6`. The comment
   at `hullcase.py:170–171` ("no task may use it before results/C3AUDIT2 accepts the lemma") is
   out of date: C3AUDIT2 accepted the lemma with conditions, and this report covers the
   integration.
4. **Operational, not soundness.** `close_tree.py` has no `--mirror-h6`. Its SHARD mode
   (`close_tree.py:15`) still takes the 1,630 roots of the unreduced tree. That is sound, but the
   work spent on the 720 dropped H6 roots is not needed for the cut. Use `needed_roots.tsv` for
   the work lists. Also note that 19 dropped roots are closed while their partner, which is in the
   cut, is still open. The corollary holds for **any** choice of at least one member of each φ-pair,
   so a rule that picked the closed member would save those 19 roots (483 → 464). That would be a
   new rule: it would need its own code and its own check, so I did not apply it.
5. **Checked, no problem (condition 2).** No other reduction acts inside an H6 subtree.
   `tree_children` reduces only the root's H3 child (`hullcase.py:192–193`, unchanged from C3-S)
   and, with the flag, the 10 H6 nodes (`hullcase.py:194–197`). The work-in-progress σ-cube tools
   of `results/C3U/tools/compose.py` (commit 41041780) reject σ-split records at depth 1 (around
   line 153: `len(lay) < 2` → fail). They pass `mirror_h6` only to `cube_layer_children` of cube
   nodes, which have depth ≥ 2, where `tree_children` reduces nothing. C3U is outside this task,
   and I did not audit it beyond this point.

## Step 1: code review (`results/C3T/tools` at ff9b09ee)

- `h6_phi` (`hullcase.py:175–176`) is ((a − r) mod m, σ ⊕ [r < a] ⊕ [s = 0]) with None kept,
  which is exactly PLAN.md §3a. The result is sorted, so it compares as a layer.
- `h6_layer2_kept` (`hullcase.py:179–182`) calls the same `layer2_options` as the default branch.
  It is called with top `[(0, 0), (a, s)]`, and the generator reads only the residues of that
  argument, so the options and their order are those of `layer2_options(m, [(0, None), (a, None)])`.
  The key has the same form as `h3_layer2_kept` (sorted (r, −1 or σ)), and it is injective. The
  σ conventions are those of the node names: `s0` / `s1` = σ_r of the residue's label r.
- `tree_children` (`hullcase.py:185–199`): the H6 branch is taken only for `layers` exactly equal
  to `[[(0, 0), (a, s)]]` with 1 ≤ a ≤ ⌊m/2⌋ and s ∈ {0, 1}, and it uses that node's own (a, s).
  It is not `mirror_layer`. H3 (line 192) comes first and is unchanged. Every other node (depth ≥ 2)
  falls through to the full `layer2_options` (lines 198–199), so the children below a kept option
  are complete.
- `compose.py`: `MIRROR_H6` is set only by `--mirror-h6` (lines 83–86). Its only use is in
  `children` (lines 45–46), which `covered2` calls. The sha check (lines 104–118) does not depend
  on the flag. `covered2` reaches only nodes of the (reduced) tree, starting from the root, so a
  certified node under a dropped option can never make anything covered.

## Step 2: tests (`tools/test_tree.py` → `logs/test_tree.json`, 0 failures)

(a) Flag off: C3T `tree_children` is **identical** to C3-S `tree_children` at 132398c (from a
separate worktree) on the root, on all 11 top cases, and on all 1,630 depth-2 nodes. These
1,630 nodes are exactly the depth-2 rows of `results/C3-S/manifest_depth2.tsv`. It is also
identical on **3,000 random deeper nodes**: depth 3: 611, depth 4: 577, depth 5: 601,
depth 6: 1,103, depth 7: 108. On the deeper nodes the children also equal my own complete
option list.

(b) Flag on:
- the root, the H3 node (100 children), all 1,630 depth-2 nodes and all 3,000 deeper nodes are
  unchanged;
- each of the 10 H6 nodes changes from 153 to **81** children (5 one-orbit, 9 self-mirror,
  72 pairs, with exactly one member of each pair kept), **810 in all**;
- these children are a subset of the unreduced children, and they **equal the result of my own
  from-scratch rule** (strings and tuples, no repository code);
- `h6_phi` equals my φ on all 1,530 options; φ is an involution and maps options to options;
- below every tenth kept option, the children are complete;
- `h6m_kept` columns of `results/C3W3/lists/*.tsv`: all 1,026 rows were checked. The 926 H6 rows
  agree with my rule (A_s0, C_s1two, D_s1one), and the 100 H3 rows are `na`.
- Mutations: each wrong map gives a kept set different from C3T's, and each leaves φ-pairs with
  neither member kept. The H3 map m − r differs in 10 of 10 cases and leaves 470 options
  uncovered. With no σ change: 9 cases, 20 options. Without [r < a]: 8 cases, 36. Without [s = 0]:
  5 cases (the s = 0 ones), 48.

## Step 3: soundness addendum

`soundness_h6m.md` has Lemma H6M with a full proof. I re-derived every step: the reflection, the
sweep that brings back a ≤ 5, the σ of each residue, the point reflection for s = 0, and the
layers. It also has the involution with its reason, the count of the fixed options (9), the
corollary, the Theorem with the reduced tree, and the code that implements it (C3T ff9b09ee:
`hullcase.py:175–199`, `compose.py --mirror-h6`; and `tools/mycompose.py --h6m`).

## Step 4: two composers

`tools/mycompose.py` is `results/C3AUDIT/tools/mycompose.py` plus my own `phi6` and the
reduction at depth 1 (`--h6m`), plus a `--dump` of the frontier and of the depth-2 status. It
does not use C3T code. In `--h6m` mode it skips the comparison of its tree with C3-S `hullcase`,
which is the unreduced tree. C3T `compose.py` was run unchanged, with full sha checks, through
`tools/c3t_dump.py`. The wrapper only records which nodes `children` expands, and it asserts that
its frontier count and `class_covered` equal `compose.py`'s. The base CNF was rebuilt with C3-S
`gen_case.py 11 7 none` at 132398c: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`, which match.
Driver: `tools/runall.sh`. Outputs: `logs/compose/*.json`.

Record sets:
- **T** (the task's set): the 114 files in `files.txt`, read at **b05b8ba7**. That is every
  `C3WAVE1/*/out.jsonl`, `C3WAVE1/*/recheck.jsonl` (C00, C13, C14), `C3WAVE2/*/out.jsonl`,
  `C3WAVE2/K36/recheck.jsonl`, `C3S0/*/out.jsonl` and `C3W3/*/out.jsonl`. No `C3S0` or `C3W3`
  recheck file exists at that commit. Not included, because their names do not match the list:
  `C3WAVE1/C11/rechecks.jsonl`, `C3WAVE1/C04/out_reconstructed.jsonl`, and
  `C3WAVE1/C09/notes/removed_records.jsonl`.
- **A** and **B**: FIX1's sets (`results/C3T/tests/logs/files_set{A,B}.txt`), read at 2408f075.

| set | composer | mode | cert. records | cert. nodes | covered | frontier | depth-2 roots | open roots |
|---|---|---|---|---|---|---|---|---|
| A | C3T compose.py | off | 41,750 | 41,750 | no | **7,717** | 1,630 | 1,026 |
| A | mycompose.py | off | 41,750 | 41,750 | no | 7,717 | 1,630 | 1,026 |
| A | C3T compose.py | --mirror-h6 | 41,750 | 41,750 (24,660 in cut) | no | 5,146 | 910 | 573 |
| A | mycompose.py | --h6m | 41,750 | 41,750 | no | 5,146 | 910 | 573 |
| B | C3T compose.py | off | 42,602 | 42,599 | no | **7,453** | 1,630 | 1,025 |
| B | mycompose.py | off | 42,602 | 42,599 (3 dup.) | no | 7,453 | 1,630 | 1,025 |
| B | C3T compose.py | --mirror-h6 | 42,602 | 42,599 (25,508 in cut) | no | **4,883** | 910 | 572 |
| B | mycompose.py | --h6m | 42,602 | 42,599 | no | 4,883 | 910 | 572 |
| T | C3T compose.py | off | 45,827 | 45,824 | no | 11,562 | 1,630 | 924 |
| T | mycompose.py | off | 45,827 | 45,824 (3 dup.) | no | 11,562 | 1,630 | 924 |
| T | C3T compose.py | --mirror-h6 | 45,827 | 45,824 (28,721 in cut) | no | 9,004 | 910 | **483** |
| T | mycompose.py | --h6m | 45,827 | 45,824 | no | 9,004 | 910 | **483** |

- In every row pair, the two composers agree on the counts, on the **set** of frontier nodes,
  and on the **set** of open depth-2 roots (compared with `cmp`; 6 of 6 equal).
- Without the reduction, both reproduce FIX1's counts: A gives 41,750 / 7,717, B gives
  42,599 / 7,453. With it, B gives 4,883, which is FIX1's TESTONLY number.
- In off mode mycompose's check of its own tree against C3-S `hullcase` gives 0 mismatches on
  677, 686 and 774 prefix nodes. No sha mismatch was found.
- Frontier counts grow from A/B to T because more certified nodes add more expanded prefixes.
- Negative test (`logs/negative_tests.txt`). I removed one certified record from set T.
  - Removing a kept H6(3, 0) root (`0s0-3s0_1s0-10s0`) opens it in both modes and in both
    composers: 924 → 925 open roots off, 483 → 484 on.
  - Removing a dropped one (`0s0-3s0_1s1-2s0`) changes only the off mode (924 → 925); on stays 483.
  - The two composers agree in all 4 runs.
- The σ-cube records `results/C3SIG/*/out.jsonl` are not in the task's sets. Their 20 parent nodes
  are all closed by layer split anyway (15 in the cut, 5 dropped), so they change nothing here.

## Step 5: roots still needed (`needed_roots.tsv`, status from set T at b05b8ba7)

One row per depth-2 root of `results/C3-S/manifest_depth2.tsv` (1,630 rows), with the columns
node, stratum, `in_reduced_cut`, mirror partner (for H6) and status. A root is *closed* when it is
covered, *partial* when it has a certified node at or below it but is not covered, and
*untouched* otherwise. A root's status is the same in both modes, because nothing is reduced
below depth 2. Every one of the 720 dropped H6 roots has its partner in the cut, and 90 H6 roots
are self-mirror.

| stratum | roots | in cut | closed | partial | untouched | **still needed** | dropped (of which closed) |
|---|---|---|---|---|---|---|---|
| H3, one-orbit L2 | 5 | 5 | 0 | 0 | 5 | **5** | 0 |
| H3, two-orbit L2 | 95 | 95 | 0 | 10 | 85 | **95** | 0 |
| H6(1,0) one / two | 9 / 144 | 5 / 76 | 5 / 76 | 0 / 0 | 0 / 0 | **0 / 0** | 4 (4) / 68 (68) |
| H6(1,1) one / two | 9 / 144 | 5 / 76 | 0 / 68 | 5 / 8 | 0 / 0 | **5 / 8** | 4 (0) / 68 (44) |
| H6(2,0) one / two | 9 / 144 | 5 / 76 | 3 / 68 | 2 / 0 | 0 / 8 | **2 / 8** | 4 (2) / 68 (38) |
| H6(2,1) one / two | 9 / 144 | 5 / 76 | 0 / 26 | 2 / 11 | 3 / 39 | **5 / 50** | 4 (0) / 68 (9) |
| H6(3,0) one / two | 9 / 144 | 5 / 76 | 1 / 76 | 4 / 0 | 0 / 0 | **4 / 0** | 4 (0) / 68 (68) |
| H6(3,1) one / two | 9 / 144 | 5 / 76 | 0 / 4 | 0 / 2 | 5 / 70 | **5 / 72** | 4 (0) / 68 (0) |
| H6(4,0) one / two | 9 / 144 | 5 / 76 | 0 / 65 | 2 / 3 | 3 / 8 | **5 / 11** | 4 (0) / 68 (38) |
| H6(4,1) one / two | 9 / 144 | 5 / 76 | 0 / 1 | 1 / 2 | 4 / 73 | **5 / 75** | 4 (0) / 68 (0) |
| H6(5,0) one / two | 9 / 144 | 5 / 76 | 0 / 34 | 0 / 11 | 5 / 31 | **5 / 42** | 4 (0) / 68 (8) |
| H6(5,1) one / two | 9 / 144 | 5 / 76 | 0 / 0 | 0 / 0 | 5 / 76 | **5 / 76** | 4 (0) / 68 (0) |
| H6 total, one-orbit | 90 | 50 | 9 | 16 | 25 | **41** | 40 (6) |
| H6 total, two-orbit | 1,440 | 760 | 418 | 37 | 305 | **342** | 680 (273) |
| **all** | **1,630** | **910** | **427** | **63** | **420** | **483** | 720 (279) |

So the reduced cut needs **483** depth-2 roots: 100 H3 and 383 H6. Without the reduction it
would need 924. 279 of the dropped roots were already closed, so that work is not needed for the
cut.

## What I could not check

- I wrote no exact-coordinate test of my own for Lemma H6M. I relied on my paper re-derivation
  and on C3AUDIT2's independent test (14,000 sets, 0 failures). The proof is not machine-checked
  (no Lean).
- I did not re-audit the base encoding, Lemmas 1–5, the drivers or the proofs. They are used as
  stated in `soundness.md` and the earlier audits. The certified records are trusted as
  `compose.py` filters them (both checker verdicts, plus the re-derived CNF sha256); no proof
  was re-solved here.
- C3U's σ-cube tools are work in progress. I checked them only for condition 2.
- The record sets are a snapshot at b05b8ba7. Waves that push later change the statuses in
  `needed_roots.tsv`, but not the `in_reduced_cut` column.

## Files

`env.txt`; `files.txt` (set T); `soundness_h6m.md`; `needed_roots.tsv`; `tools/test_tree.py`,
`tools/mycompose.py`, `tools/c3t_dump.py`, `tools/needed_roots.py`, `tools/runall.sh`;
`logs/test_tree.json`, `logs/compose/*.json`, `logs/negative_tests.txt`,
`logs/needed_counts_raw.txt`.
