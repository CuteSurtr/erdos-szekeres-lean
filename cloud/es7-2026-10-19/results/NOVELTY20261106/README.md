# NOVELTY20261106: novelty check of the project's candidate results (6 November 2026)

**Rigor: evidence only (bounded literature inspection).** This record says what was searched, what was found and how
each candidate result compares with it. It is not a priority claim. Absence of prior work in the sources below is
evidence, not proof, and indexing can miss manuscripts, journal versions and non-English work.

*Note added 6 November 2026, after 07:41 KST.* This record keeps its wording of the morning of 6 November. Since then
the hash-bound cake_lpr replay (6 Nov 2026) has finished: all 64 sixfold cube formulas (32 per encoder) were regenerated
with their recorded hashes and solved again, and cake_lpr accepted every fresh proof, 64 of 64
(`C6UPPER/replay-2026-11-06/README.md`, `C6UPPER` §6). Where this page says that only 6 of the 64 are hash-bound, or
that the full replay is planned, that describes the state before the replay. The novelty verdicts are unchanged.

## Purpose and scope

The question was which results, if any, are worth reporting to professors, and with what wording. The check ran on
6 November 2026 as one workflow: an inventory of the project's results from its own records, four literature checks
(ES(8) upper bound; the symmetric k = 8 table; the chord lemma and realizability certificates; the lrat-check
defect), three adversarial reviews (ES(8) upper bound; symmetric table; chord lemma), each told to refute the
novelty claim with new search terms and to re-run the stored checkers, and a synthesis. The agent outputs are in the
session's workflow journal (outside Git). No project file was changed and nothing was posted or sent.

How sources were found and read:
- **arXiv API** (`export.arxiv.org/api/query`), titles and abstracts: `all:Szekeres` sorted by date (back to May
  2025); phrase queries "convex position", "convex octagon", "convex heptagon", "happy ending", `ti:"Erdos-Szekeres"`;
  author queries Subercaseaux, Heule, Scheucher, Balko, Valtr, Mackey, Przybocki, Krapivin; the 150 newest cs.CG
  papers up to 4 November 2026.
- **Full texts** (arXiv HTML, or PDF through pdftotext): SMQH v1; Mackey's thesis; Schroeder v1 pp. 1–3, §8 and
  App. C; Tóth–Valtr 2005; Mojarrad–Vlachos Theorem 1.1; Koshelev–Koshka Table 1 and §9.1.2; AlphaEvolve §38;
  Krapivin–Przybocki–Heule; Subercaseaux et al. (ITP 2024); Miyata–Moriyama–Imai 2009.
- **Abstract or metadata only**: Baek (full text of v2 read on 4 November, `C6C7REVIEW`), Dumitru (abstract and
  version history; HTML searched for k = 8 terms; §7 and Table 1 read on 4 November), Norin–Yuditsky, Vlachos 2015,
  Heule–Scheucher, Marić, Fukuda–Moriyama–Nakayama, the SMQH Springer chapter (Crossref only).
- **GitHub REST API** (`gh api`, read only): drat-trim issues, PRs, commits and branches; repository and code search
  for Erdős–Szekeres formalizations; contents and commit dates of GLitchfield/erdos-szekeres-convex-poly (not built).
- **Other**: Zenodo search and API, Crossref, erdosproblems.com #107, google-deepmind/formal-conjectures
  (`ErdosProblems/107.lean`), about 15 web-search phrasings, a few Russian- and Chinese-language queries.
- **Not accessed**: MathSciNet, zbMATH, Google Scholar; the SMQH chapter text; Baek–Balko (JCTA); ETV 1996;
  Bokowski–Richter 1990 and Bokowski–Sturmfels 1989 (bibliographic data only).

## Candidate results

Rigor labels: Lean-checked / certificate accepted by cake_lpr / exact computation / written proof (not refereed) /
evidence only.

| Candidate | Statement | Rigor | Novelty verdict (6 Nov) | Key comparison | Significance |
|---|---|---|---|---|---|
| ES(8) ≤ 311 | Every 311 points in general position in the plane contain 8 in convex position (`ErdosSzekeres.Omission.forces_convex_octagon_311`). | Lean-checked, kernel only: propext, Classical.choice, Quot.sound; no native_decide. One run on one machine (19 Oct 2026, about 175 CPU-h); not reproduced, not refereed. | Probably novel, high confidence: the best explicit bound found anywhere. | Peer-reviewed best 408: Mojarrad–Vlachos, DCG 56 (2016), [arXiv:1510.06255](https://arxiv.org/abs/1510.06255). Best public claim 319: Schroeder, unreviewed Zenodo v1 (19 Sep 2026), [zenodo.org/records/22842891](https://zenodo.org/records/22842891); Lean with 8 native_decide axioms. | Modest and incremental. 89 of the 97 points below 408 are Schroeder's, and so are the method and catalogs. The current catalogs cannot go below 304. |
| k = 8 rotational maxima | The largest octagon-free set in general position is 64 for 7-fold symmetry (centre plus 9 heptagons) and 60 for 6-fold (10 hexagons). A 6-fold set cannot contain the centre (a point, its half-turn image and the centre are collinear), so its size is 6t. So ES(8) = 65 holds for both types, and the largest sizes it allows are attained. | Lower bounds: exact computation (7-fold: seven pairwise non-equivalent order types, none equivalent to the classical Erdős–Szekeres set; 6-fold: five order types A, B, C, C′, D, re-checked 6 Nov). Upper bounds: certificate accepted by cake_lpr, two encoders; reduction Lean-checked (`LAYERLEAN`); encoder soundness written proof (not refereed). 6-fold: all 64 cube proofs accepted at solve time (3 Nov), but a hash-bound cake_lpr replay exists for only 6 of 64. | Probably novel, medium confidence. No prior or concurrent work found. | SMQH, Subercaseaux–Mackey–Qian–Heule, [arXiv:2506.00224](https://arxiv.org/abs/2506.00224) (CICM 2025): reaches k = 7, nothing for k = 8. Mackey, [CMU-CS-25-108](http://reports-archive.adm.cs.cmu.edu/anon/2025/CMU-CS-25-108.pdf): k = 6 only. AlphaEvolve, [arXiv:2511.02864](https://arxiv.org/abs/2511.02864) §38: 64-point sets, no symmetry stated. | Answers SMQH's §7 suspicion for k = 8, for these two symmetry types. CICM/EuroCG level; of interest to the SAT-plus-geometry community. The 3-, 4- and 5-fold upper bounds stay open. |
| Symmetric ES(7), Theorem A | Every set of at least 33 points in general position mapped onto itself by a non-identity isometry or affine bijection has a convex 7-gon. Sharp: 32-point half-turn and mirror examples. | Reduction Lean-checked. Mirror classes Lean-checked from the vendored formalization of Baek's theorem. Threefold and central: cake_lpr verdicts recorded at solve time, mostly for proofs later deleted; single encoder, written proofs (not refereed). Fivefold: retained proofs accepted by cake_lpr. | Threefold (33) and central (34) cases: no prior result found. The other classes are credited. | Mirror: corollary of Baek, EJC 124 (2025), [arXiv:2206.04260](https://arxiv.org/abs/2206.04260). Fourfold 32-point exclusion: SMQH §6.2. Fivefold: B. Dumitru, [arXiv:2512.24061](https://arxiv.org/abs/2512.24061), a reported computation with priority. | Mention with caveats. The weakest link is the recorded verdicts of deleted proofs. |
| Mirror–ETV reduction | N_mir(2j) = 2N(2j,j,2j)+2 and N_mir(2j−1) = 2N(2j−1,j,2j−1), with N the Erdős–Tuza–Valtr function; gives N_mir(7) = 32, N_mir(8) = 46. | Upper bounds Lean-checked (through Baek's theorem, no SAT input). Far-flat construction and ETV equivalence: written proof (not refereed). | The reduction was not found in print. The k = 7, 8 values follow from Baek's theorem by an elementary lemma. | Baek, [arXiv:2206.04260](https://arxiv.org/abs/2206.04260), Theorem 1.6. | Clean but shallow. |
| Lean proofs of Suk 2016 and HMPT 2020 | Formalizations of known asymptotic bounds (HMPT: ordinary point case) and of ES(n) ≥ 2^(n−2)+1. | Lean-checked (library audit, standard axioms). | Not the first formalizations. | [GLitchfield/erdos-szekeres-convex-poly](https://github.com/GLitchfield/erdos-szekeres-convex-poly) (public; created 2026-08-01, last pushed 2026-10-20): `suk_explicit_upper` and `hmpt_explicit_upper` with explicit, weaker constants (Aug 2026), and a kernel-only `tothValtr_upper` (self-reported audit), which gives ES(8) ≤ 464. Seen through the GitHub API, not built. | Formalization of known theorems. Possibly distinct: the published leading constants (not verified). |
| Chord lemma; 101 non-realizability certificates | A radius-free orientation rule for triples with two points on one regular layer; all 101 `SIX10CEGAR` hard models are non-realizable. | Lemma: written proof (not refereed), exact per-clause certificates for m = 6 (976/976). Certificates: exact computation, re-checked independently (stored checkers re-run 6 Nov). | Known methods. The lemma is unpublished but elementary half-plane geometry. | Biquadratic final polynomials: Bokowski–Richter, EJC 11 (1990); symmetric form: Bokowski–Sturmfels, LNM 1355 (1989). SDP certificates for symmetric realizations: Miyata–Moriyama–Imai, [RIMS Kokyuroku 1641 (2009)](https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1641-02.pdf). | Methods material, not a result. |
| lrat-check defect | drat-trim's lrat-check (master 2e3b2dc) prints `c VERIFIED` and exits 0 for the proof `2 0 0` of the satisfiable `p cnf 1 1 / 1 0`. | Exact reproduction (`LRATCHECK20261105/reproduce.sh`). | Publicly known upstream. E2 (20 Oct 2026) was an independent rediscovery. | drat-trim [#31](https://github.com/marijnheule/drat-trim/issues/31) (2022-07-22); fixed in cbd2915 (2022-10-19); regressed in [5cd8ac3](https://github.com/marijnheule/drat-trim/commit/5cd8ac351070adf87e21bc88b4e0eedbdc18f7c0) (2024-04-21); [#42](https://github.com/marijnheule/drat-trim/issues/42) and [PR #43](https://github.com/marijnheule/drat-trim/pull/43) (2026-09-29): same reproduction, one-line fix. | A methods caveat. Cite #42. |
| Route to 310; 71-hole vector | No bound. A 0/1 balanced hole vector with 71 holes satisfies all 3,131 balanced constraints, so h_B^min lies in [64, 71] and the current catalogs cannot prove better than ES(8) ≤ 304. | 71-hole vector: exact computation. Budget-64 search: unfinished, evidence only. | Not applicable: these are statements about the method. | — | Limits of the method, not bounds on ES(8). |

Supporting material only: Theorem E (`PRIMEFOLD`; now a certificate accepted by cake_lpr: 7/7 regenerated CNFs with
matching hashes on 5 November, `LRATCHECK20261105/recheck`, plus 10/10 from the independent encoder `enc_te.py`), the
k ≥ 9 rotational records, the even-k centrally symmetric sets (implied by Baek–Balko plus the SMQH/Mackey sets), and
the other k = 8 symmetry types (half-turn ≥ 64, 3-fold ≥ 61, 4-fold ≥ 52, 5-fold ≥ 56; upper bounds open).

## Safe wording

- **ES(8) ≤ 311.** "As far as we found, ES(8) ≤ 311 is the best explicit upper bound. It is kernel-checked in Lean 4
  (axioms propext, Classical.choice, Quot.sound only) in a single run on one machine, it is not peer reviewed, and it
  is built on Schroeder's omission method and catalogs. The peer-reviewed bound is 408 (Mojarrad–Vlachos); Schroeder's
  unreviewed preprint gives 319."
- **k = 8, rotational symmetry.** "ES(8) = 65 holds for 6-fold and 7-fold symmetric sets, and the largest sizes this
  allows, 60 and 64, are attained by explicit sets. This is computer-assisted and unrefereed: the lower bounds are
  exact computations, the upper bounds LRAT proofs from two encoders accepted by cake_lpr, on top of a written
  encoding argument. We found no prior work; this is not a priority claim."
- **Symmetric ES(7).** "Every set of at least 33 points in general position with a non-trivial symmetry has a convex
  7-gon (computer-assisted, unrefereed). The mirror case follows from Baek's theorem, the fourfold 32-point exclusion
  is due to SMQH, and the fivefold case also follows from Dumitru's earlier reported computation. We found no prior
  statement of the threefold and central cases."
- **Checker.** "Every SAT fact our stated results rely on has a verdict of the verified checker cake_lpr (some only as
  solve-time records), and only its `s VERIFIED UNSAT` line counts. The unverified lrat-check on drat-trim master accepts some invalid proofs, a known regression (drat-trim
  issue #42)."
- **Chord lemma and certificates.** "Methodological; the certificates are of classical types (Bokowski–Richter,
  Bokowski–Sturmfels, Miyata–Moriyama–Imai)."

## Do not claim

- "First", or any priority. The phrase is "we did not find prior work".
- A first Lean-checked or first kernel-only ES(8) bound: Schroeder's 319 is Lean-checked (with native_decide), and
  GLitchfield's kernel-only Tóth–Valtr proof gives ES(8) ≤ 464.
- That earlier formal work stops at n = 6, or that the Suk and HMPT proofs are the first formalizations.
- "6-fold = 60" on its own: 60 is the largest multiple of 6 below 65. State the 6-fold case of ES(8) = 65 plus
  attainment.
- That the 7-fold sets have no line-modules: shown for only 2–3 of the 7, and only for the module sizes checked;
  three have 9-point modules.
- 324 or 404 as proved bounds (an unsourced table entry and the asymptotic shape of Norin–Yuditsky), or 310 or 304 as
  bounds on ES(8).
- The lrat-check defect as the project's discovery.
- That the chord lemma is "all the local degree-2 information": evidence only, and literally false (672 further
  three-layer rules exist).
- "Accepted by both checkers" as the certificate grade: cake_lpr carries it.

## Fixes needed before sending anything

From the synthesis. Items tagged *6 Nov pass* were assigned to the records-fix pass of 6 November; the coordinator
ticks each one once its change is committed.

- [ ] `WRITEUP/note/symmetric_extremal.tex`: tab:k8 6-fold row, open problem (4) and the abstract still say
  "54; at most 60"; give 60 exactly and add the 6- and 7-fold results to the abstract. *6 Nov pass*
- [ ] Same note: Theorem E, the rigor-label definition and tab:rigor still use "lrat-check only"; anchor on cake_lpr
  alone. *6 Nov pass*
- [ ] Same note: the literature section is dated 1–2 November; add the 4 and 6 November checks. *6 Nov pass*
- [ ] `STATUS20261105` item 1 and the `C6UPPER` addendum say three order types; there are five (A, B, C, C′, D).
  *6 Nov pass*
- [ ] `docs/RELATED_WORK_2026-10-14.md` lines 1450–1451 call Baek's development the only other Lean formalization;
  cite GLitchfield and EmptyHexagonLean. *6 Nov pass*
- [ ] Cite drat-trim #31, #42, PR #43 and 5cd8ac3 in `E2/logs/lrat_check_soundness.md`, `LRATCHECK20261105/README.md`
  and `AUDIT.md`. *6 Nov pass*
- [ ] Dumitru's name: "B. C. Dumitru" in both notes' bibliographies and `author = {Bogdan, Dumitru}` in
  `LIT/references.bib` should give B. Dumitru. *6 Nov pass*
- [ ] `PRIMEFOLD/README.md` (lines 125–130 and the §9 table) still says Theorem E is lrat-check only. *6 Nov pass*
- [ ] `symmetric_es7.tex` and `WRITEUP/SYMMETRIC.md` §3 name the patched lrat-check as a trusted checker. *6 Nov pass*
- [ ] Hash-bound cake_lpr replay of all 64 sixfold cube proofs (6 of 64 now). Planned; not part of the pass.
  *Run, 6 Nov 07:41 KST: 64 of 64 accepted (`C6UPPER/replay-2026-11-06/README.md`); to be ticked by the coordinator
  once the records are committed.*
- [ ] Date the claims with an arXiv note, and make the 311 check reproducible (compact checker, gate G2). User
  decisions; not part of the pass.
- [ ] The unsent k = 8 email draft (on the Mac) still has the 6-fold value as 54 or 60. User decision.

Also raised by the reviews: the "all the local degree-2 information" wording in `CHORD20261105` §4, `SIX10LINUX20261105`
§2 and `STATUS20261105` item 2; `certs/facial_clusters` lacks the producer's checker, the 1,176 rule witnesses and the
degree-4 certificates are not in Git, and `CHORD20261105/logs` is empty.

## Unresolved

- Not read: the SMQH Springer chapter, a possible TALG version of SMQH (one search snippet; Crossref has no record),
  Baek–Balko in JCTA, ETV 1996, Balko–Valtr's journal text, the paywalled databases.
- GLitchfield: when the repository became public is unknown (the events API reaches back only to 6 October). Whether
  this project's Suk and HMPT proofs are the only ones with the published leading constants was not checked.
- The three 7-fold sets with 9-point line-modules: whether they are Baek–Balko blow-ups was not checked.
- Chord lemma: completeness is numerical evidence only, and the unit counts disagree (308 in `CHORD20261105` §4, 288
  in the facial records; the binary counts reconcile, 216 + 672 = 888).
- C6UPPER: the solve-time cake_lpr logs record cube labels, not hashes, and whether the Mac lrat-check used for the
  4 November replay was the E2-patched build is not logged. *(6 Nov, 07:41 KST: the hash-bound cake_lpr replay (6 Nov
  2026) now binds a cake_lpr verdict to the CNF and proof hashes of all 64 cube formulas, so the sixfold bound no
  longer depends on the label-only logs. The lrat-check question is still unlogged.)*
- 311: never replayed by an independent checker (lean4checker, nanoda); the compiled parts (about 500 GB) were deleted.
- Upstream: a confirming comment on drat-trim #42/#43 is the user's call. `~/.local/bin/lrat-check` on the Linux host
  is still the unpatched build.

## Suggested paragraph for a professor

To be adapted by the author; about 175 words.

> I have been working on small cases of the Erdős–Szekeres problem with computer help, and two results may interest
> you. First, ES(8) ≤ 311. The proof adapts Michael Schroeder's omission method and catalogs (his unreviewed preprint
> gives 319; the best published bound is 408, by Mojarrad and Vlachos) and is checked by the Lean 4 kernel with only
> the standard axioms. That check ran once, on one machine, and the result is not peer reviewed. Second, building on
> the symmetric SAT constructions of Subercaseaux, Mackey, Qian and Heule, whose results stop at k = 7, I found that
> ES(8) = 65 holds for point sets with 6-fold or 7-fold rotational symmetry, and that the largest sizes this allows,
> 60 and 64, are attained by explicit sets. The upper bounds are SAT proofs accepted by the verified checker cake_lpr,
> resting on a written, unrefereed encoding argument; a full re-check of the 6-fold proofs is planned. A literature
> search on 6 November found no earlier statement of these results, but I would value your view on whether they are
> new.

*Note, 6 November after 07:41 KST:* the clause "a full re-check of the 6-fold proofs is planned" is out of date. The
hash-bound cake_lpr replay (6 Nov 2026) certified all 64 cube formulas again (`C6UPPER` §6). The author may want to change
it, for example to "all 6-fold cube formulas were solved again and the proofs checked by cake_lpr against hashed files".
