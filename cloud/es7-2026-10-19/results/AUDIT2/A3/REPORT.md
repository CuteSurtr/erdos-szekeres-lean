# AUDIT2 A3: the 450-case hull-pair split (sub-case (ii))

Inputs: branch es7-cloud, TASK.md at 852bee7, budget 1.75 h. Tools built here from source:
CaDiCaL 3.0.1 (c60730422), cake_lpr a36874a8. Files in this directory: `chk_cover.py`,
`dec_data.py`, `run1.sh` (my own scripts), `obligation_sha256.txt`, `my_cover_lrat.jsonl`.

## Verdict

I found nothing that breaks the claim or weakens the trust base in my focus. The 122 cover
obligations do imply that every model of F satisfies one of the 450 case cubes, the obligation
CNFs are byte for byte the ones cake_lpr verified (I re-solved and re-checked all 122 myself),
and the Lean statements `RootCertificate` / `UpCertificates` / `caseTable` name exactly those
CNFs. There are two cosmetic findings.

## Findings (most serious first)

1. **Cosmetic. The upper-chain order is written backwards in the docs.**
   `results/Mii-S/soundness.md:27` gives the ccw hull as `…, 33, 34−u_k, …, 34−u1, u1, …, u_k`.
   The hullsplit.py docstring (`results/Mii-S/scripts/hullsplit.py:7`) says the same, hedged
   with "reversed appropriately". The code (`hull_ccw`, hullsplit.py:31-35) produces
   `33, 34−u1, …, 34−u_k, u_k, …, u1`. Example: U=(3,5) gives `[…, 33, 31, 29, 5, 3]`. The code
   is the geometrically correct order: going left from P33, the first upper vertex is the one
   with the largest x, which is 34−u1. The doc is wrong and the code is right. The certificate
   argument does not depend on this at all.
2. **Cosmetic. The geometric argument says more than it needs, and it is not formalized.**
   `soundness.md:13-14` says each realisation satisfies the cube of "exactly one" case.
   Uniqueness is only tested at random, never proved, and nothing needs it. The Lean proof uses
   only the certificate argument (`not_dimacsSatisfiable_of_clauseCover₂`). That argument is
   purely propositional, so the geometric §§1-6 are not in the trust base. Re-deriving them
   anyway, I found steps 2-6 correct:
   - P1 and P33 are the x-extremes with equal y.
   - A hull pair at chord height would put 4 points on a line.
   - |V| ∈ {4, 6} gives exactly 30 + 420 = 450 (U, L) cases.
   - (a), (b) and (c) hold; in (c) a vertical supporting line is impossible because P1 and P33
     lie on either side.
   - The orbit identity X(i,j,k) = X(34−k,34−j,34−i) holds: the reflection flips the sign, and
     reversing the order flips it back.

## What I checked and found sound

1. **F.** Rebuilt as `V3Z/tools.txt` says (gen_etv.py, then mirgen.py `--interior --yflip-unit`):
   sha256 `69c1dc8f…ffff932d`, a match.
2. **The obligation CNFs.** I regenerated all 122 with `Mii-S/scripts/cover.py` from that F.
   - All 122 sha256 equal those in `Mii-S/cover_lrat.jsonl`.
   - The obligation names are the same set: none missing, none extra, no duplicate.
3. **The cover logic, checked on the files themselves** (`chk_cover.py`, my own parser, no
   Mii-S code):
   - Each file is F's body verbatim plus extra clauses. Header counts are correct and every
     literal is in 1..47002.
   - root adds 121 distinct blocking clauses.
   - The unit sets of the 121 up files are exactly the negations of root's clauses, one to one.
   - Negated, the blocking clauses over all up files are exactly the 450 cubes of
     `Mii-S/cases.icnf`, each exactly once. Per U that is 120 (U=∅), 15 (|U|=1) and 1 (|U|=2).
   - F + cube gives the `cases.jsonl` cnf_sha256 for 450 of 450 cases.

   So: root UNSAT ⇒ every model of F satisfies some UP(U). up:U UNSAT ⇒ every model of F ∧ UP(U)
   satisfies some cube(U,L). Hence every model of F satisfies one of the 450 case cubes. This
   needs no geometry and no containment UP(U) ⊆ cube(U,L).
4. **cases.jsonl and cases.icnf** match `hullsplit.cases()` and `hullsplit.cube()` in order,
   names, U, L and literals.
5. **My own solve and check of all 122 obligations** (`my_cover_lrat.jsonl`):
   - CaDiCaL 3.0.1 with `--lrat`, then cake_lpr, with the verdict matched as the exact line
     `s VERIFIED UNSAT`. 122 of 122 are rc 20 and `s VERIFIED UNSAT`.
   - Totals: 471 s solve, 291 s check, 1.02 GB of proofs (deleted).
   - Largest: up: (180 s, 418,325,234 bytes) and root (121 s, 199,097,142 bytes). The proof sizes
     are identical to those recorded and to Haudit task 3. This is a third independent run
     after Mii-S and Haudit.
6. **The Lean statements name the same CNFs** (`dec_data.py`). I decoded `V2L/Data.lean`
   (sha256 `9df2885a…`) exactly as `unpack`/`decLit` do: 4 hex digits per literal, the low k
   digits, 2z or 2|z|+1.
   - Decoded counts: upSets 121, upCubes 121, caseSpecs 450, caseCubes 450.
   - `rootCnf` = F ++ upCubes.map negClause has the root sha256.
   - For every (U, UP) in upTable = upSets.zip upCubes, F ++ units(UP) ++ (casesOf U).map
     negClause has the sha256 of `up:U`: 121 of 121. Here casesOf is the filter of caseTable on
     p.1.1 = U.
   - caseCnf has the `cases.jsonl` sha256 for 450 of 450.
   - No zero literal in any cube.

   This independently reproduces README §5 without `v2l_data`. One assumption remains: the
   DIMACS text of `interiorCnf 33 7` is F.cnf, which is A2's item.
7. **The Lean composition**, read in full:
   - `ClauseCover.lean`: `exists_cubeSat_of_block`, `not_dimacsSatisfiable_of_clauseCover₂`
     and the leaf forms.
   - `Main.lean`, `Facts.lean` (`upTable_snd` uses the equal lengths, `mem_caseCubes_of_casesOf`),
     `TreeMain.lean` and `FinalTree.lean`.

   I found the following:
   - The two-level argument is exactly the one above.
   - Its nonzero side conditions are discharged by kernel facts.
   - zip truncation is harmless, because the lengths are proved equal: 121/121 and 450/450.
   - Every cube in `casesOf U` is shown to be a `caseTable` entry, so it gets a case
     certificate.
   - The hypotheses of `mirrorExclusionLine_final` about sub-case (ii) are only:
     - `RootCertificate`;
     - `UpCertificates`;
     - leaf UNSAT facts `cubeCnf (cubeCnf F p.2) l` for p ∈ caseTable.
   - No hypothesis is vacuous: upTable is non-empty and is the full 121.
8. **The 172 direct cases.** `Haudit/t5_all172.jsonl` has 172 distinct cases, and they are
   exactly the `method: direct` cases of `V3Z/cases_final.jsonl`. Each has a sha256 equal to
   `cases.jsonl`, rc 20 and `s VERIFIED UNSAT`. The other 278 are the wave cases, which V3 pins
   to the same case CNF (`v3_check.py:56-69` checks F + cube against the `cases.jsonl` sha256).

## What I did not check

- I did not build the Lean packages: no Lean toolchain here, and Mathlib from source does not
  fit the budget. For `#print axioms` and `treeOf_check` I rely on `V2-L/V2L/Audit.lean`
  (`#guard_msgs`) and the logs (that is A1).
- The 278 wave cases' trees and leaves (A4-A6), and the encoding soundness of F (A2).
