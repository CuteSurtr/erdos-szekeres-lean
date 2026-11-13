# Re-check of section ec, final pass, round 1

Inputs:
- `reviews/final-ec-r1-fix.md`, the fixer's log. I used it only as a pointer and re-checked every claim below.
- `snapshots/final-r1-pre/ec.tex` and `snapshots/final-r1-pre/ec.map.tsv` (before the edit), and the current
  `sections/ec.tex` and `sections/ec.map.tsv` (after it). The current files have SHA-256 prefixes `bf60ea4b643f` (tex)
  and `436b66a89f71` (map).
- Lean sources in RES:
  - `PRIMEFOLD/compat/lean/PCompatCore.lean`, SHA-256 prefix `ebc6aacefadb`, the prefix that ec.tex cites;
  - its axioms log `PRIMEFOLD/compat/lean/PCompatCore.out`;
  - `LAYERLEAN/LayerLemma.lean`, lines 103-105, 296-300 and 578-600.
- The rules in `sections/fd.tex`. A fixer edited fd.tex at the same time in this pass. Its only hunk (lines 67-86) is
  the evidence-kind (a) paragraph. That edit moved the rules the findings cite down by 8 lines:
  - the "computer-assisted in Lean" rule, cited as fd.tex:92-96, is now fd.tex:100-104;
  - the iterate notation $f^{[n]}$ is now fd.tex:133-136;
  - the Default-notation sentence that allows "$f^n$ for $f^{[n]}$", cited as fd.tex:142-146, is now fd.tex:150-154.

  The wording of these rules did not change.

Paths are relative to STAGE (sections, snapshots, build, reviews) or to RES (records and Lean sources). I ran no git
command, no Lean tool and no SAT tool.

**Verdict: pass.** The fixer fixed both findings (both minor), and both fixes are correct. The edit introduces no
blocker, major or minor problem in ec.tex or ec.map.tsv. One assembly step remains outside the section's files:
`appendix_map.tex` must be regenerated (section 4). It is reported as minor and needs no change to ec.

## 1. The findings

| # | finding | fixer | re-check |
|---|---|---|---|
| 1 | minor: the head of `ec:prop:ex341` and its map note say "computer-assisted", but the section also gives a complete written proof by hand | fixed | **resolved** |
| 2 | minor: powers of maps ($\rho^j$, $\mathrm{rotAbout}(c,2\pi/m)^{m/2}$) are used without a defining clause | fixed | **resolved** |

### Finding 1: rigor label of `ec:prop:ex341`

The current head (`sections/ec.tex:785`) is
`[$m=341$; computer-assisted in Lean; written proof by hand; \leanref{PCompat.ex341}{PRIMEFOLD/compat/lean/PCompatCore.lean:277}]`.
The map note (`sections/ec.map.tsv:37`) is
`computer-assisted in Lean; written proof by hand (Lean: kernel decide; axioms propext only)`.

**The statement matches Lean.**
- `PCompatCore.lean:277-278` is
  `Compat 341 (2 ^ (341 - 1)) ∧ 341 = 11 * 31 ∧ ¬ Nat.Prime 341 ∧ 2 ^ 10 % 11 = 1 ∧ 2 ^ 10 % 31 = 1 ∧ 2 ^ 10 % 341 = 1`.
- `Compat m N := N % m = 0 ∨ N % m = 1 % m` (line 205).
- The written statement (ec.tex:786-787) gives the same six conjuncts in the same order, and `341 - 1` is not
  truncated.

**The Lean proof is a finite computation.** The proof (lines 279-281) runs
`refine ⟨Or.inr (by decide), by decide, ?_, by decide, by decide, by decide⟩`, then
`rw [show (341 : ℕ) = 11 * 31 by decide]` and `exact Nat.not_prime_mul (by decide) (by decide)`. It runs under
`set_option exponentiation.threshold 400` (line 275). So five of the six parts are decided by kernel evaluation. This
is the first case of "computer-assisted" in fd.tex:88-95 ("the Lean proof of the statement, or of one of its parts, is
itself a finite computation").

**The written proof is complete without the machine.** I re-did the arithmetic of the proof (ec.tex:790-798):
- $11\cdot31=341$.
- $2^{10}=1024=93\cdot11+1=33\cdot31+1=3\cdot341+1$. Since $1$ is less than $11$, $31$ and $341$, the three
  remainders are $1$.
- $340=10\cdot34$, and $2^{340}=(2^{10})^{34}\equiv1\pmod{341}$. So $2^{340}\bmod341=1=1\bmod341$, and this is the
  second alternative of `Compat`.
- $11$ divides $341$ with $1<11<341$, so $341$ is not prime under the standard definition.

A one-line Python check confirms each product and $2^{340}\bmod341=1$. All six conjuncts are proved by hand-checkable
arithmetic.

**The new label is the right one.** fd.tex:100-104 prescribes exactly "computer-assisted in Lean" for this situation,
with the example wording "computer-assisted in Lean; written proof by hand". The new head uses that wording, as
pc.tex:769 (`pc:thm:word`) already does.
- The label is not rounded up: the computational nature of the Lean proof is kept ("in Lean"), and the proof text
  still says "This is a finite computation ... Lean checks the five numerical claims by kernel evaluation".
- The label is not rounded down: the statement still carries its Lean reference, so it remains Lean-checked
  (fd.tex:115-116).

**The map note's claims hold.**
- `PCompatCore.out` has `'PCompat.ex341' depends on axioms: [propext]`, so "axioms propext only" is right.
- "kernel decide" was already in the old note.

**The rest of ec still agrees with the new label.**
- The Coverage entry (ec.tex:906-907, "a finite computation") and the Axioms paragraph (ec.tex:55-60, "checked by
  kernel evaluation (\lean{decide})") describe the Lean proof, so both remain accurate.
- A grep for "computer-assisted" in ec.tex finds only line 109 (about the case classes) and line 785. No other place
  in ec labels ex341.
- No other section, and neither proofs.tex nor bibliography.tex, mentions ex341.

### Finding 2: notation for iterates of maps

The new text is in item (C), at `sections/ec.tex:170-173`:
"(In this section, for a map $f$ and $n\in\N$, $f^n$ is the $n$-fold composite of $f$, written $f^{[n]}$ in
Section~\ref{fd:sec}; so $f^0=\mathrm{id}$. The power $\mathrm{rotAbout}(c,2\pi/m)^{m/2}$ is the half-turn ...)".

**The clause is at the first use.** I checked all 106 source lines of ec.tex that contain `^`. Before line 172 the
only superscripts are powers of numbers: $e^{2\pi i/m}$ (line 13) and $2^{m-1}$ (lines 21-22). So
$\mathrm{rotAbout}(c,2\pi/m)^{m/2}$ (line 172) is the first power of a map. This is where fd.tex:153-154 ("defines
its symbols where it introduces them") wants the definition.

**It covers the later uses.** There are three later powers of maps, all after the clause and all with natural
exponents:
- $\rho^j$ at lines 251-252, with $j\in\N$ stated;
- $\rho^{m-1}y$ at line 264, with $m\in\{4,5\}$;
- $\rho^j$ at lines 402-404, with $j\in\N$ stated.

The clause says "In this section", so it covers all three.

**It does not clash with other superscripts.** The words "for a map $f$" exclude everything else that carries a
superscript in ec:
- powers of numbers or field elements: $\zeta^j$, $\zeta_m^k$, $a^j$, $a^{-1}$, $\lambda^{-1}$, $\abs{x}^2$,
  $2^{m-1}$, and $x^m$ in $x\mapsto x^m$;
- set exponents: $\R^2$ and $\R^{\mathrm{Fin}\,t}$.

No map carries $^{-1}$ or a non-natural exponent. In the $\zeta$-invariance lemmas, $\zeta^jz$ is a power of an
element, and it agrees with the $j$-fold composite of $z\mapsto\zeta z$ anyway.

**It is consistent with fd and with Lean.**
- fd.tex:133-136 defines $f^{[n]}$ as the $n$-th iterate with $f^{[0]}=\mathrm{id}$. The clause's
  "$f^0=\mathrm{id}$" therefore follows from "written $f^{[n]}$ in Section fd".
- fd.tex:150-154 explicitly allows "$f^n$ for $f^{[n]}$".
- The Lean proof of `centre_not_mem_of_even` (`LAYERLEAN/LayerLemma.lean:586`) itself uses
  `(rotAbout c (2 * Real.pi / m))^[m / 2]`, the iterate that the clause defines.

**The claims next to the clause are correct.** I checked two identities with sympy (complex form of
Definition fd:def:rot, plus a numerical check in real coordinates; script
`build/final_ec_r1_recheck_iterates.py`, output "ALL OK"):
- for even $m\in\{2,4,\dots,12\}$, the $(m/2)$-fold composite of $\mathrm{rotAbout}(c,2\pi/m)$ is $p\mapsto2c-p$;
- for $s\in\{4,5,7,8\}$ and every $k$ coprime to $s$, with $jk\equiv1\pmod s$, $\rho^j=\mathrm{rotAbout}(c,2\pi/s)$
  for $\rho=\mathrm{rotAbout}(c,2\pi k/s)$.

A first version of the script worked in real form and printed FAIL. The cause was only that sympy does not simplify
polynomial identities in $\cos(2\pi/5)$ and $\cos(2\pi/7)$; the complex form settles them exactly.

**The reference `\ref{fd:sec}` is acceptable.**
- `fd:sec` is the section label that the contract requires (`\section{...}\label{<key>:sec}`). It is defined at
  fd.tex:1, so it resolves in the assembled document.
- Other parts of the document already cite such labels: proofs.tex:34 and 41 cite `fd:sec`, the generated appendix
  cites it, and cb cites `sa:sec`.
- The finding itself proposed this reference.

The contract's list of fd labels does not name it, but it is fd's own section label, so I do not raise this.

## 2. Diff review (snapshot vs current)

**ec.tex.** `diff -u` shows exactly two hunks: `@@ -167,9 +167,10 @@` (item (C)) and `@@ -781,7 +782,7 @@` (the
ex341 head). The file grew from 923 to 924 lines. A whitespace-insensitive word-level diff shows exactly two changes:
- "(The" became "(In this section, for a map $f$ and $n\in\N$, $f^n$ is the $n$-fold composite of $f$, written
  $f^{[n]}$ in Section~\ref{fd:sec}; so $f^0=\mathrm{id}$. The";
- "computer-assisted;" became "computer-assisted in Lean; written proof by hand;".

The re-wrapped remainder of item (C) is word-for-word unchanged.

**ec.map.tsv.** One line changed: row `ec:prop:ex341`, note column only. The label, kind, lean_name and file_line
fields are unchanged. The map has a header and 41 data rows, each with 5 fields, ASCII only. Every label is defined
in ec.tex. I checked this with the generator's own functions (`collect_labels`, `check_ascii`, `clean_note`,
`note_tex`), imported read-only with `python3 -B` so that nothing was written. The new note typesets as plain text:
"computer-assisted in Lean; written proof by hand (Lean: kernel decide; axioms propext only)".

Referee checks on the hunks:
- **Mathematics:** correct (section 1).
- **Faithfulness to Lean:**
  - The statement head of `ec:prop:ex341` changed only in its rigor label. The statement was re-read against
    `PCompatCore.lean:277-278` and matches.
  - The restatement of `centre_not_mem_of_even` in item (C) is unchanged. I re-read it against
    `LayerLemma.lean:582-584`; it is faithful (`0 < m`, `Even m`, `Invariant (rotAbout c (2 * Real.pi / m)) S`,
    `GeneralPosition S`, `p ∈ S`, `p ≠ c`, conclusion `c ∉ S`).
- **Claims about files:**
  - Lean file and line: `ex341` is at `PCompatCore.lean:277`.
  - Axioms: `[propext]`, as stated.
  - The cited Mathlib lemma is unchanged text, so I did not re-check it.
- **Rigor labels:** the new label is the one fd prescribes, neither rounded up nor rounded down.
- **No machine path or tool name.** A grep of ec.tex and ec.map.tsv for the four forbidden machine-path prefixes of
  the contract and for tool names finds nothing. A grep for "verified", "certified", "certify" and "verify" also finds
  nothing.
- **Labels:** the 47 `\label`s are identical before and after.
- **LaTeX:**
  - No macro is defined and no package is loaded.
  - The new text contains no `\lean` or `\dirn` argument, so `\nolinkurl` and spaces are not an issue.
  - `$\N$`, `$f^{[n]}$`, `$\mathrm{id}$` and `Section~\ref{...}` are sound.
  - Both files end with a newline and contain no carriage return.
- **Scope:** nothing outside the two findings changed.

## 3. Compile

I compiled the wrapper `build/ec_final_recheck_r1_wrapper.tex`, which is byte-identical in content to the contract
wrapper `build/ec_wrapper.tex`. It was run twice from `build/` with
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`.
- **Clean build:** both runs exit 0. The log has no `!` error, no "Missing", no multiply defined label and no rerun
  request. The PDF has 12 pages.
- **Overfull boxes:** 0, so none above 1pt.
- **Underfull boxes:** 6.
- **Undefined references** are only labels of other sections:
  - `fd:def:cp`, `fd:def:gp`, `fd:def:inv`, `fd:def:ngon`, `fd:def:orient`, `fd:def:point`, `fd:def:rot`, `fd:sec`;
  - `lg:lem:centre`, `lg:lem:polar`;
  - `ll:lem:minperiod`, `ll:thm:card-peel`, `ll:thm:layers`, `ll:thm:reduction`;
  - `oc:lem:perm`, `oc:lem:rot-inv`, `oc:lem:same-ray`, `oc:thm:phase-orbit`;
  - `sr:def:classes`.

  These are expected in the standalone check. The only new one is `fd:sec`, discussed in section 1.

**Comparison with the snapshot.** I compiled the pre-edit snapshot the same way
(`build/ec_final_recheck_r1_snapwrapper.tex`, exit 0 twice).
- The snapshot has 7 underfull boxes. The current build has the same six, with source lines shifted by one.
- The snapshot's underfull box at the ex341 head (source lines 785-787, badness 1163) is gone.
- The edit adds no typesetting warning.

**Rendering.** `pdftotext` shows both passages as intended. The text reads "... f^n is the n-fold composite of f,
written f^[n] in Section ??; so f^0 = id. The power ...", where `??` is the standalone placeholder for `fd:sec`. The
head reads "Proposition 1.36 (m = 341; computer-assisted in Lean; written proof by hand; Lean: PCompat.ex341,
PRIMEFOLD/compat/lean/PCompatCore.lean:277)".

## 4. Remaining findings

- **minor (assembly step, not a defect of the ec edit).** `appendix_map.tex:248` still shows the old note for
  `ec:prop:ex341` ("computer-assisted (kernel decide; axioms propext only); arithmetic also done by hand in the
  proof"). `appendix_map.tex` was generated at 21:39, and ec.map.tsv was edited at 21:48. The fix log says the
  appendix was not regenerated, which is consistent with the cb, mb, pc and front fix logs of this pass.
  - Fix: after all final-pass fixes, run `python3 tools/make_appendix.py` from STAGE.
  - No change to ec.tex or ec.map.tsv is needed. The new note passes the generator's checks and typesets cleanly.

No blocker or major finding remains or was introduced.

Observation, not raised as a finding: the section-wide convention sits inside the explanatory parenthetical of item
(C). That is the place the finding prescribed and that fd.tex:153-154 requires (the first use). Moving it would be
churn in the final pass.
