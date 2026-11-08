# Final pass, round 1: fixes in section ec

Files edited: `sections/ec.tex`, `sections/ec.map.tsv` (pre-edit copies in `snapshots/final-r1-pre/`).
No label was added, removed or renamed. Everything outside the two changes below is byte-identical to the snapshot
(checked with `diff`).

## Finding 1 [minor]: rigor label of `ec:prop:ex341`

- Action: fixed.
- Location: `sections/ec.tex`, head of Proposition `ec:prop:ex341` (line 784 before the edit, 785 after it, because
  the fix for finding 2 adds one line earlier); `sections/ec.map.tsv`, row `ec:prop:ex341`, note column.
- Check of the written proof (done before the change). The Lean statement
  (`PRIMEFOLD/compat/lean/PCompatCore.lean:277`, SHA-256 prefix `ebc6aacefadb`, unchanged) is
  `Compat 341 (2 ^ (341 - 1)) ∧ 341 = 11 * 31 ∧ ¬ Nat.Prime 341 ∧ 2 ^ 10 % 11 = 1 ∧ 2 ^ 10 % 31 = 1 ∧ 2 ^ 10 % 341 = 1`,
  with `Compat m N := N % m = 0 ∨ N % m = 1 % m` (line 205); the written statement matches it exactly. The written
  proof (ec.tex, the paragraph after "The computation is small enough to do by hand, as follows.") proves all six
  conjuncts without the machine computation: 11·31 = 341; 11 is a divisor of 341 with 1 < 11 < 341, so 341 is not
  prime; 2^10 = 1024 = 93·11 + 1 = 33·31 + 1 = 3·341 + 1, which gives the three remainders 1; and
  2^340 = (2^10)^34 ≡ 1 (mod 341), so 2^340 mod 341 = 1 = 1 mod 341, the second alternative of `Compat`. Each product
  was rechecked (small integer arithmetic, also confirmed by a one-line script), and 341 − 1 = 340 involves no
  truncation. So the proof is complete and can be checked by hand, and Section fd (fd.tex:92-96) asks for the label
  "computer-assisted in Lean". (Side check, no change: the proof text says that Lean uses `Nat.not_prime_mul` with
  11 ≠ 1 and 31 ≠ 1; at the pinned Mathlib revision `f897ebcf` this lemma takes `a ≠ 1` and `b ≠ 1`, so the text is
  right.)
- Old head: `\begin{proposition}[$m=341$; computer-assisted; \leanref{PCompat.ex341}{PRIMEFOLD/compat/lean/PCompatCore.lean:277}]\label{ec:prop:ex341}`
- New head: `\begin{proposition}[$m=341$; computer-assisted in Lean; written proof by hand; \leanref{PCompat.ex341}{PRIMEFOLD/compat/lean/PCompatCore.lean:277}]\label{ec:prop:ex341}`
- Old map note: `computer-assisted (kernel decide; axioms propext only); arithmetic also done by hand in the proof`
- New map note: `computer-assisted in Lean; written proof by hand (Lean: kernel decide; axioms propext only)`
- Unchanged on purpose: the Coverage entry "\lean{ex341} (Proposition~\ref{ec:prop:ex341}, a finite computation)"
  and the Axioms paragraph ("checked by kernel evaluation (\lean{decide})") describe the Lean proof, which is still a
  finite computation; both remain accurate under the new label.
- Map check: 42 rows, 5 fields each, ASCII only. The note typesets as plain text with the appendix generator's own
  note functions (tested by importing `tools/make_appendix.py` without writing `appendix_map.tex`, which was not
  regenerated).

## Finding 2 [minor]: notation for iterates of maps

- Action: fixed.
- Location: `sections/ec.tex`, item (C) of the list after Remark `ec:rem:cases` (lines 170-172 before the edit,
  170-173 after it). This is the first use of a power of a map in the section (the superscripts before it are powers
  of numbers).
- Old: `... then $c\notin S$. (The power $\mathrm{rotAbout}(c,2\pi/m)^{m/2}$ is the half-turn $p\mapsto 2c-p$, and
  $p$, $c$, $2c-p$ would be three distinct collinear points of $S$.)`
- New: `... then $c\notin S$. (In this section, for a map $f$ and $n\in\N$, $f^n$ is the $n$-fold composite of $f$,
  written $f^{[n]}$ in Section~\ref{fd:sec}; so $f^0=\mathrm{id}$. The power $\mathrm{rotAbout}(c,2\pi/m)^{m/2}$ is
  the half-turn $p\mapsto 2c-p$, and $p$, $c$, $2c-p$ would be three distinct collinear points of $S$.)`
- Coverage of the later uses: the clause is stated for the whole section, so it covers $\rho^j$ in
  Remark `ec:rem:es7-sharp` (lines 250-251 before the edit), $\rho^{m-1}y$ in Remark `ec:rem:orbits` (line 263) and
  $\rho^j$ in Remark `ec:rem:big-order` (lines 401-403), all of which come after it, and also the order of a rotation
  used in those remarks. The clause is restricted to maps, so the powers of numbers in the section ($\zeta_m^k$,
  $\zeta^j$ in a group with zero, $2^{m-1}$, $\abs{x}^2$) keep their usual meaning; I found no other superscript on a
  map. `fd:sec` is a foundations label, which sections may reference. Item (C) restates Lemma `lg:lem:centre`
  (`centre_not_mem_of_even`, `LAYERLEAN/LayerLemma.lean:582`); its statement is unchanged, and only the explanatory
  parenthetical gained the clause. (The half-turn claim is unaffected: for even m > 0, the (m/2)-fold composite of the
  rotation by 2π/m is the rotation by π.)

## Compile check

From `build/`: `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error ec_wrapper.tex`, run twice. Both runs
exit 0. The log has no errors and no "Missing $". It has no overfull boxes at all (so 0 overfull boxes > 1pt). The
undefined references are labels of other sections only (fd:, ll:, lg:, oc:, sr:, including the new `fd:sec`), as
expected in the standalone check.
