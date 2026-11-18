# VERIFY_N5: adversarial check of ETV5N20261113 (claim N5 ≤ 65)

Independent verifier, phase 2, 13 November 2026, 20:20–21:35 KST. Draft written at 20:40 and updated
when the compute finished (see the status line in §0).
Scratch directory: `/home/jay/research/data/verify-N5-20261113` (V). W =
`/home/jay/research/data/etv5-20261113`, which I only read. Two systemd units ran one after the other:
`nov13c-vfy-N5-drv` (1 thread, MemoryMax 1500M, MemorySwapMax 0, RuntimeMaxSec 3720, nice 10), started at
20:27:56 after `cpu_free.sh` reported 9 free threads, and `nov13c-vfy-N5-their` (same limits, RuntimeMaxSec
300), started at 21:24:27 with 5 threads free. The memory guard stopped neither. The short checks I ran in my session
took under a minute each. I made no git changes. This file is the only file I wrote in the repository.

Labels as in the README: PROVED, CERTIFIED (cake_lpr `s VERIFIED UNSAT` for a CNF whose hash is recorded),
EXACT (my own exact-integer recomputation), COMPUTED (solver verdict only), HEURISTIC.

## 0. Verdict

**N5 ≤ 65 is confirmed.** I found no error in the written arguments (§2 of the README), in the clause
families of `coupled5.py`, in the Baek block-row argument, in the transport argument, in the cube cover or
in the PB step. I recomputed every exact ingredient with my own code: the catalog, both domain tables, the
six-order triple table, all 148 cycle rows, all 3 block rows and all 114,670 transported rows (σ). I then
re-proved the arithmetic step with **my own PB encoder** (written from scratch, without pysat). Its 32 cube
CNFs are refuted by CaDiCaL 2.1.3 LRAT proofs that cake_lpr accepts: **32 of 32 `s VERIFIED UNSAT`**
(finished 21:24). The arithmetic step is therefore CERTIFIED a second time, on a CNF that shares no
encoder code with the record. Real point sets violate no row: 4,035 sets checked, including the exact ETV
42-point set.

Status line: compute finished at 21:24:16 (driver) and 21:25:48 (one of the record's own cubes);
this file was finalised at 21:30.

The remaining issues are wording issues (§3). None affects the bound.

## 1. Verdict per claim

| # | Claim (README) | Verdict | Basis |
|---|---|---|---|
| 1 | Labels in [1..3]×[1..6], 84 states, state separation, fixed states 0 = (0,0,0) and 1 = (1,0,0) | confirmed | proof re-read; EXACT: on 4,035 real sets the owner states are injective and every label lies in I(v)∖I(u) |
| 2 | Lemma R (refined domain D′) | confirmed | proof re-read (both halves, including the case where u is the first point); EXACT: 0 labels outside my D′ on 4,035 real sets |
| 3 | Six-order test: 49,482 forced triples, none forced both ways, cyclic invariance, refinement by D′ adds nothing | confirmed | my own table (`mygeo.triple_table`, also checked against a literal definition on 3,000 random triples) equals the record's TT and TTR entry by entry |
| 4 | 148 cycle rows (Lemma 2.2) | confirmed | EXACT: each stored list order passes my table on every triple; demand = k − 7 (96 rows with k = 8, 52 with k = 9) |
| 5 | 3 Baek block rows (capacity 22, demand 6) | confirmed | argument checked (a 4-cap needs three strictly increasing first coordinates on consecutive owner pairs, impossible inside a 2-set K); EXACT with my D′: rows 1 and 3 have K = {1,2}, row 2 has K = {2,3}; Lean `BaekGeometry.geometric_capacity22` read: its hypotheses are "no 4-cap inside the subset" and "no convex octagon in the whole configuration", which is what the row needs; no `sorry` in Baek.lean, BaekGeometry.lean or BlockGeometry.lean |
| 6 | Soundness of every clause family of `coupled5.py` for (A,B) = (3,6) | confirmed | code review, family by family (§2.1); semantic test with my own geometry: 297 CNFs (8–14 owners), 25,900,659 clause evaluations, 0 violated |
| 7 | Transport: σ plus a certified template CNF gives a valid row | confirmed | argument checked (§2.2); EXACT: all 114,670 σ re-checked with my tables (4,672,112 tests, 0 failures); CERTIFIED by me: 2 templates; template CNF hashes reproduced with the uncached builder for one template of every size used (n = 9, 11, 13, 14, 15, 16, 17), so the static cache is correct for every n; COMPUTED: the own full CNFs of 20 random transported rows, in random index order, are UNSAT (20/20) |
| 8 | 428 coupled cores, own full CNF CERTIFIED | confirmed, partly re-run | all 428 listed with `s VERIFIED UNSAT`; I rebuilt and re-certified one core (hash equal to the record's); the other 427 rest on the recorded cake_lpr verdicts |
| 9 | Arithmetic: PB CNF "≤ 18 holes" over the 115,249-row subset, 32 cubes CERTIFIED | confirmed | the 32 cubes are all 2⁵ assignments of states 22, 37, 45, 53, 67; the record's base hash `6e99282f…` and all 32 cube CNF hashes reproduced from the subset file; my own encoder: all 32 cubes CERTIFIED (CaDiCaL 2,853 s in total, at most 119.2 s per cube; LRAT 20.7 GB in total, at most 933 MB, all deleted after hashing; cake_lpr 511 s in total); also re-run: the record's own cube 00001 (CNF rebuilt, sha256 equal to the recorded one), CaDiCaL UNSAT in 69.7 s, LRAT 419,566,039 bytes (byte count identical to the record), cake_lpr `s VERIFIED UNSAT` |
| 10 | No row of the subset is violated by real 5-cap-free octagon-free sets | confirmed (HEURISTIC as a soundness check) | 4,035 sets checked with my own code; 0 violations; the fullest row is 93.3 % occupied; the ETV set meets some row with slack exactly 0 |
| 11 | Totals in README §4.1 (2,994 s, 21.4 GB, 841 s wall; 3,442 s, 22.25 GB for the all-rows run; 32/32 verified) | confirmed | recomputed from `cubes19_sub_info.json` and `cubes19_all_info.json` |
| 12 | Novelty | no novelty claim made; see §3 | NOVELTY20261113B C3: no prior art for 65 was found; the baseline from printed statements is 78, not 84 |

## 2. What I checked, and how

### 2.1 Written arguments and the encoder (read line by line)

- **Growth with ceilings**, family 3. For every ordered triple (a,b,c) of owners and every k, the clause
  is: before(a,b) ∧ before(b,c) ∧ [orientation of (a,b,c) < 0] ∧ cap_ge(a,b,k) → cap_ge(b,c,k+1). Here
  orient((a,b,c)) carries the parity sign of the permutation. At k = 1 the clause becomes "→ cap_ge(b,c,2)";
  at k = 3 it becomes "→ ¬cap_ge(a,b,3)" (ceiling, no 5-cap). The cup version is the same with ceiling 6
  (no 8-cup). Both directions are right: a negative determinant on an x-increasing triple is a cap and
  raises d₁. The label atoms belong to the unordered pair and mean d(earlier, later), as the README says.
- **Signotope packets**: for each of the 24 orders of each quadruple, conditioned on that x-order, the 8
  sign sequences with at least 2 changes are excluded (BAD4 has 8 entries). I re-derived the impossibility
  from the two math.md §2.1 identities (β and γ are positive combinations of α and δ) and from
  δ − γ + β − α = 0 (β − γ = α − δ, so (+,−,+,−) is impossible).
- **convex_four**: the cofactor vector ([bcd], −[acd], [abd], −[abc]) is the affine dependency, and
  "exactly two positive" means convex position. The code counts negatives (¬w, z, ¬y, x) == 2, which is
  equivalent. The atom is fully defined (16 clauses per quadruple), so the octagon clauses cannot be
  satisfied by setting it false.
- **Complete no-octagon**: if all 70 quadruples of 8 points are convex, no point lies in a triangle of
  three others, so by Carathéodory no point lies in the hull of the others: a convex octagon. Correct.
- **empty / domain / positive**: the domain clause is
  ¬before(u,v) ∨ ¬cap_ge(a) ∨ cap_ge(a+1) ∨ ¬cup_ge(b) ∨ cup_ge(b+1), with ge(k ≤ 1) = true and
  ge(k > max) = false. That is "label ≠ (a,b)", and the boundaries are right. A positive tag (i,k,j) stands
  for the unit −orient(i,j,k). It is valid when TT[s_i, s_k, s_j] holds, which is the check that
  final_verify and my script make.
- **Lemma R**: the attaining chain minus its last point ends with (t,u), so (1, d₂(t,u)) and
  (d₁(t,u), 1) lie in I(u). If u is the first point, the label is (1,1) and D′ = {(1,1)} ∩ I(v). Correct.
- **Block rows**: a 4-cap among F-owners has consecutive pairs that are all F-owner pairs, and their labels
  lie in D′. Three strictly increasing first coordinates inside a 2-set are impossible. The Lean theorem is
  applied to the subset O ∩ F with the global octagon hypothesis. Correct.
- **Cycle rows and TT**: the parity convention is right. Even chronological order → forbid cap growth on
  coordinate 0 → a cup, which is positive in list order. Odd order → forbid cup growth → a cap, which is
  positive in list order after the sign flip. The outer pair's domain is also required to be nonempty,
  which is sound.
- **Counting**: UNSAT at budget 18 means at least 19 holes, so |S| = 84 − holes ≤ 65. For |S| ≤ 1 the
  bound is trivial. No off-by-one.

### 2.2 Transport

Every static clause is a geometric truth for any n owners of distinct states. A kept test's clause depends
only on its tag. So the template CNF is a set of clauses that are all valid for the owners of σ(0..n−1)
whenever every kept test holds on σ (positive: TT[σ…]; empty: D′ = ∅; domain: (a,b) ∉ D′, also valid when
D′ = ∅, because then ¬before holds). The index order need not be sorted. The argument is sound. The
builder-equality remark in the README is not even needed.

### 2.3 Commands and outputs (in V)

- `python -I check_rows.py` (my tables, `myTT.pkl` from `mygeo.triple_table`):
  `rows 115249, rows_match_justification true, kinds {cycle 148, block 3, core 428, transported 114670},
  bad {}, template_tests_checked 4672112, templates_used 299, templates_failing_own_core 0,
  malformed_tags 0, cycle_sizes {9: 52, 8: 96}, block_K [[1,2]], [[2,3]], [[1,2]]` (1.6 s).
- Table comparison: `forced ordered triples plain 49482 refined 49482, equal tables True, both orientations
  forced 0, cyclic invariant True, literal-definition mismatches 0/3000, their TT equals mine True, their
  TTR equals mine True, their DREF equals mine True`.
- `python -I semtest.py 55 7`: `sets 76, cnfs 228, clauses 13751191, violations 0` (static 13,535,670;
  domain 198,965; empty 8,000; positive 8,556). The sets are ETV subsets, mirrored ETV subsets (x ↦ −x
  keeps caps as caps) and greedy uniform sets, all validated by my code. Each CNF uses 8–13 owners in
  random index order. A second run, `semtest2.py 50 13` (dense ETV subsets of 30–42 points and their
  mirrors, 12–14 owners), gave `cnfs 69, clauses 12149468, violations 0` (domain 108,388; positive 5,511;
  empty 3,944). Total: 297 CNFs, 25,900,659 clause evaluations, 0 violations.
- `python -I realcheck_mine.py subset19_rows.json 55 1` and `realcheck_mine2.py … 58 2`: 2,507 + 1,528
  real sets (ETV 42-point set; 3,500 random subsets of it, 500 of them mirrored; 1,018 greedy sets from
  uniform, parabola, cluster and arc samplers; sizes 8–42). All were validated with my code (general
  position, no 5-cap, no 8-cup, largest convex polygon ≤ 7 by the cup+cap chain DP), except for the
  unmirrored ETV subsets, which are subsets of a validated set. Result: `violations 0,
  lemmaR_violations 0, label_not_in_plain_domain 0, max_occupied_fraction 0.933, min_slack 0`. 80 of the
  84 states occur. The ETV 42-point set itself is valid by my code and occupies the 42 states
  0–26, 28, 30–33, 35, 38–40, 43, 46, 47, 50, 54, 61.
- Hash reproduction of the record's arithmetic certificate (their encoder, pysat):
  `their base sha reproduced True 6e99282f589975b9`, `cube cnf hashes reproduced 32 of 32`.
- Template and core rebuilds with the uncached builder (`tmpl_build.py`; coupled5.py and etv_common.py
  copied into V/theirs, sha256 equal to W and to tools/): templates 818fa44741fc7ef3 (n 13, the template
  used by 7,181 rows), 26262c9dffc88b56 (n 13, random), a6db950c69aac9b4 (n 11), 8a2c2eb7134f55f9 (n 9),
  a3a7bef402ed93ee (n 14), 2c75b2b537315fd6 (n 15), 2fbb648008823693 (n 16), 2f74a1e0bbcfec09 (n 17): all
  `match true`, missing tests 0. Core 0,4,7,10,12,14,19,25,32,36,40,57,66: `match true`.
- Driver unit `nov13c-vfy-N5-drv` (V/driver.py, V/status.json, V/driver.log), CaDiCaL 2.1.3
  `--lrat=true --binary=false`, then `cake_lpr --CML_HEAP_SIZE=1000 --CML_STACK_SIZE=100`. Every LRAT was
  deleted after hashing:
  - template 818fa44741fc7ef3: UNSAT, LRAT 2.2 MB, `s VERIFIED UNSAT`
  - template 26262c9dffc88b56: UNSAT, LRAT 3.3 MB, `s VERIFIED UNSAT`
  - core 0,4,7,…,66: UNSAT, LRAT 21 KB, `s VERIFIED UNSAT`
  - my PB cubes: **32/32 CaDiCaL exit 20 and `s VERIFIED UNSAT`**. Per-cube CNF and LRAT sha256, sizes
    and times are in V/status.json. The order of the run was 10111 (the cube of the record's 18-hole witness),
    01111 (the record's slowest), then the rest by the record's times in ascending order. Slowest of
    mine: 00111, 119.2 s, LRAT 933 MB, cake_lpr 23.2 s.
  - the record's own cube 00001 (`theircube.py 00001`, unit nov13c-vfy-N5-their): `cnf_sha256_match true, cadical_exit 20, cadical_s 69.7, lrat_bytes 419566039, cake s VERIFIED UNSAT, cake_s 9.6`.

### 2.4 My own PB encoder (V/mypb.py)

Variables h_s = s+1 (hole), with s indexed by my own catalog: sorted by (sum, f). The fixed states 0 and 1
and the branch states (6,0,0), (6,2,0), (6,3,0), (6,4,0), (6,6,0) = 22, 37, 45, 53, 67 are derived from
that catalog. The encoding has units ¬h₀ and ¬h₁ and a counter c[i][j] = [x₁+…+x_i ≥ j] for "≤ 18". Each of
the 55 rows with d ≥ 2 gets its own prefix counter. Each of the 115,194 demand-1 rows is a plain clause.
Every clause is true under the canonical counter values whenever h satisfies the PB system, so UNSAT of the
CNF implies that no hole vector with at most 18 holes satisfies the rows. A brute-force self-test on
300 random instances (99 SAT, 201 UNSAT) passed. The base has 3,054 variables and 120,542 clauses; each
cube adds 5 units.

## 3. Problems found

No error that affects the bound. Points to correct or keep in mind:

1. **Wording, README §2, line 29.** "distinct x-coordinates (rotate if necessary)": caps and cups depend on
   the direction, and a rotation can create a 5-cap. N5 is defined in §1 for the given x-direction, so the
   parenthesis should be deleted. This is cosmetic. Lemma A of THEORY310N uses the same fixed direction.
2. **Context, README §1 and §4.1.** The README compares 65 only with the internal 71, cup-cap 84 and the
   conjectured 42. NOVELTY20261113B (C3, §10) shows that 78 follows from printed statements in one step
   (endpoint split with Baek's 22 and cup-cap 56) and asks that 65 be compared with 78, 84 and 42. The
   README makes no novelty claim, so nothing is overstated, but a write-up must cite 78.
3. **Scope of my re-runs (not an error).** I re-certified 2 of the 299 templates and 1 of the 428 cores.
   The remaining 297 templates and 427 cores rest on the recorded cake_lpr verdicts and hashes. The static
   cache, the only shared component, is confirmed by hash for every template size used.
4. **The record's own soundness tests are HEURISTIC** (as labelled). My semantic test (§2.3) is
   independent of geom.py and soundness_test*.py and agrees with them.

## 4. Files (in V, scratch only)

`mygeo.py` (my catalog, domains, triple table, geometry), `check_rows.py`, `semtest.py`, `semtest2.py`,
`realcheck_mine.py`, `realcheck_mine2.py`, `mypb.py`, `tmpl_build.py`, `driver.py`, `theircube.py`,
`status.json`, `driver.log`, `theircube.log`, `check_rows.out`, `semtest1.out`, `semtest2.out`,
`realcheck1.out`, `realcheck2.out`, `cubes/` (my 32 cube CNFs, 4.9 MB each). Units:
`nov13c-vfy-N5-drv` (20:27:56–21:24:16) and `nov13c-vfy-N5-their` (21:24:27 to 21:25:48). Each used
1 thread and at most about 1.1 GB, and neither was stopped by the guard.
