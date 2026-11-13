# Section ar, polish round 1: diff audit (lens: diff)

**Verdict: pass.** No blocker and no major finding. Three minor findings (m1–m3), all optional wording changes in
Remark `ar:rem:classes`.

Inputs: the passed version `snapshots/sections-r1pass/ar.tex` and `ar.map.tsv`; the current `sections/ar.tex` (797
lines) and `sections/ar.map.tsv`; the fix log `reviews/ar-polish-r1-fix.md`; the four round-1 reports and
`reviews/ar-writer-concerns.md`. No earlier polish audit (`ar-p*-diff.md`, `ar-p*-referee.md`) exists.

Paths are relative to STAGE (`sections/`, `build/`, `reviews/`), to RES (`SYMLEAN/...`, `WRITEUP/...`, `C2FINAL/...`) or
to the repository root (`ErdosSzekeres/...`). Line numbers `ar.tex:N` refer to the current file.

## 1. Scope of the diff

- `snapshots/polish-r1-pre/` (the fixer's pre-edit snapshot) is byte-identical to `snapshots/sections-r1pass/` for
  both files. Every hunk is therefore the work of this round and is covered by the fix log.
- `diff -u` gives 16 hunks in `ar.tex` (752 → 797 lines) and 2 in `ar.map.tsv`.
- The 31 `\label`s are unchanged and in the same order, and the 30 statement heads (`\begin{...}[...]` lines) are
  byte-identical. Two statement bodies changed: `ar:lem:cp-affine` (bound variable renamed) and `ar:thm:main`(e)
  (a parenthesis added). Both were re-read against Lean (below).

## 2. Hunk-by-hunk check

| # | where (current) | change | check | result |
|---|---|---|---|---|
| H1 | ar.tex:8–15 | Introduction: hE is "a parameter of the theorem, so the transfer is an implication and asserts neither statement on its own"; "the Euclidean statement supplied by Theorem sr:thm:main" | consistent with Theorem ar:thm:transfer and Remark ar:rem:hE(1); the next sentence still says the five theorems are conditional | correct |
| H2 | ar.tex:17–23 | Overview: S contains three non-collinear points (general position, at least N ≥ 3 points), so some g^m fixes them and L^m = 1; T^{-1} carries the n points back | matches Proposition ar:prop:averaging(a), the proof of ar:thm:transfer (V = T'(U)) and Lean `AffineReduction.lean:1338–1360`, `:1413–1420` | correct |
| H3 | ar.tex:25–42 | Sources paragraph turned into a list | five SHA-256 prefixes recomputed (6d5ec90a4215, 2425500eefd1, f67955ac7091, 13667aa2d3dc, c7db9bbbb65e); lines 1–1058 of `SYMLEAN/AffineReduction.lean` equal `SymmetricReduction.lean` (cmp); §9 starts at 1059, §10 at 1467; `Orientation.lean:9`, `Basic.lean:15`, `OrientationGeometry.lean:66` are the cited declarations | correct |
| H4 | ar.tex:47–49 | axioms file "followed by a blank line, nine `#print axioms` lines and one `#check` line" | `wc -l` 1544; lines 1–1533 = `AffineReduction.lean` (cmp); 1534 empty; 1535–1543 the nine `#print axioms`; 1544 `#check @...heptagon_of_nontrivial_affineEquiv`; SHA-256 f6cb9372b174 | correct |
| H5 | ar.tex:50–51 | new bullet: `SYMLEAN/logs/runs.tsv` records both files compiled on 1 November 2026 with exit code 0 | runs.tsv: `AffineReduction.lean` 41cfc0b6 2026-11-01T14:54:56Z exit 0; `AffineReductionAxioms.lean` f6cb9372 2026-11-01T14:55:01Z exit 0 | correct |
| H6 | ar.tex:52–53, 62–63 | date and exit code removed from the two `.out` bullets | `.out` SHA-256 38d0b6f59398; `logs/AffineReduction.out` is 0 bytes | correct |
| H7 | ar.tex:64–66 | "the output of the `#check` line, in the same log as the axioms" | `logs/AffineReductionAxioms.out` lines 18–27 show the five classes as premises | correct |
| H8 | ar.tex:90 | M(M'z) = (MM')z for matrices M, M' | removes the clash with the threshold N | correct |
| H9 | ar.tex:93–96 | note: `Nat.iterate` recurses as g^{k+1} = g^k ∘ g; the form g^{k+1}(p) = g(g^k(p)) is `Function.iterate_succ_apply'`, used by the Lean proof of ar:lem:iter | Mathlib f897ebcf (same rev as the repository's lake-manifest): `Mathlib/Logic/Function/Iterate.lean:36–38` (`succ k, a => iterate op k (op a)`), `:169` `iterate_succ_apply' : f^[n.succ] x = f (f^[n] x)` inside `namespace Function`; `AffineReduction.lean:56` `open Function`, `:1205` uses it twice | correct |
| H10 | ar.tex:129–131 | `AffineEquiv.ext` justified: f_lin(v) = f(v) − f(0) | defining property with p = 0; checked symbolically (`build/ar_p1diff_algcheck.py`) | correct |
| H11 | ar.tex:364–366 | orient-affine proof: "the entries L00, L01, L10, L11 in place of the four parameters of lin2" (no reuse of b) | factor L00 L11 − L01 L10 = det L; sympy, including the translation | correct |
| H12 | ar.tex:427–430 | statement of ar:lem:cp-affine with S instead of s | Lean `:1263–1265`: `{s : Finset Point} (hs : ConvexPosition s) (f : Point →ᵃ[ℝ] Point) (hf : Injective f) : ConvexPosition (s.image f)` | exact |
| H13 | ar.tex:446–452 | Step 2 renamed; "By this identity and Step 1" | f(S)∖{f(q)} = f(S∖{q}) then Step 1; matches Lean `:1271–1272` (`Set.image_diff hf`, `AffineMap.image_convexHull`) | correct |
| H14 | ar.tex:471–475 | Definition ar:def:E: "the type of hE, up to two changes of notation" | Lean hE at `:1331–1332` (same at `:1424–1425`, `:1434–1435`, `:1445–1446`): `∀ (S) (g), GeneralPosition S → N ≤ S.card → IsEucIsometry g → g ≠ id → Invariant g S → HasConvexNGon n S`; quantifiers, five premises in order and conclusion match; the only differences are the renaming and the unfolding (curried premises read as "if ..., then", the usual reading) | accurate |
| H15 | ar.tex:507–509 | base case r = 0 of the common-period induction | g^0 = id; step g^{(r+1)m_i} = g^{m_i} ∘ g^{r m_i} | correct |
| H16 | ar.tex:522–523 | "Lemma ar:lem:lin2(b), applied to T = lin2(s, β/s, 0, t)" | factor st − (β/s)·0 = st; sympy | correct |
| H17 | ar.tex:552–558 | "Relation to Lean" completed | Lean steps exist with the stated roles: hα `:1362`, hδ `:1363`, hs `:1369`, ht `:1370`, hTiT `:1375`, hTTi `:1376`, hnT `:1377`, hiso `:1386`, hTinj `:1392` and hTiinj `:1393` (both `LeftInverse.injective` of the inverse identities), hne' `:1394`, hgp' `:1401–1403` (`generalPosition_image_of_orient (D := s * t - β / s * 0)` with `orient_lin2`; D is used nowhere else), hinv' `:1407` | accurate, and complete for the statements of (b) and (c) |
| H18 | ar.tex:597–598, 745 | lead sentences of Remarks ar:rem:hE and ar:rem:scope | the remarks have three and four items | correct |
| H19 | ar.tex:664–667 | Theorem ar:thm:main(e): "(in this part b and f are real numbers)" | Lean `:1521–1526`: `(a b c d e f : ℝ) (hdet : a * d - b * c ≠ 0) (hg : ∀ p, g p = ![a * p 0 + b * p 1 + e, c * p 0 + d * p 1 + f])`; statement otherwise unchanged | exact |
| H20 | ar.tex:688–691 | Lean-proof summary of ar:thm:main | Lean `:1477–1529`: each proof is a two-line term; (a) `:1506–1507`, (c) `:1495–1496`, (d) `:1484–1485`, (e) `:1528–1529` pass `heptagon_of_nontrivial_isometry h2 h3 h5 hm1 hm0` as hE with `(by norm_num)` for 3 ≤ 33; (b) `:1516–1517` applies `heptagon_of_nontrivial_affineEquiv` after converting `g '' ↑S ⊆ ↑S` to `Invariant` | accurate |
| H21 | ar.tex:703–739 | Remark ar:rem:classes rewritten (sources; mirror bullet; four kinds of evidence) | §3 below | supported; minor wording m1–m3 |
| H22 | ar.tex:791–792 | Coverage: description of the axioms file | as H4 | correct |
| H23 | ar.map.tsv | multi-name rows: ", " → "; " in columns 3 and 4 (10 rows) | `build/ar_p1diff_mapcheck.py`: header correct, 30 rows × 5 fields, ASCII, no CR, final newline; label, kind, names and file:line of every row equal the statement head, in order; notes unchanged | consistent |

Every hunk was also checked for machine paths, tool names, rigor vocabulary ("verified", "certified",
"proved", "proven"; case-insensitive) and macros. There are no hits in `ar.tex` or `ar.map.tsv` beyond pre-existing,
correct wording ("re-prove", "no unproved claim") and the new "prove 3 ≤ 33 by norm_num", which describes the Lean term.

## 3. The new claims of Remark ar:rem:classes, checked against the records

| claim (ar.tex) | record evidence | result |
|---|---|---|
| sources "SYMLEAN/README.md §§5, 6 and 9; WRITEUP/SYMMETRIC.md §§1, 3 and 4" (703–704) | the sections exist and contain what the remark draws from them (below) | ok |
| mirror classes: Lean-checked, `mirrorOneAxis33_proved` line 4274, `mirrorNoAxis34_proved` line 4282, obtained without SAT input "from ... Baek's theorem ... and the mirror reduction" (706–711) | `SYMLEAN/mirror/ReductionThreeClasses.lean:4274`, `:4282`, `:4303` are the cited theorems; `SYMLEAN/mirror/axioms.out` lines 23–24 and 37–38 give `[propext, Classical.choice, Quot.sound]` for both; README Status and §5: "follow from Baek's theorem ... by the mirror reduction", "Lean-checked, no SAT input"; mb:thm:classes, mb:thm:baek, mb:thm:main3 are defined in `sections/mb.tex` | ok |
| "computer-assisted claims of the records C2FINAL (with C2C34 and C2P–C2P5), C3FINAL and SYM5" (714–715) | README §5 table (certificate column); all eight record directories exist | ok |
| "Every certificate that these claims use, including every piece of their case splits, carries a recorded acceptance by the proof checker cake_lpr" (718–719) | central: `C2FINAL/recount.py:16–17` counts a record (orbit closure and cover alike, `:81`) only with status UNSATISFIABLE, lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`; `recount.json`: P1–P8 each 287 of 287 orbits closed, `cover_certified` 1, `problems` empty; hull cover and 120 hexagonal hulls: `C2C34/README.md` (both checkers), re-checked on hash-checked files (`C2RECHECK` §1, 120 of 120). Threefold: `C3FINAL/README.md:38–40` ("every certified record used here was accepted by both proof checkers ... lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. The records carry those verdicts"). Fivefold: `SYM5/README.md:26`, P1 accepted by cake_lpr at heap 30,000 MiB (`:95–97`) | supported (wording: m2) |
| cake_lpr the only checker in the trust base since a revision of 6 November 2026; lrat-check secondary; SYMLEAN/README.md §9 predates it and names both (719–721) | `WRITEUP/SYMMETRIC.md` §3: "Only cake_lpr ... is trusted ... *Revised 6 November 2026:* lrat-check ... is a secondary check only and not part of the trust base". Read-only history: the sentence entered with commit ad1edc4ca (6 November, +0900); the previous version said both checkers "are trusted". `SYMLEAN/README.md` was last changed in f353ac364 (2 November, +0900); its §9 reads "the checkers lrat-check and cake_lpr are [trusted]" | ok |
| proofs deleted for the parallelogram pieces and the 116,883 threefold pieces; "for most of these pieces only the recorded verdicts remain"; re-solves in C2FINAL §§4, 5, 9, C2RECHECK, C3SPOT, C3PIECES (721–724) | README §9; SYMMETRIC.md §3 "Recorded verdicts (proofs deleted)"; C2FINAL §4 (7 pilot units), §5 (24 + 8 sample units), §9 (224 of 2,304 facts by 1 November 19:43 UTC); C2RECHECK §6 final totals (58 pilot orbits, 65 of 65 Mac-only units, 177 of 242 lanes); C3SPOT 2,120 and C3PIECES 204 of 116,883. A clear majority of both remains on recorded verdicts | ok |
| written proofs "reviewed or audited within the project (listed in WRITEUP/SYMMETRIC.md, §3)": encoders, reductions A and B, the normal form `C3-S/soundness.md`, Lemma 5 and Lemma H6M, the perturbation argument for Threefold33 and Fivefold35 (725–729) | SYMMETRIC.md §3 "Written proofs, refereed or audited (not Lean-checked)" lists all of them; README §5 says "reviewed", §6.5 item 3 gives the perturbation gap; `C3-S/soundness.md` exists. "Reviewed or audited within the project" is the records' level or below it (C2ENC's internal "refereed" is not claimed), so no label is rounded up | ok |
| exact computations compose the pieces; two bookkeeping steps Lean-checked: cover of the 910 threefold roots and closure of the central parallelogram orbits (Theorems cb:thm:c3, cb:thm:c2); record/hash matching outside Lean (730–734) | SYMMETRIC.md §3 (Lean-checked bookkeeping; "an exact computation in Python"); C2FINAL §3 (2,589 of 2,589 hashes rebuilt) and §6 (`decide +kernel`, axioms `propext` only); C3FINAL (116,883 CNF hashes re-derived, 910 roots, 0 open); `sections/cb.tex:1115` (cb:thm:c3 = `C3Cover.all_roots_covered`) and `:1365` (cb:thm:c2 = `Central34.all_cases_closed`), both export labels in the contract table | supported (label nuance: m1) |
| no formal link from a Lean class to its CNF; the match was checked by reading (735–736) | README §6: "The match itself was checked by reading: no formal link joins a Lean class to its CNF" | ok |
| "The records list the remaining caveats and open checks (WRITEUP/SYMMETRIC.md, §4)" (738) | SYMMETRIC.md §4 "What remains open" | ok |

The remark still ends with "The unconditional form of Theorem ar:thm:main is therefore computer-assisted, and it is not
Lean-checked as a whole." No hypothesis is presented as proved.

## 4. Findings marked fixed, declined or duplicate

**Fixed, and fixed correctly:** fidelity F1 (H4, H22), F2 (H20), F3 (H17), F4 (H14), F5 (H19); rigor m2 for its first
three parts (H11, H16, H8, H12–H13), m4 (H10), m5 (H2), m6 (H21); claims F2 (H1), F4 (H5–H6), F5 (725), F6 (714–716,
725–734), F7 (H23).

**Duplicates:** rigor m1, m3, m7, m8; adversarial F1–F4; claims F1, F3, F9. Each duplicates a finding fixed above, and
the fix covers its text, including adversarial F1's counterexample S = {0}, g(p) = 2p, now excluded by H2.

**Declined or no change, judged:**
- Fidelity F6 (mb: refs): acceptable. `mb:thm:baek`, `mb:thm:classes` and `mb:thm:main3` are export labels in the
  contract table and are defined in `sections/mb.tex`. The new refs `cb:thm:c3` and `cb:thm:c2` are export labels of cb
  and are defined in `sections/cb.tex`. All 19 foreign refs are allowed and defined.
- Rigor m2, g_A part: acceptable. g_A, g_B and g_C occur only at ar.tex:170, 177 and 191 (Definitions ar:def:gram,
  ar:def:avgq; Lemma ar:lem:nsq-mulvec). They always carry a subscript and a matrix argument, and no map g is in scope
  there. (The log also names ar:lem:avgq-eq, which uses q_A, q_B, q_C only. This slip is in the log, not the section.)
- Claims F8, group kept: acceptable under the task note, which says to leave section-local `\sloppy` unless it causes
  a problem. The build has 0 overfull boxes and 68 underfull warnings, the same as before. The stretched multi-reference
  heads come from the head format, as the fixer's note to the preamble maintainer explains.
- Writer concerns 2, 4, 5 and contract discrepancy 2: acceptable. None is an inaccuracy in the section.

## 5. Compile check

`build/ar_p1diff_wrapper.tex` has the contract's wrapper content. From `build/`,
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error ar_p1diff_wrapper.tex` was run twice (outputs
`build/ar_p1diff_run1.txt`, `build/ar_p1diff_run2.txt`, `build/ar_p1diff_wrapper.log`).
- Exit 0 on both passes; 11 pages; no `!` error, no "Missing", no multiply-defined label, no rerun request.
- **Overfull boxes: none** (0 of any size). Underfull: 68.
- Undefined references, all allowed: `fd:def:{cp,gp,inv,ngon,orient,point}`, `fd:lem:{affine-cp,affine-orient,collinear,
  cp-hull}`, `sr:def:classes`, `sr:def:iso`, `sr:thm:main`, `sr:thm:variant`, `mb:thm:baek`, `mb:thm:classes`,
  `mb:thm:main3`, `cb:thm:c2`, `cb:thm:c3`.
- Rendered pages 1, 8 and 10 were inspected. The Sources and Rigor lists, "Relation to Lean", and the nested list of
  Remark ar:rem:classes (closing sentence inside the second outer item) are set correctly.

## 6. Findings (all minor)

**m1 (minor, optional): the two bookkeeping theorems are called "Lean-checked" without their computational label.**
- Location: ar.tex:730–732, Remark ar:rem:classes, bullet "Exact computations".
- Issue: the text reads "Two bookkeeping steps are Lean-checked: the cover of the 910 threefold roots and the closure
  of the central parallelogram orbits (Theorems cb:thm:c3 and cb:thm:c2)". Both are kernel evaluations
  (`decide +kernel`). Section cb labels them computer-assisted (`cb.map.tsv` rows `cb:thm:c3`, `cb:thm:c2`), as
  contract rule 6 asks. "Lean-checked" is correct, and the bullet is headed "Exact computations", so nothing is rounded
  up. The remark is about rigor labels, though, so it should carry both.
- Fix: "Two bookkeeping steps are Lean-checked by kernel evaluation (computer-assisted): ...".

**m2 (minor, optional): "including every piece of their case splits" can be read as "every piece has its own
certificate".**
- Location: ar.tex:718–719.
- Issue: under the intended reading (every certificate used, including those of the case-split pieces, carries a
  cake_lpr acceptance) the claim holds; see §3. In the central case, however, not every subcase has a certificate.
  There are 107 UNKNOWN records, and an orbit is closed by one certified member (`C2FINAL` §2). A reader could take the
  appositive as a claim about every subcase.
- Fix: "Every certificate that these claims use, including those of the pieces of their case splits, carries ...".

**m3 (minor, style, optional): a file name stands for the normal form.**
- Location: ar.tex:727.
- Issue: "the normal form `C3-S/soundness.md` of Threefold33" reads as if the file were the normal form.
- Fix: "the normal form of Threefold33 (`C3-S/soundness.md`)".

## 7. Notes (not findings)

- In `\lean{...}` names with an apostrophe (`Function.iterate_succ_apply'`, `hgp'`, `hinv'`, `hne'`), the apostrophe is
  typeset as a curly quote. This was already so in the passed version (`hinv'`, `hne'`). It is a preamble matter
  (straight quotes in the typewriter font), outside this diff.
- Contract rule 9 ("Coverage") is unaffected. The Coverage list is unchanged except the axioms-file sentence (H22).
- Evidence scripts: `build/ar_p1diff_mapcheck.py` (map against heads) and `build/ar_p1diff_algcheck.py` (the three
  identities behind H10, H11 and H16). Both were run under `nice -n 15` with the project's sympy environment, and all
  checks passed.
