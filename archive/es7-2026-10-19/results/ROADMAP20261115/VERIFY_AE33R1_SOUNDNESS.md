# VERIFY_C-ae33-radius1_soundness (independent verifier, lens SOUNDNESS AND SEMANTICS, no compute slot, 21 Nov 2026, 22:00-22:40 KST)

**Verdict: all seven claims CONFIRMED at their stated labels.** No error was found that changes a claim or a label.

- Three text fixes are recommended (§5):
  - the draft README calls AE33 "heptagon-free", which is wrong;
  - one sentence on order-type invariance is imprecise;
  - a two-line step (p's slot in Q1) is missing from the cited soundness texts.
- Computer-assisted, unrefereed. This is support evidence for ES(7) = 33 only; no bound changes.

| key | label | verdict | decisive basis (soundness lens) |
|---|---|---|---|
| ae33-r1-203-certified | CERTIFIED | **confirmed** | I checked all 203 fresh cake_lpr outputs from both runs (worker's and the rebuild verifier's): each is exactly the one line `s VERIFIED UNSAT`, and the worker's stderr files are empty. The hash chain tsv = certify.jsonl = summary.jsonl holds 203/203. The certified bytes are the bytes that were family-checked. I did not re-run cake_lpr |
| ae33-r1-regen-exact | EXACT | **confirmed** | binary hashes equal; `cnf_all4_equal` 203/203; regenerated independently by the rebuild verifier; I re-hashed 7 kept CNFs and they equal the tsv |
| ae33-r1-families-exact | EXACT | **confirmed** | Both independent generators (worker `indep.py`, rebuild `fam.cpp`) implement the sound definitions: I read the literal rules, ccw orders, W signs and R2 cone checks. My own hand-rule spot check: the 7 predicted clauses are each found exactly once in the right block of the certified bytes. They cover all 6 JK positions of the W literal plus OCTX and OCTY; the W-flipped mutants are absent |
| ae33-inputs-exact | EXACT | **confirmed** | own: JSON × 10^17 = `ae33.txt`; 0 collinear triples; H is a ccw convex 7-gon in the stated order; the 203 names are exactly the pairs meeting H; bases 203/203 and `_pts` 203/203 byte-equal; the second integer file has the same labelled order type. Uniqueness of H follows from convex7 = 0 in the 203 bases (§3.4). The m = 4..6 counts were not recounted by me |
| ae33-realpair-exact | EXACT | **confirmed** | Two independent evaluators plus L18's own give 21 JK / 57 OCTX / 125 OCTY. In my 7 spot pairs, every literal of the predicted clause is false under the real configuration, computed two ways |
| ae33-r1-soundness-proved | PROVED | **confirmed** | own family-by-family re-derivation (§2), plus a full reading of `l2enc.cpp`. Gap filled and scope noted (§5.3, §5.4) |
| ae33-r1-corollary | PROVED (CERTIFIED + PROVED soundness) | **confirmed** | The cases are covered: 203 + 325 = 528 = C(33,2). The 325 trivial pairs need only that H is convex, which I checked, plus the fact that orientations decide convex position. Premises are stated. Radius 0 follows |

## 0. What I did

**Budget.** I had no compute slot.
- All my checks were reading level: a few CPU-seconds in total, at most 15 MB RSS. `spot.sh` measured 1.3 s
  (user + sys); the greps over the ~1,200 small output files, the hashing and the JSON tallies add a little.
- I ran no unit, no cake_lpr, no solver and no CNF regeneration.
- YIELD was absent.

**Read.**
- The house rules: SKILL.md §1-§4.
- LOWERBOUND_RUN_1118: §(2) and the claims table.
- ABSAT8_INDEPENDENT §2-§3.
- LOWERBOUND_PLAN_1115PM, E7-2 (definition of radius 1) and E8-3.
- VB's VERIFY_LOWERBOUND_L18_E72.
- `L18/copied/l2enc.cpp`: all 469 lines (`171a3e7c…`).
- `L18/bin/run_e72.sh`.
- The worker's README.md, VERIFY_AE33R1.md, `tools/indep.py`, `tools/geom.py`, `tools/run_pairs.sh`, and the CaDiCaL part of `tools/summarize.py`.
- The rebuild verifier's README.md, VERIFY_C-ae33-radius1_rebuild.md, and the generator and literal parts of `tools/fam.cpp`.

**Own code** (directory `verify/soundness_lens/`):
- `spot.py` and `spot.sh` predict clauses by a hand rule, grep for them in the certified bytes, and include a mutant control;
- `bases_check.py`.

These were written from the note's semantics. They do not import or copy l2enc, indep.py or fam.cpp.

**Read as data:**
- `hashes_203.tsv`, `results.jsonl`, `summary.json`, `indep/*.json`, `negctl/negctl.jsonl`;
- the three sets of cake outputs (worker, rebuild verifier, L18);
- L18's `summary.jsonl`, `cert/certify.jsonl`, `summary.log` and `cert/ae_*.cadical.log`.

Every SHA-256 cited in the claims matches the current file. I hashed them all, including the concatenation of the
203 `indep/ae_d*_*.json` files in LC_ALL=C order (`5040baf7…`; the `.err` and `.time` files in that directory are not
part of it).

## 1. What the CNF asserts, and what "radius 1" means

**Radius 1.** LOWERBOUND_PLAN_1115PM defines it: E7-2, target 3; E8-3 calls it "move two points".
- Delete u and v from AE33.
- Keep the other 31 points up to order type.
- Add two arbitrary new points p and q.

B = AE33 − {u, v} keeps the 31 points in file order, with labels 0..30. The task's reading matches the plan.

**Variables** (961 in all):
- X(a,b) = [orient(a,b,p) > 0];
- Y(a,b) = [orient(a,b,q) > 0];
- W(a) = [orient(a,p,q) > 0].

`chi()` in l2enc.cpp sorts each triple with permutation parity. It returns a constant only for three base points, and it aborts on any other repeated or invalid triple. So the literal of "orient(i,j,k) > 0" is right for every triple with a new point. In particular:
- orient(x,p,q) > 0 ⟺ W(x);
- orient(p,y,q) > 0 ⟺ ¬W(y).

**Families.**
- The consistency families are R2X, R2Y, ACX, ACY, RAD, GPA and GPP∪GPQ. Each clause holds for every real configuration in general position.
- The k-gon families are OCTX, OCTY and JK. Each violated clause exhibits a convex 7-gon through p, through q, or through both.

**Convention.** A convex 7-gon is 7 points in convex position, not necessarily empty. That is the ES(7) convention, and it is what OCT and JK produce.

**Not present** (machine-checked by two generators, and confirmed by my reading of the encoder):
- no symmetry breaking, no unit clauses, no cubes, no auxiliary variables;
- no colour or other bounds (none apply to this problem).

p and q are not identified with each other. l2enc emits JK in the order "p first" only (no `--jkq`), which makes the CNF weaker, not unsound.

**Direction.** UNSAT excludes every realization B′ of B's labelled order type, with every p and q such that B′ ∪ {p,q} is in general position and has no convex 7-gon through p or q. Only soundness (every clause valid) is needed. Completeness is neither claimed nor needed.

## 2. Soundness, family by family (own re-derivation)

I agree with VERIFY_AE33R1 §2, LOWERBOUND_RUN_1118 §(2), VB and the rebuild verifier. These are the points I checked myself.

1. **R2.** Let v_x = ε_x(x′ − a′), with ε_x fixed from B.
   - det(v_x, v_y) = ε_xε_y·orient(a,x,y), so the three cone determinants of an emitted triple are positive in every B′.
   - Cramer's rule gives v_{i+1} = λv_i + μv_k with λ, μ > 0. Then sign det(v_x, t − a′) = S_x, so S_i = S_k forces S_{i+1} to the same value. The two clauses state exactly this.
   - l2enc sorts with the comparator det > 0. Every u_x lies in the half-open upper half-plane, and general position rules out parallel vectors, so this is a strict order.
   - l2enc dies if any cone determinant is ≤ 0. indep.py asserts the same, and fam.cpp checks every pair i < j.
2. **AC.** [abt] + [bct] + [cat] = [abc]. With σ = sign[abc] (an order-type constant), at least one term on the left has sign σ.
3. **RAD.** Take the 4×4 matrix with rows (x, y, 1, 1). Laplace expansion along the last column gives [bpq] − [apq] + [abq] − [abp] = 0. Four nonzero terms with sum 0 are not all of one sign.
4. **GP.** [efg][ehi] − [efh][egi] + [efi][egh] = 0 is the 2-D Plücker relation after translating e to the origin. The three products are nonzero.
   - **Order independence.** I computed the three adjacent transpositions, which generate all permutations of
     f, g, h, i:
     - f ↔ g maps (T1, T2, T3) to −(T1, T3, T2);
     - g ↔ h maps (T1, T2, T3) to −(T2, T1, T3);
     - h ↔ i maps (T1, T2, T3) to −(T1, T3, T2).
   - So every permutation maps the signed terms to a **common** sign times a permutation of themselves. Hence the
     forbidden set "all of one sign" does not depend on the order of f, g, h, i.
   - This justifies the different argument orders in indep.py and l2enc.
5. **OCT.** This is the visibility lemma plus the slot lemma of ABSAT8 §3 (i)-(ii), which I re-read.
   - The proof needs Q in **ccw** order. I checked each implementation:
     - l2enc: the DFS starts at the lowest vertex, takes candidates in angular order, and requires left turns, a closing left turn, and a turn at v < π;
     - indep.py: the successor of each vertex is the vertex with all others strictly to its left;
     - fam.cpp: the order comes from the hull.
   - Convex position and ccw order are decided by orientations, so Q is a ccw convex hexagon of B′ too.
6. **JK.** Suppose the p-part is violated.
   - By step 5 with m = 5, Q ∪ {p} is in convex position.
   - p's slot is (Q_i, Q_{i+1}), as follows (the argument missing from the cited texts, §5.3):
     - The hexagon's cyclic order restricted to Q is Q's own ccw order.
     - So p lies between some Q_j and Q_{j+1}, and the left turn at p gives orient(Q_j, Q_{j+1}, p) < 0: p sees e_j.
     - Since e_i is the only visible edge, j = i.
   - So Q1 = (…, Q_i, p, Q_{i+1}, …) is a ccw convex hexagon.
   - The q-part says that q sees exactly one edge of Q1. By step 5 with m = 6, Q1 ∪ {q} is a convex 7-gon through p and q.
   - W signs: lit(x,p,q) = W(x) and lit(p,y,q) = ¬W(y). These are verified on the certified bytes in all six positions (§3.3).
7. **Order type and mirror.**
   - The CNF is *computed* from B's coordinates: ε and the R2 sort order depend on them.
   - The *validity* of every clause depends only on order-type data: the R2 cone signs, σ, [axy], and the convex 5- and 6-subsets with their ccw orders.
   - A mirror realization becomes a realization of B's order type by reflection, which keeps general position and convexity.
8. **Encoder-level facts** (`l2enc.cpp`):
   - `forbid_terms` drops a variable only when every completion of the kept part is forbidden, which is sound. It never fired in these CNFs: all GP and RAD clauses are full length (two checkers).
   - JK drops only duplicates and tautologies; there were 0 tautologies.
   - With `--allow-kgon` absent, the encoder dies on a base with a 7-gon. Its stats give convex7 = 0 for all 203 bases.

## 3. Checks per claim

### 3.1 ae33-r1-203-certified

- **Worker's fresh run** (`ae33/cake/`): 203 `.cake.out` files, each exactly one line equal to `s VERIFIED UNSAT` (`grep -cx` = 1, total lines = 1). The 203 `.cake.err` files hold 0 bytes in all.
- **Rebuild verifier's fresh run** (`verify/cake/`): 203 `.cake.out` files, each exactly that one line.
- **L18's original run:**
  - 269 `cert/*.cake.out` files contain the line;
  - the 269 `summary.jsonl` rows all have `certify_rc` 0 and `verdict_lines` 1, with no duplicates;
  - `summary.log` shows the run finished at 04:58:22, and no "NOT UNSAT" line.
- **Hash chain**, 203/203, no duplicate rows. Each `hashes_203.tsv` row equals:
  - in `cert/certify.jsonl`: `cnf_sha256`, `lrat_sha256` and `lrat_bytes`;
  - in `summary.jsonl`: `cnf_sha256`, clauses, vars = 961, convex7 = 0 and jkq = 0.

  For 7 CNFs, `zstd -dc` of the kept `.cnf.zst` hashes to the tsv value, and the header is `p cnf 961 <tsv clauses>`.
- **Which CNF cake_lpr checked.** `results.jsonl` has `cnf_all4_equal` true for 203/203. cake_lpr ran on the regenerated bytes (`run_pairs.sh`), the same bytes that the family check covers. So the CERTIFIED verdict applies to exactly the CNF that the soundness argument covers.
- **cake_lpr binary:** `c14ff498…`, as claimed.
- **CaDiCaL provenance:** my grep finds `c Version 2.1.3` and `c exit 20` in 203/203 L18 logs. The rebuild verifier re-solved 5 CNFs and got byte-identical LRATs.
  - `results.jsonl` has an empty `cadical_version` field: `run_pairs.sh` greps `CaDiCaL Version`, which the log does not contain.
  - `summary.json`'s 2.1.3 × 203 comes from a separate direct parse of the logs (`summarize.py`).
  - This is a bookkeeping defect only. The validity of the UNSAT verdict rests on cake_lpr alone.
- **Negative controls** (worker and rebuild verifier): a wrong CNF and a truncated proof each give 0 verdict lines. So the grep can fail.
- **Not done by me:** a cake_lpr run.

### 3.2 ae33-r1-regen-exact

- `L18/bin/l2enc_l18`, `L18/bin/l2enc` and the worker's `bin/l2enc_rebuilt` all hash to `af75c610…`.
- `results.jsonl`: `cnf_all4_equal` 203/203 and `stats_equal_summary` 203/203.
- The rebuild verifier regenerated from its own base files with an own build, and obtained the same hashes.
- The stats line is identical only because the relative path in its `points` field is the same; the rebuild verifier noted this. It is immaterial.

### 3.3 ae33-r1-families-exact

**Semantics of the two independent generators** (read, not run):
- `indep.py`: literals come from inversion parity over (base labels, p, q); convex sets from a 4-point brute force, self-tested against the hull definition; ccw order from the successor test.
  - R2 asserts all three cone determinants.
  - AC uses σ·lit over (a,b), (b,c), (c,a).
  - RAD and GP forbid every full assignment that puts all signed terms on one sign.
  - OCT uses deduplicated 4-chains of ccw hexagons.
  - JK uses p in slot i, then q on each edge of Q1, with W literals from the parity rule.
- `fam.cpp`: literals come from cyclic rotation, with (i,p,q) ↦ W(i) and (i,q,p) ↦ ¬W(i); convex sets and ccw orders from a brute-force hull. RAD, GP and JK are as above.
- Each implements the definitions that §2 proves sound, so their equality with the CNF blocks (203/203, 223,165,944 clauses) carries the soundness to the certified bytes.

**Own spot check** (`soundness_lens/spot.py`, `spot.sh`; `spot.json` `all_ok: true`):
- **Rule.** For each pair, I derived from H's ccw order alone the clause that §2 says the real pair violates:
  - JK if both points are on H: Q = H − {u,v}, Q1 = H − {v}, and the edge of Q1 that q sees;
  - OCTX or OCTY otherwise: the hexagon H − {u} or H − {v}.

  I converted it to B labels and DIMACS numbers, then grepped the certified CNF bytes for the exact line: the sorted form for JK, all orders for OCT.

| pair | type | predicted clause | found at line | block lines | W literals (position) |
|---|---|---|---|---|---|
| ae_d14_15 | both | −353 444 −348 −946 −954 −813 | 731,453 | JK 334,188-1,069,379 | q-edge (p,Q_{i+1}): ¬W; neighbour (Q_i,p) before it: ¬W |
| ae_d25_32 | both | −338 −413 −330 954 −878 945 | 981,934 | JK | q-edge (Q_i,p): W; neighbour (p,Q_{i+1}) after it: W |
| ae_d14_17 | both | −338 444 −333 798 945 −855 | 730,316 | JK | neighbour (p,Q_{i+1}) before the q-edge: W |
| ae_d15_25 | both | 331 345 −363 −810 −902 −945 | 843,645 | JK | neighbour (Q_i,p) after the q-edge: ¬W |
| ae_d17_32 | both | 349 −330 −402 896 −867 804 | 844,132 | JK | none (cyclic distance 3) |
| ae_d14_16 | only u on H | −338 444 −330 | 323,354 | OCTX 311,986-323,415 | - |
| ae_d0_14 | only v on H | −787 909 −779 | 334,276 | OCTY 323,165-334,343 | - |

- Each clause was found exactly once, inside its block. Block ranges come from L18's stats, in the order r2x … jk.
- Each CNF's SHA-256 equals `hashes_203.tsv`.
- Under the real configuration (p = u, q = v), every literal is false. I computed this two ways, and they agree:
  - the semantic sign of orient(x,y,t) from AE33's coordinates;
  - the variable definitions read through the literal.
- **Mutant control (can fail):** the same clause with its W literals negated (or, without W, its first literal), in any literal order. It has **0** hits in all 7 CNFs.

**Controls that can fail.** The worker's mutation control flagged exactly the 3 mutated blocks. The rebuild verifier detected 1,152 of 1,152 mutations, rejected 11 malformed files, and found the tiny bases equal to l2enc (40/40 and 45/45).

### 3.4 ae33-inputs-exact

Own `spot.py` and `bases_check.py`:
- `points_7` × 10^17 (Decimal, 80 digits) is integral and equals `L18/e72/ae33.txt`.
- AE33 has 0 collinear triples.
- H in the order 14, 15, 17, 20, 23, 32, 25 has every other vertex strictly to the left of each edge, so it is a ccw convex 7-gon.
- The `ae_` targets are exactly the 203 pairs meeting H: 21 with both points on H, 57 with only u, 125 with only v. The other 325 pairs miss H.
- For all 203 pairs, `bases/ae_d<u>_<v>.txt` is AE33 without lines u and v, and `_pts` is that plus line u plus line v.
- `results/D/calib/alphaevolve_int.txt` has the same labelled order type as `ae33.txt` (all 5,456 triples).
- **Side remark** (not part of any claim): the smallest |orient| over the 5,456 triples is 1.52·10⁻⁸ in the JSON's unit coordinates.
  - Rounding a coordinate to a binary64 double moves it by at most 2.75·10⁻¹⁷ (computed; all coordinates lie in
    [0.34, 0.49]). That changes an orientation by less than 10⁻¹⁶.
  - So AE33's order type is the same whether the JSON numbers are read as decimals or as doubles.
- **Uniqueness of H, deduced without a recount.**
  - Suppose AE33 had a convex 7-subset H2 ≠ H. Pick h ∈ H \ H2 and any w ∉ H2 with w ≠ h.
  - Then {h, w} meets H, so it is one of the 203 pairs, and its base contains H2.
  - But all 203 L18 `summary.jsonl` rows have convex7 = 0 (my cross-check), and the encoder would abort on a base with
    a 7-gon.
  - So H is the only convex 7-subset, and there is no convex 8-subset (one would contain eight 7-subsets).
  - This rests on the convex7 = 0 enumerations of l2enc, indep.py and fam.cpp, not on a recount of my own.
  - The m = 3 count is C(33,3) = 5,456 by general position.
- **Not recomputed by me:** the m = 4, 5, 6 counts (24,758 / 47,945 / 32,055). Two independent implementations agree
  on them (the worker's in Python; the rebuild verifier's in Python and in C++). For the corollary only the convexity
  of H is load-bearing.

### 3.5 ae33-realpair-exact

- The worker's `indep/*.json` (203 files) gives 21 JK / 57 OCTX / 125 OCTY, with exactly 1 violated clause each and 0 in R2, AC, RAD and GP.
  - Each pair's type matches its name.
  - Each file has 1 real 7-gon, through "pq", "p" or "q" as the type says.
- L18's own `summary.jsonl` `eval_real_pair` has the same split.
- The rebuild verifier's evaluator agrees.
- My spot check confirms that the predicted clause is violated in 7 pairs. I did not count all violated clauses myself.
- The record correction (the sentence "exactly one OCTY clause") is right. At 04:00 only pairs with u < 14 had run, and all of those have only v on H.

### 3.6 ae33-r1-soundness-proved

See §2. This is a written argument; the machine checks are listed separately, as the PROVED label requires.
- The random-tuple identity checks are only sanity checks; the identities themselves are classical and proved in §2.
- The citation `logs/indep_selftest.json` holds only a summary sentence. The asserting code is `indep.py identities_selftest`, and the rebuild verifier ran its own.
- For scope, see §5.4.

### 3.7 ae33-r1-corollary

Let S be a 33-point set in general position, and T ⊂ S a 31-point subset with an orientation-preserving (or reversing) bijection φ: AE33 − {u,v} → T.
- **{u,v} misses H** (325 pairs): φ(H) is in convex position, because the 4-point test is a conjunction of sign equalities, which global reversal preserves.
- **{u,v} meets H** (203 pairs): T labelled by φ realizes B's labelled order type (or its mirror). S − T = {p, q}, and S is in general position. By §2 and the CERTIFIED UNSAT verdict, S has a convex 7-gon through p or q.
- **Radius 0:** a 32-point subset of type AE33 − w contains a 31-point subset of type AE33 − {w,t} for any t ≠ w.

**Premises stated:** general position, labelled order type (or mirror), CERTIFIED + EXACT + PROVED inputs. Nothing is rounded up: the claim says "support evidence for ES(7) = 33 only" and "unrefereed".

## 4. Controls: can they fail?

| control | who | can it fail? | outcome |
|---|---|---|---|
| cake_lpr with a wrong CNF, and with a truncated proof | worker, rebuild verifier | yes (would print the verdict line) | 0 verdict lines; the positive twin prints 1 |
| mutated literal / dropped clause / appended clause | worker (3 blocks), rebuild verifier (1,152) | yes | every mutation detected, in its own block |
| tiny bases: own families vs l2enc | worker 40, rebuild verifier 45 | yes | all equal |
| identities on random integers | worker, rebuild verifier | yes | exact |
| real pair: no consistency violation, exactly 1 k-gon violation | worker, rebuild verifier, L18 | yes (an unsound consistency clause could fire) | as claimed |
| SAT direction (8 heptagon-free real configurations) and 8,600 + 6,097 random real configurations | rebuild verifier | yes | 0 violations, 0 oracle mismatches |
| hand-predicted clause present; W-flipped mutant absent | this note | yes (a wrong W convention gives 0 or 1 hits the other way) | 7/7 found once; 0/7 mutants |

## 5. Issues found (none changes a verdict or a label)

1. **Wording error in the draft README §1:** "AE33 is AlphaEvolve's 33-point heptagon-free near miss".
   - AE33 has exactly one convex heptagon (the claim, and my check that H is convex).
   - A heptagon-free 33-point set would refute ES(7) = 33.
   - Suggested: "AlphaEvolve's 33-point near miss for ES(7), with exactly one convex heptagon".
2. **Imprecise sentence:** README §2 item 5 and VERIFY_AE33R1 §2.7 say "every constant of the CNF depends only on B's labelled order type". The R2 clauses depend on coordinates (ε, sort order); what is invariant is each clause's validity.
   - Suggested, as in ABSAT8 §3: "The CNF is computed from B's coordinates, but every clause stays valid for every realization of B's labelled order type (or, after reflection, of its mirror)."
3. **Missing step:** LOWERBOUND_RUN_1118 §(2) item 5 and VERIFY_AE33R1 §2.6 state p's cyclic position in Q1 without an argument. Add the two lines of §2.6 above. The rebuild verifier found the same gap and gave a different argument.
4. **Scope of `ae33-r1-soundness-proved`.** "Soundness of l2enc for k = 7" for an arbitrary B rests on reading `l2enc.cpp`. I read all of it here and it is consistent with the note. The machine bridge (families-exact) covers exactly the 203 CNFs, which is all the corollary uses.
   - Suggested wording: "the families F(B) are sound for every B in general position (PROVED), and `l2enc B 7` = F(B) for the 203 bases (EXACT)."
5. **VERIFY_AE33R1 §2.4:** "± a permutation of themselves" should read "a common sign times a permutation". Only a common sign keeps the forbidden set order-independent, and the computation in §2.4 above shows the sign is common.
6. **Evidence hygiene:**
   - `results.jsonl` `cadical_version` is empty (§3.1);
   - `logs/indep_selftest.json` records the identity test only as a sentence (§3.6).

   Neither is load-bearing.

## 6. Not checked

- No cake_lpr run, no CaDiCaL run, no regeneration of all 203 CNFs: I had no slot. For these I rely on the two fresh runs' outputs, which I inspected, and on the hash chain.
- The convex m-subset counts of AE33 for m = 4, 5, 6 were not recomputed. Uniqueness of H is deduced from the
  convex7 = 0 enumerations (see §3.4).
- Track L's controls C1-C4 and `l2enc --selftest`: not re-run.
- The 66 symmetric bases: not in scope.
- Novelty: not judged.

## 7. Files (`verify/soundness_lens/`) and SHA-256

| file | SHA-256 |
|---|---|
| `spot.py` | `b01f2604f6218f5e6a5946bc3ba95a1d5dea5ee4c51aa50ea864f04eea5b4b92` |
| `spot.sh` | `4017b8c921db5ec5d4d6ad25d8b5c9e0c736421dd936cae5a0e8908887407b93` |
| `bases_check.py` | `7a1c71b5457a124d4b80dd3d8b61aff8b9e578fdf3b075df476bb7afb6820771` |
| `prep.json` (inputs and predicted clauses) | `e3843eb921352a35a5c82a89eec2ba035b3aa3a591fe70d92a9c87d3b505af58` |
| `spot.json` (final, `all_ok: true`) | `f058a3c558b2bd0833b6275d1de1a9943c15c2d664d814b95c71901e32447475` |
| `bases_check.json` | `b459ae3c6e7fdb52e95fb5607c9bf69376646d5c983990e6f065e4c121be3892` |

Per pair, the directory also holds `<name>.pat`, `.mut.pat`, `.hits`, `.mut.hits`, `.sha` and `.head`, all small.

Besides these files, the only thing I wrote was a 203-line name list, briefly, in the session scratchpad under `/tmp`;
I deleted it. No git, no unit.

## 8. Re-run (about 1.5 CPU-seconds, no unit needed)

```
bash /home/jay/research/data/lower-20261121/ae33/verify/soundness_lens/spot.sh
python3 -I /home/jay/research/data/lower-20261121/ae33/verify/soundness_lens/bases_check.py
```
