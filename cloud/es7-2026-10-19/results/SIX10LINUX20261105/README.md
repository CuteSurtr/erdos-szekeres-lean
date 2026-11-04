# SIX10LINUX20261105: the 5 November campaign on the sixfold 60-point question

5 November 2026, 00:00–01:20 KST, on a 32-core Linux machine. A coordinator ran five parallel workstreams: CEGAR,
facial reduction, alternative certificates, realization and direct search. Most attacks went to the open case of
`STATUS20261104`: is the largest 6-fold octagon-free set 54 or 60 points?

**Outcome.** The question is settled by construction: **60** (`SIX60`). This directory records everything else the
campaign established on the way. Rigor labels: exact computation / written proof (not refereed) / evidence only.
"Re-checked" means the coordinator re-checked it with code written independently of the producer's.

## 1. The 101 hard models of SIX10CEGAR are all non-realizable (exact, re-checked)

`SIX10CEGAR` left 10 clusters (101 blocked models) that no implemented degree-2 certificate excluded. All are now
excluded, by three independent certificate types.
- **Facial-reduction degree-2 certificates** (`certs/facial_clusters/<cube>/`): one clause per cluster that avoids
  the cluster's free signs.
  - Re-checked by `../CHORD20261105/tools/facial_indep.py`, which rebuilds the forms in oblique coordinates and binds
    the signs to the original cluster files. All 10 are negative semidefinite, and every member of every cluster
    falsifies its clause (101/101).
  - The last cluster, c11111, falls to a 2-record certificate: an instance of the chord lemma.
  - Four clusters (c00001, c01001, c10000, c11000) need genuine nested-face certificates without phase rows.
- **Biquadratic final polynomials** (`certs/altcert/`, Bokowski–Richter).
  - Exact certificates on 3 layers (4 for c11111) for every GP-consistent cluster.
  - Re-checked by `certs/altcert/bfp_indep.py`: 55/55 certificates accepted and 40/40 corruptions rejected. Each
    clause equals exactly the negation of the bracket signs its comparisons use, so it is a sound general cut.
  - The complete directed product graph (all 4,551,260 rotation-reduced GP identities) is acyclic for all 83
    GP-consistent models, so plain product cycles fail while the log-linear LP succeeds.
  - On those 3-layer subsets a degree-4 Lasserre relaxation still has positive margin (evidence).
- **Grassmann–Plücker violations** (`certs/gp/`). c11000 (15/15) and 3 of 8 c10000 models violate 3-term GP
  relations. That gives 436 six-literal cuts, re-checked by `../CHORD20261105/tools/gpcheck_indep.py`, with 0
  violations on 300 random real configurations.
  - **Each family is explained by one orbit sign** (`certs/gp/gp_culprit.py`, `flipgp.py`): every violated identity
    involves the orbit of (2.0, 3.4, 4.5) for c11000, resp. (4.0, 5.2, 9.0) for c10000.
  - Flipping that single bit leaves a model satisfying all 4,551,260 GP identity classes. So the GP obstruction is
    one inconsistent ray in the circular sequence at one point.
  - The facial certificates do not use those bits, so they also exclude the repaired neighbours.

These are certificates for individual abstract models, kept for the record. They do not bear on the theorem, which
is settled by `SIX60`.

## 2. Why those models looked hard: the chord lemma (written proof + exact)

See `../CHORD20261105`. A radius-free lemma fixes the orientation of a triple with two points on one layer from the
phases alone. The encoder lacks it, including every triple that contains an antipodal pair.
- 90 of the 101 hard models violate it.
- The old pipeline always ran its SDP with `--no-phase --no-radius`, so these certificates were invisible to it.
- An independent agent classified all locally forced signs at degree 2 on at most three layers, with a clear
  numerical gap. That classification shows the lemma is all the local degree-2 information that prunes models.

## 3. The 10-layer CEGAR on Linux (evidence; stopped)

`records/cegar_README.md` describes the rebuild:
- encoder A plus the 10,608 verified cuts, with lazy GP refinement in place of the missing archive blocks;
- an inbox for certified cut families from the other workstreams;
- one lane per phase-order cube;
- every cut accepted by an exact checker before use, with blocked models kept apart as assumptions.

Rates fell from about 3,000 to about 1,650 models per 10 minutes over all lanes once the local families were
loaded. The lanes then reached abstract models with **strictly positive** Hermitian SDP margin even with phase and
radius rows (+1.9e-10 to +9.6e-6). Steering the SAT solver by real configurations produced 17 such models with
margins up to 2.8e-4, comparable to the realizable 54-point sets (4e-5 to 4e-4). No degree-2 certificate can exclude
those models, which pointed to realizability. The 60-point sets of `SIX60` then showed that cube c11111 is
realizable, so the lanes were stopped at 01:04 KST.
- The real 60-point set A satisfies all 2,157,010 clauses of the 74 clause files then present.
- Set B satisfies all 2,195,980 clauses of the 84 files present at 01:25.
- This is a strong consistency check of every cut family used.

## 4. Constructive results (exact; see `SIX60`)

Two methods found 60-point sets:
- **alternating projections** between real configurations, phase-guided SAT models and fits (realization
  workstream; sets A and B);
- **a phase-fixed SAT plus LP CEGAR**, where for fixed phases every orientation is linear in the inverse radii
  (direct-search workstream; set C).

Earlier evidence from the same night: pure annealing of the octagon count stalled at 90 octagons, and adding one
hexagon to either certified 54-point set left at least 414 octagons on fixed-radius grids.

## 5. The known record sets do not extend by one layer (certificate: LRAT, lrat-check)

For each known record set, the realization workstream fixed all its layers' orbit signs and phase order, inserted
one new layer at every nesting position and phase gap, and solved the encoder formula. The logs in `extensions/`
record exit codes, lrat-check results and SHA-256 prefixes of each CNF and proof; the proof files themselves are
outside Git.
- **6-fold** (`extensions/lrat_ext_sixfold54.log`): neither 54-point order type of `ES8SYM` extends to 10 layers.
  All 36 cases are UNSAT, and lrat-check accepts 36 of 36 proofs.
  - For the nine-layer set the formula is encoder A alone.
  - For the one-orbit set, the innermost insertion also uses the verified cut file and a snapshot of the GP clauses.
- **4-fold** (`extensions/mfold_ext/lrat_ext4.log`): the 52-point order type of `ES8SYM/sets/c4_52pts_13layers` does not
  extend to 14 layers. All 26 cases are UNSAT with encoder A alone (`gen.py 4 8 14`), and lrat-check accepts 26 of 26.
- **5-fold** (`extensions/mfold_ext/lrat_ext5.log`): the 56-point set, centre dropped, extends to 12 layers only with
  the new layer innermost. 32 of the 33 cases are UNSAT, and lrat-check accepts 32 of 32. The innermost case is SAT
  for encoder A. Attempts to realize it failed (evidence only: at least 3,125 convex octagons).

These statements rest on the written soundness of encoder A and concern extensions of these specific order types
only. The 60-point sixfold sets of `SIX60` contain neither 54-point order type, as this result requires.

## Files

- `records/`: the five workstream READMEs as of 01:15 KST (`cegar`, `facial`, `altcert`, `search`, `realize`),
  with machine paths replaced by placeholders.
- `certs/facial_clusters/`: the cluster certificates, their clauses and logs, and the producer's checker.
- `certs/altcert/`: the final-polynomial certificates (`bfp_certs/`), the producer's checkers, and the
  coordinator's `bfp_indep.py`.
- `certs/gp/`: the GP cuts, witnesses and checker, and the coordinator's culprit analysis.
- Outside git, in the campaign work directory: all lane models, cut files (about 0.4 GB of inbox clauses), lifts
  and logs.
