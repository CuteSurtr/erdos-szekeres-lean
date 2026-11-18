# VERIFY_D1: adversarial check of DELTA2N20261113 (verifier D1, phase 2, 13 November 2026)

Verifier D1, 20:48–22:05 KST. I read the record's README in full first (the version of 20:47). Scratch
directory `/home/jay/research/data/verify-D1-20261113` (abbreviated V; not in Git). At most one thread at a
time, in units `nov13c-vfy-D1-*` (MemoryMax 1.5 GB or less, MemorySwapMax 0); five short checks ran while
the main unit was frozen (`systemctl --user freeze` / `thaw`), so two of my processes never ran at once. I changed no file of the record. This file is the only
one I wrote in the repository. No git operation.

**Status: FINAL (21:47 KST).** All D1 units have ended; none was stopped by the memory guard.

## 1. Verdicts

| claim of the record | verdict | short reason |
|---|---|---|
| Weak Conj(6) holds for every point set (11 CNFs m = 5..15, base refutation at 16, all cake_lpr) | **confirmed** (CERTIFIED) | all 12 CNFs regenerated, hash-equal, clause-multiset-equal to my own encoding, re-certified with byte-identical proofs; a second, independent encoding certified for m = 8..14 and the base at 16 (§2.1–§2.4) |
| Lemma S (soundness of the abstract model, record §2) and the completeness argument (m ≤ 15 + base at 16 covers all sizes) | confirmed | §3, §2.4 |
| Complete strong cases (4, 5), (4, 6), (5, 5) | confirmed | every CNF of each chain re-certified, proofs identical (§2.5) |
| Complete strong case (4, 7) | **not confirmed by me** in one step | all 12 CNFs regenerated and equal to my encoding; m = 6..15 and the base at 17 re-certified; for m = 16 CaDiCaL reproduced the record's proof byte for byte, but cake_lpr ran out of heap at 1000 and 1300 MB, the most my 1.5 GB cap allows; the record's own check (default heap, 18:05) is the only one (§2.5) |
| PROVED lemmas of record §6 (Lemmas 1–5) | confirmed | §4; one gap in a side claim of record §2 (§5, problem 2) |
| Head item 1 wording "the first complete case of the conjecture" | weaker than stated | weak Conj(5) is complete by the record's own (5, 5) result (§5, problem 1) |
| Consistency with NOVELTY20261113B §8/§10 (strong form false at (5, 6) with 15 and at (6, 6) with 16 real points) | confirmed: consistent | exact re-check of both sets (§2.6) |

Problems found: §5. No counterexample to any claimed statement was found.

## 2. Checks run

Tools: Python `/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python`, CaDiCaL 2.1.3
(`/usr/bin/cadical`), cake_lpr (`~/.local/bin/cake_lpr`, symlink to
`/home/jay/research/sat/tools/cake_lpr/cake_lpr`). Every certification below is
`cadical -q -t T --lrat=true --binary=false F.cnf F.lrat` (exit 20) followed by
`cake_lpr --CML_HEAP_SIZE=H --CML_STACK_SIZE=100 F.cnf F.lrat`, and counts only if its output is exactly
`s VERIFIED UNSAT`. Proofs were deleted after the check; their SHA-256 is recorded in V/status*.log.

My scripts (V; SHA-256):
- `myenc.py` (006a3f59…): my own encoder, written from the mathematics in the README, not from
  `eager_cert.py`. NAT = the encoding the README describes, over symbolic objects (triples, 4-caps,
  4-sets, 5-sets). ALT = a different formulation of the same statement (see §2.3).
- `compare.py` (d1905dc8…): regenerates the record's CNF with the record's `Enc` (imported read-only, written
  to V), hashes it, looks it up in `data/cnf_hashes.tsv`, maps its variables to objects and compares the
  clause multiset with NAT.
- `sigequiv.py` (47bbc4aa…), `realsets.py` (c0f28c7b…), `checkmodel.py`: §2.3, §2.6.
- `negctl.sh`: negative controls of the cadical/cake_lpr chain (§2.2).
- Drivers `driver.sh`, `driver2.sh`, `driver4.sh`, `driver5.sh`, `driver7.sh`; logs `status.log`,
  `status2.log`, `status4.log`, `status5.log`, `status7.log`, `compare.log`, `compare2.log`, `compare5.log`.

### 2.1 Is the CNF for size m the statement for all signotopes on m points? (encoding check)

How the exists-forall is quantified (read in `tools/eager_cert.py`, class `Enc`, and confirmed on the files):
the negation "some valid σ defeats every Δ" is ∃σ ∀Δ (Δ fails). The ∀Δ is expanded: one clause per subset Δ
of [m], all 2^m of them (`pool(0, m)`; no sampling, no symmetry breaking, no size window).
"Δ fails" = ⋁{Y_K : K ⊆ Δ, |K| = a−1} ∨ ⋁{Z_G : G ⊆ [m]∖Δ, |G| = n−1}, with one-directional witnesses
Y_K → (K is a cap), Z_G → (all 4-subsets of G convex). So "for every 4-cap-free Δ" is expressed as "for
every Δ: Δ contains a 4-cap, or a convex pentagon avoids Δ". This is the right quantification.

Check 1 (clause count, by hand for (5, 6, 15)): 8·C(15,4) + C(15,5) + 11·C(15,6) + 2·C(15,4) + 4·C(15,4)
+ 5·C(15,5) + 2^15 = 10,920 + 3,003 + 55,055 + 2,730 + 5,460 + 15,015 + 32,768 = 124,951, the number in the
record's table. Base (5, 6, 16): 8·1,820 + 4,368 + 11·8,008 = 107,016 (record: 107,016).

Check 2 (regeneration, hash, clause multiset). `compare.py a n m form V/work` for each line below. Output
(`V/compare.log`, `V/compare2.log`): every regenerated CNF has the SHA-256 of its line in
`data/cnf_hashes.tsv`, and its clause multiset, after mapping variables to objects, is **equal** to the
multiset of my NAT encoding:

| case | CNF SHA-256 (prefix) | clauses | record CNF = NAT (multiset) |
|---|---|---|---|
| F(5,6,5..15; weak) | d239a2fb… (m = 5) … 0615078f… (8) … 728df2e7… (14), 5c656cdd… (15) | 108 … 124,951 | equal for all eleven m = 5..15 |
| base(5,6,16) | b36eb295… | 107,016 | equal |
| base(4,5,8), base(4,6,12), base(4,7,17), base(5,5,9) | cf08995d…, 35847bf2…, 4c368ea5…, e7ab3460… | 854; 9,075; 138,108; 2,016 | equal |
| F(4,5,4..7), F(5,5,4..8), F(4,6,5..11), F(4,7,6..16), all strong | (25 + 2 files) | up to 277,956 | equal for all 27 |

So the record's CNFs are exactly the statement as the README defines it, read independently. What remains
to trust is the definitions themselves (§3) and the solver/checker chain.

### 2.2 Re-certification of the record's own CNFs (regenerated, hashes equal)

V/status.log, V/status2.log. "LRAT identical" = my proof has the size and SHA-256 recorded in
`data/cnf_hashes.tsv` (CaDiCaL is deterministic; the time limit does not change the search).

| CNF | CaDiCaL | LRAT bytes | LRAT identical to the record | cake_lpr |
|---|---|---|---|---|
| base(5,6,16) | UNSAT, 99.4 s | 283,141,758 | yes (bfc1d82e…) | `s VERIFIED UNSAT`, 7.5 s |
| F(5,6,m; weak), m = 5..13 (V/status5.log) | UNSAT, ≤ 12.1 s | 85 … 143,304,849 | yes, all nine | `s VERIFIED UNSAT` (9/9) |
| F(5,6,14; weak) | UNSAT, 139.3 s | 979,078,411 | yes (9a76200a…) | `s VERIFIED UNSAT`, 24.1 s |
| F(5,6,15; weak) | UNSAT, 848.7 s | 2,637,382,249 | yes (f410a052…) | `s VERIFIED UNSAT`, 83.8 s (heap 1150 MB) |
| base(4,5,8), base(4,6,12), base(4,7,17), base(5,5,9) | UNSAT, ≤ 1.4 s | 1,193; 33,891; 6,374,580; 23,991 | yes, all four | `s VERIFIED UNSAT` (4/4) |
| all 25 strong CNFs (4,5) m = 4..7, (5,5) m = 4..8, (4,6) m = 5..11, (4,7) m = 6..14 | UNSAT, ≤ 25.0 s | up to 249,697,326 | yes, all 25 | `s VERIFIED UNSAT` (25/25) |

The CNFs with m ≤ a + n − 4 contain empty clauses (counted: 25, 35, 35 lines `0` for (5,6) m = 5, 6, 7; 10–21
for the trivial strong ones; none for (5,6) m = 8): a Δ with a − 2 points then has a complement too small to
hold an (n−1)-set, so its pool clause is empty. That is correct, the statement is trivial there; five of
them have a 0-byte proof.

Negative controls of the checker chain (`negctl.sh`, V/negctl.log): the correct pair (F(5,6,10), its proof)
gives `s VERIFIED UNSAT`; the same proof without its last three lines gives `c empty clause not derived at
end of proof`; the proof of m = 10 against the CNF of m = 11 gives `c Checking failed at line: 0`. So the
`s VERIFIED UNSAT` lines above are not produced unconditionally.

### 2.3 Independent second encoding (ALT) for weak Conj(6)

ALT (`myenc.py`, `alt_build`) differs from the record's formulation in every defined notion: signotope axiom
as the 8 forbidden 4-vectors (4-literal clauses); caps as "all triples −"; hexagon-freeness of the base as
"some 4-subset of every 6-set is not convex" (with C_T ↔ convexity of T); the pentagon witness of the pool as
"some cap/cup split of G" (weak gon) instead of 4-subset convexity. For point sets both encodings say the
same thing, so an UNSAT answer of ALT is an independent proof of the same point-set statement.

`sigequiv.py` (from-scratch enumeration of all signotopes on 4, 5, 6 points: 8, 62, 908, the known
numbers): for every subset of 4–6 points, "all 4-subsets convex" ⟺ "weak gon", and "consecutive triples −"
⟺ "all triples −". Output: `conv4!=weakgon: 0  consec-cap!=all-triples-cap: 0` at m = 4, 5, 6 (19,976
subsets at m = 6). So ALT and the record's CNF are also equivalent on signotopes for n = 6.

| ALT CNF | vars / clauses | CaDiCaL | LRAT bytes | cake_lpr |
|---|---|---|---|---|
| base(5,6,16) | 2,380 / 41,496 | UNSAT, 311.8 s (wall, includes a ~50 s freeze) | 976,794,344 | `s VERIFIED UNSAT`, 25.9 s |
| base(5,6,15) (sanity) | 1,820 / 29,848 | SAT; the model is a signotope with 0 five-caps, 0 convex hexagons (both notions), 263 convex pentagons (`checkmodel.py`) | – | – |
| F(5,6,8; weak) … F(5,6,13; weak) | 700/3,140 … 13,299/57,670 | UNSAT, 0.003 s … 35.5 s | 3,839 … 319,437,414 | `s VERIFIED UNSAT` (6/6) |

| F(5,6,14; weak) (V/status7.log) | 20,384 / 91,459 | UNSAT, 332.4 s | 1,735,631,145 | `s VERIFIED UNSAT`, 44.1 s (heap 1150 MB) |

ALT at m = 15 was not run (several hours on one thread). There the verdict rests on the record's CNF, which
equals my NAT encoding and was re-certified (§2.2).

### 2.4 Why m ≤ 15 plus the 16-point refutation covers all sizes

- m ≤ 4: no convex pentagon, Δ = ∅ works. m = 5, 6, 7: trivial (a 3-point Δ leaves at most 4 points); the
  CNFs contain an empty clause.
- m = 8..15: F(5,6,m; weak) UNSAT (record, cake_lpr; every one re-run here with an identical proof, §2.2; ALT
  independently for m = 8..14, §2.3).
- m ≥ 16: base(5,6,16) UNSAT means no signotope on 16 points has no 5-cap and no convex hexagon. Validity
  (no a-cap, no convex n-gon) is defined by triples inside a subset, so it passes to every sub-configuration;
  a valid set with m ≥ 16 points would have a valid 16-point subset. So there is nothing to prove.
- 16 is the Erdős–Tuza–Valtr bound N(6; 5, 6) + 1, not ES(6) = 17: Σ_{i=0}^{3} C(4, i) = 15. The 15-point
  set of NOVELTY E4 is valid (§2.6), so 15 is attained. Re-certified here twice: the record's base CNF
  (identical proof) and ALT's base CNF (a different proof).

### 2.5 Strong complete cases

(4, 5), (4, 6), (5, 5): every CNF of the chain (m = n−1 .. m₀−1 and the base at m₀ = 8, 12, 9) was
regenerated, found equal to NAT, and re-certified with an LRAT proof identical to the record's (§2.2).
(4, 7): m = 6..14 and base(4,7,17) the same; m = 15, 16 regenerated (hash equal, multiset equal) and
re-certified in unit `nov13c-vfy-D1-s47` (V/status4.log):

| CNF | CaDiCaL | LRAT bytes | identical to the record | cake_lpr |
|---|---|---|---|---|
| F(4,7,15; strong) | UNSAT, 129.8 s | 1,046,577,649 | yes (43c5f777…) | `s VERIFIED UNSAT`, 36.0 s (heap 1000 MB) |
| F(4,7,16; strong), first try | UNSAT, 402.9 s | 1,862,165,342 | yes (12ddb983…) | **failed: `CakeML heap space exhausted.`** after 11.5 s with `--CML_HEAP_SIZE=1000` (no verdict) |
| F(4,7,16; strong), retry (`driver7.sh`, heap 1300 MB, stack 50 MB) | UNSAT, 407.7 s | 1,862,165,342 | yes (12ddb983…) | **failed again: `CakeML heap space exhausted.`** after 31.1 s (no verdict) |

So the last link of the (4, 7) chain is not re-verified here: the proof is the record's proof (byte-identical),
but its check needs more than 1300 MB of CakeML heap, above what one verifier unit may use (1.5 GB, stopped
by the guard at 95 %). The record checked it at 17:51–18:05, before the memory policy, i.e. with cake_lpr's
default heap (`data/queue1.log` lines 139–140; `data/results_eager.jsonl`: `s VERIFIED UNSAT`, 103.2 s). I
have no reason to doubt that check, but I could not repeat it. Its §9 sentence "`--CML_HEAP_SIZE=900` …
sufficed for every proof of this record" does not cover this proof (§5, problem 5).

### 2.6 Consistency with NOVELTY20261113B §8 and §10

`realsets.py`, exact integers; convex position by the point-in-triangle test, caps/cups by consecutive
triples in x-order; all 2^m subsets Δ. The 16 points as quoted in NOVELTY §8.

- E1, the public 16-point set, (a, n) = (6, 6): valid; 47 five-caps, 72 five-cups, 292 convex pentagons, 0
  convex hexagons; Δ with no 5-cap meeting every pentagon: 5,175 (weak); of these, pentagon-free: **0**
  (strong). Matches NOVELTY E1 and E2.
- E4, the 15 points after deleting (0, 1955462) and reflecting y → −y, (a, n) = (5, 6): valid (0 five-caps,
  0 convex hexagons); 72 four-caps, 47 five-cups, 220 convex pentagons; weak Δ: **316**; strong Δ: **0**.
  Matches NOVELTY E4.

So the strong form fails at (5, 6) on a real 15-point set and at (6, 6) on a real 16-point set, and the weak
form holds on both. This is consistent with DELTA2N: (5, 6) strong and (6, 6) strong are certified only up to
m = 11, and weak Conj(6) predicts a weak Δ on E4 (there are 316). NOVELTY's request that these sets be re-run
before a record relies on them is met by this check (an independent pure-Python script, not the record's
`verify_cex.py`).

## 3. Lemma S and the completeness argument (record §2)

Lemma S is correct. Put t := σ and every witness to its true value. Base clauses hold because σ is a valid
signotope; witness clauses are one-directional implications whose right sides are then true; the clause of a
failing Δ holds through a true witness. The record's code has exactly these clauses (§2.1), with no extra
constraint (no symmetry breaking, no "reduced" clauses in the main CNFs: the regenerated, hash-equal files are
multiset-equal to NAT, which has none).

For point sets: σ_P is a signotope; "no 5-cap and no convex hexagon" makes σ_P satisfy the base (a convex
hexagon's upper chain is a cap of at most 4 points, its lower chain a cup); a 4-cap of P has its consecutive
triples clockwise; a convex pentagon of P has all 4-subsets in convex position, and for x < y < z < w,
"y in triangle xzw" ⟺ σ(xyz) ≠ σ(xyw) and "z in triangle xyw" ⟺ σ(xzw) ≠ σ(yzw) (x, w are hull vertices).
So F UNSAT ⟹ the statement for all point sets in general position with distinct x-coordinates. The
completeness argument (heredity of validity, base refutation) is correct (§2.4).

## 4. PROVED lemmas of record §6

I checked each proof line by line.
- Lemma 1: correct (o followed by the (a−1)-cap would be an a-cap; the mirror likewise).
- Lemma 2: correct. (2): the induction step uses that the cap (p, d, …) inside L^{i−1} is a cap of S, so
  Lemma 1 applies and d ∈ L^{i−1}. (3): the cup part has n + 1 − c points. "L^{a−2} contains no gon" follows
  because Q₀ ∪ … ∪ Q_{a−3} = S ∖ L^{a−2}.
- Lemma 3: correct. (1) also covers a one-point cup (c, p, d). (3) proves the right-end statement; the
  left-end statement is the mirror (not written, immediate).
- Lemma 4: correct.
- Lemma 5: correct. (1) uses that a cap and a cup from u to v share no inner point (σ(u w v) is − on a cap and +
  on a cup) and that sub-chains of caps/cups are caps/cups (proved in record §2). The converse "a longest cap
  and a longest cup of a saturated pair form a gon" needs "weak gon ⟹ convex in the 4-subset sense"; see §5,
  problem 2.
- The fractional remark (weight ½) is correct: a 4-cap gets 2 ≤ 3, a pentagon 2.5 ≥ 1.

## 5. Problems

1. **Wording, "the first complete case of the conjecture" (record head, item 1).** Weak Conj(n) is defined as
   D(5, n; weak). The record itself certifies D(5, 5; strong) completely (m = 4..8, base at 9; re-certified
   here), and the strong form implies the weak form, so weak Conj(5) is also complete; so are weak
   D(4, 5), D(4, 6), D(4, 7). Weak Conj(6) is the first complete case with a < n (and the first where the
   strong form fails), not the first complete case. The mathematical claim is unaffected.
2. **Gap in a side claim of record §2:** "In every signotope a set is a convex k-set iff it is a weak gon" is
   argued in writing only in one direction (4-subset convex ⟹ weak gon). The converse rests on the exhaustive
   control C5 (k ≤ 7) and, for k ≤ 6, on my `sigequiv.py`. It is not needed for the point-set statement, and
   for n ≤ 8 the control covers every k that occurs (k ≤ n − 1 ≤ 7). Lemma 5 (1)'s converse half uses it in
   the same way. Suggest: state it for k ≤ 7 with the control as the proof, or add the argument.
3. **Novelty of (5, 5) strong** is not discussed in record §10: it is the n = 5 instance of the public
   two-class SPLIT question (GLitchfield experiment 0096, NOVELTY C5). Whether SPLIT(5) is settled there was not
   checked by NOVELTY or by me.
4. Minor: §4.1's phase-2 note says the first failure of (6, 6) strong lies "somewhere in 12–16". True, but
   GLitchfield's facts file (NOVELTY C5) reports that the split exists up to 15 points by their SAT check; if
   that is right the first failure is at 16. Not checked here.
5. **Heap statement and reproducibility, (4, 7) strong at m = 16.** Record §9 says the explicit heap of
   900 MB (1150 MB for the 5.9 GB proof) "sufficed for every proof of this record". The m = 16 proof of
   (4, 7) was checked before that change, with the default heap (about 4 GB), and it does not fit in 1000 or
   1300 MB (§2.5). Anyone re-running it with the record's current tools (`eager_cert.py`: inline heap 900 MB;
   `cake_deferred.sh`: default 1100 MB) gets no verdict. The record should state that this proof needs a
   CakeML heap above 1300 MB (the default heap, about 4 GB, worked at 18:05). The claim itself rests on that
   18:05 check, which I could not repeat within the verifier memory cap.
6. Record §8 says CNFs and proofs above 30 MB were deleted after the verdict; the CNFs are rebuilt
   deterministically and I confirm that for every CNF of the claims checked here (hashes equal), and that
   CaDiCaL 2.1.3 reproduces each recorded LRAT hash exactly (43 proofs, §2.2, §2.5).

No counterexample, encoding error, off-by-one, wrong inequality, hash mismatch or CERTIFIED-but-only-COMPUTED
label was found for the claims checked.

## 6. Files (V = /home/jay/research/data/verify-D1-20261113; not in Git)

Scripts `myenc.py`, `compare.py`, `sigequiv.py`, `realsets.py`, `checkmodel.py`, `negctl.sh`, drivers
`driver.sh`, `driver2.sh`, `driver4.sh`, `driver5.sh`, `driver7.sh` (`driver3.sh` was stopped while still
waiting; `driver6.sh` was stopped 40 s into its ALT m = 14 run to make room for the (4, 7) retry); logs `status.log` (main: compare, base 16, ALT, m = 14, 15, bases), `status2.log`
(strong chains), `status4.log` ((4, 7) m = 15, 16), `status5.log` ((5, 6) m = 5..13), `status7.log` ((4, 7)
m = 16 retry, ALT m = 14), `compare*.log`, `sigequiv.log`, `realsets.log`, `checkmodel.log`, `negctl.log`.
All LRAT files were deleted after their check; the regenerated CNFs are in V/work, V/work2, V/work5 and
V/hashonly.
