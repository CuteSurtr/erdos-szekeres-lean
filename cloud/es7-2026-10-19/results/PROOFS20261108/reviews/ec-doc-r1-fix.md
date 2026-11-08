# Fix log: section `ec`, round doc-r1

Paths: `sections/`, `snapshots/`, `build/` and `reviews/` are relative to the staging area. Research paths are relative
to `RES = cloud/es7-2026-10-19/results`. Nothing under the repository was modified. Lean, lake and solvers were not run.

Input: the diff audit `reviews/ec-doc-r0-audit.md` (verdict pass; no blocker or major finding; one minor finding, m1).
Snapshot before editing: `snapshots/doc-r1-pre/ec.tex` and `snapshots/doc-r1-pre/ec.map.tsv`.

## Notes

| # | lens | note (summary) | action | location (current file) | check against the sources |
|---|---|---|---|---|---|
| 1 | diff m1 | Remark `ec:rem:cases`, closing paragraph: the paraphrase of `phase_ne_of_not_mem_orbit` ("a point of such a set outside the orbit of a point $x$ has a direction at $c$ that differs from that of $x$ by no integer multiple of $2\pi/m$") does not say that $x$ lies in the set, nor that both points differ from $c$. Read literally with $x$ outside the set, it is false. | fixed | `ec.tex` 139-141 | `LEANEXT/orbit/OrbitConsistency.lean:420` re-read: `Even m`, `0 < m`, `Invariant (rotAbout c (2 * Real.pi / m)) S`, `GeneralPosition S`, `0 < r`, `0 < r'`, `hx : polar c r α ∈ S`, `hy : polar c r' β ∈ S`, `horb : ∀ j : ℕ, polar c r' β ≠ (rotAbout c (2 * Real.pi / m))^[j] (polar c r α)` ⊢ `∀ k : ℤ, β ≠ α + k * (2 * Real.pi / m)`; `polar c r θ = c + r (cos θ, sin θ)` (`:112`). New text: "and if $x$ and $y$ are points of such a set, both different from $c$, and $y$ is not in the orbit of $x$ under that rotation, then the directions of $x$ and $y$ at $c$ differ by no integer multiple of $2\pi/m$". This names both points, puts both in the set (`hx`, `hy`), states $x,y\ne c$ (`0 < r`, `0 < r'`), and keeps the orbit condition (`horb`; the forward orbit is the whole orbit, since the $m$-th iterate of the rotation is the identity) and the conclusion. The conclusion does not depend on the chosen angles, because $2\pi=m\cdot(2\pi/m)$ is an integer multiple of $2\pi/m$. Every point other than $c$ has the form `polar c r α` with `r > 0`. The first half of the sentence (`same_ray_false`, `:295`, re-read; the audit found it exact) was not changed except for the punctuation "," -> ";". |

No note was declined.

## Other changes

None. The map `sections/ec.map.tsv` is unchanged: the note of `ec:rem:cases` says only that the even-order ray fact has
Lean-checked forms, and it makes no claim about the hypotheses. `diff` against the snapshot shows one hunk in `ec.tex`
(lines 139-140 replaced by 139-141) and none in the map. All 47 labels, all statement heads and all `\leanref` pairs
are unchanged. The edited lines are ASCII, with balanced braces and `$` signs. No macros or packages were added, and
no machine paths or tool names appear in `ec.tex` or `ec.map.tsv`. Neither does "verified", "certified" or "proved".

## Compile check

`build/ec_wrapper.tex`, two passes of `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` from `build/`:
- exit 0 and 0; 12 pages;
- no `!` errors, no "Missing $", no undefined control sequences, no multiply defined labels;
- **overfull boxes: 0** (so 0 above 1pt); 21 underfull warnings, as before;
- undefined references only to other sections' export labels: `fd:def:{cp,gp,inv,ngon,orient,point,rot}`,
  `ll:lem:minperiod`, `ll:thm:{card-peel,layers,reduction}`, `lg:lem:{centre,polar}`,
  `oc:lem:{perm,rot-inv,same-ray}`, `oc:thm:phase-orbit` and `sr:def:classes`. All are contract export labels, and
  none is an `ec:` label.

The rendered text of the edited passage was read in the PDF (`pdftotext`, `build/ec_docr1.txt`, l. 105-108).
