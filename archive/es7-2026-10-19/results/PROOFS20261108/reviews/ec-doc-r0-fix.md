# Fix log: section `ec`, round doc-r0

Paths: `sections/`, `snapshots/`, `build/` and `reviews/` are relative to the staging area. Research paths are relative
to `RES = cloud/es7-2026-10-19/results`. Nothing under the repository was modified. Lean, lake and solvers were not run.

Input: the seven open minor notes for `ec` in `build/open_minors.json` (from `reviews/ec-p1-diff.md` and
`reviews/ec-p1-referee.md`). Snapshot before editing: `snapshots/doc-r0-pre/ec.tex` and `ec.map.tsv`.

## Notes

| # | lens | note (summary) | action | location (current file) | check against the sources |
|---|---|---|---|---|---|
| 1 | diff m1 | Remark `ec:rem:cases` says that only the layer lemma is checked in Lean. But the ray fact behind the even-m sector normal form is also Lean-checked (`same_ray_false`, `phase_ne_of_not_mem_orbit`). So are the orientation facts behind the triple-orbit variables. | fixed | `ec.tex` 123-145 (Fourfold32 bullet and the closing paragraph); dependency paragraph 71-73 | `LEANEXT/orbit/OrbitConsistency.lean:295, :420` re-read. `LEANEXT/README.md` lists both as Lean-checked. `C4CUT/README.md:30-32` gives the sector step. `AUDIT3/reports/A4_fivefold_layers.md` A4-1 (l. 57-59, 76). The `oc` labels are on these declarations (`oc.tex:508, :595`). New text: the bullet states the sector normal form. The closing paragraph names the Lean-checked ray fact (Lemma `oc:lem:same-ray`, Theorem `oc:thm:phase-orbit`) and says that the counting step is not in Lean. It names the rotation invariance and the sign rule of orientations (Lemmas `oc:lem:rot-inv`, `oc:lem:perm`), on which the encoders' one variable per orbit of triples rests (`SYM5/symcnf.py` docstring; AUDIT3 l. 176: P1 and L1 share that clause family). It says that nothing in Lean connects any of these to the formulas. `encoder_literal_sound` (`oc:thm:encoder`) is not cited. The records and section `oc` tie it to `C7UPPER/gen.py` and `C6UPPER/encb/gen_b2.py`, not to `SYM5`. All four `oc` labels are allowed export labels. |
| 2 | diff m2 | lrat-check is named as a co-checker on an equal footing with cake_lpr. The records anchor certificates on cake_lpr alone. | fixed (together with #5) | `ec.tex` 110-113 (new caveat), 117 (Fivefold35), 125-127 (Fourfold32) | `WRITEUP/SYMMETRIC.md` section 3: only cake_lpr is trusted, and lrat-check is a secondary check only. `LRATCHECK20261105/README.md` "Consequences". `E2/README.md`: lrat-check is unsound on the empty clause. The bullets now name cake_lpr only. One caveat sentence before the list says that the records also show lrat-check acceptances, which the project does not count, and why. |
| 3 | diff m3 | Remark `ec:rem:es7-sharp`: "apply to every set with symmetry C_5, respectively C_4" drops finiteness and general position. | fixed | `ec.tex` 242-243 | `WRITEUP/note/symmetric_es7.tex:49` defines general position, and `prop:C` (l. 326-328) defines N(Γ) as the largest size of a set in general position. The theorems assume a `Finset` in general position. The text now reads "every finite set in general position with symmetry C_5, respectively C_4". |
| 4 | diff m4 | Sources: "the two files in PRIMEFOLD/compat/lean" is loose, since the directory has four files. | fixed | `ec.tex` 43 | `ls`: two `.lean` and two `.out`. The text now reads "the two Lean files". The hashes were recomputed: `ebc6aace…` and `05a67c3b…` match `PRIMEFOLD/README.md:35,38`. |
| 5 | referee F1 | Same issue as #2. The referee adds that C4CUT does not record which lrat-check build was used (AUDIT3 A4-5). | fixed (with #2) | `ec.tex` 125-127 | AUDIT3 A4-5 (l. 321-361) says that neither checker build is recorded and concludes that the claim is "carried by cake_lpr". The Fourfold32 bullet now says that the final run does not record which checker builds it used, and gives A4-5's conclusion. It also cites the hash-bound replay (`REPLAY/README.md` l. 8, 50, 87: both checkers, SHA-256 of the binaries equal to the manifest), which accepted the proof again with cake_lpr. |
| 6 | referee F2 | The gloss of Definition `ec:def:compat` ("the form 1 mod m makes the case m = 1 work") is inaccurate. | fixed | `ec.tex` 699-702 (statement sentence unchanged) | Lean `PCompatCore.lean:205`, `def Compat (m N : ℕ) : Prop := N % m = 0 ∨ N % m = 1 % m`, re-read before and after the edit. The statement sentence matches it exactly and was not changed. Exhaustive check with Lean's `n % 0 = n` for 0 ≤ m < 80 and 0 ≤ N < 600: `Compat` and "N mod m ∈ {0,1}" never differ. The new gloss says that for m ≥ 1 it is the same condition as N mod m ∈ {0,1} (with both reasons). It says that the form 1 mod m matches the right side of Theorem `ec:thm:compat`(b), and keeps the m = 0 caveat. |
| 7 | referee F3 | Remark `ec:rem:big-order`: the step from "a rotation of order m" (the k = 8 tables) to `rotAbout(c, 2π/m)` is missing. | fixed | `ec.tex` 390-395 | `WRITEUP/note/symmetric_extremal.tex:338` reads "Let ρ be a rotation of order m about O", and `ES8SYM/README.md` l. 15 and 33 read "Rotation of order >= 8". `ES8SYM/proofs/layers.md` l. 6-7 uses the rotation by 2π/m. The remark now says that Lemma 2(a) needs no extra step. For the tables, ρ = rotAbout(c, 2πk/m) with gcd(k, m) = 1. Pass to ρ^j = rotAbout(c, 2π/m) with jk ≡ 1 (mod m), as in Remark `ec:rem:es7-sharp`. ρ^j maps every ρ-invariant set into itself, so the corollary applies to ρ^j. Corollary `ec:cor:planar` itself is unchanged. |

No note was declined.

## Other changes

1. **Dependency paragraph** ("Rigor and dependencies", `ec.tex` 71-73). It now lists the new cross-section references:
   Lemmas `oc:lem:rot-inv`, `oc:lem:perm` and `oc:lem:same-ray`, and Theorem `oc:thm:phase-orbit`.
2. **Rigor vocabulary in `ec:rem:cases`.** "were shown unsatisfiable" (twice) became "are recorded as unsatisfiable"
   (SYM5 table P1/L1, `C4CUT/README.md` section 3). A CNF verdict is a hypothesis-level input, and it is now
   attributed to the records.
3. **Rigor vocabulary in `ec:rem:big-order`.** "and we prove it here" became "and a written proof follows".
4. **Map TSV.** Two notes were updated, for `ec:rem:cases` (cake_lpr anchor; ray fact Lean-checked in `ll`/`oc` but not
   linked to the formulas) and `ec:rem:big-order` (power step). No label, kind, Lean name or file:line changed. The map
   has 41 rows of 5 fields, and they match the 41 statement environments in order.

Unchanged: all labels (47, identical list), all statement heads and `\leanref` pairs, and every statement text except
the gloss in Definition `ec:def:compat`. No macros or packages were added. The writer's local `\begingroup\sloppy` was
left as is. No machine paths or tool names appear in `ec.tex` or `ec.map.tsv`, and neither does "verified",
"certified" or "proved". The only occurrence is the map's negative "never proved in Lean", which is unchanged.

## Compile check

`build/ec_wrapper.tex`, two passes of `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` from `build/`:
- exit 0 and 0; 12 pages;
- no `!` errors, no "Missing", no undefined control sequences, no multiply defined labels;
- **overfull boxes: 0** (so 0 above 1pt); 21 underfull warnings, as before;
- undefined references only to other sections' export labels: `fd:def:{cp,gp,inv,ngon,orient,point,rot}`,
  `ll:lem:minperiod`, `ll:thm:{card-peel,layers,reduction}`, `lg:lem:{centre,polar}`,
  `oc:lem:{perm,rot-inv,same-ray}`, `oc:thm:phase-orbit` and `sr:def:classes`. All are contract export labels, and
  none is an `ec:` label.

The rendered text of every edited passage was read in the PDF (`pdftotext`).
