# Section `mm`, polish round 1: independent referee report

**Verdict: PASS.** There is no blocker and no major finding, and one minor finding (R1 below).

I read the whole section (`sections/mm.tex`, 961 lines), its map (`sections/mm.map.tsv`, 21 rows), the Lean source of
every statement, and the fd and mb statements that the section cites. I checked each step myself. I read the earlier
reports (`mm-r1-*.md`, `mm-polish-r1-fix.md`) only after forming my own view, and I found nothing in them that is
still open.

## What I checked, and how

1. **Fidelity, statement by statement.** I compared every head with its declaration in
   `MIRRORETV/lean/MirrorMain.lean` and `ErdosSzekeres/Omission/Realization.lean`. For each one I checked the argument
   order and implicit arguments, strict vs weak inequalities, `Finset` vs set, maps-into symmetry (`mir p ∈ S`,
   `lineRefl … p ∈ S`), truncated subtraction (`2*m-1`, `m-1`, `K-1`, which the hypotheses `m ≥ 3`, `K ≥ 4` make
   ordinary, as the Conventions paragraph says), and the conclusions (`HasConvexNGon (2*m)`, `(2*m-1)`, `S.card ≤ 2*M`,
   `≤ 2*M+2`, `n ≤ K-1`). Specific checks:
   - `cap_below_lines`: `hy : ∀ i, 0 ≤ c i 1`, with implicit `{i j}`, explicit `l`, `hij`, and `hl : 0 < c l 1`.
   - The axis polygons: `h0 : c ⟨0,_⟩ 1 = 0`, `hy : 0 < i.val → 0 < c i 1`, `hlast : c ⟨m-1,_⟩ 1 = 0`, and
     `i.val < m-1`.
   - All nine generated polygon lemmas: the hypotheses and the exact membership lists, which match the `cycK` calls at
     lines 388, 635, 812, 989, 1164, 1278, 1354, 1429 and 1504. In particular `cap_mirror_pentagon` has no `c0 ∈ P`
     and `cap_mirror_heptagon` has no `mir c0 ∈ P`.
   - `transport`: the four conjuncts under all three hypotheses.
   - `mirror_odd_general` and `mirror_even_general`: (hM) with `¬c.HasCap (j+1)` or `¬c.HasCap j`, and the `_line`
     versions with implicit `{n0 n1 c}` after `hM`.

   Every statement matches its declaration.
2. **Every `\leanref` file:line (71 references) and every line number in the prose.** The prose numbers are 993,
   1587, 2542–2557, 2060, 1716, 1512, 1529, 1676, 1803, 1812, 1820, 1969, 1977, 2631, 2636, 2662–2677, FarFlat
   12/15/34/55/60/67/89, `MirrorNine_append.lean:131`, `MirrorMain.out` 848–863 and 860–861, `MirrorNine.out` 881, and
   `SYMLEAN/mirror/axioms.out` 1–16. Every reference points at the named declaration or record line.
3. **Records.**
   - All SHA-256 prefixes match: MirrorMain `ca623e55a1b9`, Realization `ae4970e0808e`, ConvexCycleCuts
     `b4ad0ba9e583`, Definitions `2425500eefd1`, Basic `13667aa2d3dc`, Orientation `f67955ac7091`,
     OrientationGeometry `c7db9bbbb65e`, ReductionThreeClasses `0cc83994fe8c` and FarFlat `08a79f881eea`.
   - `diff` shows that MirrorMain lines 3–2677 are byte-identical to ReductionThreeClasses lines 1562–4236 (offset
     +1559). The preceding part of that file closes its namespace at line 1559, so `MirrorOdd` sits at the root there
     too.
   - `MirrorMain.out` has 0 errors and 121 warnings, all "This simp argument is unused".
   - The file contains no `sorry`, `admit`, `native_decide` or `axiom`. Every `by decide` in a treated declaration
     proves a comparison of explicit `Fin` elements. The only `decide` on `Nat.choose` is in `capacity16`, which the
     section does not treat.
   - Neither `gen_lean.py` nor `gen_certs.py` is present in `MIRRORETV`.
   - Lean 4.24.0 and Mathlib `f897ebcf` agree with `lean-toolchain`, `lake-manifest.json` and
     `SYMLEAN/mirror/README.md`.
   - The claim that every treated declaration is used by one of the sixteen audited theorems holds. I traced it
     through `unframe_apply`, `unframeLin`, `sortPt_x`, `emb_mem`, `xset_card`, `cyc4`–`cyc8`, `hasCap3_of` and
     `hasConvexNGon_of_le`.
4. **Proofs, step by step.**
   - `cap_below_lines`: all five positions of l.
   - The four cases and the injectivity claim of `cap_mirror_polygon`.
   - Both axis versions, including Cases 3a/3b and the s<m≤r case of Claim 2.
   - The derivations of the nine small polygons. These are not circular: the general theorems never use the generated
     lemmas.
   - Lemmas count, injx, sort, ngon, upper-caps and cup.
   - Theorems odd, even, line and small, and Remark (hM) items (1)–(4). This includes the small-j instances (2,4),
     (3,5) and (2,1), the instances (3,16), (4,22) and (4,113), and the index shift.
   - Every hypothesis of every lemma the section applies is available at the point where it is used.
5. **Identities checked with sympy** (script `build/mmp1ref/check_identities.py`, all residuals 0):
   - `orient_mir3`, `orient_mir2`, `orient_cycl`, `orient_swap12`, `orient_rev`.
   - Part (e): orient(a,b,mir d) = orient(a,b,d) − 2d₁(b₀−a₀).
   - The middle case of `cap_below_lines`: −(x_j−x_i)y_l − y_i(x_j−x_l) − y_j(x_l−x_i).
   - Slope (b), including the intermediate form.
   - The collinearity of p, q, mir p when q₀ = p₀, and three points on the axis.
   - frame(p) = Rp − (0, cs).
   - The four identities with defect (s−1) in the proof of Lemma `mm:lem:frame`, including the intermediate forms.
   - All six `linear_combination` certificates of the Lean proofs.
   - λ(lineRefl p) = λ − 2λs, the invariance of n₁p₀ − n₀p₁, and R(n₀,n₁)ᵀ = (0,s)ᵀ.
6. **Numerical check of the explicit cyclic lists** (`build/mmp1ref/check_lists.py`, exact rationals). I ran 300
   random caps with m from 2 to 7, in the no-axis, left-axis and right-axis versions. Every list was injective and had
   every triple, taken in list order, positive. I also confirmed the five-point example of PROOFS.md §3: it turns left
   at every vertex, and (−18,−62) lies strictly inside the triangle (−88,−82), (37,−76), (1,66).
7. **Cross-references.**
   - The fd labels used (13 of them) say what the section uses. In particular:
     - `fd:lem:orient`(a) is the exchange of the last two arguments.
     - `fd:lem:orient`(d) covers all permutations.
     - `fd:lem:pos-cycle` takes an injective `p`, an embedding `e` and all increasing triples.
     - `fd:lem:mono`(a)–(d).
     - `fd:lem:affine-orient` covers any map of the form x ↦ Ax + v.
     - `fd:lem:affine-cp`(d′).
   - The mb labels `mb:thm:baek`, `mb:thm:seven`, `mb:thm:eight` and `mb:thm:nine` are export labels, and they state
     what is claimed: `main` at `Vendor/ETV/Main/Main.lean:87`, the bounds 32 and 46, and parts (a)–(c) for 113 and
     226.
   - `capacity22g` rests on `main` through `geometric_capacity22` and `Baek.capacity22` (`main 5`), as stated.
8. **Coverage.** Every top-level declaration of `MirrorMain.lean` is either covered or listed with a reason. The
   FarFlat description and its axioms record (five of the six theorems) are accurate.
9. **Build** (`build/mmp1ref/`, two passes of `nice -n 15 pdflatex`): exit 0 both times, no overfull boxes. The only
   undefined references are `fd:` labels and the four mb export labels. The section has no `\newcommand` or
   `\usepackage`. The only local setting is the `\begingroup\setlength{\emergencystretch}…\endgroup`, which causes no
   problem. Neither file contains a machine path or a tool name.
10. **Rigor vocabulary.**
    - (hM) appears as a hypothesis in Theorems `mm:thm:odd` and `mm:thm:even`, in parts (b) and (c) of
      `mm:thm:line`, in Rigor, and in Remark `mm:rem:hm`.
    - The written steps are labelled as such: part (e) of `mm:lem:orient-mir`, part (b) of `mm:lem:slope`, and
      `mm:lem:upper-caps`.
    - The section does not present any computation as a hand proof. The generated polygon lemmas are given a different
      written proof, and the section says so.
    - The words "verified" and "certified" do not occur.

## Findings

### R1 (minor): Remark `mm:rem:hm`, item (2): the derivation "(hM) holds for M equal to this number" also needs N finite

- **Location:** `sections/mm.tex`, lines 681–684.
- **Issue:** The remark says that (hM) with M = N(2j+1, j+1, 2j+1), or M = N(2j, j, 2j), follows "from two facts":
  consecutive caps are all-triples caps, and a cup is in convex position. Those two facts show that the point set of a
  configuration satisfying the premises of (hM) lies in the class that defines N. To conclude n ≤ M with M ∈ ℕ, one
  also needs the class to be bounded, so that "the largest size" is a natural number. PROOFS.md §1 gets this from the
  cups–caps theorem ("It is finite by the cups–caps theorem"). The remark cites §1, but it lists only the two facts.
  This does not affect correctness: the remark says the claim is not used in the section.
- **Fix:** Insert "(N is a natural number: the class is bounded by the cups–caps theorem, PROOFS.md §1)" after "for M
  equal to this number", or replace "from two facts" with "from the finiteness of N and two facts".

## Remarks (no action needed)

- The four unlabelled explanatory remarks have no map rows. The polish fix log records the convention for this round
  (rows for non-remark environments, rows for labelled remarks optional), and the one remark that rule 7 requires has
  the label `mm:rem:hm` and a row. I do not count this as a finding.
- I checked the parenthetical in the proof of Theorem `mm:thm:small`(b) about the Lean case split against
  `MirrorMain.lean:2065–2090`. The relabelings it states, (g) with (a,c₀,c₁) := (c₂,c₀,c₁) and (f) with
  (a,c₀,c₁) := (c₀,c₁,c₂), match the calls `axis_right_pentagon (c 2) (c 0) (c 1)` and
  `axis_left_pentagon (c 0) (c 1) (c 2)`.
