# Section `ec`, round doc-r1: diff audit

Lens: diff. Inputs:
- the pre-edit snapshot `snapshots/doc-r1-pre/ec.tex` (914 lines) and `ec.map.tsv`;
- the current `sections/ec.tex` (915 lines) and `sections/ec.map.tsv`;
- the fix log `reviews/ec-doc-r1-fix.md`;
- the notes behind it: `reviews/ec-doc-r0-audit.md` (m1, the only open note), and the earlier `reviews/ec-p1-diff.md`
  (m1-m4) and `reviews/ec-p1-referee.md` (F1-F3), which were fixed in round doc-r0.

Paths below are relative to STAGE (`sections/`, `build/`, `reviews/`, `snapshots/`) or to RES (Lean sources and
records). Nothing under the repository was modified. No Lean, lake or solver was run.

**Verdict: pass.**
- No blocker, no major and no minor finding.
- 1 note marked fixed (doc-r0 audit m1); it is fixed correctly. 0 declined.
- Build clean: both passes exit 0, no error, 0 overfull boxes.

## 1. Hunks checked

`diff -u` gives exactly one hunk in `ec.tex` (`@@ -136,8 +136,9 @@`; old lines 139-140 replaced by current lines
139-141) and no change in `ec.map.tsv`. Mechanical comparison of snapshot and current file:
- 47 labels (all `ec:`, all unique), 41 statement environments and 49 `\leanref` pairs, all unchanged;
- every statement head line is identical (script comparison);
- the map has 41 rows of 5 fields, and its labels equal the 41 environment labels in order.

The edited text is inside Remark `ec:rem:cases`, not in a statement environment. It is ASCII, with balanced braces
(5/5) and an even number of `$` signs, and it adds no `\ref`, macro or package.

| # | Location (current file) | Change | Check | Result |
|---|---|---|---|---|
| 1 | Remark `ec:rem:cases`, closing paragraph, l. 139-141 | old: "..., and a point of such a set outside the orbit of a point $x$ has a direction at $c$ that differs from that of $x$ by no integer multiple of $2\pi/m$". New: "...; and if $x$ and $y$ are points of such a set, both different from $c$, and $y$ is not in the orbit of $x$ under that rotation, then the directions of $x$ and $y$ at $c$ differ by no integer multiple of $2\pi/m$" | Lean re-read and the equivalence argument (below); records; numerical sanity test | OK |

**Lean re-read** (`LEANEXT/orbit/OrbitConsistency.lean`, namespace `ErdosSzekeres.OrbitConsistency`):

| Lean | Hypotheses and conclusion | Wording in the remark |
|---|---|---|
| `phase_ne_of_not_mem_orbit` (:420) | `heven : Even m`, `hm : 0 < m`, `hinv : Invariant (rotAbout c (2 * Real.pi / m)) S` (maps into, :47), `hgp : GeneralPosition S`, `S : Finset Point`; `hr : 0 < r`, `hr' : 0 < r'`, `hx : polar c r α ∈ S`, `hy : polar c r' β ∈ S`, `horb : ∀ j : ℕ, polar c r' β ≠ (rotAbout c (2 * Real.pi / m))^[j] (polar c r α)` ⊢ `∀ k : ℤ, β ≠ α + k * (2 * Real.pi / m)`; `polar c r θ = c + r (cos θ, sin θ)` (:112) | new clause, exact (see below) |
| `same_ray_false` (:295) | `Even m`, `0 < m`, the same `hinv`, `hgp`; `x ∈ S`, `y ∈ S`, `x ≠ y`, `0 < l`, `y - c = l • (x - c)` ⊢ `False` | first clause, unchanged except "," -> ";"; exact (if `x = c` the ray equation forces `y = x`) |

Why the new clause states `phase_ne_of_not_mem_orbit` exactly:
- *Points of the set.* "$x$ and $y$ are points of such a set" is `hx`, `hy`. "such a set" refers back to "a finite set
  in general position that is invariant under rotAbout$(c,2\pi/m)$", with even $m>0$; these are `heven`, `hm`, `hinv`,
  `hgp`, and `S : Finset`. The old wording left `hx` implicit; the new one states it, which was the point of m1.
- *Different from $c$.* Since $|\mathrm{polar}(c,r,\alpha)-c|=|r|$, a point $x\ne c$ is $\mathrm{polar}(c,r,\alpha)$
  with $r=|x-c|>0$ and $\alpha$ an argument of $x-c$. Conversely, `0 < r` gives $x\ne c$. So "both different from $c$"
  is `hr`, `hr'`.
- *The orbit.* `horb` excludes the forward iterates $\rho^{[j]}x$, $j\in\N$. By `rotAbout_iterate` (:105),
  $\rho^{[m]}=\mathrm{rotAbout}(c,m\cdot2\pi/m)=\mathrm{rotAbout}(c,2\pi)$, which is the identity, and $m>0$. So the
  forward orbit is the whole orbit, and "$y$ is not in the orbit of $x$ under that rotation" is `horb`.
- *The conclusion.* "the directions differ by no integer multiple of $2\pi/m$" is `∀ k : ℤ, β ≠ α + k (2π/m)`. It does
  not depend on the representatives $\alpha$, $\beta$, which are fixed only modulo $2\pi$, because
  $2\pi=m\cdot(2\pi/m)\in(2\pi/m)\Z$. With $k$ ranging over $\Z$, the order of $\alpha$ and $\beta$ does not matter.

The clause no longer admits the false literal reading the doc-r0 audit pointed out (with $x$ outside the set, a point
on the open segment from $c$ to a point $y$ of the set, $k=0$ works). It is also consistent with the statement of
Theorem `oc:thm:phase-orbit` (`sections/oc.tex:595-602`), which is written with $\mathrm{polar}$.

**Records.** `LEANEXT/orbit/logs/axioms.log` lines 12 and 15 list `same_ray_false` and `phase_ne_of_not_mem_orbit`
with the standard axioms `[propext, Classical.choice, Quot.sound]`; the log ends `exit=0`, and so does
`logs/build.log`. The file has no `sorry`, `admit`, `native_decide` or `axiom` (grep). `LEANEXT/README.md:14` and
`LEANEXT/orbit/REPORT.md:24-25` list both theorems. So "Lean-checked forms" (unchanged wording) is backed, and the
edit does not round up any label.

**Numerical sanity test** (`build/ec_docr1audit/phasecheck.py`, plain Python): 3000 random sets that are unions of
1-4 orbits under the rotation by $2\pi/m$ about a random centre, $m\in\{2,4,6,8,10\}$, all in general position. Over
643,408 ordered pairs from different orbits, with the angles shifted by random multiples of $2\pi$, the direction
difference was never within $10^{-7}$ of a multiple of $2\pi/m$. As expected, same-orbit pairs always give a multiple.
This only confirms that I read the direction of the statement correctly. The statement itself is Lean-checked.

**Rigor and hygiene (whole current file and map).**
- No machine path (`/private`, `/Users`, `/home`, `/tmp`) and no tool name (grep).
- "verified" and "certified" do not occur. "proved" occurs only in the map's unchanged negative "never proved in
  Lean" (row `ec:def:cases`).
- No `\newcommand`, `\def`, `\usepackage` or `\input`.
- lrat-check occurs only in the caveat that the project does not count it (l. 112). cake_lpr is the anchor
  (l. 110-111, 117, 125-127).
- `ec.tex` makes no reference to `sa:` labels. All 18 cross-section labels it references are allowed export labels,
  each defined exactly once, in its home section (`fd`, `ll`, `lg`, `oc`, `sr`).

## 2. The fixer's notes

| # | Note | Status |
|---|---|---|
| 1 | doc-r0 audit m1: the paraphrase of `phase_ne_of_not_mem_orbit` does not say that $x$ lies in the set, nor that both points differ from $c$ | **fixed**, see §1. The new wording differs from the audit's proposed one ("outside the orbit of a point $x$ of the set (both different from $c$)") but is equivalent and names both points explicitly. |

No note was declined.

The notes of the earlier rounds stay fixed. The doc-r1 hunk touches none of their text, and the current file still has:
- "the two Lean files" (l. 43; p1-diff m4);
- "every finite set in general position with symmetry $C_5$, respectively $C_4$" (l. 243-244; m3);
- the cake_lpr-only wording with the lrat-check caveat and A4-5 (l. 110-113, 117, 125-127; m2, F1);
- the Lean-checked ray fact and the counting gap (l. 135-143; m1);
- the `Compat` gloss (l. 699-703; F2);
- the power step $\rho^j$ (l. 390-395; F3).

The predecessor's two "Notes (no finding)" need no action.

The fix log's claims were checked:
- one hunk, old l. 139-140 replaced by l. 139-141;
- map unchanged;
- labels, heads and `\leanref` pairs unchanged;
- Lean hypotheses quoted correctly (:420, :112, :295);
- compile figures: exit 0/0, 12 pages, 0 overfull, 21 underfull;
- the list of undefined references;
- `build/ec_docr1.txt` l. 105-108 is the rendered passage.

One sentence of the log is slightly loose (see §5).

## 3. Compile check

The wrapper is `build/ec_docr1audit_wrapper.tex`, identical to the contract's wrapper (it inputs `../preamble` and
`../sections/ec`). I ran `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` twice from `build/`:
- exit codes 0 and 0; 12 pages;
- no `!` error, no "Missing", no undefined control sequence, no multiply-defined label;
- **overfull boxes: 0**, so none above 1pt; 21 underfull warnings, as in earlier rounds;
- the only undefined references are to allowed export labels of other sections: `fd:def:{cp,gp,inv,ngon,orient,point,rot}`,
  `lg:lem:{centre,polar}`, `ll:lem:minperiod`, `ll:thm:{card-peel,layers,reduction}`,
  `oc:lem:{perm,rot-inv,same-ray}`, `oc:thm:phase-orbit` and `sr:def:classes`. No `ec:` reference is undefined.

I read the rendered passage in the PDF (`pdftotext`, `build/ec_docr1audit.txt`, l. 103-111). It reads as intended,
with "$m>0$", "rotAbout$(c,2\pi/m)$" and "$2\pi/m$" typeset correctly. Logs: `build/ec_docr1audit_pass{1,2}.out`,
`build/ec_docr1audit_wrapper.log`.

## 4. Findings

None.

## 5. Notes (no finding)

1. The fix log's "Other changes" says that no machine paths or tool names appear in `ec.tex` or `ec.map.tsv`, and
   adds "Neither does 'verified', 'certified' or 'proved'". The map does contain "proved", in the unchanged negative
   "never proved in Lean" (row `ec:def:cases`), which every earlier audit accepted and the doc-r0 log mentioned
   explicitly. This is a small imprecision in the log, not a defect of the document.
2. In the source, the edited paragraph now has a short line 141 ("... $2\pi/m$. The") before l. 142. Source line
   breaks do not affect the output.
