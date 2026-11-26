# N66N20261113: the internal catalog for (no 6-cap, no 6-cup, no convex octagon) (13 November 2026)

> **Re-solve (25-26 Nov 2026):** the 105 level-15 cube proofs deleted on 24 Nov were re-solved with the proofs kept:
> 105/105 `s VERIFIED UNSAT` (cake_lpr). Each `trim.cnf` equals its receipt hash, and the texts match the Lean hash
> binding of `CubesUnsat105R`. See `receipts/resolve-20261126/README.md`. The 132 level-14 proofs were not re-solved.

> **Proof deletion (24 Nov 2026, owner: "verify every one of these git push and commit, then delete"):** the 237
> kept cube proofs (trim.lrat.zst of the 132 level-14 leaves in p2/c14 and the 105 level-15 leaves in p2/c15 and
> p2/cal15; 96.5 GB) are deleted after this receipt file was committed and pushed: `receipts/n66_cube_proofs_20261124.tsv`.
> Each row: the proof file's SHA-256 and size; the SHA-256 of the decompressed proof, recomputed on 24 Nov and equal
> to cert.json's trim_lrat_sha256; the trim.cnf hash (recomputed, equal to cert.json); the campaign's exact
> cake_lpr line; and the independent fresh re-check that had already accepted it (level 14: U1 76, VB 15 Nov 23, VB 16
> Nov 6, VB 18 Nov 27 cubes, per cubes20261115/VERIFY_N66LE55_FINAL.md; level 15: vfy15). 237 of 237 OK. The
> certified trim.cnf files, cert.json, the cake outputs and the compressed full CNFs stay. After deletion nobody can
> re-run cake_lpr on these proofs without re-solving the cubes; the Lean theorems keep the verdicts as named
> hypotheses, now backed by two recorded cake_lpr acceptances each.


Track A of the 13 November evening session (phase 1, 16:53–19:40 KST, cut off without warning by a usage limit at
about 19:40) and task A2 of phase 2 (from 20:25 KST). Work directory `/home/jay/research/data/n66-20261113/`
(abbreviated W; not in Git). Small tools are copied to `tools/`, certificate data to `data/`. Nothing is committed.
Phase 1: units `nov13c-n66-*`, at most 6 threads, 20 GB until the memory rule of 18:17, then 9 GB (exceptions in
§0). Phase 2: at most 3 threads and 9 GB (anonymous memory + swap, summed over the track's units).

Labels: **PROVED** = written argument (plus exact checks as stated); **CERTIFIED** = a CaDiCaL 2.1.3 LRAT
proof accepted by cake_lpr (`s VERIFIED UNSAT`) for the stated CNF, every clause of which is accounted for as
stated; **COMPUTED** = solver verdict only; **HEURISTIC** = search statistics.

<!-- STATUS -->
- **Update 18 Nov 2026, 04:35 KST (main session): N66 ≤ 55 CERTIFIED by the level-14 cube campaign**
  ([cubes20261115/STATUS_campaign.md](cubes20261115/STATUS_campaign.md), final 04:28:08). All 132 leaves of the 2^6
  split have an accepted certificate (CaDiCaL 2.1.3 LRAT of base F_c + cube units, cake_lpr exact line, acceptance
  rules of cubes20261115/README.md §6); cover complete by the driver (COVER_OK) and by the independent checker
  `budget34/VERIFY307/tools/n66_cover_check.py --deep` (track P307V's own code, claim `p307v-n66-cover` CONFIRMED by VS):
  0 of 16,384 assignments of the 14 split states uncovered. U1's four independent checks per cube: U1 76 + VB 23 (15
  Nov) + VB 6 (16 Nov) + VB 25 of today's 27 at 04:28 (VERIFY_N66CUBES_1118.md, rest in progress). Same trust base as
  N66 ≤ 56 (written model §2 and the checks named there); not Lean-checked; unrefereed. Claim
  `n66-le55-cubes-1118`: **CONFIRMED by VS (04:33, own cover code) and by VN (08:31, own code: exact partition of the
  split, all 132 cubes four-checked, every cert.cnf = F_c + its cube units byte for byte, fresh cake_lpr on hooooo and one
  random cube)**; verify files cubes20261115/VERIFY_N66LE55_FINAL.md and VERIFY_N66LE55_FINAL_VN.md. Use: with the budget-35 slice (20,15) closed, ES(8) ≤ 307
  (ROADMAP20261115/ROUTE307_1116.md route A).
- **Update 23:43 KST (driver): N66 ≤ 56 CERTIFIED** (level 13, `W/p2/b13g/it1`; §9 and n66_certified.json). The items below were written at 21:55.
**STATUS (updated 21:55 KST, phase 2; later results are added by the driver as lines above this one and in §9).**
- **N66 ≤ 57: CERTIFIED** (21:43, §7.4): every set of the class has at least 13 holes among the 70 states.
  Certificate: the trimmed sub-CNF "at most 12 holes" of the monolithic CNF, 206,705 clauses (197,647 mono66
  clauses, 7,913 row clauses, 1,141 counter clauses, 2 units), SHA-256
  `80b55b0c2c2ef445f485901e69fda3fdbb994fc1d882b5828d9227a85a695ee7`; trimmed CaDiCaL 2.1.3 LRAT 2,992,431,389 bytes,
  SHA-256 `3971e63f869224cca0e39d3b40e5070cfd737a2c13fdab8abb68bd6a105a5978`; cake_lpr `s VERIFIED UNSAT`; the 7,913
  rows re-justified from scratch (417/417 templates, 204/204 cores cake_lpr-certified; `final_verify66.py` 0 bad;
  link re-check ALL_OK); `p2_verify.py` ALL_OK. Data `data/cert57/`. Use (LO33N20261113, Lemma S): with N5 ≤ 65,
  N66 ≤ 57 gives ES(8) ≤ 309 **once slice 20 (pair (64, 57)) is closed** — that tree is not this track's; N66 ≤ 56
  would give ES(8) ≤ 309 with the trees that exist already.
- **N66 ≤ 58: CERTIFIED** (20:56, §7.2; data `data/cert58/`), N66 ≤ 59: CERTIFIED (phase 1, §4.1). Lower bound
  N66 ≥ 50 (ETV set, §5).
- Trust base of the phase-2 certificates: the written soundness arguments of §2 (rows) and §6.3 (monolithic
  families), the exact clause-membership checks (`p2_verify.py`, `final_verify66.py`, `p2_recheck_rows.py`) and
  cake_lpr. Not yet re-verified by an independent track. Row hints are used (no row-free certificate; §8).
- Level 13 (N66 ≤ 56; it would make slice 20 unnecessary): not decided; three batch runs since 21:44–21:50 (§7.5).
  The driver (§8) certifies further levels by itself until 06:00 KST and records them in
  `/home/jay/research/data/phase2-20261113/n66_certified.json`, in §9 and as a line at the top of this block.
<!-- /STATUS -->

## 1. Question

N66 = N(cap ≤ 5, cup ≤ 5) is the largest size of a planar point set with distinct x-coordinates, in general
position, with no 6-cap, no 6-cup and no convex octagon. Cup–cap bound: N66 ≤ C(8,4) = 70. Erdős–Tuza–Valtr
value for (a, b, n) = (6, 6, 8): C(6,2) + C(6,3) + C(6,4) = 50 (their construction; exact set built here, §5).
Before this record: N66 ≤ 64 (cycle rows only, COMPUTED at 16:43 in this session).
Use (THEORY310N20261113 Lemma A): n_R ≤ N5 + N66 with N5 ≤ 65 (ETV5N20261113), so N66 ≤ 55 would give
n_R ≤ 120 and ES(8) ≤ 309 without any residual row. Each further hole is one more point off.

## 2. Model and soundness (PROVED: written arguments; checks as stated)

This section re-derives ETV5N20261113 §2 for labels in [1..4] × [1..4] and states what changes.
Throughout, S is a finite planar point set in general position with distinct x-coordinates, with no 6-cap,
no 6-cup and no convex octagon; |S| ≥ 2. Points are indexed by increasing x. "Cup"/"cap" as in math.md §2.1
(positive/negative determinant on increasing triples).

**2.1 Labels.** For u < v, E₋(u,v), E₊(u,v) are the largest numbers of points of a cap / cup of S ending with
the pair (u,v). No 6-cap and no 6-cup give d(u,v) = (E₋ − 1, E₊ − 1) ∈ [1..4] × [1..4].
*Change:* the box is 4 × 4 instead of 3 × 6; the cup ceiling now comes from the hypothesis "no 6-cup", not
from the octagon.

**2.2 Growth with ceilings** (math.md §2.1; the proof extends an attaining chain and does not use the box):
for u < v < w, a cap (u,v,w) gives d₁(v,w) > d₁(u,v), a cup gives d₂(v,w) > d₂(u,v). With the ceilings:
d₁(u,v) = 4 forces every later w to make a cup with (u,v) (else a 6-cap), and d₂(u,v) = 4 forces a cap
(else a 6-cup). In the CNF: cap_ge(·,·,5) and cup_ge(·,·,5) are the constant false.

**2.3 States.** I(v) is the down-set of [1..4]² generated by the incoming labels {d(u,v) : u < v}: a Young
diagram in the 4 × 4 box, encoded by column heights 4 ≥ f₁ ≥ f₂ ≥ f₃ ≥ f₄ ≥ 0 (column a = cap coordinate a).
There are C(8,4) = 70 states. State separation (math.md Lemma 2.1, same proof): d(u,v) ∈ I(v) \ I(u) for
u < v; so the owner map v ↦ I(v) is injective and |S| = 70 − (number of holes).

**2.4 Fixed states.** The first point has I = ∅ (state 0 = (0,0,0,0)); the second has the single incoming label
(1,1), so its state is (1,0,0,0) (state 1). Both are occupied whenever |S| ≥ 2. (`etv_common.FIXED_OCC` is
generic in A; `final_verify66.py` asserts the two profiles.)

**2.5 Lemma R (rank attainment)** holds verbatim: d₂(u,v) ≤ cupH(u) + 1 and d₁(u,v) ≤ capH(u) + 1, with
cupH(u) = f₁(u) and capH(u) = #{a : f_a(u) ≥ 1}. The proof (ETV5N §2: the predecessor t of u on an attaining
chain gives d₂(t,u) ≥ d₂(u,v) − 1 and the cell (1, d₂(t,u)) ∈ I(u); the same for caps) does not use the box.
Refined domain: D′(s→t) = {(a,b) ∈ I(t) \ I(s) : a ≤ capH(s) + 1, b ≤ cupH(s) + 1}.

**2.6 Cycle rows** (math.md Lemma 2.2, unchanged): a list of k distinct states that passes the six-order
bounding-box test on every triple in list order has its owners in convex position in that cyclic order, so at
most 7 are occupied: demand k − 7. The 7 is tied to "octagon", not to the box. Triple table for the 4 × 4
box: 29,436 forced ordered triples, none with both orientations forced, cyclically invariant.

**2.7 Coupled rows.** For a support T of distinct states, all assumed occupied with owners v_i, the CNF of
`coupled5.py` (run with ETV_A=4, ETV_B=4) has the atoms before(i,j), cap_ge(i,j,k), cup_ge(i,j,k) (k = 2..4),
orientation(i,j,k), convex_four(i,j,k,l), and the nine clause families of ETV5N §2. Each holds for the owners
of a real set of the class:
1. threshold monotonicity; 2. order transitivity; 4. signotope packets; 5. convex_four definition;
   6. complete no-octagon (for every 8 owners some 4 are not in convex position): unchanged, they do not
   mention the box.
3. growth: before(a,b) ∧ before(b,c) ∧ (a,b,c) negative ∧ cap_ge(a,b,k) → cap_ge(b,c,k+1) with
   cap_ge(·,·,5) false, and the cup version with cup_ge(·,·,5) false: §2.2. (`MAXK = {cap: A, cup: B}` in
   `coupled5.py`: no literal 3 or 6.)
7. empty, 8. domain, 9. positive: state separation + Lemma R + the six-order test, as before, with the 4 × 4
   tables.
"No 6-cap / no 6-cup among owners" is not a separate family: five owners in a 6-cap would need four growth
steps above 1, exceeding 4. In this class a convex octagon is exactly a 5-cap and a 5-cup on common endpoints
(k + l − 2 = 8 with k, l ≤ 5); the complete no-octagon family remains valid as it is.
So if the CNF is unsatisfiable, the states of T are never all occupied: **demand-one row on T**.

**2.8 Mirror lemma (new; PROVED).** Let ρ(x,y) = (x,−y). ρ keeps x-coordinates, general position and the
x-order, negates every determinant, hence swaps caps and cups and maps convex polygons to convex polygons. So
ρS is in the class, E₋ and E₊ are exchanged, d_{ρS}(u,v) = (d₂(u,v), d₁(u,v)), and the state of every point
is transposed: I_{ρS}(v) = I_S(v)ᵀ. Let τ be the transposition of states (conjugate partition; 16 of the 70
states are fixed; τ fixes both fixed states). Then Occ(ρS) = τ Occ(S). If (T, d) is a valid row (every set of
the class has at least d holes in T), then for every S: |τT \ Occ(S)| = |T \ τOcc(S)| = |T \ Occ(ρS)| ≥ d.
**So (τT, d) is a valid row.** ∎
Checks: τ transposes cells and refined domains and exchanges capH and cupH; TT[τa,τb,τc] = TT[a,c,b]
(`sym66.py`); all 50 baseline cycle rows have a valid mirror cycle row; and at the CNF level the renaming
cap_ge ↔ cup_ge, orientation ↦ ¬orientation maps `coupled5.CNF(S)` onto `coupled5.CNF(τS)` clause for clause
(`check_bigtemplate.py`, 6/6 supports), so a mirrored coupled row is also refuted by the renamed proof.
Use: the row set is kept closed under τ; a row known only as a mirror image is justified as "mirror of a
justified row" (kind `mirror` in the justification files, re-checked by `final_verify66.py` with τ recomputed
from the profiles).

**2.9 Transport (PROVED; ETV5N §2, unchanged) and the large-core template format (new).** A template is a
CNF that is unsatisfiable and consists of (i) static clauses, which depend only on the number n of owners,
and (ii) state-dependent clauses identified by their tags (tests). For an injective σ that passes the tests,
σ's full CNF contains (or implies, for domain tests under an empty domain) every clause of the template, so it
is unsatisfiable and image(σ) is a demand-one row. In ETV5N the static part was the whole static block. Here
cores have up to 29 states, where the complete no-octagon family (C(n,8) clauses of 70 literals) is too large;
the template is CNF(S; octs, tests) = all static clauses except the no-octagon family
(`coupled5.CNF(S, octagon=False)`, tag None) + the no-octagon clauses of an explicit list `octs` of 8-subsets
+ the kept tests (`bigcore.py`). This is a sub-CNF of `coupled5.CNF(S)` (checked: `check_bigtemplate.py`,
subset 6/6 and equality 6/6 when all 8-subsets are listed), and each of its static clauses is state
independent, so the transport argument applies verbatim. A core used directly is certified from
CNF(S; octs, all tests). The lists `octs` are short (3–29 in a test): these refutations use few octagon
clauses.

**2.10 No block rows (COMPUTED, negative).** For K ⊆ cap coordinates and J ⊆ cup coordinates, a family whose
pairwise refined domains use only K × J has owners with no (|K|+2)-cap and no (|J|+2)-cup, hence at most
C(|K|+|J|, |K|) owners (cup–cap; Baek's 22 and N5 ≤ 65 are weaker here because of the cup ceiling). Exact
maximum-clique search over all (K, J) ≠ (full, full): the largest family always has exactly C(|K|+|J|, |K|)
states (`blocks66.py`). No block row exists; the block branch was removed from the loop and the checkers.

**2.11 Code paths checked for hard-coded 3, 6, 84.** `etv_common.py`, `coupled5.py`, `engine.py`,
`transport5.py`, `geom.py`, `cyclists.py`, `pbcnf5.py`, `pb_lrat.py`, `cube_lrat.py`, `rowsio.py`: generic in
A, B, N (the constants 7 and 8 in the cycle rows and the 8 in the no-octagon family are tied to the octagon).
Hard-coded and replaced: `loop12.py` block rows (`>= 23`, `- 22`) → removed (`loop66*.py`);
`template_cert2.py` / `final_verify.py` block branch (22, 23) → removed (`template_cert66.py`,
`final_verify66.py`, which assert A = B = 4, N = 70 and the two fixed profiles); `cubecegar.py` (branch states
22, 37, 45, 53, 67, budget 18, 84-state paths) → not used. `realcheck.py`, `soundness_test2.py`: generic
(`realcheck66.py` adds the ETV set).

## 3. The row loop (phase 1; COMPUTED discovery, rows justified separately)

The phase-1 loop (`loop66.py` → `loop66b.py` → `loop66c.py` → `loop66d.py`) alternates (i) a hitting-set step
(CP-SAT, later CaDiCaL on the PB CNF) that finds hole vectors with the current number of holes violating no known
row, and (ii) refuters that turn the occupied set of such a vector into new demand-one rows: probes and the
propagating transport enumerator (`transport66.py`, templates `templates.jsonl`), and from 17:30 the full-support
oracle (`dp66c.py` / `lazy66.py`) whose minimal cores (13–29 states) become large-core templates
(`bigtemplates.jsonl`, §2.9). Every row is a claim "no set of the class occupies all states of T"; it is only used
in a certificate after its justification (cycle order, cake_lpr-certified core, cake_lpr-certified template +
transport map, or mirror of one of these) has been re-checked by `final_verify66.py`. Row store at 18:32
(`W/mono/rows_1832.json`, τ-closed): 15,648 demand-one rows, supports of 8–29 states (most often 13: 5,767;
14: 3,007; 18: 2,050). The loop was stopped by the memory guard at 18:17 (§0) and not restarted.

## 4. Certificates of phase 1 (CERTIFIED)

Both are "PB CNF over justified rows" (`pb_lrat.py`): the clause ∨_{s∈T} ¬sel_s per demand-one row (cycle rows
with demand k − 7 as cardinality constraints; encoder consistency test `pb_consistency.py` on 200 random instances) plus "at most B holes among the
68 non-fixed states"; no geometry beyond the rows. Pipeline `final66.sh` (all rows → CaDiCaL LRAT → used rows →
justification → the PB CNF again over exactly the used rows → cake_lpr → `final_verify66.py`).

**4.1 N66 ≤ 59** (at least 11 holes; 18:11; `data/cert59/`): PB CNF "≤ 10 holes" over the 3,052-row subset,
SHA-256 `920489253e49d2b8527ff32771b08afa05cc2956f149d3c20711657b5b4f4ab0` (4,262 clauses, 650 variables),
CaDiCaL 2.1.3 LRAT 162,152,215 bytes, SHA-256 `9272dfbc3364eff199dd1713e054d1879931e6dab2f0b301a0bb4e79b472a244`,
cake_lpr `s VERIFIED UNSAT`; rows: 51 cycle, 1,447 transported (281/281 templates certified), 67 cores (68/68),
1,487 mirror; `final_verify66.py`: 0 bad, row multiset equal to the subset file.

**4.2 N66 ≤ 60** (at least 10 holes; 17:37; `data/cert60/`): PB CNF "≤ 9 holes" over 2,100 rows, SHA-256
`dcd64c5a4b899526dc56c13d0501922633a75c8f020263670ef1ef9956b28c62`, LRAT SHA-256
`c7f8c381668e1d640bbc06832e1f2de6811c5fad33b025371abaa005f694df47`, cake_lpr `s VERIFIED UNSAT`.

The PB route stops at N66 ≤ 59: "≤ 11 holes" stayed satisfiable over every row set found (loop rounds at 18:16 still
returned 11-hole vectors over 15,648 rows), which is why the monolithic CNF (§6) was built.

## 5. The ETV set and the phase-1 controls (COMPUTED)

- Exact ETV 50-point set for (a, b, n) = (6, 6, 8) (`etvcon.py`, `etv50.py`): in the class; its 20 holes are
  exactly the states with f₁ = 4 and f₄ ≥ 1. So N66 ≥ 50 and the gap is 50 ≤ N66 ≤ (current bound).
- Clause soundness of the coupled CNF (`soundness_test2.py` as `sound2_66.out`): 459 real sets (up to 26 points),
  1,836 CNFs, 144,951,058 clause evaluations, 0 violations, all 70 states seen as owners.
- Rows against real sets (`realcheck66.py`, `realcheck_1818.out`): 14,914 rows, 14,618 ETV-derived and 7,307 greedy
  sets (largest 50 points), 0 violations.
- Big-template format = sub-CNF of the coupled CNF, and the mirror renaming maps CNF(S) onto CNF(τS):
  6/6 supports each (`check_bigtemplate.out`).
- Greedy fill from the ETV set in the monotone model: none of the 20 holes can be added (17:59–18:02).
- The monolithic CNF: §6.4.

## 6. The monolithic CNF (`mono66.py`) and its soundness (PROVED; controls COMPUTED)

**6.1 Atoms.** All 70 states are *potential owners*; owner s is "the point of S whose state is s", if there is one
(the owner map is injective, §2.3, so every point of S is the owner of exactly one state). The atoms are those of
`coupled5.CNF(W, static=False)` for W = all 70 states (before(i,j); cap_ge(i,j,k), cup_ge(i,j,k) for k = 2..4;
orientation(i,j,k); unused convex_four variables are allocated but occur in no clause), plus
- the **selector** sel_s = "state s is occupied" (70 variables, numbered right after the coupled5 variables),
- **chain atoms** C_k(a,b,c), U_k(a,b,c) (k = 3, 4, 5) for every ordered triple of distinct states whose three
  refined domains D′(a→b), D′(b→c), D′(a→c) are nonempty ("can"), meaning "a k-cap (k-cup) of S starts at owner a
  and ends with the owners (b, c)",
- **end atoms** CE(p,q), UE(p,q) = "some 5-cap (5-cup) of S goes from owner p to owner q".

**6.2 Clause families** (`mono66.generate`; every geometric clause carries the guard literals ¬sel_o of all owners
o it mentions, so it constrains only configurations in which those owners exist):
- F1 (pairs, triples): the state-dependent clauses of coupled5 for the 70 states — *empty* (D′(s_u→s_v) = ∅ ⇒
  ¬before(u,v)), *domain* ((a,b) ∉ D′(s_u→s_v) ⇒ before(u,v) → label(u,v) ≠ (a,b)), *positive* (six-order test
  TT ⇒ orientation forced).
- F2 (pairs): threshold monotonicity cap_ge(i,j,k+1) → cap_ge(i,j,k), the same for cup_ge.
- F3 (triples, can(a,b) ∧ can(b,c)): transitivity before(a,b) ∧ before(b,c) → before(a,c).
- F4 (triples, all three domains nonempty): growth with ceilings: before(a,b) ∧ before(b,c) ∧ (a,b,c) cap ∧
  cap_ge(a,b,k) → cap_ge(b,c,k+1) for k = 1..4, where cap_ge(·,·,1) is true and cap_ge(·,·,5) is false; the cup
  version with orientation positive.
- F5 (triples): chain start: before(a,b) ∧ before(b,c) ∧ (a,b,c) cap → C₃(a,b,c); cup → U₃(a,b,c).
- F6 (quadruples): chain step: C_k(a,b,c) ∧ before(c,d) ∧ (b,c,d) cap → C_{k+1}(a,c,d) for k = 3, 4; the same
  for U with cups.
- F7: C₅(p,u,q) → CE(p,q) and U₅(p,u,q) → UE(p,q) (guards p,u,q); **¬CE(p,q) ∨ ¬UE(p,q)** (guards p,q).
- F8 (quadruples, all six domains nonempty): signotope packets: before(a,b) ∧ before(b,c) ∧ before(c,d) → the
  orientations of (abc, abd, acd, bcd) do not follow one of the 8 sign patterns with two or more sign changes.
- Tail (no geometry): the units sel₀, sel₁ (§2.4); optional row clauses ∨_{s∈T} ¬sel_s (§6.5); "at most L of the
  68 hole literals ¬sel_s, s ∉ {0, 1}, are true" (pysat sequential counter in every certificate; `lazymono.py` uses
  a totalizer during the search only).
Transitivity, growth, chain and signotope clauses are written only for orders that the refined domains allow; the
others would be implied (the *empty* units and transitivity falsify a premise), and omitting clauses can never affect
soundness. The complete instance has 39,017,853 geometric clauses (2.8 GB); F6 and F8 are almost all of it.

**6.3 Soundness.** Let S be a set of the class (general position, distinct x-coordinates, no 6-cap, no 6-cup, no
convex octagon) with |S| ≥ 2. Its *canonical assignment*: sel_s = [s is occupied]; for occupied owners, before =
the x-order, cap_ge/cup_ge = the thresholds of the labels d = (E₋ − 1, E₊ − 1), orientation = the sign of the
determinant in index order; C_k(a,b,c) = [a, b, c occupied, x(a) < x(b) < x(c), and some k-cap of S starts at a
and ends with (b, c)], U_k likewise with cups, CE(p,q) = [some 5-cap of S goes from p to q], UE likewise; every other
atom false. **Every clause of F1–F8 is true under it.** A clause with a guard of an unoccupied state is true by
that guard; otherwise all its owners exist and:
F1: state separation, Lemma R and the six-order test, as for the coupled CNF (§2.3, §2.5, §2.6, §2.7 items 7–9).
F2: thresholds of one number. F3: the x-order is a linear order. F4: §2.2 (appending c to a largest cap ending with
(a,b) is a cap ending with (b,c); no 6-cap / no 6-cup cap the labels at 4). F5: a cap triple in x-order is a 3-cap.
F6: a chain in x-order is a cap iff its consecutive triples are caps, so a k-cap a…b,c extended by d with (b,c,d) a
cap is a (k+1)-cap a…c,d. F7: the first part by definition; for the exclusion, a 5-cap and a 5-cup with the same
first point p and last point q have their three inner points strictly above and strictly below the segment pq
respectively, and the eight points are in convex position (a k-cap and an l-cup with common endpoints form a convex
(k+l−2)-gon): a convex octagon, which S does not have. F8: for four points in general position with x(a) < x(b) <
x(c) < x(d) the orientation sequence (abc, abd, acd, bcd) changes sign at most once (the signotope property of point
sets). Tail: sel₀, sel₁ by §2.4; a valid row contains a hole of every set of the class; the hole literals true
under the assignment are exactly the h holes of S, and the sequential counter "at most L" has an extension to its
auxiliary variables iff h ≤ L.
Consequently, if the clause set (F1–F8 + tail with budget L) — or **any subset of it** — is unsatisfiable, then
every set of the class with at least two points has at least L + 1 holes, i.e. |S| = 70 − (holes) ≤ 69 − L:
**N66 ≤ 69 − L** (sets with at most one point are irrelevant for L ≤ 67). The subset clause is what makes the lazy
engine and proof trimming harmless: a sub-CNF of a set of clauses that every real set satisfies is still satisfied
by every real set.

**6.4 Controls (COMPUTED).** `mono_check.py` builds the canonical assignment of real sets with exact integer
arithmetic and evaluates the complete clause stream: the exact ETV 50-point set and its two reflections: 0
violations among 12,396,220 / 12,396,220 / 7,898,616 clauses with all guards true; with the selectors fixed to the
real occupancy, the tail is satisfiable at budget 20 (= the number of holes) and unsatisfiable at budget 19
(17:45). In total 26 real sets (ETV, reflections, ETV subsets of 38–49 points, greedy random sets of 18–23 points):
113,074,249 clause evaluations, 0 violations (`mono_check.out`, 18:38). Every certificate CNF of §7 is re-checked
clause by clause against the stream of `mono66.generate` (`p2_verify.py`, exact literal tuples; phase 1:
`lazymono_verify.py`, hashed tuples).

**6.5 Row hints and their justification.** Rows enter as clauses ∨_{s∈T} ¬sel_s. They are not consequences that the
certificate checks; each row is a separate claim with its own certificate (§2.6–2.9, §3). The lazy runs use all
15,648 rows of `rows_1832.json` as hints, but a certificate only depends on the rows its proof uses: `p2_lrat_trim`
keeps exactly the original clauses in the derivation cone of the empty clause (`trim.cnf`) and renumbers the proof
(`trim.lrat`); cake_lpr checks `trim.lrat` against `trim.cnf`, so an error in the trimming could only make the check
fail. The rows of `trim.cnf` are then justified from scratch by `p2_template_cert66.py` (`template_cert66.py` with
an explicit cake_lpr heap: fresh CaDiCaL + cake_lpr certificates for every template and core used) and re-checked
by `final_verify66.py` (cycle orders, transport maps against the template tests, mirror images, row multiset equal
to the used-row file). Finally `p2_verify.py` classifies every clause of `trim.cnf`: mono66 clause (exact member of
the regenerated stream), fixed unit, justified row, or clause of the re-encoded sequential counter.
Trust base of a phase-2 certificate: the written arguments of §2 (coupled CNF, for the rows) and §6.3 (monolithic
families), the clause-membership checks of `p2_verify.py` and `final_verify66.py`, and cake_lpr.

**6.6 Why not monolithic in one piece.** The complete instance needs about 11 GB in CaDiCaL (17:40–18:32, §0), above
the 9 GB track budget. `lazymono.py` keeps F1–F5, F7 and the tail eagerly (1.49 M clauses for 70 states) and adds the
12 clauses of F6 + F8 of a (quadruple, chronological order) only after a model violates one of them; a model with
no violated quadruple would be a model of the complete CNF.

**6.7 Optional symmetry breaking under the mirror map (PROVED; used only by the runs marked `--sb`).** Let
P = ((s₁,t₁), …, (s_m,t_m)) be pairs with t_j = τ(s_j) ≠ s_j from distinct τ-orbits (τ = transposition of states,
§2.8), and let LEX(x) say: at the first j with x_{s_j} ≠ x_{t_j}, x_{s_j} = 0 (hole) and x_{t_j} = 1 (occupied).
*Claim:* if some set S of the class has at most L holes, then some set of the class with at most L holes has an
occupancy vector satisfying LEX. *Proof:* x = occupancy of S, y = occupancy of the mirror image ρS; by §2.8
Occ(ρS) = τ Occ(S), so y = x∘τ, and ρS is in the class with the same number of holes. If x and y agree on all pairs,
both satisfy LEX. Otherwise the first index j where x_{s_j} ≠ x_{t_j} is also the first index where y_{s_j} ≠ y_{t_j},
and y_{s_j} = x_{t_j}, y_{t_j} = x_{s_j} (τ is an involution): exactly one of x, y satisfies LEX. ∎
The encoding (`p2_sb.py`; auxiliary e_j = "the first j pairs agree", numbered after the counter: clauses
[¬e_{j−1}] ¬x_{s_j} x_{t_j}, [¬e_{j−1}] ¬x_{s_j} ¬x_{t_j} e_j, [¬e_{j−1}] x_{s_j} x_{t_j} e_j) is satisfied by every x
with LEX(x) once e_j takes its meaning. So adding it to F1–F8 + tail keeps a model whenever some set has at most
L holes, and §6.3's conclusion holds for CNFs that contain these clauses. The pair list (27 pairs, one per
non-trivial orbit; the 16 τ-fixed states are self-conjugate; order by decreasing hole frequency of the phase-1
vectors, first pair (32, 37)) is stored in `layout.json`; `p2_verify.py` checks every pair against τ recomputed from
the profiles and compares the clauses exactly. Controls (COMPUTED): `p2_sb.py` self-test (20,000 random selections:
exactly one of x, x∘τ satisfies LEX unless they agree on the pairs; 3,000 random selections: the CNF encoding agrees
with LEX); `p2_verify.py` classified the 79 clauses of the encoding (27 + 2·26) and, as a negative control, rejected
2 deliberately altered clauses (one counter-side, one mono66) as unclassified.

## 7. Phase 2: certification of levels 11 and 12, search for level 13 (from 20:25 KST)

*Naming.* In phase 2 (as in the task) **level L** means budget L: "at most L holes" is UNSAT, i.e. every set of the
class has at least L + 1 holes and N66 ≤ 69 − L. (The phase-1 log in §0 counts holes instead: its "level 11" is
N66 ≤ 59, which is level 10 here.)

**7.1 Tools** (W, copied to `tools/`): `p2_write.py` (writes the certificate CNF of a lazymono state: eager clauses,
the 12 clauses of every activated quadruple, units, rows, sequential counter; layout file with the clause ranges),
`p2_lrat_trim.cpp` (backward pass over the LRAT text with a bitset of needed clause ids, forward pass writing
`trim.cnf` / `trim.lrat` with compact ids), `p2_cake.py` + `p2_mem.py` (cake_lpr with the smallest sufficient heap
inside the memory budget), `p2_used_rows.py`, `p2_template_cert66.py`, `p2_verify.py`, `p2_cert.sh` (the pipeline),
`p2_lazymono.py` (lazymono with warm start from earlier activated sets, optional mirror closure of the activated set,
a log line and a saved state after every iteration, one budget per run), `p2_batch.py` (the same lazy loop with a fresh
CaDiCaL 2.1.3 run with LRAT per iteration, so that the last run is the certificate run; optional `--sb`), `p2_sb.py`
(§6.7), `p2_recheck_rows.py` (link re-check of the row certificates, §7.2), `p2_driver.py` (§8).
Tests (20:27–20:34): the trimmer on a pigeonhole instance padded with 3,000 irrelevant clauses and on a random
3-SAT instance (block sizes from 300 B to 64 MB give identical output; cake_lpr accepts every trimmed proof);
the whole pipeline on 32 states (the 30 most core-frequent states and the two fixed ones): budget 2 without rows
(402 mono66 + 112 counter + 2 unit clauses) and with rows (21 used rows: 13 transported, 6 mirror, 2 cycle; 11
templates re-certified): ALL_OK in both.

**7.2 Level 11: N66 ≤ 58.** Input: `W/lm/full_L11.json` (phase-1 lazymono state at 18:58: 70 states, 322,818
activated quadruples, hints `W/mono/rows_1832.json`).
- `p2_write.py` → `W/p2/c11/cert.cnf`: 1,647,653 variables, 5,380,347 clauses (eager 1,489,581; quadruple
  3,873,816; units 2; rows 15,648; counter 1,300), SHA-256
  `82fa7697df9aaf04091af2c81cff38a80fdf70f615e0eed72821167614c014b2`.
- CaDiCaL 2.1.3 `--lrat=true --binary=false` (default options): **UNSAT in 455 s** (1.71 GB), LRAT 2,408,231,441 bytes.
- `p2_lrat_trim`: 23,594,446 proof lines, 13,650,465 additions, 2,947,884 of them in the cone of the empty clause;
  92,446 of the 5,380,347 original clauses used: 51,270 eager, 34,458 quadruple, 2 units, **5,738 rows**, 978
  counter clauses. `trim.cnf` 5,697,605 bytes, `trim.lrat` 976,854,118 bytes.
- cake_lpr (heap 2,000 MB) on `trim.cnf` / `trim.lrat`: **`s VERIFIED UNSAT`** (22.7 s).
  The untrimmed proof (SHA-256 `6c3889553a55b4ffbcb9cd3ec5569bf574bd06b0bc9c1d5f4a0a53d4419040a0`) was deleted after
  this check; the trimmed one is kept in W (`p2/c11/trim.lrat`, not in Git: 977 MB).
- Rows (20:39–20:56, `p2_template_cert66.py`, 989 s): the 5,738 used rows are 2,691 transported (415 templates, each
  re-certified: CaDiCaL LRAT + cake_lpr), 2,793 mirror images, 203 cores (205 core CNFs certified, 2 of them as
  preimages of mirror rows) and 51 cycle rows; `final_verify66.py`: `bad 0`, `rows_match true`.
- `p2_verify.py` (34 s): `trim.cnf` has 92,446 distinct clauses: 85,728 found exactly in the stream of
  `mono66.generate` (39,017,853 clauses), 5,738 justified rows, 978 clauses of the re-encoded sequential counter
  (budget 11), 2 fixed units; 0 unclassified; variables ≤ header (1,647,653). **ALL_OK.**
- Link re-check (21:22–21:25, `p2_recheck_rows.py`, 163 s): the static clause files that the template and core CNFs
  are built from (`static/static*_A4_B4_<n>.txt`, n = 9…29) are byte-identical to a fresh generation by
  `coupled5.CNF` without the cache, and the SHA-256 of every certified CNF (415 templates, 205 cores) equals the hash
  of the CNF regenerated from its definition (core, tests, octagon list): **ALL_OK** (`data/cert58/recheck.json`).
  So the CNFs that cake_lpr checked are exactly the ones the justification refers to.
**Result: N66 ≤ 58 is CERTIFIED** (labels as in the header: written soundness §2, §6.3; cake_lpr for the main proof
and for every template and core). `data/cert58/`: `trim.cnf.gz`, `cert.json`, `verify.json`, `layout_summary.json`,
`used_rows.json`, the justification (`justification.json.gz`, `template_certs.jsonl.gz`, `core_certs.jsonl.gz`,
`fv66.out`), logs, `SHA256SUMS`. Re-check without a solver: `p2_verify.py p2/c11 p2/c11/tcert`; with the proof:
`cake_lpr --CML_HEAP_SIZE=2000 trim.cnf trim.lrat` (W/p2/c11).

**7.3 Level 12 (N66 ≤ 57): search** (all 70 states, budget 12, all 15,648 row hints; a portfolio, the first
UNSAT wins; **won by `s12c` at 21:24**, §7.4):
- `s12a` (20:30): `p2_lazymono.py` (pysat CaDiCaL 1.9.5, incremental), warm start = the 322,818 quadruples of
  `full_L11.json`, seed 1. Iterations 1–3 found 12-hole selections violating 27k / 18k / 15k quadruples in 31 / 49 /
  132 s; iteration 4 has been running since 20:34.
- `s12b` (20:30–20:51): the same engine with the mirror-closed warm start (554,371 quadruples); its first solve ran
  about 16 CPU-minutes without an answer; stopped and replaced by the batch engine (parked in the driver).
- `s12c` (20:51): `p2_batch.py` — the same CNF family solved by fresh CaDiCaL 2.1.3 runs with LRAT (the solver that
  refuted level 11 in 455 s), so that the final UNSAT run is already the certificate run; warm start = the
  mirror-closed state of `s12a` at 20:51 (641,229 quadruples; CNF 9.7 M clauses).
- `s12d1` (21:01): `p2_batch.py` with the union of the four level-11 activated sets (941,372 quadruples), seed 4.
  (A first launch `s12d` at 21:01:26 shared the iteration directory with `s12c` because of a driver bug; it was
  stopped after 10 s, before its CaDiCaL started and before it replaced any file of `s12c`; its partial temporary
  file was deleted; `s12c` was not affected. Fixed: one directory per slot and launch.)
- `s12d1` was stopped at 21:15 (frozen 10 min during a test, about 3 CPU-minutes of solving; parked).
- `s12e` (21:17): `p2_batch.py --sb`: the warm start of `s12c` (641,229 quadruples, τ-closed) plus the lex-leader
  clauses of §6.7, seed 5. With `s12c` this compares the same CNF with and without symmetry breaking.
Tests of `p2_batch.py` (20:46–20:50, `s12b` frozen meanwhile): at budget 11 without rows from a 180k warm start, five
SAT iterations of 7–90 s; at budget 0 (no rows) UNSAT in 30 s followed by the whole certificate pipeline (ALL_OK);
with `--sb` (21:04–21:16): the same, ALL_OK (the lex clauses were not needed at budget 0).

**7.4 Level 12: N66 ≤ 57 (CERTIFIED, 21:43).** Input: the `s12c` state (`W/p2/s12/c_L12.json`): 641,229 activated
quadruples (the τ-closure of the `s12a` state at 20:51, which itself extends `full_L11.json` by three level-12
iterations), hints `rows_1832.json`.
- `W/p2/b12/it1/cert.cnf` (`p2_write.py`): 1,647,698 variables, 9,201,367 clauses (eager 1,489,581; quadruple
  7,694,748; units 2; rows 15,648; counter 1,388), SHA-256 `ab101c49c8ca3ae309072f3b7e151c7ec3fa8988e8f8e65fe115fa960bded9ee`.
- CaDiCaL 2.1.3 `--lrat` (default options): **UNSAT in 1,997 s**, 9,989,759 conflicts (level 11: 3,227,140), 2.77 GB
  RSS, LRAT 6,392,937,024 bytes (SHA-256 `7a529cad0d00849fd9aa8431a40430759aea4268c0125d925db26b1faf56ca42`, deleted
  after the trimmed proof was accepted).
- `p2_lrat_trim` (30 s): 47,726,879 proof lines, 28,933,318 additions, 8,390,284 in the cone; 206,705 original clauses
  used: 86,029 eager, 111,620 quadruple, 2 units, **7,913 rows**, 1,141 counter. `trim.cnf` 13,504,197 bytes
  (2 clauses occur twice), `trim.lrat` 2,992,431,389 bytes (kept in W).
- cake_lpr (heap 2,000 MB, RSS 2.06 GB): **`s VERIFIED UNSAT`** in 66.9 s.
- Rows (21:26–21:43, 1,011 s): 3,769 transported (417 templates re-certified), 3,891 mirror, 203 core (204 core CNFs
  certified), 50 cycle; `final_verify66.py`: `bad 0`, `rows_match true`. Link re-check (`p2_recheck_rows.py`,
  21:44–21:47): static files equal to a fresh generation, 417/417 template and 204/204 core CNF hashes reproduced:
  **ALL_OK**.
- `p2_verify.py` (35 s): 197,647 clauses found exactly in the 39,017,853-clause mono66 stream, 7,913 justified rows,
  1,141 counter clauses (budget 12), 2 fixed units; 0 unclassified. **ALL_OK.**
**Result: N66 ≤ 57 is CERTIFIED.** `data/cert57/` holds `trim.cnf.gz`, `cert.json`, `verify.json`,
`layout_summary.json`, `used_rows.json`, the justification files, `recheck.json`, logs and `SHA256SUMS`.
Re-check: `p2_verify.py p2/b12/it1 p2/b12/it1/tcert`; `cake_lpr --CML_HEAP_SIZE=2000 trim.cnf trim.lrat` in W/p2/b12/it1.

**7.5 Level 13 (N66 ≤ 56): search** (opened by the driver at 21:25; warm start = the 641,229 quadruples of
`c_L12.json`; budget 13; all three slots are batch runs since 21:50, each a fresh CaDiCaL 2.1.3 run with LRAT):
- `s13e1` (21:44): with the symmetry breaking of §6.7 (first launch `s13e` 21:27–21:30, stopped to give the level-12
  row justification room);
- `s13c1` (21:47): without symmetry breaking (first launch `s13c` 21:31–21:33, stopped for the same reason);
- `s13g` (21:50): with symmetry breaking and CaDiCaL's `--unsat` configuration (`p2_batch.py --cadopts`);
- `s13a` (lazy engine, 21:26–21:50): stopped by hand and parked — the lazy engine lost level 12 (its iteration 4 ran
  51 minutes without an answer while the batch engine refuted the τ-closed set in 33 minutes).
Status: §9 (driver) and `n66_certified.json`.

## 8. What remains, and how to resume

**8.1 The driver** (`W/p2_driver.py`, unit `nov13c-n66-drv18` since 21:51, 5 % CPU, RuntimeMaxSec ending 05:59:30
KST; restarted after every change of its code: `drv` … `drv18`). Every 60 s it
- watches the search slots of the open level (`p2_lazymono.py` = lazy engine, pysat CaDiCaL 1.9.5 incremental;
  `p2_batch.py` = fresh CaDiCaL 2.1.3 runs with LRAT, optionally `--sb`), relaunches a slot whose unit ended (warm
  start from the slot's own last state, at most 4 launches per slot, at most one search launch per 3 minutes), and
  never restarts a unit that the memory guard stopped;
- on UNSAT (a file `p2/s<L>/<x>_L<L>.json`) stops the level's other units; a batch winner certifies in its own unit
  (`p2_cert.sh` on its iteration directory), a lazy winner gets the unit `c<L>` (`p2_cert.sh p2/c<L> <state>`:
  write, CaDiCaL, trim, cake_lpr, rows, link re-check, `p2_verify.py`); one retry if that unit ends without
  `cert.json`; then it opens level L+1 (slots a, e, c of `p2/driver_config.json`, warm start from the UNSAT state);
- on `cert.json` with ALL_OK (70 states, no cube) rewrites `/home/jay/research/data/phase2-20261113/n66_certified.json`
  (best bound + history), appends a line to §9 and, from level 13 on, inserts an update line at the top of the
  STATUS block;
- keeps at most 3 threads (sum of my units' CPUQuota) and checks `cpu_free.sh`; launches only if my anonymous memory
  plus the unit's estimate stays ≤ 8.5 GB; if a certificate step waits for room (`need_room.json`, written by
  `p2_cake.py` / `p2_template_cert66.py` through `p2_mem.py`) or my units exceed 8.3 GB it stops one search unit
  (highest level first; slot order b, d, c, e, a) and does not start further searches while that certificate runs;
- launches nothing after 05:15 KST; every unit it starts ends by 05:58 (RuntimeMaxSec).
State `W/p2/driver_state.json`, configuration `W/p2/driver_config.json` (read every minute), log `W/p2/driver.log`.
A mock test of the level transition (`W/p2/test/drv_mock_test.py`: batch winner, room request, certificate, next
level) passed at 21:20.

**8.2 Resume by hand** (all from W, with `ETV_A=4 ETV_B=4`, inside a `systemd-run --user` unit as in rule 2):
- driver: `python -u p2_driver.py` (reads its state; to change slots edit `p2/driver_state.json` while it is stopped);
- a search: `python -u p2_batch.py --out p2/s13/x.json --dir p2/b13x --L 13 --rows mono/rows_1832.json --warm p2/s12/c_L12.json [--tauclose] [--sb]`
  or `python -u p2_lazymono.py --out p2/s13/y.json --L 13 --rows mono/rows_1832.json --warm p2/s12/c_L12.json`;
- a certificate: `./p2_cert.sh <dir>` on a directory with `cert.cnf`, `layout.json`, `cert.lrat`, `cadical.log`
  (`exit 20`), or `./p2_cert.sh p2/c<L> <UNSAT state file>` from scratch; every step that is done is skipped;
- re-checks without a solver: `python p2_verify.py <certdir> <certdir>/tcert`, `python final_verify66.py <certdir>/tcert`,
  `python p2_recheck_rows.py <certdir>/tcert`; with the proof: `cake_lpr --CML_HEAP_SIZE=2000 trim.cnf trim.lrat`.
  Certificate directories: level 11 `W/p2/c11`, level 12 `W/p2/b12/it1` (trimmed proofs 977 MB and 2.99 GB).

**8.3 Open.**
- A certificate without row hints (the task's preferred form): not attempted in phase 2; the level-11 and level-12
  proofs use 5,738 and 7,913 rows. Without rows the phase-1 ladder run needed 340 s for budgets 0–3; the rows carry the
  coupled no-octagon knowledge that the chain form would have to rediscover.
- Level 13 (N66 ≤ 56) and beyond: the driver's runs (§7.5, §9).
- Independent re-verification of `data/cert57`, `data/cert58` by a verifier track (`trim.cnf.gz` is in the record;
  the trimmed proofs are in W).
- The gap: 50 ≤ N66 ≤ 57.

## 0. Running log (KST)

- 16:53 start. Baseline (cycle rows only, `cyc_base_A4B4.json`): 6 holes, N66 ≤ 64 (COMPUTED, CP-SAT OPTIMAL).
- 16:56 mirror map τ checked on the tables (`sym66.py`): cells, refined domains, capH/cupH transpose;
  TT[τa,τb,τc] = TT[a,c,b]; all 50 baseline cycle rows have a valid mirror cycle row (48 already present).
- 16:57 block rows: for every (K, J) ≠ (full, full) the largest family equals its cup-cap capacity
  C(|K|+|J|, |K|) (`blocks66.py`, exact clique search): no block row exists. COMPUTED (negative).
- 16:57 loop started (`loop66.py`, 5 threads). 16:59: level 8 (CP-SAT INFEASIBLE at ≤ 7; COMPUTED).
- 16:58 exact ETV 50-point set for (6,6,8): in class; its 20 holes are exactly the states with f₁ = 4 and
  f₄ ≥ 1 (a 5-cup and a 5-cap both end at the point).
- 17:04 (rule note) a 20-second single-thread analysis overlapped the 5-thread loop and the 1-thread control:
  7 threads for about 20 s. After that the 6th thread was used by one job at a time.
- 17:06 level 9; 17:08 clause soundness control done: 459 real sets (max 26 points), 1,836 CNFs,
  144,951,058 clause evaluations, 0 violations, all 70 states seen as owners (`sound2_66.out`).
- 17:12 loop restarted as `loop66b.py` (propagating transport enumerator `transport66.py`, equal to the old
  search on 12 templates, 30–60× faster). 17:14 level 10. Probe yield then collapsed (17 new rows in 4 min).
- 17:20–17:27 large-support engines (discovery only): `lazy66.py` (standard families, lazy no-octagon
  clauses; agrees with the full CNF on 325/325 random supports) and `dp66.py` (cap/cup chain form of the
  no-octagon condition, polynomial size; agrees on 247/247, 25/25 minimised cores UNSAT in the standard CNF).
  **Full-support oracle**: the complete occupied set (60 states) of a 10-hole vector is refuted in 0.4 s
  after an 18 s build (18.4 M clauses); minimal cores of 18–26 states.
- 17:30 loop restarted as `loop66c.py`: every vector goes to the oracle; cores of any size become
  templates in the form (static clauses without the no-octagon family) + (a short list of no-octagon
  clauses) + (kept tests) (`bigcore.py`). Round 1: 5 vectors, 40 cores (13–27 states), 351 new rows, 117 s.
- 17:34 dry run of the certificate pipeline at budget 9 (`final66.sh 9 final10 1`).
- **17:37 first certificate: N66 ≤ 60** (at least 10 holes), self-contained (`final66.sh 9 final10 1`,
  `data/cert60/`): PB CNF "≤ 9 holes" over a 2,100-row subset (CNF SHA-256 `dcd64c5a…`, byte-identical to the
  self-tested encoder), CaDiCaL 2.1.3 LRAT (35 MB, SHA-256 `c7f8c381…`), cake_lpr `s VERIFIED UNSAT`;
  rows: 51 cycle, 1,058 transported (115/115 templates cake_lpr-verified), 8 cores (8/8 verified),
  983 mirror rows; `final_verify66.py`: 0 bad, row multiset equal to the subset file.
- 17:40 monolithic CNF `mono66.py` (all 70 states as owners with selector variables, chain form of the
  no-octagon condition; 39.0 M clauses, 2.8 GB): CaDiCaL needs about 11 GB; the first run was given 7 GB and
  swapped (4 GB of swap for about 2 minutes) and was stopped. No result from it.
- 17:45 clause-level control of the monolithic CNF on the exact ETV 50-point set and its two reflections:
  0 violations (12.4 M / 12.4 M / 7.9 M clauses with all guards true), budget 20 satisfiable, 19 not
  (`mono_check.py`, `mono_check.out`).
- **17:48 level 11** (N66 ≤ 59, COMPUTED): CaDiCaL on the PB CNF "≤ 10 holes" over the 12,478 rows present
  (CNF SHA-256 `ec102bed…`): UNSAT in a few seconds (CP-SAT had returned UNKNOWN after 60 s).
  17:49 loop restarted at level 11 with the CaDiCaL finder (`loop66d.py`, 4 workers), and the certificate
  pipeline for budget 10 started (`final66.sh 10 final11 1`).
- 17:59–18:02 greedy fill from the ETV 50-state set in the monotone model (`greedy_fill.py`, engine over all 70
  states): none of the 20 hole states can be added, and no 1-for-2 exchange was found in 4 trials (COMPUTED).
- 18:10 restricted monolithic instance on 52 states (18 small states dropped): satisfiable with 11 holes among the
  52 (CaDiCaL, 215 conflicts): dropping states loses the bound; no claim.
- **18:11 certificate: N66 ≤ 59** (at least 11 holes), self-contained (`final66.sh 10 final11 1`, `data/cert59/`):
  PB CNF "≤ 10 holes" over a 3,052-row subset (CNF SHA-256 `92048925…`, equal to the self-tested encoder's output),
  CaDiCaL 2.1.3 LRAT (162 MB, SHA-256 `9272dfbc…`), cake_lpr `s VERIFIED UNSAT`; rows: 51 cycle, 1,447 transported
  (281/281 templates verified), 67 cores (68/68 core certificates verified), 1,487 mirror rows;
  `final_verify66.py`: 0 bad, row multiset equal to the subset file.
- 18:11 controls: big-template format is a sub-CNF of the standard CNF (6/6 supports; equal when all 8-subsets are
  listed); the cap↔cup / orientation-negating renaming maps CNF(S) onto CNF(τS) exactly (6/6) (`check_bigtemplate.py`).
- 18:13 monolithic run at budget 11 stopped by me after 9 minutes (82,444 conflicts, no verdict); loop restarted
  with 5 oracle workers.
- **18:17 memory rule.** A session memory guard came into force (track budget 9 GB of resident memory + swap,
  every unit below 80 % of its own MemoryMax, no swap; `/home/jay/research/data/memguard-20261113/`). Jobs of this
  track that had broken a limit before or were stopped by the guard:
  - 17:41 `nov13c-n66-mono10` (CaDiCaL on the 39 M-clause CNF with MemoryMax 7 GB): swapped 4.2 GB for about two
    minutes; stopped by me. My mistake: no memory estimate before the launch.
  - 17:57 `nov13c-n66-monoor` and 18:11 `nov13c-n66-mono13`: killed by the kernel at their MemoryMax (8 GB, 9.8 GB).
  - 18:17 `nov13c-n66-loopi` (5 oracle workers, 10.8 GB): stopped by the guard (track budget).
  - 18:22 `nov13c-n66-dw3`, 18:27 `nov13c-n66-dwfull1` (selector engine in pysat on 52 / 59 states): stopped by the
    guard at 90 % of their MemoryMax (3.8 GB): the solver grew from 2.0 to 3.8 GB during one query.
  - 18:32 `nov13c-n66-m11p` (plain CaDiCaL on the 39 M-clause CNF, MemoryMax 8.6 GB, estimate 6.1 GB, actual
    8.2 GB): stopped by the guard.
  What changed: no monolithic instance on disk any more; a memory-lean oracle (`dp66c.py`, 2.0–2.3 GB instead of
  3.2 GB per worker, agreement 460/460); and the **lazy monolithic engine** `lazymono.py`, which holds only the
  pair/triple-level clauses (1.5 M for 70 states) and adds quadruple-level clauses on demand (0.9–1.1 GB
  resident in the runs so far). From 18:36 on the track stayed below 3 GB.
- 18:19 demand of state sets in the monotone model (selector engine with a totalizer, COMPUTED): the 30 most
  core-frequent states need 2 holes, the top 38 need 5, the top 46 at least 7 (budget 6 refuted in 45 s).
- 18:29 for one 11-hole vector H that satisfies all rows, "at most 3 holes among the 59 occupied states" is
  refuted (plain CaDiCaL 2.1.3, 2,149 conflicts, 9 s; again by the lean form, 1,897 conflicts; again by
  `lazymono.py` with 240,000 activated quadruples): this H is at least 4 holes away from any consistent selection.
- 18:38 control of the monolithic clause families finished: 26 real sets (the ETV 50-point set, its reflections,
  subsets, greedy sets), 113,074,249 clause evaluations, 0 violations (`mono_check.out`).
- 18:37 `lazymono.py` started on all 70 states with the 15,648 rows as hints, from budget 11.

### Phase 2 (from 20:25 KST)

- 19:40 (phase 1 cut off) state found at 20:20: `nov13c-n66-lmfull` (lazymono, all 70 states, 15,648 row hints)
  proved budget 11 UNSAT at 18:58 after 1,242 s (12 iterations, 322,818 activated quadruples), then worked on budget
  12 until its 80-minute RuntimeMaxSec at 19:57: no verdict and no saved state (lazymono saved its state only at a
  verdict). The three level-11 cubes on states 32 = (3,2,2,1) and 37 = (4,3,1,0) (A: both holes, B: 32 hole / 37
  occupied, C: both occupied) were UNSAT after 430 / 535 / 644 s (COMPUTED); the fourth cube was never run (not
  needed after the full run). `lm/cert_occfull_L4` (18:40–18:47): a CERTIFIED but restricted test statement — on the
  59 occupied states of one 11-hole vector, "at most 4 holes among these 59 states" is refuted (CaDiCaL --plain
  107 s, cake_lpr `s VERIFIED UNSAT`, `lazymono_verify.py` ALL_OK, no rows); the first attempt `lmcert0` was stopped
  by the guard at 3.4 GB because cake_lpr runs with a 4,096 MB heap by default (the old script passed the heap as an
  environment variable, which cake_lpr ignores; it takes `--CML_HEAP_SIZE=<MB>`). `lm/ladder.out`: without rows,
  budgets 0–3 UNSAT on all 70 states in 340 s (COMPUTED), stopped at 18:47 for the cubes.
- 20:25 phase 2 start; the work directory and the record are this task's. Units of this phase (all `nov13c-n66-*`,
  1 thread each, the driver 5 %): `c11`, `c11v`, `s12a`, `s12b`, `s12c`, `s12d`, `s12d1`, `s12e`, `s13a`, `s13e`,
  `s13e1`, `s13c`, `s13c1`, `s13g`, `rck11`, `rck12`, tests `ptest`…`ptest8`, driver `drv`…`drv18`; at most 3
  compute threads at any time (the tests ran while one search unit was frozen or stopped).
- 20:27 `c11`: `p2_write.py lm/full_L11.json` (5.5 s) and CaDiCaL 2.1.3 with LRAT on the 5,380,347-clause CNF.
- 20:30 level-12 searches `s12a`, `s12b` (§7.3), 3 GB MemoryMax each, 1.6 / 2.2 GB at the start.
- 20:33–20:34 pipeline tests (§7.1) in `ptest`, `ptest2`; `s12b` was frozen (cgroup freezer) for those two minutes so
  that the track kept 3 busy threads.
- 20:34 CaDiCaL: **UNSAT in 455 s** (1.71 GB RSS, LRAT 2.41 GB).
- 20:39 `c11v` (`p2_cert.sh p2/c11`): trimmed to 92,446 original clauses (5,738 rows) and a 977 MB proof in 10 s;
  **cake_lpr `s VERIFIED UNSAT`** in 22.7 s with a 2,000 MB heap (RSS 2.05 GB); row justification started.
- 20:39 driver started; restarted twice within the minute (RuntimeMaxSec now ends 05:59:30; the driver no longer
  counts its own 5 % unit as a thread), later restarted after each change of its code or state (`drv4`–`drv8`).
- 20:46–20:50 tests of `p2_batch.py` (`ptest3`; `s12b` frozen meanwhile).
- 20:51 `s12b` stopped (first solve without answer after ~16 CPU-min), `s12c` (batch engine) started.
- **20:56 level 11 CERTIFIED: N66 ≤ 58** (§7.2); 20:57 the driver wrote `n66_certified.json` (bound 58) and §9.
- 21:01 `s12d` / `s12d1` (§7.3, including the directory collision that was caught after 10 s).
- 21:02 certificate data copied to `data/cert58/`, tools to `tools/` (24 files).
- 21:04–21:16 symmetry breaking (§6.7) implemented and tested; a test pipeline waited 10 min for memory room while
  `s12d1` was frozen (the driver frees room only for the certificate directories it knows); `s12d1` then stopped.
- 21:17 `s12e` (batch engine with symmetry breaking) started by the driver.
- 21:22 `s12e` stopped and slot e paused for the link re-check of the level-11 row certificates (`rck11`, 163 s,
  ALL_OK, §7.2).
- **21:24 level 12 UNSAT (COMPUTED)**: `s12c`, first batch iteration (641,229 activated quadruples = the τ-closure of
  the `s12a` state at 20:51; CNF 9,201,367 clauses, SHA-256 in `W/p2/b12/it1/layout.json`), CaDiCaL 2.1.3 UNSAT in
  1,998 s, LRAT 6,392,937,024 bytes; no SAT iteration was needed. 21:25 the driver stopped `s12a` (its iteration 4
  had run 51 min without an answer) and opened level 13 (slots a, e, c). 21:25 trimmed: 206,705 of 9,201,367 original
  clauses, 8,390,284 of 28,933,318 proof additions, `trim.lrat` 2,992,431,389 bytes; cake_lpr started.
- 21:26 cake_lpr `s VERIFIED UNSAT` on the trimmed level-12 proof (66.9 s); 7,913 rows to justify. 21:26 the driver
  started `s13a`, 21:27 `s13e`.
- 21:30 and 21:33 the driver stopped `s13e` and `s13c` because the row justification asked for room for a cake_lpr
  heap (n66 budget); it relaunched `s13c` once in between (a thrash: since 21:37 the driver starts no further search
  unit while a certificate step that asked for room is running). No unit of this track was stopped by the memory guard
  in phase 2.
- **21:43 level 12 CERTIFIED: N66 ≤ 57** (§7.4); 21:43:55 the driver wrote `n66_certified.json` (bound 57) and §9,
  and resumed `s13e` as `s13e1`. 21:44–21:47 link re-check of the level-12 rows: ALL_OK. 21:47 data in `data/cert57/`.
- 21:47 `s13c1`; 21:50 `s13a` stopped (parked), `s13g` (`--unsat`, symmetry breaking) started; the driver's next
  levels use the slots e, c, g (`p2/driver_config.json`).
- 21:51 driver `drv18` (adds the STATUS update line; mock test of the level transition including that line: OK).
  Memory at 21:52: the three level-13 runs 2.29 / 2.36 / 2.49 GB anonymous; no unit of this track stopped by the guard.
- 21:55 this session hands over to the driver (§8.1); results after this line come from the driver (§9).

## 9. Driver log (appended automatically by `W/p2_driver.py`; times KST, 13/14 Nov)

- 20:57 (driver) **CERTIFIED: N66 ≤ 58** (at least 12 holes): `W/p2/c11`, trimmed CNF SHA-256 `424f330442a1f140033fff23b8a16f5a879418ef2064e915648e993ce3faf73d`, trimmed LRAT SHA-256 `8c80abacf5332d563c71a3516786d1fa6e984110e723db2cc07627d4be45cc17`, 92446 clauses {'units': 2, 'rows': 5738, 'card': 978, 'geometric': 85728}, 5738 used rows justified, p2_verify ALL_OK; n66_certified.json updated.
- 21:25 (driver) level 12: search run `W/p2/s12/c_L12.json` reports "at most 12 holes" UNSAT (COMPUTED); certificate: p2_cert.sh in the same unit on `W/p2/b12/it1`.
- 21:30 (driver) memory: search unit s13e stopped to make room for a certificate step; its slot resumes from its saved state when no certificate unit runs.
- 21:33 (driver) memory: search unit s13c stopped to make room for a certificate step; its slot resumes from its saved state when no certificate unit runs.
- 21:43 (driver) **CERTIFIED: N66 ≤ 57** (at least 13 holes): `W/p2/b12/it1`, trimmed CNF SHA-256 `80b55b0c2c2ef445f485901e69fda3fdbb994fc1d882b5828d9227a85a695ee7`, trimmed LRAT SHA-256 `3971e63f869224cca0e39d3b40e5070cfd737a2c13fdab8abb68bd6a105a5978`, 206705 clauses {'units': 2, 'rows': 7913, 'card': 1141, 'geometric': 197647}, 7913 used rows justified, p2_verify ALL_OK; n66_certified.json updated.
- 23:14 (driver) level 13: search run `W/p2/s13/g_L13.json` reports "at most 13 holes" UNSAT (COMPUTED); certificate: p2_cert.sh in the same unit on `W/p2/b13g/it1`.
- 23:36 (driver) memory: search unit s14c stopped to make room for a certificate step; its slot resumes from its saved state when no certificate unit runs.
- 23:43 (driver) **CERTIFIED: N66 ≤ 56** (at least 14 holes): `W/p2/b13g/it1`, trimmed CNF SHA-256 `8d4b9099cf045ca72ba5ac56e8ecea00a73a44652d5a9f3d100f63f1f10bc151`, trimmed LRAT SHA-256 `ff79c2ef3805255b18917dc0769c5088cca0ee8106c5eefb78b8f212fa487296`, 319611 clauses {'units': 2, 'rows': 6775, 'card': 1201, 'geometric': 311576, 'sb': 56}, 6775 used rows justified, p2_verify ALL_OK; n66_certified.json updated.

## Addendum, 15 November 2026 (02:05 KST): level 14 (N66 ≤ 55) resumed, undecided

Resumed from the saved level-14 states with the record's unchanged `p2_batch.py` (work dir
`/home/jay/research/data/n66-20261113`), two slots from 22:55 to 02:05 KST, 1 CPU and MemoryMax 5.8 G each, environment
`ETV_A=4 ETV_B=4 P2_UNIT=<unit>` (as the driver set it):
- `esr-n66-s14h2`: `--warm p2/s14/c.json` (660,810 activated quadruples) `--tauclose --sb --cadopts=--unsat --seed 11`;
- `esr-n66-s14i2`: `--warm p2/s14/g.json` (654,351) `--tauclose --sb --cadopts=--unsat --seed 13`.
**Outcome: undecided (COMPUTED: no verdict).** Both stopped at the 3 h 10 min runtime limit inside the first CaDiCaL
solve of iteration 1 (on 13 November level-14 iterations took 195-702 s). N66 ≤ 56 stays the established bound.
The partial LRAT files `p2/b14h2/it1/cert.lrat` (29.6 GB) and `p2/b14i2/it1/cert.lrat` (29.2 GB) cannot be certified
(no UNSAT verdict); they are kept, and deleting them is the owner's decision. Two first attempts (`h`, `i`) stopped
at import because the unit environment lacked ETV_A/ETV_B; nothing ran. Next: a cube-and-conquer split of level 14,
or a different relaxation, rather than longer monolithic solves.
