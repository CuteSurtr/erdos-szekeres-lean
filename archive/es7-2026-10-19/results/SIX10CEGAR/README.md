# SIX10CEGAR: parallel cube CEGAR on the 60-point sixfold instance (4 November 2026)

**Question.** Is the largest 6-fold octagon-free set 54 or 60 points? `C6UPPER` gives "54 or 60". Ten nested regular
hexagons in general position without a convex octagon would give 60.

**Outcome: evidence only; no cube closed.** The sixfold maximum stays **54 or 60**.
- Over about 2½ hours on 12 lanes, every lane kept finding new abstract models.
- 10,917 exact realizability cuts were made, and no cube became UNSAT.
- No near-realization was found.

## Setup

**Base formula.** `current.cnf` of the review archive `es8-rot-refine-2026-11-04/m6`, SHA-256 `4281bf37…`, with
9,198,581 clauses. It consists of:
- encoder A (`C7UPPER/gen.py 6 8 10`), with 1,609,785 clauses;
- the GP and determinant-identity cut blocks of `ROTREFINE20261104`, review branch `es8-c6c7-review-2026-11-04`.

**Cubes.**
- The reflection unit Y(1,2), plus the 12 consistent sign patterns of Y(1,3), Y(1,4), Y(2,3), Y(2,4) and Y(3,4).
  These are the 12 phase orders of `C6UPPER` §3, given as assumptions (`tools/cubes.txt`).
- One lane per cube (`tools/worker.py`): CaDiCaL 3.0 via PySAT, used incrementally. The lane first adds the shared cuts
  and then solves under its cube.
- `tools/supervisor.sh` restarts lanes that stop.

**Per SAT model.** The lane tries, in order:
1. the face certificate on the `model0090` face (`SIX10REFINE`);
2. the negative-definite certificate (`sdp_ext.py`, then `check_def.py`);
3. the generalized face read from the SDP lift (`facegen.py`, `face_sparse_g.py`, `face_cert_g.py`,
   `check_cert_g.py`);
4. faces read from lifts on layer subsets (`subface.py`, `facegen_sub.py`; added at 14:47);
5. negative-definite certificates on subsets with one or two layers dropped.

Face certificates are shortened by greedy exact row removal (`minimize.py`). A clause is appended to the shared cut file
only after an exact checker accepts its witness, and only if it falsifies the model it came from.

**Why every cut is sound** (written proof, `SIX10REFINE`). Suppose a positive combination of signed orientation forms
is negative semidefinite. Then no seed vector z ∈ R^20 gives all its records their required signs: that would make the
combination strictly positive. The cut is therefore valid for every configuration with the sixfold rotation. It uses no
convexity property.
- **Layer subsets.** A realization restricts to every subset of layers. Layers outside the subset are free coordinates
  of the face, so the certificate is still a statement on all 20 coordinates.

## Results

| Item | Value |
|---|---|
| cuts made | 10,917 (10,914 distinct) |
| UNSAT cubes | 0 of 12 |
| methods (cuts since 14:35) | face+min 2762, faceg+min 1827, subfaceg 433, def 84, faceg 50, face 23 |
| re-verified at the end | 10,608: audit with model binding 7,118; audit without it 963; exact re-certification 2,527 |
| not re-verified | 309 (checked only when made; witness lost) |

**Re-verification.**
- **Bookkeeping fault before 14:35.** Restarted lanes reused round numbers and overwrote earlier model and witness
  files. From 14:35 each lane generation has its own directory, and every provenance line names its witness and model.
- **Audit** (`audit.py`). It re-ran the exact checkers on a stored witness for each cut.
  - When the model file survived, the original checker ran, including the binding of the record signs to the model.
  - Otherwise a copy of it ran with only the three model-binding lines removed.
- **Cuts with no surviving witness** were re-certified from their own literals (`recert/recert.py`). The certificate
  search is restricted to the cut's records. A cut counts as re-certified when an exact checker accepts a witness whose
  clause is a subset of the cut.
- **Result.** 2,838 cuts had no surviving witness at 14:41:
  - 1,708 were re-certified on a face;
  - 821 were re-certified as negative definite;
  - 309 were not re-certified. The second pass, which tries 40 faces, was stopped at 16:16 after 166 of its 387 cuts.
- `cuts_verified.clauses` holds exactly the re-verified cuts. Any later UNSAT proof should use only this file.

**Face census.** Of 4,662 minimized face cuts made after 14:35, 2785 (60%) use one face, the `model0090` face:
layers 1–8 form one orbit, with layers 1–4 rotated by 60°, and layer 9 is at the centre.
- The next most common face has layers 1–9 at the centre (189 cuts).
- **What repeats is the face, not the configuration.** For most models the relaxation's optimum degenerates onto the
  same face, as a PSD mixture on it. The models themselves do not cluster at one face configuration: 40 sampled models
  disagree with every point of the face, over a 46 × 60 polar grid, on 301–1,053 (median 768) non-degenerate orbit
  triples (`near_face.py`).
- **No slowdown.** New models keep coming at about 40–150 rounds per cube per 10 minutes.

**Stalled lanes and multi-scale lifts.** Three lanes (c11111, c00001, c11110) kept returning the same model after every
restart.
- **The lift.** For c11111 the SDP lift is multi-scale: the layer norms are 1, 0.2, 1.4·10⁻³, 2.5·10⁻⁴ (five layers),
  1.8·10⁻⁴ and 10⁻⁶.
- **Why the margin proves nothing.** The margin of −9·10⁻¹³ is below solver tolerance, so it does not refute the
  model. A realization with very small inner layers would have orientations of that size.
- **Why the first face failed.** The face read from the full lift had 4 groups but rank 3. The face SDP was infeasible
  under both Clarabel and SCS.
- **The subset lift.** On layers 1–9 the lift shows a clean face: layers 3–7 coincide and layer 9 is at the centre. A
  21-term certificate on that face passes `check_cert_g.py`.
- **After the change.** Once `subface.py` was added, all three lanes resumed.
- **Hard models, blocked as an assumption** (from 15:00). Some models resist every method, including the subset
  search. Each such model is written to `blocked.clauses` (in the archive; index in `logs/blocked_models.tsv`) as the
  negation of its 5,710 triple signs, and the lane goes
  on. This file is never mixed into the cut file, and an UNSAT reached after a block would be logged as conditional.
  - By 16:10, 101 models were blocked.
- **The hard models tested in detail** (c11110 `147579e4`, c11001 `eddcc688`, c11001 `c12e54f7`):
  - none of the 40 faces used in the run gives a certificate on them (`facetry.py`);
  - neither do four faces read by hand from the subset lifts;
  - the margin SDP after rescaling each layer to unit norm (`sdp_scaled.py`; equivalent by congruence, so only the
    conditioning changes) stays at about −10⁻⁹, while the scales keep shrinking toward the centre;
  - the 4af547de control behaves the same way, so the rescaled SDP does not separate the cases;
  - the review's exact product-cycle search (`ROTREFINE20261104/m6_product_cycles.py`) finds no cycle on windows of
    up to 4 layers; the full mode stopped incomplete at its 6M-edge cap;
  - numerically, the dual combination of the margin SDP is negative semidefinite to 10⁻¹¹ relative, but its spectrum
    is graded (… 10⁻¹², 10⁻⁹, 10⁻⁸, 10⁻⁵ …), the signature of a nested kernel. The control 4af547de has the same
    shape, and its exact certificate was found on a layer subset.
- **Small subsets.** For `147579e4` and `eddcc688`, every subset of 3–6 layers that contains layer 9 (210 subsets
  each) has a strictly positive SDP margin: at least 4.7·10⁻⁷ and 3.8·10⁻⁵ respectively (evidence only). So any
  degree-2 certificate for them needs at least 7 layers.
- **The blocked models form one small cluster per cube.** 101 blocked models, in 10 clusters (cube: size): c00000: 12, c00001: 13, c01001: 16, c10000: 8, c10100: 3, c11000: 15, c11001: 1, c11011: 15, c11110: 3, c11111: 15.
  - Cubes c01011 and c11100 had none.
  - For 100 of the 101 blocked models, the nearest blocked neighbour differs in **one** triple sign.
  - Inside each cluster only 2–6 triple variables vary. The 16 models of c01001 are all 2⁴ settings of its 4 free
    signs.
  - So each cube's residue is one hard core pattern with a few free signs, and blocking single models only walks
    through those free signs.
  - The question 54 vs 60 thus comes down to these few cores: certify them, with a nested face on at least 7 layers,
    or realize them.
- **Why these models are hard.** By the Gordan-type alternative for the PSD cone, either a strictly feasible lift
  exists or an exact negative semidefinite certificate exists. A supremum of 0 approached only in the limit points to
  the second case. The certificate's kernel would then be a nested face that these tools cannot read off exactly.

**Numerical realizability probes** (evidence only; `realize_try.py`, `realize_opt.py`). These fit seeds in log-polar
coordinates, with a scale-free orientation loss.
- c11111 `4af547de`: at best 110 of 5,710 orbit signs wrong.
- c11110 `147579e4`: at best 87 of 5,710 orbit signs wrong.
- Nothing came close to a realization.

**Approaches tried that did not help.**
- **Cut images under relabelings.** Rotating one layer's labels by 60°, or applying the mirror, maps a cut to a valid
  cut. In a sample of 6 models, only 1 was excluded by such an image of an earlier cut (`image_test.py`).
- **Numerical attack on cuts** (`adversary.py`).
  - It maximizes the smallest signed orientation over a cut's records.
  - It breaks 10 of 10 random fake cuts, but 0 of 20 real cuts with one literal flipped. So it has no power on
    near-degenerate patterns.
  - It is **not** used as evidence of soundness.
- **Random configurations against all cuts** (`sample_check.py`): generic configurations, plus perturbations of the 20
  most common faces at scales from 10⁻⁶ to 10⁻¹. No cut was violated, but no one-flip mutant was violated either. The
  sampled configurations never reach these sign patterns, so this is **not** evidence.

## Rigor

- **Each cut: exact computation plus written proof.** The exact checkers are stdlib Python with rational LDL. They have
  had no second-person review.
- **The loop and its outcome: evidence only.** No UNSAT, so nothing about the maximum follows.
- **Not certificates:** the numerical probes and the census.

## Files

- **`tools/`**: the lane, the supervisor, the certificate scripts, the audit and the re-certifier.
  - Machine paths are replaced by placeholders: `<run-dir>`, `<SIX10REFINE>`, `<review-results>`, `<research-venv>`.
  - They need `ES_RESULTS` pointing at a results directory with `C7UPPER/gen.py` and
    `ROTREFINE20261104/math_linear.py`, which is on the review branch.
- **`logs/`**: per-lane logs, the event log, cut provenance, the audit and re-certification tables, and summaries.
- **`cuts_verified.clauses`**: the 10,608 re-verified cuts, in DIMACS clause lines.
- **`hard_models/`**: the 101 blocked hard models, stored losslessly as 10 cluster files, one per cube.
  - Each file holds a representative's true variables (triple orbits and phase order) and each member's flips.
  - `INDEX.tsv` gives the sizes and the representative's model-file SHA-256.
  - These are the targets of the next step.
- **Not committed:** `cuts.clauses`, with all 10,917 cuts, and `blocked.clauses`. Both are in the archive.
- **Archive:** the full run directory (all models, witnesses and SDP lifts) is in
  `proof-archives/es8-six10-cegar-2026-11-04/` (tar + zstd, round trip verified, `SHA256SUMS`).

## Credit

- The base formula, the GP and identity cut blocks, and `sdp_ext.py`'s linear-form module come from the review branch
  (`ROTREFINE20261104`).
- The face certificate for `model0090` is in `SIX10REFINE`.
- SDP certificates of non-realizability are classical; see Bokowski–Richter 1990, Richter-Gebert 1996, Parrilo 2003
  and `PRIORITY20261104` (review branch). No novelty is claimed for the method.
