# Section `ec`, round doc-r0: diff audit

Lens: diff. Inputs:
- the pre-edit snapshot `snapshots/doc-r0-pre/ec.tex` (891 lines) and `ec.map.tsv`;
- the current `sections/ec.tex` (914 lines) and `sections/ec.map.tsv`;
- the fix log `reviews/ec-doc-r0-fix.md`;
- the notes it addressed: `reviews/ec-p1-diff.md` (m1-m4) and `reviews/ec-p1-referee.md` (F1-F3).

Paths below are relative to STAGE (`sections/`, `build/`, `reviews/`, `snapshots/`) or to RES (Lean sources and
records). Nothing under the repository was modified; no Lean, lake or solver was run.

**Verdict: pass.**
- No blocker, no major finding; 1 minor finding (wording, §4).
- 7 notes marked fixed; all 7 are fixed correctly. 0 declined.
- Build clean: both passes exit 0, no error, 0 overfull boxes.

## 1. Hunks checked

`diff -u` gives 6 hunks in `ec.tex` and 2 changed rows in `ec.map.tsv` (notes of `ec:rem:cases` and
`ec:rem:big-order`). All 47 labels, all 49 `\leanref` pairs and all 41 statement heads are identical to the snapshot
(mechanical diff). The changed lines are pure ASCII with balanced braces and `$` signs. The only statement environment
touched is Definition `ec:def:compat`, and only in its parenthetical gloss; the defining sentence is unchanged.

| # | Location (current file) | Change | Check | Result |
|---|---|---|---|---|
| 1 | Sources, l. 43 | "the two files" -> "the two Lean files" in `PRIMEFOLD/compat/lean` | `ls`: two `.lean`, two `.out`. SHA-256 recomputed: `PCompatCore.lean` `ebc6aacefadb...`, `L0Check.lean` `05a67c3b8b16...`, equal to `PRIMEFOLD/README.md:35,38` | OK |
| 2 | Rigor and dependencies, l. 72-73 | adds Lemmas `oc:lem:rot-inv`, `oc:lem:perm`, `oc:lem:same-ray`, Theorem `oc:thm:phase-orbit` | all four are contract export labels of `oc`, defined at `oc.tex:224, 338, 508, 595` on `orient_rotAbout_inv`, `orient3_perm`, `same_ray_false`, `phase_ne_of_not_mem_orbit`; they are cited only in Remark `ec:rem:cases` (backward references, no use in any proof) | OK |
| 3a | Remark `ec:rem:cases`, l. 110-113 | new caveat: only cake_lpr verdicts count; lrat-check is secondary, upstream build unsound on the empty clause | `WRITEUP/SYMMETRIC.md` §3 "Trust base": "Only cake_lpr ... is trusted", "lrat-check (2e3b2dc with the E2 patch) is a secondary check only and not part of the trust base. Unpatched, it accepts invalid proofs"; `E2/README.md:56` "lrat-check is unsound on the empty clause" (l. 16-17: 2e3b2dc is upstream master); `LRATCHECK20261105/README.md` title, item 3 ("The unsound path is the empty clause") and "Consequences" | OK |
| 3b | Fivefold35 bullet, l. 116-117 | "were shown unsatisfiable ... accepted by lrat-check and cake_lpr" -> "are recorded as unsatisfiable; the LRAT proofs of both were accepted by cake_lpr" | `SYM5/README.md` table l. 84-85: P1 and L1 UNSAT, cake_lpr `s VERIFIED UNSAT` (heap 30,000 MiB, resp. default) | OK |
| 3c | Fourfold32 bullet, l. 125-133 | cake_lpr only; unrecorded checker builds (A4-5); hash-bound replay; statement of the sector normal form and its one-sentence argument | `C4CUT/README.md` §3 l. 65-71 (UNSAT; cake_lpr `s VERIFIED UNSAT`; "the checker binaries are not named in the records"); `AUDIT3/reports/A4_fivefold_layers.md` A4-5 (l. 321-361: neither the lrat-check nor the cake_lpr build is recorded; the claim is carried by cake_lpr, conditional in the finding on the binary being the recorded build, and confirmed by the independent check: 2fee767 is the only cake_lpr build on the machine, "the claim does not depend on it"); `REPLAY/README.md` l. 8, 50, 87 (both checkers on hash-checked files, binary SHA-256 equal to the manifest, c4cut-final `s VERIFIED UNSAT`); `C4CUT/README.md` §1 l. 30-32 (open quadrant between the rays through (0,0) and (0,1), orbit 0 outermost; "a point on a bounding ray would be collinear with two antipodal points of the first orbit"); A4-1 (l. 57-59) | OK |
| 3d | closing paragraph, l. 135-145 | Lean-checked forms of the layer lemma and of the even-order ray fact; counting step not in Lean; rotation invariance and permutation sign rule Lean-checked; nothing connects them to the formulas | Lean re-read (below). `LEANEXT/orbit/logs/axioms.log` lines 1, 5, 12, 15 list the four theorems with the standard axioms; `LEANEXT/README.md:14` lists them. No Lean file under RES or `ErdosSzekeres/` states the one-point-per-quadrant count for the `SYM5` encoders (grep for "quadrant"/"sector": only EncB/gen_b2 and the D3 encoding of `H2`, both other encoders). `SYM5/symcnf.py` docstring: one variable per orbit of unordered triples, sign bookkeeping by rotation invariance and antisymmetry; `symcnf_layers.py` imports `SymEncoding` from it, so "the encoders'" (both forms, and C4CUT, which uses `symcnf_layers.py` for m = 4) is right. `encoder_literal_sound` is correctly not cited (records tie it to `C7UPPER/gen.py`) | OK, one wording point (minor m1) |
| 4 | Remark `ec:rem:es7-sharp`, l. 242-243 | "every set" -> "every finite set in general position" | `ES7Corollaries.lean:1183, 1216` re-read: `S : Finset Point`, `GeneralPosition S`; `symmetric_es7.tex:49` (general position) and `prop:C` (l. 326-328) | OK |
| 5 | Remark `ec:rem:big-order`, l. 390-395 | Lemma 2(a) direct; tables: rotation of order m reduced by the power rho^j | `ES8SYM/proofs/layers.md:6-7` (R = rotation by 2pi/m), Lemma 2(a) l. 33; `symmetric_extremal.tex:338` "Let rho be a rotation of order m about O"; `ES8SYM/README.md:15, 33`. Math: rho = rotAbout(c, 2 pi k/m) with gcd(k, m) = 1, j k = 1 mod m gives rho^j = rotAbout(c, 2 pi/m); numerically checked for 8 <= m <= 40 and all coprime k in [-3m, 3m] (error < 2e-13). Corollary `ec:cor:planar` unchanged | OK |
| 6 | Definition `ec:def:compat`, l. 699-702 | new gloss: for m >= 1 the same as N mod m in {0,1}; 1 mod m matches Theorem `ec:thm:compat`(b) | Lean `PCompatCore.lean:205` re-read: `def Compat (m N : ℕ) : Prop := N % m = 0 ∨ N % m = 1 % m`; the defining sentence is unchanged and exact. Exhaustive check (Lean `n % 0 = n`) for 0 <= m < 200, 0 <= N < 1200: no difference. `card_mod` (l. 112-114): right side `(if 0 ∈ S then 1 else 0) % m` | OK |
| map | rows `ec:rem:cases`, `ec:rem:big-order` | notes only | 41 rows x 5 fields, in the order of the 41 environments; notes ASCII; a dry run of the appendix generator's `note_tex` on both rows gives valid LaTeX (`cake\_lpr` escaped; `ll:thm:layers`, `oc:lem:same-ray`, `oc:thm:phase-orbit` become `\ref`s to defined labels) | OK |

**Lean re-read for hunk 3d** (`LEANEXT/orbit/OrbitConsistency.lean`):

| Lean | Hypotheses and conclusion | Wording in the remark |
|---|---|---|
| `same_ray_false` (:295) | `Even m`, `0 < m`, `Invariant (rotAbout c (2π/m)) S` (maps into), `GeneralPosition S`, `x y ∈ S`, `x ≠ y`, `0 < l`, `y - c = l • (x - c)` ⊢ `False` | "for even m > 0, no two points of a finite set in general position that is invariant under rotAbout(c, 2π/m) lie on one open ray from c": exact (if x = c the ray hypothesis forces y = x) |
| `phase_ne_of_not_mem_orbit` (:420) | same set hypotheses; `0 < r`, `0 < r'`, `polar c r α ∈ S`, `polar c r' β ∈ S`, `∀ j : ℕ, polar c r' β ≠ ρ^[j] (polar c r α)` ⊢ `∀ k : ℤ, β ≠ α + k * (2π/m)` | "a point of such a set outside the orbit of a point x has a direction at c that differs from that of x by no integer multiple of 2π/m": right, but the hypothesis that x lies in the set is left implicit (minor m1) |
| `orient_rotAbout_inv` (:117) | orient is invariant under `rotAbout c θ` | "rotation invariance of orientations" |
| `orient3_perm` (:178) | `orient3 (t ∘ σ) = sign σ * orient3 t` | "their sign rule under permutations" |

The counting step was also checked: for m = 4, an orbit none of whose points lies on the four rays from c through
the outermost orbit has its four points in the four rotated open quadrants, one in each (random-phase test, 100,000
cases).

**Rigor and hygiene.** "were shown unsatisfiable" became "are recorded as unsatisfiable", and "we prove it here"
became "a written proof follows". Every Lean-checked label in the new text is backed by an axioms log. The case
statements stay hypotheses, CNF verdicts are attributed to records, and cake_lpr is the anchor, as the contract
requires. No "verified", "certified" or "proved" occurs in `ec.tex`; the map has only the unchanged negative "never
proved in Lean". The word "certificate(s)" is a noun used for the records. `ec.tex` and `ec.map.tsv` contain no machine
path and no tool name. No macro or package was added, and `\begingroup` and `\endgroup` are balanced (one
each).

## 2. The fixer's notes

| # | Note | Status |
|---|---|---|
| 1 | diff m1: Lean coverage understated (ray fact, triple-orbit facts) | **fixed**: hunks 2, 3c, 3d. The Fourfold32 bullet now states the sector normal form; the closing paragraph names the Lean-checked ray fact and the counting gap. |
| 2 | diff m2: lrat-check on equal footing with cake_lpr | **fixed**: hunks 3a-3c |
| 3 | diff m3: "every set" drops finiteness and general position | **fixed**: hunk 4 |
| 4 | diff m4: "the two files" | **fixed**: hunk 1 |
| 5 | referee F1: lrat-check caveat; C4CUT checker build unrecorded (A4-5) | **fixed**: hunks 3a, 3c, with the replay as additional support |
| 6 | referee F2: inaccurate gloss of `Compat` | **fixed**: hunk 6, in the form the referee proposed |
| 7 | referee F3: rotation of order m vs rotation by 2π/m | **fixed**: hunk 5 |

No note was declined. The "Other changes" 1-4 of the log match the diff. The log's claims about the files under RES that
are cited in its table were spot-checked (`C4CUT/README.md:30-32`, A4-1 and A4-5, `REPLAY/README.md` l. 8, 50, 87,
`symmetric_extremal.tex:338`, `layers.md:6-7`, `PRIMEFOLD/README.md:35,38`, `PCompatCore.lean:205`), and all are
accurate.

## 3. Compile check

Wrapper `build/ec_docr0audit_wrapper.tex`, identical to the contract's wrapper (it inputs `../preamble` and
`../sections/ec`). Two passes of `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` from `build/`:
- exit codes 0 and 0; 12 pages;
- no `!` error, no "Missing $", no undefined control sequence, no multiply-defined label. The only "missing" line is
  the microtype info about a small-caps glyph;
- **overfull boxes: 0** (so none above 1pt); 21 underfull warnings, as in earlier rounds;
- undefined references only to allowed export labels of other sections: `fd:def:{cp,gp,inv,ngon,orient,point,rot}`,
  `ll:lem:minperiod`, `ll:thm:{card-peel,layers,reduction}`, `lg:lem:{centre,polar}`,
  `oc:lem:{perm,rot-inv,same-ray}`, `oc:thm:phase-orbit` and `sr:def:classes`. No `ec:` reference is undefined.

The rendered text of every edited passage was read in the PDF (`pdftotext`). Helper scripts are in
`build/ec_docr0audit/` (`check.py`, `hunkcheck.py`, `notecheck.py`).

## 4. Findings

**m1 (minor, wording). Remark `ec:rem:cases`, l. 139-140: the point x of the phase statement is not said to lie in
the set.**
- The paraphrase of `phase_ne_of_not_mem_orbit` reads "a point of such a set outside the orbit of a point $x$ has a
  direction at $c$ that differs from that of $x$ by no integer multiple of $2\pi/m$".
- The Lean theorem assumes `hx : polar c r α ∈ S`, so x is a point of the set. With r > 0 and r' > 0, both points also
  differ from c.
- Read literally with x outside the set, the sentence is false. For example, take x on the open segment from c to a
  point y of the set: the orbit of x misses the set, and k = 0 works.
- The intended reading is clear from context, so this is a wording point only.
- **Fix.** Write "outside the orbit of a point $x$ of the set (both different from $c$)".

## 5. Notes (no finding)

1. A4-5's own finding states its conclusion conditionally: "carried by cake_lpr if that binary is the recorded CakeML
   build". Its independent check then makes it firm (only one cake_lpr build on the machine; "the claim does not
   depend on it"). The remark's "which concludes that the claim is carried by the cake_lpr verdict" is a fair summary
   of the whole entry, and the next clause cites the hash-bound replay, which removes the condition.
2. In the closing paragraph, "Apart from the layer lemma and the ray fact ..., none of these written arguments is
   checked in Lean" is followed by "are Lean-checked too" for the rotation invariance and the sign rule. These are
   ingredients of encoder soundness, not items of the bullet list, so there is no contradiction. Encoder soundness as a
   whole has no Lean form for the `SYM5` encoders: `H2/D3Encoding` Lean-checks a different encoder, `d3cnf.py`, for D3.
