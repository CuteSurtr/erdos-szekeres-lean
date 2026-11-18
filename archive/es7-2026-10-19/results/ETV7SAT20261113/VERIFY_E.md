# VERIFY_E: adversarial check of ETV7SAT20261113 (13 November 2026, 20:48–21:20 KST)

Independent verifier E, phase 2. I read the README as it stood at 20:47 (SHA-256 `ddcfea48…`, snapshot in X) line by line
before testing. X = `/home/jay/research/data/verify-E-20261113` (scratch, not in Git): `my/` holds my own
scripts, `gen/` holds copies of the record's generators (needed to regenerate the CNFs), and `run/` holds the job scripts and logs.
All compute ran in units `nov13c-vfy-E-*`: one thread, MemoryMax 1,400–1,500 MB, swap 0. No unit was stopped. This
file is the only file written in the repository. No Git state was changed.

Rigor labels: as in the record. **CERTIFIED (by E)** means that I regenerated the CNF myself with a matching hash and
saw `s VERIFIED UNSAT` from cake_lpr in my own run. **EXACT** means my own exact-integer program. **COMPUTED** means a
solver verdict only.

## Verdicts

| claim | verdict | reason (details below) |
|---|---|---|
| M(5; 7) ≤ 36 (every 37-point set in general position with distinct x and no 5-cap contains a convex heptagon) | **not confirmed** | Everything I could check holds: the soundness argument, the CNF identity, and all positive and negative controls. **But I could not re-check the N = 37 UNSAT certificate.** The LRAT was deleted after its check. Re-solving takes about 70 min, and cake_lpr needs a heap of at least 4.2 GB (2.6 GB failed); this verifier has 1.5 GB per unit and about 75 min. The only evidence of UNSAT is the log line in `data/lad_ns37_N37.cake`. Its CNF hash equals my regenerated CNF. |
| Certificate N = 37 (`--nosig`, rows, ALL ≤ 37) | **not confirmed** | CNF regenerated, SHA-256 `8762b9f0…` matches. The LRAT `d3205363…` is gone, so it is log-only. |
| Certificates N = 41 (`--nosig`; `--sigmax 1 --link`), 40, 38 | **not confirmed** | All four CNFs regenerated with the recorded hashes. The LRATs are deleted, so they are log-only. cake_lpr cannot even *load* a 3.95 M- or 5.57 M-clause ladder CNF with a 1,150 MB heap (`CakeML heap space exhausted` with an empty proof), so no target-catalog certificate fits this verifier. |
| Soundness of the owner model (§2.1–2.3), including "exactly N" | **confirmed** | Line-by-line review of the argument and of the code (`cat_common.py`, `owner.py`, `owner_v1.py`, `addrows.py`). No gap found. Own semantic positive controls on 16 real point configurations (the 4 ETV sets `etv757`, `etv756`, `etv747`, `etv656`, their mirrors, and 8 random subsets of `etv757` or its mirror) and on 2 non-signotope colourings: 0 falsified clauses. Negative controls show that the test is not vacuous. |
| "N = 37 UNSAT gives 36 for all larger sets; 38–41 not needed" | **confirmed** | Subset argument (all hypotheses are hereditary). The N = 37 CNF differs from the controlled N = 26 CNF only in the counter clauses. |
| §5.1 lemmas: (5,6) geometric and colouring; Baek n = 7 geometric and colouring | **confirmed (CERTIFIED by E)** | All four CNFs regenerated with the recorded hashes. cake_lpr on the four LRAT files kept in W: 4 × `s VERIFIED UNSAT`. The encoders were reviewed. |
| Schroeder's M₇(5, 6) ≤ 25 re-proved by one CNF, and its colouring strengthening | **confirmed** | Same certificates. The (3,4,7) model accepts the ETV 25-point set and its mirror (full model with family S), and a non-signotope colouring (`--nosig` model). As the record says, this is not a new theorem. |
| 27-vertex colouring with no 5-cap path, no 7-cup path and no weak heptagon | **confirmed (EXACT, own program)** | Longest cap path 4, longest cup path 6, no (a, b) with a + b ≥ 9 on common end-vertices, largest weak polygon 6, 383/17,550 violated packets. Wording caveat on novelty (Problem 3). |
| Positive controls: the encoder accepts the ETV 26-point set; SAT at the conjectured sizes | **confirmed** | The ETV 26 set and its mirror are models of the N = 26 CNFs with the flags of every certified rung (`--nosig`, `--sigmax 1 --link`, full). One model was checked clause by clause (EXACT). (3,4,7,25) is SAT without units. 9/9 known-answer checks behave as expected. |

## 1. Soundness of the owner model (§2): line by line

Every item of §2.1 was re-derived; I found no gap:
- **Labels in range.** Caps have ≤ CA + 1 = 4 points, and cups ≤ CB + 1 = 6 points, since a 7-cup is a convex heptagon. So d ∈ [1..3] × [1..5], because E± ≥ 2.
- **Growth** (extend an attaining chain).
- **State separation.** For t < u < v: a cap (t,u,v) gives d₁(u,v) > d₁(t,u), and a cup gives d₂(u,v) > d₂(t,u). So d(u,v) is not below any generator of I(u), and d(u,v) ∈ I(v) ∖ I(u).
- **Lemma R** (prefix of an attaining chain; for the first point capH = cupH = 0, so d = (1,1)).
- **Exact predecessor:** E₊(t,x) ≥ b from the prefix, and ≤ b by Growth.
- **Corners.**
- **Colouring model:** all of the above are path arguments.

Code against §2.2:
- `cat_common.make` builds exactly the stated catalog: C(8,3) = 56 states (35 for CB = 4), cells, capH = number of nonzero columns, cupH = f₁, and D′.
- `owner.py` families:
  - P1–P4. P3 and P4 with a missing P are the constant false. That is valid: the actual label lies in D′ of the actual direction.
  - L1–L3 and T0–T2. The thresholds are fully defined by T0/T1/T2 and L2.
  - Gcup/Gcap. Here `thr` returns False above the ceiling, or when no label of D′(y→z) reaches k + 1. Both cases are valid.
  - A. For state ∅ there is no clause.
  - W. W2 covers k ≥ 3; k = 2 is covered by W1's P[t,x]. The predecessor's state forms a feasible triple with (x, y).
  - S. Each clause forbids one alternating 3-subsequence of the 4 signs, so together they say "at most one sign change". That is the signotope property of x-sorted points.
  - C1–C4. `polys` = [(3,6), (4,5)] for the target and [(4,5)] for CB = 4. The types (2,7), (5,4), (6,3) and (7,2) are excluded by the ceilings.
  - F and K. K is a one-sided Sinz counter, satisfied by "≥ j holes among the first i".
- Every clause that contains an `ori` literal also contains the P (or threshold or chain) literals of its pairs. So the semantic value of `ori` on unoccupied triples is irrelevant.
- `--link`: family CL is valid (a b-cup ending with (j,k) forces d₂(j,k) ≥ b − 1), and the dropped clauses only weaken the CNF.
- `--sigmax`: a sub-family of S.
- `--nosig`: no S clause. Confirmed by the generator statistics of the N = 37 CNF, which have no family S.
- `owner_v1.py` against `owner.py`: the diff touches only the `--link`/`--sigmax` machinery and the guards for missing chain variables, which are no-ops without `--link`.
- `addrows.py`: one-sided counters over the `occ` variables. The families are S1 = {f₁ ≤ 4} (35 states), S2 = {f₃ ≥ 1} (35), B1 = {f₃ = 0} (21), B2 = {f₁ = 5} (21) and ALL (56).
- Row arguments of §2.3, re-derived:
  - S2: if a 4-cap a b c p ends at p, then (c,p,q) is a cup for every q > p, so c followed by a 6-cup from p is a 7-cup.
  - B2: with a 6-cup x₁…x₅p and a 4-cap p y₂ y₃ y₄, the triple (x₅,p,y₂) gives a 7-cup or a 5-cap.
  - All four are path arguments, so they hold for colourings. The external bounds they use are exactly the §5.1 statements, in the matching model.
- **"Exactly N".** K says at least N states are occupied, and the row ALL says at most N. Every hypothesis (general position, distinct x, no 5-cap, no heptagon, or the path versions for colourings) passes to subsets, and states and rows are recomputed for the subset. So UNSAT at N = 37 alone excludes every set with ≥ 37 points. The rungs N = 38–41 are independent, weaker certificates and are **not needed** for 36.
- Baek encoder `etv_sat2_orig.py` (n = 17, maxcap 3, maxcup 6, gon 7). Signotope axioms and chains are as stated. The no-4-cap clause is SC₃(s,i,j) ∧ cap(i,j,k) → ⊥, and the polygon type is (3,6) only; all other heptagon types contain a 4-cap or are the excluded 7-cup. Sound for point sets, and sound for colourings without its first 19,040 = 8·C(17,4) clauses.

## 2. Certificates (commands in `X/run/regen37.sh`, `lemmas.sh`, `ctl1.sh`, `sl41.sh`)

| CNF (regenerated by E) | SHA-256 (E) = record | LRAT | cake_lpr by E |
|---|---|---|---|
| `owner_v1.py 3 4 7 26` | `9646633e…` yes | W `om_s56_N26.lrat`, `642b4660…` = record | `s VERIFIED UNSAT` (heap 1000 MB, 12.6 s) |
| `owner_v1.py 3 4 7 26 --nosig` | `df8ace7f…` yes | W `om_s56_N26_nosig.lrat`, `7d40c209…` = record | `s VERIFIED UNSAT` (7.7 s) |
| `etv_sat2_orig.py 17 3 6 out 7` | `d76bf0e3…` yes | W `pos_hep47_n17.lrat`, `3a2a1aba…` = record | `s VERIFIED UNSAT` |
| the same minus its first 19,040 clauses (my own cut) | `09136d73…` yes | W `pos_hep47_n17_nosig.lrat`, `54638b1c…` = record | `s VERIFIED UNSAT` |
| `owner.py 3 5 7 37 --nosig` + `addrows` S1:25 S2:25 B1:16 B2:16 ALL:37 | `8762b9f0…` yes | deleted | not possible (see Verdicts) |
| N = 38 `--nosig` (`owner.py`) | `d35b0c4f…` yes | deleted | not possible |
| N = 40 `--sigmax 1 --link` | `d6fc98d8…` yes | deleted | not possible |
| N = 41 `--sigmax 1 --link` | `047fd356…` yes | deleted | not possible: heap test failed (below) |
| N = 41 `--nosig` (`owner_v1.py`) | `dafcc24c…` yes | deleted | not possible |

`W/run` also keeps eight of these nine CNFs, all except N = 41 `--nosig`. Their SHA-256 values equal the recorded ones (re-hashed by E at 21:10).
Heap tests: `cake_lpr --CML_HEAP_SIZE=1150` with an empty proof on the N = 37 CNF and on the N = 41 `--sigmax 1 --link` CNF ended both times with `CakeML heap space exhausted` (RSS 1.18 GB, 26–27 s). So a heap of 1,150 MB does not even hold the CNF. My planned
independent re-solve of the N = 41 rung was therefore aborted before CaDiCaL started.
Negative control for cake_lpr: the geometric (5,6) proof against the signotope-free CNF gives
`c Checking failed at line: 0. Reason: clause index unavailable: 1753568` with **exit status 0**, and no verdict line.
The `data/*.cake` files of the record contain the lines `s VERIFIED UNSAT` with the hashes quoted in §6.2. For N = 37,
the first check failed at heap 2,600 MB, and the second passed at 4,200 MB with the same hashes. The CaDiCaL log
`W/run/lad_ns37_N37.log` is consistent with this:
- Version 2.1.3, `--lrat=true --binary=false`, input `run/lad_ns37_N37.cnf`;
- header `p cnf 457861 5569650`, the same as my regenerated CNF;
- `s UNSATISFIABLE` after 8,848,423 conflicts, exit 20.

This is a log-level consistency check only, not a verification.

## 3. Positive and negative controls (own code: `my/ptcheck.py`, `my/semunits.py`, `my/colcheck.py`, `my/modelcheck.py`)

**Point sets** (`ptcheck.py`, exact integers). Two methods: a DP (longest cap, longest cup, largest convex polygon = max
over (s,t) of cap(s..t) + cup(s..t) − 2), and brute force (every 7-subset tested by a monotone-chain hull, every 5-subset tested as a cap).

| set | n | general position | cap / cup / largest polygon | brute force: convex 7-subsets, 5-caps |
|---|---|---|---|---|
| `etv757.json` and mirror | 26 | yes | 4 / 6 / 6 | 0, 0 |
| `etv756.json` | 25 | yes | 4 / 5 / 6 | 0, 0 |
| `etv747.json` | 16 | yes | 3 / 6 / 6 | 0, 0 |
| `etv656.json` | 15 | yes | 4 / 5 / 5 | no convex 6-subset |

**Semantic positive controls** (`semunits.py`). From coordinates or a colouring alone, my code computes:
- the labels, the states and the owners;
- on the data: injectivity, d ∈ D′(I(u)→I(v)) (separation and Lemma R) and corner attainment; 0 failures everywhere;
- the values of all primary variables (`occ`, `P`, `Lab`, `cupge`, `capge`, `ori`; for the target catalog that is 38,522 units).

Only the variable names come from the generator. It then reduces the CNF under these units; a clause with no literal left counts as
falsified. CaDiCaL decides the residual, which contains only the witness, chain and counter variables.

| CNF (generated by E) | configuration | falsified | residual |
|---|---|---|---|
| (3,5,7,26) `--nosig` + S1 S2 B1 B2 + ALL:26 (the flags of the N = 37 rung) | ETV 26; ETV 26 mirror | 0; 0 | SAT; SAT. The mirror model satisfies **all 5,569,804 clauses** of the unreduced CNF and occupies exactly the mirror's 26 states (`modelcheck.py`, EXACT). |
| the same, `--sigmax 1 --link` (flags of N = 40, 41) | ETV 26; mirror | 0; 0 | SAT; SAT |
| the same, full model (all 9,165,336 packets; 14,735,140 clauses) | ETV 26; mirror | 0; 0 | SAT; SAT |
| (3,5,7,2) `--nosig` + S1 S2 B1 B2 | 8 random subsets (14–23 points) of ETV 26 or its mirror; `etv747` and mirror; `etv656` and mirror | 0 in all 12 | SAT in all 12 |
| (3,5,7,27) `--nosig` + rows + ALL:27 | the 27-vertex colouring (non-signotope) | 0 | SAT |
| (3,4,7,25) full (`owner_v1.py`) | ETV 25 (`etv756`); mirror | 0; 0 | SAT; SAT |
| (3,4,7,2) `--nosig` | the 18 vertices of the 27-colouring where no 6-cup path ends: a colouring with longest cap 4, longest cup 5, no weak heptagon, 94 violated packets | 0 | SAT |

The rows are exercised at their bounds: the ETV 26 set has exactly 25 owners in S1 and 16 in B1, and it meets K and ALL at N = 26 exactly.

**Negative controls**: the test detects violations.
- The 27-colouring against the full (3,5,7,27) model falsifies **766 = 2 × 383** signotope clauses. Each violated 4-tuple falsifies exactly two clauses.
- The 18-vertex colouring against the full (3,4,7,2) model falsifies **188 = 2 × 94**.

**CNF identity across N** (`my/diffN.py`). After every clause that mentions a counter variable (`cnt`, `rc`) is removed, the N = 37 CNF and the
controlled N = 26 CNF are **identical in order**: 5,561,940 clauses with the same variable names. They differ only in 7,710 against
7,864 counter clauses (K plus the five rows).

**Counter clauses of the exact N = 37 CNF** (`my/countertest.py`). I took the 7,710 counter clauses plus units for
all 56 `occ` variables, with occupancy patterns I constructed (COMPUTED):

| pattern | expected | result |
|---|---|---|
| (a) 37 states with S1 = 25, B2 = 12, S2 = 21, B1 = 16 (S1 and B1 at their bounds) | accepted | SAT |
| (b) 38 states, all rows respected | rejected by ALL ≤ 37 | UNSAT |
| (c) 36 states | rejected by K | UNSAT |
| (d) 37 states with S1 = 26 | rejected | UNSAT |

So the N = 37 CNF = the controlled non-counter part + counters that encode exactly "37 occupied, rows respected".

**SAT at the conjectured sizes.**
- (3,4,7,25) full model without units: `s SATISFIABLE` in about 1 s (COMPUTED).
- At the target size 26, every rung's flag set is satisfiable, witnessed by the ETV set (above).
- Known-answer checks (`owner.py`, no rows, COMPUTED) all came out as expected: owner(2,5,7,17), (2,4,6,12), (3,3,6,15) and (2,6,8,23) UNSAT; (2,5,7,16), (2,4,6,11), (3,3,6,14), (2,6,8,22) and (3,3,7,20) SAT.

## 4. The 27-vertex colouring (`my/colcheck.py`, EXACT)

For every pair (s,t), the program computes the *exact sets* of vertex counts of cap paths and of cup paths from s to t (not only the
maxima). It does not use the CNF.

Output on `data/colouring27_nosig.json` (SHA-256 `b42aebe4…`, as recorded):
- n = 27, 1,918 positive triples;
- longest cap path 4, longest cup path 6;
- **no pair (a, b) with a + b ≥ 9** on common end-vertices (2-vertex paths included);
- largest weak polygon with a, b ≥ 3: 6;
- 383 of 17,550 violated packets;
- the 27 incoming states are distinct and equal to `states_in_order`.

The claims of §7 table rows 1–3, 6 and 7 are reproduced; row 7 is the semantic control in §3.
Rows 4–5 were also reproduced (COMPUTED; `X/run/ctl5.sh`, own unit script `my/colunits_pos.py`):
- `etv_sat2_orig.py 27 4 6 · 7` (269,802 clauses), without its first 140,400 = 8·C(27,4) signotope clauses, plus the 2,925 units of χ: `s SATISFIABLE`;
- with them: `s UNSATISFIABLE`.

## 5. Problems found

1. **The N = 37 certificate (and N = 38, 40, 41) cannot be re-checked as published.**
   - The LRAT files were deleted right after cake_lpr ran. The CERTIFIED label rests on a log line.
   - An independent re-check needs a re-solve of the regenerated CNF: CaDiCaL 2.1.3 `--lrat --no-binary`, about 70 min and 1.5 GB at N = 37. It then needs cake_lpr with `--CML_HEAP_SIZE=4200`, in a unit of about 4.5 GB.
   - Until a verifier with that budget has done this, M(5; 7) ≤ 36 is "CNF certified per log + written argument". It is not independently confirmed.
   - No defect was found in anything that could be checked.
2. **One certified CNF is not in W, contrary to §10/§11** ("W keeps `run/*.cnf` … of the certified rungs").
   - `W/run` keeps eight of the nine certified CNFs. I re-hashed all eight at 21:10, and they equal the recorded hashes.
   - The N = 41 `--nosig` CNF (`lad_nsc_N41.cnf`, `dafcc24c…`) is missing; only its `.names.pkl` and logs remain.
   - This is harmless: it regenerates from `owner_v1.py` with the recorded hash (§2 above).
   - (An earlier draft of this file said that no certified CNF was in W. That was my error: a truncated directory listing.)
3. **Novelty wording, status item 4 and §7.**
   - "The colouring version of ETV(7; 5, 7) is false" needs a qualifier: the **weak-heptagon** version.
   - NOVELTY20261113B §6 (C4, item 5) quotes Balko–Valtr's abstract value N^(5,7,7) ≥ 27, so the abstract analogue of exactly this case already fails in their (strong-polygon) model. The record mentions their 27-vertex colourings only in §9.1.
   - §7's phrase "refines the known failures of the colouring analogue of the full conjecture at k = 7" should name this specific predecessor. The item-8 caveat (definitions not compared) stands.
   - The 27-colouring is still a correct object (§4).
4. **Wording**, status item 4 and §7: "26 cannot be proved ... without four-point axioms". What is shown is narrower: no proof can use only the path and weak-polygon properties of a triple colouring. The colouring violates four-point packets, but it is not shown that four-point information is the only realizability information that would suffice. A minor overstatement.
5. **cake_lpr exits with status 0 when it rejects a proof** (§2 above). The record's scripts grep for `s VERIFIED UNSAT`, which is correct. `vfy_exit` in `vfy.sh` logs is not a verdict.
6. Cosmetic: the order and naming of W1–W3 in the §2.2 table differ from the generator's family names (in the code, W3 is the disjunction). No effect.

## 6. Not done

- The re-solve and cake_lpr of any target-catalog rung (budget; see Problem 1).
- The unchecked N = 36 case-B proof (not claimed by the record; it needs about 4.5 GB).
- No literature search of my own. The novelty points rest on NOVELTY20261113B §§3, 6 (C4) and 10.
