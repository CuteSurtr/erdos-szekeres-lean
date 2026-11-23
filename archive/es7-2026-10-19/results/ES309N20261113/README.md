# ES309N20261113 — ES(8) ≤ 309

> **Retention update (23 Nov 2026, owner OK):** the verify309-codex copies named in VERIFY309N's retention update
> (C24 residual proof copies, C32 UNKNOWN trace, C33 second proof) were deleted; the originals and the receipts stay.


13 November 2026, after the independent audit in [VERIFY309N20261113](../VERIFY309N20261113/README.md).

**PROVED (computer-assisted, with written geometric arguments and CERTIFIED / EXACT TREE components).**
Every set of 309 points in the real plane in general position (no three collinear) contains eight
points in convex position. Equivalently, every octagon-free set in general position has at most
308 points, and **ES(8) ≤ 309**.

**This is not a fully Lean-checked theorem and nothing here is refereed.** The previously Lean-checked
bound is ES(8) ≤310. The new step uses geometric encoder soundness arguments, cake_lpr certificates
and integer tree replays outside Lean. No root README or `math.md` was changed; no commit or push was made.

## Simpler two-slice chain, confirmed 14 November

**PROVED, computer-assisted with CERTIFIED and EXACT TREE components.** The
[independent N66 follow-up](../VERIFY309N20261113/followup56/VERIFY_N66_56.md)
confirms **N66 ≤ 56**. It recognizes all 319,611 trimmed clauses, including
56 sound mirror-symmetry clauses; rejustifies all 6,775 used rows; and covers
all 624 supporting CNFs with 620 prior independent checks and four fresh
certificates. The retained main LRAT passed an independent cake_lpr replay.

The hypotheses and Lean components in steps 1–3 below are unchanged. Lemma A
now gives h(Lo)≥14. If the total number of holes were at most 33, the existing
Lean exclusion forces exactly 33, while the nine F-rows give h(F)≥18.
Because F and Lo partition the catalog, h(F)=33−h(Lo)≤19. Thus only slices
18 and 19 remain. Their independently replayed trees use precisely the
2,650 Lean rows plus the two slice capacity rows:

| Slice | Capacity rows | Nodes | Minimum margin |
|---|---|---:|---:|
| 18 | h(F)≥18, h(Lo)≥15 | 3,815 | 1 |
| 19 | h(F)≥19, h(Lo)≥14 | 186,077 | 1 |

The only pending leaf is state 0 missing, excluded by actual residual-owner
occupancy. Hence total holes≥34, residual population≤120, and the existing
composition gives ES(8)≤187+120+2=309. This route uses neither slice 20 nor
the residual coupled-owner rows. No N5 bound is required.

Main N66 CNF SHA-256:
`8d4b9099cf045ca72ba5ac56e8ecea00a73a44652d5a9f3d100f63f1f10bc151`.
Retained and freshly replayed LRAT SHA-256:
`ff79c2ef3805255b18917dc0769c5088cca0ee8106c5eefb78b8f212fa487296`.
The two tree-archive hashes remain in the table below. A separate fresh
main solve ended UNKNOWN after 600 seconds and is not evidence for this
chain; the main certificate was independently checked by replaying the
retained proof, as stated above.

This removes one encoder family from the preferred argument. Lemmas A and S,
the N66 encoder and supporting certificates, and the tree replay still lie
outside Lean. Neither full Lean checking nor refereeing is claimed.

## Original three-slice chain and hypotheses

Let S be an octagon-free finite real point set in general position. The existing projective chart and
minimum-slope partition reduce it to a balanced configuration H and a residual configuration R, with
|S| ≤ 1+|H|+|R|. Small/empty cases are immediate. The chart has distinct x-coordinates and general
position; the residual configuration has no 6-cap, no convex octagon, and no junction consisting of
a 6-cup ending where a 5-cap starts. The existing Lean population-composition theorem handles the
chart reduction for arbitrary S.

1. **PROVED, existing Lean-checked component: |H| ≤187.**
   `ErdosSzekeres.Omission.Compact310.balanced_population_187`, in
   `experiments/omission-compact-checker-2026-11-05/assembly/Final310Compact.lean`.

2. **PROVED, existing Lean-checked components: residual catalog and base exclusion.**
   Residual owners inject into the 154-state catalog. For a nonempty residual configuration, state 0
   is occupied. Its Boolean hole vector h satisfies all 2,650 proved rows, and
   |R|+Σh=154. The existing exclusion `E310.residual_excludes_32` gives Σh≥33.
   Sources: `Residual32Bridge2650/Rows.lean`, the residual zero-state theorem, and the existing compact
   310 assembly; the correspondence of the archived row catalog was checked in `LO33N20261113/VERIFY_LO.md`.

3. **PROVED, written geometric Lemma A: h(Lo) ≥70−N66.**
   Define F={states with f₁≥5}, of size 84, and Lo={states with f₁≤4}, of size 70.
   Here f₁(v) is the longest cup ending at v minus one. An owner in Lo cannot be the endpoint of
   a 6-cup in the Lo subset, since that would give f₁≥5. The Lo owners also inherit no 6-cap,
   no convex octagon, distinct x-coordinates and general position. Thus their number is at most N66,
   where N66 is the maximum size of a (no 6-cap, no 6-cup, no convex octagon) set. Owner injectivity
   gives the stated hole inequality.
   Sources: `THEORY310N20261113`, §2; independent check `LO33N20261113/VERIFY_LO.md`, §2.6.

4. **CERTIFIED, with written encoder soundness: N66 ≤57, hence h(Lo) ≥13.**
   `N66N20261113`, certificate `data/cert57`, rechecked in `VERIFY309N20261113`, link (a).
   The 70-state monolithic sub-CNF for at most 12 holes is UNSAT, with no cube or symmetry-breaking
   assumption. Every clause was independently recognized as a valid geometric family, a fixed-state
   unit, a justified row or a sequential-counter clause. The trimmed CNF was reconstructed with its
   exact SHA-256; a fresh CaDiCaL 2.1.3 proof was accepted by cake_lpr.
   All 7,913 rows were independently re-justified. Their 621 distinct supporting CNFs are covered by
   272 freshly regenerated and certified checks plus 349 identical CNFs independently verified earlier.
   The canonical real-set assignment satisfies the geometric clauses; therefore UNSAT rules out
   any set with at most 12 holes, so its population is at most 70−13=57.

5. **PROVED, exact arithmetic Lemma S: only slices 18, 19, 20 can remain at 33 holes.**
   Nine of the 2,650 Lean rows each have demand 6 and support size 28 inside F, with each F-state
   occurring exactly three times. Summing yields 3h(F)≥54, hence h(F)≥18. This incidence identity
   was independently recomputed in `VERIFY309N20261113/logs/f18.json`.
   If Σh≤33, step 2 forces Σh=33. Write t=h(F); then h(Lo)=33−t. Step 4 gives t≤20, so
   t∈{18,19,20}. This is `LO33N20261113`, Lemma S. **No N5 bound is needed.**

6. **EXACT TREES: each of those three slices is impossible.**

   | slice t | additional capacity rows | other rows | nodes | verification |
   |---|---|---|---:|---|
   | 18 | h(F)≥18, h(Lo)≥15 | only the 2,650 Lean rows | 3,815 | independently replayed in VERIFY_LO |
   | 19 | h(F)≥19, h(Lo)≥14 | only the 2,650 Lean rows | 186,077 | independently replayed in VERIFY_LO |
   | 20 | h(F)≥20, h(Lo)≥13 | 2,650 Lean rows plus 578 coupled rows | 3,468,657 | independently replayed in VERIFY309N |

   Every tree has minimum integer margin 1. The single pending leaf is state 0 missing, impossible
   for a nonempty actual residual configuration. For slice 20, all 2,048 contexts cover the master
   frontier exactly, with paths independently reconstructed and checked against the stored paths.
   The capacity rows are precisely the ones in the table, not additional unproved population claims.

   The 578 coupled rows are **CERTIFIED** for CNFs whose soundness for every real residual
   configuration is **PROVED by the written family-by-family audit** in VERIFY309N link (c).
   All 578 regenerated CNF hashes match the record; 448 received fresh cake_lpr acceptances and
   130 match previously independently verified CNFs. All 448 fresh LRAT hashes also reproduce the
   original hashes. Thus the tree rows are justified for actual residual configurations.

7. **PROVED, written conclusion plus existing Lean-checked composition:**
   The contradiction in step 6 gives Σh≥34, so |R|≤154−34=120. Therefore an octagon-free set satisfies
   |S|≤1+187+120=308. The existing theorem
   `ErdosSzekeres.Omission.Partition.forces_of_population_bounds` combines
   `BalancedBound 187` and `ResidualBound 120`, with the immediate positivity premise, to give
   `ForcesConvexNGon (187+120+2) 8`, namely the claimed threshold 309.
   The new `ResidualBound 120` argument and its instantiation of this theorem have not been exported
   to Lean in this audit.

## Hashes and evidence locations

| artifact | SHA-256 |
|---|---|
| 2,650-row source, decompressed bytes | `e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6` |
| 2,650-row source, gzip file | `8c7fe9ef5264182524095d46ef50ed6bc691cab425efa965756d1870112241aa` |
| N66 trimmed CNF, budget 12 | `80b55b0c2c2ef445f485901e69fda3fdbb994fc1d882b5828d9227a85a695ee7` |
| original N66 trimmed LRAT | `3971e63f869224cca0e39d3b40e5070cfd737a2c13fdab8abb68bd6a105a5978` |
| fresh independent N66 LRAT | `46305acfef8d9f3961a5f7b94f1f96a2550e995611441ae16be4562e015956cc` |
| slice-18 Lean-row context archive | `52fc93b18eb0c1650a79a8bdce49a17b96786fc20d44b3bfe4541cf421f2fa4e` |
| slice-19 Lean-row context archive | `cabbdbdf27bb5e724bf63fa4d4a6caec96fba5c692411e4645e5e8ef6ffba8e2` |
| slice-20 extra rows | `d12f624f1858e8670988df864686accf1d35f4e02c7127b8c355bc918055ecee` |
| slice-20 normalized master nodes | `15cd5892e5b11ae103902ee8beb874962562f6cc9f19cc2c304641e8f88cd9b0` |
| slice-20 context digest | `709a345e47be19866a452ca9268644648d62c0df5b982fa5c1a78d78b4966567` |
| 578-row certificate inventory | `2f065615bc44a3c5d86693f0d57b29a1b2501df68439f4e210fd1bf15661682f` |

The fresh LRAT differs from the original because it is a fresh refutation of the trimmed CNF; both
refer to the same pinned CNF. The fresh proof, new row subproofs and residual proof objects are retained
under `/home/jay/research/data/verify309-codex-20261113/`. The large slice-20 tree is under
`/home/jay/research/data/lo33-20261113/bb_64_57/`; the slice-19 archive remains in the corresponding
`cert_65_56_leanrows/` directory. These external directories are essential evidence and are not committed.

The verification record retains commands, source code, every context hash, per-certificate receipts,
checker output, input/binary hashes and the final coverage summary. Its `SHA256SUMS` covers the archived
audit files. Existing source archives and previous verification records are named explicitly rather
than represented as fresh checks in this audit.

## What is and is not Lean-checked

**Previously Lean-checked:** geometric partition/composition, balanced population 187, residual owner
injectivity and catalog counting, the 2,650 base rows, state-0 occupancy and the exclusion at budget 32.
Their existing source signatures were inspected here; no new Lean build was run.

**Not Lean-checked here:** Lemma A's transfer to Lo capacity, Lemma S's slice gluing, the two CNF encoders'
soundness, LRAT checking by cake_lpr, the Python tree checker and its data parser, and the new residual
population-120 argument. The monolithic audit shares PySAT's sequential-counter encoder; that dependency
is explicitly retained. Real-set controls are **COMPUTED** finite tests, never substitutes for proofs.

In particular, this does **not** establish `Excludes2650Zero 33` over the base rows alone; that statement
is false because abstract 33-hole vectors exist. The proof uses geometric information valid for actual
residual configurations. A future Lean export must incorporate that information.

## Comparison with the literature

The bounded literature search in [NOVELTY20261113B](../NOVELTY20261113B/README.md), dated 13 November,
reports Schroeder's unrefereed bound 319, the refereed bound 408, and no bound at or below 310 found by
that search. This result improves the project's existing Lean-checked 310 by one, with a different
verification status: 309 currently has the computer-assisted trust boundary above.

This audit did not rerun the literature search. Its negative findings are **HEURISTIC evidence of
absence**, not a priority proof. The record lists unread journal sources and a comment thread, and
concurrent public work on related ETV cases. No novelty or priority claim stronger than that record is
made. The state-map, SAT and certificate methods have substantial precedent; nothing here is refereed.

## Scope and follow-up

All required links for this 309 chain passed; no counterexample or verification failure was found.
N66 ≤56 is now independently confirmed and gives the simpler two-slice chain
above. The slice-21 driver has reported closure, but that tree is neither
needed nor independently replayed in this audit. The separate E2 and D1b
checks completed during the Delta work; neither is needed by this chain.
The optional 308 route and a complete Lean export were not attempted. Research guards remain running
because other research jobs are active. Repository state remains uncommitted on the original branch.
