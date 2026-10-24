# C3AUDIT: adversarial review of the 3-fold class setup

Task: `TASK.md` at 3d83517 (H = 1.25 h). One cloud VM, 4 cores, 15 GB (`env.txt`), 00:44 to
about 01:25 UTC on 2026-10-21. Tools built from source: CaDiCaL 3.0.1 (c6073042) and cake_lpr
(a36874a, `make`, from the repository's `cake_lpr.S`). I did not build lrat-check: cake_lpr is
the checker I used.

**Verdict: I found nothing that breaks soundness.** If every node of a cut is refuted, as
`compose.py` checks it, then the 3-fold class is empty, given three trusted pieces: the C3a base
encoding (tested, not proved), the paper Lemmas 1–5 (re-derived here and tested independently),
and the driver logs (proofs are not kept). The findings below weaken the trust base or are
cosmetic. None of them invalidates a recorded closure.

## Findings, most serious first

1. **Weakens the trust base: a certified node is a self-reported log line, and the proof is gone.**
   `close_node.py:52-61` and `close_tree.py:59-70` delete the CNF and the proof. They record only
   the solver status, `proof_bytes`, and the checker output strings. `compose.py:42-44` accepts a
   record when it has `certified: true`, `lrat_check == "c VERIFIED"` and
   `cake_lpr == "s VERIFIED UNSAT"`. It recomputes the CNF sha256, which ties the record to the
   node. Nothing ties the record to a proof: there is no proof hash, and no proof is kept. So
   the composed claim rests on the honesty and correctness of about 50 drivers' jsonl files. The
   only audit path is to re-solve. I did that for 19 nodes, and all 19 passed (item A4 below).
   Suggestion: record the proof sha256, and keep a random sample of proofs, or re-solve a random
   sample of every shard on a different machine.
2. **Weakens the trust base (minor): `compose.py` does not pin BASE.** `compose.py:47-53`
   recomputes each node's sha from whatever BASE file it is given. It never compares BASE (or the
   records' `base_sha256`) with `bf0e502e…dd6da`. The sha check is a bare `assert` (line 53), so
   `python3 -O` skips it silently. With the correct base the check does its job, because a base
   with extra clauses would give different shas. But the compose claim is only as good as the
   operator's choice of file. Suggestion: hard-code the base sha256, and replace the `assert`
   with an explicit failure.
3. **Weakens the trust base (inherent): at m = 11, the 7-gon clauses can be tested only on
   in-class sets, and none are known.** I tested them at m = 4..7 with k = 7 (full CNF). At m = 11
   I tested them with k = 11, on sets without a convex 11-gon, using the same generator code
   (A3). Any defect specific to k = 7 at m = 11 would have to escape all of these tests.
4. **Cosmetic: the documented node names differ from the names the tree uses.** The
   `hullcase.py:78` comment gives `"0" = H3`, `"0-2s1"`, `"0_5"`, `"0_3s0-7s1"`, and
   `C3-S/README.md:105` uses `0_5`. The tree and `compose.py` use `0s0`, `0s0-2s1`, `0s0_5`.
   `"0-2s1"` does not even parse into a valid layer: `layer_order` asserts that s is set. A
   record named `0_5` has the same CNF as `0s0_5` but would never be counted by `compose.py`.
   A driver started at root `0` would also skip the mirror reduction (`tree_children` tests
   `layers == [[(0, 0)]]`). That costs work only and is not unsound. All wave roots come from
   `tree_children`, and no record uses the old names (0 of 24,445).
5. **Cosmetic: the `controls.dual` heap setting has no effect.** `controls.py:28` passes the
   heap size to cake_lpr through `CML_HEAP_SIZE`/`CML_STACK_SIZE`, which cake_lpr a36874a
   ignores. The wave machines work around this with `cake_lpr_wrapper.sh`. Acceptance is still
   cake_lpr's own `s VERIFIED UNSAT`, so this can cost a failed check but cannot produce a
   false acceptance.
6. **Note (already known): lrat-check is not an independent second check.** E2 found that
   unpatched lrat-check accepts an empty clause without a RUP conflict (fixed by the one-line
   patch). cake_lpr is the verified checker and the real trust anchor.
   The "both checkers" rule adds little beyond cake_lpr.

## What I checked and found sound

**A1. Symmetry reduction** (`results/WRITEUP/MIRROR.md` §2, re-derived). The symmetry group is
C_s or D_s.
- s ≥ 7: an orbit is a regular s-gon, which contains a convex 7-gon.
- s even: there is a half-turn. Since 33 is odd, its centre o is in S, and then p, o, −p are
  collinear.
- s = 5: neither 33 nor 32 is divisible by 5.
- So s ∈ {1, 3}, and for s = 3 the centre is not in S (11 orbits).

The point-reflection (order-2) case is therefore impossible, by general position plus parity.
It needs no CNF. Inside C3-S, the point reflection is used only as a normalization (σ_0 = 0,
`sb`), never as a symmetry of S. The D3 count 33 = 6·5 + 3·1 is correct. D3 sets are also
3-fold, so the C3 encoding covers them anyway.

**A2. Base CNF.** I rebuilt `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256
`bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`. This equals the documented
hash and every record's `base_sha256`. Byte identity with C3a's chain CNF holds by construction:
`gen_case` with case `none` calls `C3Enc(11, 7).build()` and `write` unchanged.

**A3. Independent exact test of encoding plus decomposition** (`tools/indep.py`, `tools/drive.py`).
My own code covers:
- **Generator:** integer lattice; the rotation is A = [[0,−1],[1,−1]] of order 3, conjugate to
  +120° by an orientation-preserving map; the reflection M = [[0,1],[1,0]] with M A M = A⁻¹.
- **Canonicalization:** all 2n positions and orientations of l, for S and for M(S).
- **Labels and σ:** computed directly from cross products, with no y/x arithmetic.
- **Layers and node names:** exact integer convex hulls give the layers and the node names.

From the repository the test uses only the literal maps (`E.T`, `E.s`, `E.ccw`, `E.sig`) and the
code under test (`tree_children`, `layer_clauses`). For every admissible frame it checks:
- the convention R(i) = (i − m) mod n (asserted on every point);
- σ_{r+m} = 1 − σ_r and σ_{r+2m} = σ_r;
- the T orbit map is consistent with the true orientations of every triple;
- the node path is a path of the tree, or pruned only by the H3 mirror rule;
- every layer unit and the `sb` unit are true;
- some frame of S or of M(S) lands in the kept tree.

Results, all with 0 failures (`logs/geo*.json`, `logs/sat*.json`):

| test | sets | result |
|---|---|---|
| geometry only, m = 11 (4 seeds) | 1,050 | all covered; all 11 top cases hit; depths 6–10; 187 covered only through the mirror |
| geometry only, m = 7 and m = 9 | 300 + 300 | all covered |
| full base CNF (k = 7) + node units + true T, σ fixed, must be SAT; m = 4, 5, 6, 7, in-class sets only (brute-force no convex 7-gon) | 100, 150, 120, 30 | all SAT |
| m = 11, base CNF without the `gon` section + node units + true T, σ fixed | 100 | all SAT |
| m = 11, full C3Enc(11, 11) CNF (no convex 11-gon, by an O(n⁴) DP checked against brute force) + k = 7 node units + true T, σ fixed | 55 | all SAT |

The tests have teeth (`tools/mut.py`, `tools/mut2.py`):
- reversed 2-orbit layer order: 270 false units;
- σ of r + m not swapped: 270 false units;
- mirror without the σ flip: 3 of 60 sets uncovered;
- one orientation orbit flipped: 39 of 40 CNFs UNSAT.

So every 3-fold-symmetric set I generated, in the class or the relaxed class, gives a satisfying
assignment of its own node's CNF.

**A4. Re-check of certified nodes** (`tools/recheck.py`, `logs/recheck_wave1.jsonl`,
`logs/recheck_wave2_depth2.jsonl`). I generated the units with my own layer-order code and
assembled the CNF myself (base + appended units). Then I ran CaDiCaL 3.0.1 `--lrat
--binary=false` and cake_lpr a36874a. Nodes: 13 wave-1 nodes (all four H6(1|2, ·) top cases that
occur, depths 2–5), 4 wave-2 nodes, and 2 depth-2 C3-S closures (`0s0-4s0_7s1-9s1`,
`0s0-5s1_1s0-10s1`). In all **19 of 19**:
- the unit count equals the record;
- the CNF sha256 equals the record;
- CaDiCaL answers UNSAT;
- cake_lpr prints `s VERIFIED UNSAT`.

**A5. Lemmas 1–5 against `hullcase.py`.**
- I checked the hull orders H3: 0, 2m, m; H6(a,0): 0, a, 2m, a+2m, m, a+m; H6(a,1):
  0, a+m, 2m, a, m, a+2m by hand from the keys (σ, i). `layer_order` implements the same key
  (σ flipped on r + m only).
- One-orbit order r, r+2m, r+m: R(r) = r + 2m is the point 120° further counter-clockwise.
- Layers: each layer is a convex R-invariant set, so it has 3 or 6 points and contains c
  inside. Units are taken only against the remaining points (`rest`). `layer2_options` lists
  every 1-orbit layer and every 2-orbit layer with all 4 σ pairs, so a last layer with fewer
  points is always among the options.
- Renormalization a ≤ 5: moving label 0 to the other orbit sends a to m − a, and both s are
  kept. In the test, every H6 set had a frame with a ≤ 5.
- Mirror: `mirror_layer` is (r, s) ↦ (m − r, 1 − s). `h3_layer2_kept` keeps the key-minimal
  member of each pair: 100 of 190 kept, 10 self-mirror.

I found no configuration that no node covers.

**A6. Drivers and the cut.**
- *Drivers.* `close_node.py` and `close_tree.py` hash exactly the file they solve and check,
  and set `certified` only from `dual()`. `dual()` requires both strings exactly. A SAT answer
  or a rejected proof stops the run.
- *Cut check.* `compose.py` counts a node as covered only if it is certified, or if it is a
  prefix of a certified node and all its `tree_children` are covered. A leaf, or an empty child
  list, is never vacuously covered: such a node is not a prefix of any certified node.
- *Own cut check.* `tools/mycompose.py` uses my own tree definition (my own mirror rule) and
  reads all 24,445 certified records (wave 1 and wave 2 at the time). It gives the same answer
  as `compose.py`: not covered, 6,591 frontier nodes, 0 duplicate records, and 0 child-list
  differences from `tree_children` on the 417 prefix nodes.
- *sha256 recomputation.* I ran `compose.py`'s sha check with the rebuilt base over **every**
  certified record: all 22,622 wave-1 records (`logs/compose_sha_C01_C17.txt`,
  `logs/compose_sha_g0..3.txt`) and the 2,213 wave-2 records present at about 01:05 UTC
  (`logs/compose_sha_wave2.txt`). No mismatch.

## What I could not check

- An in-class test of the 7-gon clauses at m = 11 (finding 3). No in-class 33-point set is
  known, and finding one is the point of the search.
- A formal proof of the C3a encoding or of Lemmas 1–5. They are checked only by the tests
  above and by hand.
- The ~24,400 closures that I did not re-solve. Their proofs no longer exist (finding 1).
- lrat-check: I did not rebuild it. I relied on cake_lpr alone.
- Wave-2 records that arrived after about 01:05 UTC.
- The E/E2 D3 encodings themselves. They are not needed for the C3 class (D3 sets are
  3-fold), only for the separate D3 claim.
