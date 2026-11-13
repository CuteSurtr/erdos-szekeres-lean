# Final pass, round 1, section mb: fixes

Files edited: `sections/mb.tex` and `sections/mb.map.tsv` (snapshot before editing: `snapshots/final-r1-pre/`).
Line numbers refer to the edited `sections/mb.tex` (1219 lines; the edits add four source lines). Paths of records are
relative to RES (`cloud/es7-2026-10-19/results`), other paths to the repository root or to STAGE as indicated.

All five findings were checked against the sources and are right; all five are fixed. Declined: none.

## Finding 1 (minor): "the eight parallelogram hull cases"

- Action: fixed, with the requested wording.
- Location: Remark `mb:rem:main3`, item `HalfTurn34`, ll. 1108-1110 (was ll. 1105-1106).
- Check against the sources:
  - `C2C34/README.md` section 2: the hull is a quadrilateral `P<a>` (16 cases) or a hexagon `H<a>-<b>` (120 cases);
    under rotation and reversal of the gap sequence, 8 quadrilaterals and 24 hexagons are canonical (`canonical.txt`).
  - `C2FINAL/README.md` section 1, item 4: "Case P_a and P_(17-a) are equivalent (reduction A, reviewed in
    `C2P/review`), so P1..P8 suffice."
  - `C2FINAL/Central34Orbits.lean`: the module docstring says "In hull case `P a` (`1 <= a <= 8`)", and the three
    theorems (ll. 273, 284, 291) quantify over `List.range 8` with `a = k + 1`.
- Old wording: "namely that the listed subcases of the eight parallelogram hull cases meet every orbit of second-layer
  subcases"
- New wording: "namely that the listed subcases of the eight canonical parallelogram hull cases $P_1,\dots,P_8$ (to
  which reduction~A reduces the others) meet every orbit of second-layer subcases"
- Note: the next sentence, which is unchanged, says that "the two reductions of the case split have written proofs".
  Reduction A is one of these two.

## Finding 2 (major, rigor label): the closure of the central orbits was called plainly "Lean-checked"

- Action: fixed.
- Check against the sources:
  - `find RES/C2FINAL -type f`: 27 files, and none of them is a compile, build or axioms log of a Lean build. The only
    `.out` files are `evidence/central34-cover/*.out`: SAT solver and proof checker outputs for the hull cover, not Lean
    output.
  - `C2FINAL/Central34Orbits.lean` ends with three `#print axioms` commands (ll. 296-298). Their output is nowhere in
    the repository. I grepped the whole repository, outside `.git` and `.lake`, for `Central34`, `all_cases_closed`,
    `closed_are_subcases` and `subcases_reflection`. The only hits are:
    - the `.lean` file itself, `C2FINAL/README.md` and `C2FINAL/gen_lean.py`;
    - `C2ENC/class_table.md`;
    - `AUDIT3/reports/A5_central_geometry.md`, whose row 12 says that the auditor recomputed the closure in Python;
    - `WRITEUP/SYMMETRIC.md` (ll. 127, 207), which only states the claim.

    None of these is Lean output.
  - The Lean check is recorded only in `C2FINAL/README.md` section 6: "Core Lean 4.24.0, `decide +kernel`, axioms
    `propext` only, about 6 s".
  - So by the rule of Section fd (`sections/fd.tex` ll. 76-78), the label of `Central34.subcases_reflection`,
    `Central34.closed_are_subcases` and `Central34.all_cases_closed` is "Lean-checked according to the record".
  - All three proofs are `decide +kernel` (ll. 281, 288, 292), so "by kernel evaluation, so computer-assisted" stays
    correct.
  - `C3LEAN/C3Cover.lean` has saved logs: `C3LEAN/logs/compile.log` l. 18 reads "`C3Cover.all_roots_covered` depends
    on axioms: [propext, Quot.sound]", and there is also `C3LEAN/review/logs`. So the C3 item keeps "Lean-checks", as
    the finding says.
- Location 1: Remark `mb:rem:main3`, item `HalfTurn34`, ll. 1110-1111 (was ll. 1106-1107).
  - Old wording: "is Lean-checked by kernel evaluation, so computer-assisted (Theorem~\ref{cb:thm:c2})"
  - New wording: "is Lean-checked according to the record (\dirn{C2FINAL/README.md}, \S6), by kernel evaluation, so
    computer-assisted (Theorem~\ref{cb:thm:c2})"
  - Reason for the parenthesis: it names the record on which the qualified label rests. The same item already cites the
    status paragraph of that README.
- Location 2: `sections/mb.map.tsv`, row `mb:rem:main3`, column note (keeps the map in sync).
  - Old: "...; the case-split bookkeeping (cb:thm:c2, cb:thm:c3) is Lean-checked by kernel evaluation, so
    computer-assisted"
  - New: "...; the case-split bookkeeping is Lean-checked according to the record (cb:thm:c2) or Lean-checked
    (cb:thm:c3), in both cases by kernel evaluation, so computer-assisted"
  - I rendered the note with the functions of `tools/make_appendix.py` (`collect_labels`, `clean_note`, `note_tex`;
    nothing was written). The result is "... the case-split bookkeeping is Lean-checked according to the record
    (Theorem~\ref{cb:thm:c2}) or Lean-checked (Theorem~\ref{cb:thm:c3}), in both cases by kernel evaluation, so
    computer-assisted". I did not regenerate `appendix_map.tex`, because that file is outside my edit scope.
- Other places in mb, checked; none needs a change for this finding:
  - The paragraph "Dependencies and rigour" (ll. 97-113) cites `cb:thm:c2` only as a result that Remark `mb:rem:main3`
    refers to, and gives it no label. Its sentence "Every Lean declaration stated below is Lean-checked" is about the
    declarations stated in this section, whose axioms logs are listed under "Lean version and axioms".
  - No other place in `mb.tex` cites `cb:thm:c2` or mentions the closure or bookkeeping of the central orbits. I
    grepped for `cb:`, `closure`, `orbit`, `bookkeeping` and `Central34`.
  - The layer-lemma clause (l. 1123: Theorems `ll:thm:layers`, `lg:thm:nesting`) keeps "Lean-checked", because
    `LAYERLEAN/logs/axioms.log` ll. 3 and 5 print the axioms of `layers_are_orbits` and `strict_nesting`.

## Finding 3 (minor): Theorem mm:thm:even in the main "We use" list

- Action: fixed.
- Location: paragraph "Dependencies and rigour", ll. 102-108 (was ll. 101-105).
- Check: before the edit, `grep mm:thm:even sections/mb.tex` found it in three places only:
  - l. 101, the Dependencies list;
  - l. 904, inside Remark `mb:rem:eight` (old ll. 901-906);
  - l. 1192, Coverage.

  It is not cited in any proof. I also classified every cross-section `\ref` of `mb.tex` by its enclosing environment
  with a short script. Exactly three remarks refer to results that no proof uses:
  - `mb:rem:generated` refers to `fd:lem:pos-cycle`;
  - `mb:rem:eight` refers to `mm:thm:even`;
  - `mb:rem:main3` refers to `ll:thm:layers`, `lg:thm:nesting`, `cb:thm:c2` and `cb:thm:c3`.

  Remark `mb:rem:seven` cites only `mm:thm:odd`, `mm:thm:mirror-polygon` and `mm:thm:axis-polygon`, and proofs use all
  three: `mm:thm:odd` is used in the proof of Theorem `mb:thm:nine`(b),(c), l. 977. So "Three remarks" is exact.
- Old wording: "... Theorems~\ref{mm:thm:mirror-polygon}, \ref{mm:thm:axis-polygon}, \ref{mm:thm:odd},
  \ref{mm:thm:even}, \ref{mm:thm:line}, and in Subsection~\ref{mb:ssec:three} ... \ref{ar:thm:main}. Two remarks refer
  to further results that no proof of this section uses: Remark~\ref{mb:rem:generated} (on the Lean proofs of
  Lemma~\ref{mb:lem:polygons}) to Lemma~\ref{fd:lem:pos-cycle}, and Remark~\ref{mb:rem:main3} ..."
- New wording: "... Theorems~\ref{mm:thm:mirror-polygon}, \ref{mm:thm:axis-polygon}, \ref{mm:thm:odd},
  \ref{mm:thm:line}, and in Subsection~\ref{mb:ssec:three} ... \ref{ar:thm:main}. Three remarks refer to further
  results that no proof of this section uses: Remark~\ref{mb:rem:generated} (on the Lean proofs of
  Lemma~\ref{mb:lem:polygons}) to Lemma~\ref{fd:lem:pos-cycle}, Remark~\ref{mb:rem:eight} (on the second Lean proof
  \texttt{mirror\_eight\textquotesingle} of Theorem~\ref{mb:thm:eight}(a)) to Theorem~\ref{mm:thm:even}, and
  Remark~\ref{mb:rem:main3} ..."
- Notes:
  - The remarks are listed in document order.
  - The parenthesis for `mb:rem:eight` follows the pattern of the other two, and its wording "second Lean proof"
    follows Remark `mb:rem:seven`.
  - The Coverage mention of `mm:thm:even` (l. 1196) is unchanged. That list names results that are the subject of
    another section, not results this section uses.

## Finding 4 (minor): [n] used both generically and as the codomain

- Action: fixed, with the requested wording verbatim.
- Location: paragraph "Conventions", ll. 119-121 (was ll. 116-118).
- Check:
  - `mb:ssec:bridge` exists. It is the Subsection "From configurations to points of the plane" (l. 255), where
    $f\colon[k]\to[n]$ is introduced (l. 261).
  - In Lean, `ErdosSzekeres/Omission/Realization.lean:9` has `structure Configuration (n : Nat)` with
    `point : Fin n -> Point`, and `:64` defines `HasCap c k := exists f : Fin k -> Fin n, StrictMono f /\ ...`. So the
    domain of the cap map is `Fin k` and its codomain is `Fin n`, as the new sentence says.
  - The new generic "[m] ... Lean's Fin m" matches the convention of Section mm (`sections/mm.tex` ll. 96-97).
- Old wording: "Where $[n]$ is the index set of a configuration of $n$ points, or the domain or codomain of a cap map
  such as $f\colon[k]\to[n]$ (Subsection~\ref{mb:ssec:bridge}), it is the same set viewed as Lean's \texttt{Fin n}, as
  in Definition~\ref{mm:def:config}."
- New wording: "Where $[m]$ is the index set of a configuration of $m$ points, or the domain or codomain of a cap map
  (such as $f\colon[k]\to[n]$ in Subsection~\ref{mb:ssec:bridge}), it is the same set viewed as Lean's
  \texttt{Fin m}, as in Definition~\ref{mm:def:config}."

## Finding 5 (minor): Schroeder's archive without a pointer to the References

- Action: fixed.
- Location: paragraph "Sources", item on the bridge files, ll. 47-48 (was l. 47; the source line is rewrapped).
- Check:
  - `bibliography.tex` has `\bibitem{Sch26}`: M. Schroeder, Erdos-Szekeres: upper bounds for convex heptagons and
    octagons, archive version 1, 19 September 2026, doi:10.5281/zenodo.22842891.
  - The same version-1 archive with the same DOI is named in `docs/THIRD_PARTY.md` ll. 46-48 and in the adaptation
    headers of the bridge files (for example `ErdosSzekeres/Omission/Baek.lean` ll. 2-3).
  - The front matter (`proofs.tex` l. 96) already cites "the archive of M.~Schroeder~\cite{Sch26}".
- Old wording: "using the strategy of M.~Schroeder's archive), and six files adapted from that archive (MIT licence):"
- New wording: "using the strategy of M.~Schroeder's archive~\cite{Sch26}), and six files adapted from that archive
  (MIT licence):"
- Notes:
  - This is the first `\cite` in a section file. The comment at the top of `bibliography.tex` says "The sections cite
    them inline, by author and title". That comment is now slightly out of date, and I did not change it because the
    file is outside my edit scope.
  - In the standalone wrapper the citation is undefined, because the wrapper does not input the bibliography. A scratch
    wrapper that also inputs `../bibliography` (`build/final_mb_r1_bibcheck.tex`, two passes: exit 0, no citation
    warning, no error, no overfull box) shows it resolved as "[9]", the Schroeder entry. `proofs.tex` inputs
    `bibliography.tex`, so the citation resolves in the full document.

## Checks

- Diff against `snapshots/final-r1-pre/`: only the five passages above changed in `mb.tex`, and one note in
  `mb.map.tsv`. Everything else is byte-identical.
- Labels: the sequence of the 57 `\label` lines is unchanged.
- Map: 43 lines, 5 tab-separated fields each, ASCII only.
- No statement environment was touched, so no Lean statement needed re-matching. I re-read the Lean declarations
  behind the edited sentences and they match the new wording:
  - `Central34.subcases_reflection`, `Central34.closed_are_subcases` and `Central34.all_cases_closed` in
    `C2FINAL/Central34Orbits.lean` (ll. 273, 284, 291);
  - `Configuration` and `Configuration.HasCap` in `ErdosSzekeres/Omission/Realization.lean` (ll. 9, 64).
- Compile: from `build/`, `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error mb_wrapper.tex`, run twice.
  - Exit 0 both times, 0 errors, no "Missing $".
  - 0 overfull boxes, so 0 above 1pt.
  - No multiply defined labels and no rerun request; 16 pages.
  - Undefined references: only `fd:` labels and other sections' export labels. This is the same set as in the
    pre-edit baseline build (`build/final_mb_r1_base.*`). The one addition is the citation `Sch26`, which is expected
    in the standalone check (see Finding 5).
  - Underfull boxes: 3, against 2 in the baseline. The new one is a page-level underfull vbox at the page-2 break of
    the standalone build, caused by a pagination shift. I checked the page visually and it looks normal. The full
    document paginates differently.
- pdftotext: the new sentences are typeset as intended. Remark 1.34 is `mb:rem:eight`, Theorem 1.33 is
  `mb:thm:eight` and Subsection 1.2 is `mb:ssec:bridge`.
- grep of `mb.tex` and `mb.map.tsv`:
  - no machine paths and no tool names;
  - no "verified" or "certified" in `mb.tex`;
  - no `\newcommand` or `\usepackage`.
