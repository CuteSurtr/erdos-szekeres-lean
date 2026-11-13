# STATUS20261104: where the project stands (4 November 2026, evening KST)

This is the page to read first when continuing on another machine. Details are in the linked results directories.
Rigor labels: Lean-checked / certificate (an LRAT proof accepted by both checkers) / exact computation / written proof
(not refereed) / evidence only.

## Results

**ES(7) = 33 for symmetric sets** (`WRITEUP/SYMMETRIC.md`).
- **Theorem A:** every set of at least 33 points in general position with a non-trivial symmetry contains a convex
  7-gon. Certificates plus a Lean reduction (`SYMLEAN`); written proofs for the encoders.
- **Sharpness:** there are 32-point examples with a half-turn and with a reflection.

**k = 8: the largest m-fold set in general position without a convex octagon** (note `WRITEUP/note`; `LAYERLEAN`,
`LEANEXT`).

| Symmetry | Value | Status |
|---|---|---|
| reflection | 46 | via Baek, Lean-checked bounds |
| half-turn | 64 | exact computation |
| 3-fold | ≥ 61 | open |
| 4-fold | ≥ 52 | open |
| 5-fold | ≥ 56 | open |
| 6-fold | 54 or 60 | certificate (`C6UPPER`, two encoders); exact value open (`SIX10REFINE`, `SIX10CEGAR`) |
| 7-fold | exactly 64 | certificate (`C7UPPER`, two encoders) |
| order ≥ 8 | 1 | Lean-checked |

**Lean-checked** (`LAYERLEAN`):
- the layer lemma, with strict nesting and the centre excluded for even m;
- the chain-clause family and the angular rules in polar form;
- the reductions from `Sixfold66` and `Sevenfold70`.

**Still written proof:** the phase-pattern classification inside the generators and the code-to-clause step.

**The newest result** (`SIX10CEGAR`, evidence only). For the exact 6-fold value, the parallel cube CEGAR closed no
cube, but it reduced what remains to **10 clusters of hard abstract models**, one per cube:
- 101 models in total, stored losslessly in `SIX10CEGAR/hard_models/`;
- each cluster is one core sign pattern with 2–6 free triple signs;
- no implemented certificate excludes them, and no numerical fit realizes them.
- **Next step:** an exact nested-face certificate. It would use exact linear relations among layer seeds, on at least
  7 layers, with a matching exact checker, aimed at the 10 cores.
  - If all 10 fall, rerun the lanes with the 10,608 verified cuts (`cuts_verified.clauses`) plus the new ones.
  - If a core survives, it is the candidate for a 60-point set.

## Branches

| Branch | Where | Contents |
|---|---|---|
| `es7-night-2026-11-01` | pushed (this branch) | all results above, on top of `es7-cloud` |
| `es7-cloud` | pushed | the earlier cloud campaigns |
| `es8-c6c7-review-2026-11-04` | **local on the Mac only, not pushed** | the independent review: `C6C7REVIEW`, `ROTREFINE20261104` |

**Dependency.** `SIX10CEGAR/tools` need `ROTREFINE20261104/math_linear.py` (through `sdp_ext.py`) and
`ROTREFINE20261104/m6_product_cycles.py`. Both are on the review branch, which must be pushed or copied before those
tools run elsewhere.

## Not in git (on the Mac, under the repository's `proof-archives/`, about 241 GB)

- LRAT proofs, with SHA256SUMS and round-trip records: `es8-c6-octagon-2026-11-03`, `es8-c7-octagon-2026-11-03`, and
  the `es7-*` campaigns.
- **The CEGAR base formula:** `es8-rot-refine-2026-11-04/m6/current.cnf`, 78 MB as zstd, SHA-256 `4281bf37…`, with
  9,198,581 clauses. It is encoder A plus the review's cut blocks, which are listed in the archive's manifest.
- **The full 6-fold CEGAR run:** `es8-six10-cegar-2026-11-04/six10_cegar_run.tar.zst` (616 MB). It has every model,
  witness and SDP lift, all 10,917 cuts, and `blocked.clauses`.
- **Also local only:** the append-only research log, and a draft email about the k = 8 results (not sent).

The CNFs regenerate in seconds from the committed generators (`C7UPPER/gen.py`, `C6UPPER/encb/gen_b2.py`). Only the
CEGAR base needs the review's cut blocks.

## Setting up on Linux

**Solvers.**
- CaDiCaL 3.0.1, `lrat-check` from drat-trim, and `cake_lpr`, the verified CakeML checker.
- Typical calls: `cadical --lrat --binary=false X.cnf X.lrat`, `lrat-check X.cnf X.lrat`, and
  `cake_lpr --CML_HEAP_SIZE=8000 X.cnf X.lrat`.

**Python.**
- The generators and checkers need only the standard library (`python3 -I`).
- The SDP and CEGAR tools need a venv. Versions used: python-sat 1.9.dev19, which provides the `cadical300` binding;
  numpy 2.5; scipy 1.18; cvxpy 1.9.3; clarabel 0.11.1.

**Lean.** Use elan with `leanprover/lean4:v4.24.0` (`lean-toolchain`). Get Mathlib at the pinned revision with
`lake exe cache get`. Check a file with `lake env lean <file>` from the repository root.

**Paths in `SIX10CEGAR/tools`.** Replace the placeholders with local directories:
- `<run-dir>`: a scratch working directory;
- `<SIX10REFINE>`: `results/SIX10REFINE`;
- `<review-results>`: a results directory that contains `C7UPPER` and `ROTREFINE20261104`;
- `<research-venv>`: the venv;
- `<proof-archives>`: the archive directory.

Also set `ES_RESULTS` to the review results directory.

## Decisions pending

1. Push or merge the review branch `es8-c6c7-review-2026-11-04`.
2. Merge the draft k = 8 section into the note. The draft is here: `k8_section.tex`, plus `k8_wrapper.tex`,
   which compiles it standalone with the note's preamble.
3. Send the k = 8 email (draft kept locally).
4. Optionally fast-forward `es7-cloud` to this branch.
