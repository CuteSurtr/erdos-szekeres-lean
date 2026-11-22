# res118-rowblocks DESIGN (M0), 22 Nov 2026

## 1. Target

Res118 (`/home/jay/research/data/formalize-20261122/res118/lean/Res118/Glue.lean`) defines, for a literal support
`s : List ℕ` over the 154 residual states,

```lean
def ValidUnitRow (s : List ℕ) : Prop :=
  ∀ n, ∀ c : Configuration n, ∀ (noCap : ¬ c.HasCap 6) (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)), 0 < n →
      1 ≤ ∑ i ∈ lsupp s, holesOf (c.residualOccupied noCap noOctagon noJunction) i
def BlockValid (rows : List (List ℕ)) : Prop := ∀ s ∈ rows, ValidUnitRow s
```

Targets (Mathlib side, module `RowGeo.Blocks`):

```lean
def RowsUnsat (rows : List (List ℕ)) : Prop := ∀ s ∈ rows, ¬ EncB.DimacsSatisfiable (RowEnc.rowCnf s)
theorem blockValid_P : RowsUnsat Res118.rowsP → Res118.BlockValid Res118.rowsP     -- likewise Q, U, A
theorem residual_bound_118_of_rows (n66 : N66Bound 55) (hP : RowsUnsat rowsP) (hQ …) (hU …) (hA …) (six slices) :
    Partition.ResidualBound 118        -- = Res118.residual_bound_118_of_slices with vP … vA discharged
```

and the text form `rowUnsat_of_text`: if every `EncB.parseDimacs` parse of `RowEnc.rowText s` (the exact string the
exe prints) is unsatisfiable, then `¬ DimacsSatisfiable (rowCnf s)` (ENCBLEAN `parseDimacs_render`).

Label when done: `BlockValid rowsP/Q/U/A` **Lean-checked modulo `RowsUnsat` (one cake_lpr verdict per row, 2,021
supports) and trust items E1-E6**. No bound and no record label changes.

Core lemma (generic in S, nothing evaluated on a concrete row):

```lean
theorem RowGeo.missing_of_unsat (S : List ℕ) (hS : RowEnc.WF S) (h : ¬ DimacsSatisfiable (rowCnf S))
    {n} (c : Configuration n) (noCap) (noOctagon) (noJunction) : ∃ x ∈ S, ⟨x, _⟩ ∉ c.residualOccupied …
```
`WF S`: strictly increasing, entries < 154, `S.length ≤ 16` (all block rows have 9-14 entries; kernel-checked per block).

## 2. The generator (byte identity, M1)

Every certified row CNF was written by `coupled.CNF(S, octagon='full', static=True)` with `S` sorted, laid out as
`p cnf {nv} {len(clauses)}\n` + `' '.join(map(str, clause)) + ' 0\n'`:
- cut rows: `LO33N…/budget34/tools/cut34*.py build` (lines 77-90, `canonical(s)` asserts sorted, 8 ≤ |S| ≤ 17);
- pool rows: `fastbb-20261113/killtools/certify.py` (`coupled.CNF(S).dimacs()`, `S = sorted(...)`) and its p2 copies.
All copies of `coupled.py` (sha256 01277b36 RES33N, 959072b1 killtools = the receipts' `encoder_pins`, a867d827 lo33,
080c4c57/87eae3ab discovery) differ only in path strings; class `CNF` is identical. `fast_dimacs` (static block
first) is NOT the certified layout.

Numbering: all variables are allocated in the constructor, in this order: per pair (i<j, combinations order)
`before, cap_ge 2..4, cup_ge 2..6`; per triple (combinations) `orientation`; per 4-set (combinations) `convex_four`.
So nv = 9·C(n,2) + C(n,3) + C(n,4) (534 at n = 9, 1309 at n = 12: receipts agree). Lean: `allocCodes n` (codes of the
atoms in that order), `num a = 1 + first position of code a` through `EncB.numberMap` (ENCBLEAN/n66enc pattern),
decoded by `EncB.decode`; soundness never depends on the numbers being Python's (byte identity checks them).

`add(lits)` = `finish`: a `True` constant drops the clause, `False` constants are removed, duplicates removed,
tautologies dropped, literals sorted by |·|.

Clause order (generator lines refer to `fastbb-20261113/killtools/coupled.py`, sha256 959072b1):

| # | family (generator lines) | clause | Lean helper |
|---|---|---|---|
| F1 | threshold (60-62), per pair, cap k=2..3, cup k=2..5 | `[¬ge(t,i,j,k+1), ge(t,i,j,k)]` | `threshClause` |
| F2 | source (64), per pair, (u,v) ∈ [(i,j),(j,i)] | `[¬before(u,v), ¬ge(cup,u,v,h₁(S[u])+2)]` | `sourceClause` |
| F3 | empty direction (65-67) | `[¬before(u,v)]` if `CELLS[S[v]] − CELLS[S[u]] − {(1,6)}` is empty, then skip F4 | `emptyCheck` analog |
| F4 | domain (68-72), a=1..4, b=1..6, (a,b) not in that difference | `[¬before(u,v), ¬ge(cap,a), ge(cap,a+1), ¬ge(cup,b), ge(cup,b+1)]` | `domainClause` |
| F5 | transitivity (73-74), per ordered triple (permutations order) | `[¬before(a,b), ¬before(b,c), before(a,c)]` | `transClause` |
| F6 | growth (75-79), same triple: cap k=1..4, then cup k=1..6 | `[¬before(a,b), ¬before(b,c), ±ori(a,b,c), ¬ge(t,a,b,k), ge(t,b,c,k+1)]` | `growthClause` |
| F7 | forced sign (80-83), per triple (combinations) | `[ori(q)]` if TT[a,b,c] elif `[¬ori(q)]` if TT[a,c,b] | `fixedClauses` |
| F8 | packets (84-89), per 4-set, per permutation (itertools order), bits in BAD4 | 3 order lits + 4 sign lits | `packetClause` |
| F9 | convex-four (90-96), per 4-set, bits in product order | 4 sign lits + convex(quad) with polarity `[¬w,z,¬y,x].count = 2` | `convexClause` |
| F10 | no octagon (97-99), per 8-set (combinations) | `[¬convex(q) : q ⊂ eight, |q| = 4]` | `octClause` |

## 3. Soundness of each family (M3/M4)

Semantics (library `ErdosSzekeres.Omission.Coupled`, CoupledSemantics.lean): a `Context k n states` is an actual
residual configuration with injective owners `owner : Fin k → Fin n` of the states `S[i]`; atoms `before i j` =
owner order, `capGe/cupGe i j t` = threshold of `edge i j` = `labels n cup` of the earlier-to-later owner pair
(`(6 − future-cap rank, past-cup rank − 1)`), `positive` = orientation sign, `convex` = convex position.
Written argument: VERIFY309N20261113 §(c) (audit of the same `coupled.py`); this table names the Lean proof.

| # | written reason | Lean |
|---|---|---|
| F1 | thresholds of one integer label | from `Context.holds_ge` (new, one line) |
| F2 | remove v from a longest cup ending with (u,v): the prefix ends with some (t,u), so d₂(t,u) ≥ d₂(u,v) − 1, and (1, d₂(t,u)) is an incoming label of u, so h₁(state u) ≥ d₂(u,v) − 1 | **new**: `EndingPath` step case + `ActualRanks.rank_ge` + `ResidualDomains.owner_contains` |
| F3 | state separation: d(u,v) ∈ I(v) \ I(u), and ≠ (1,6) (no junction) | `Context.empty_clause` (+ my difference test = `emptyCheck`, via state table = catalog) |
| F4 | same | `Context.domain_clause` (`Allowed`) |
| F5 | before is the strict owner order | `Context.transitive_clause` |
| F6 | cap/cup rank growth | `Context.growth_clause` |
| F7 | six-order bounding-box test on the plain cell differences | **adapted**: `CycleSigns.checked_triple_positive` with my Std table, whose `ResidualDomains.valid` is proved generically (`actual_pair_fits`), as in `residual_positive_of_checked_states` |
| F8 | signotope packets | `Context.packet_clause` (BAD4 ⇔ ¬`PacketValid`, decide on 16 cases) |
| F9 | convex ⇔ 2-2 sign split | `Context.convex_clause` |
| F10 | octagon-free ⇒ every 8-set has a non-convex 4-subset | `Context.no_octagon_clause` (+ `combs` membership: all 4-subsets of the sorted 8-list) |

Owner extraction: generalise `CoupledTemplate.exists_missing_index` from 13 to k (needs S nodup, entries < 154).
Bridge: Std-only helpers `before/ge/positive/disagree/domainClause/growthClause/packetClause/convexClause` mirror the
library's with ℕ indices; `toExpr` maps them to `Coupled.Expr k`; the equations are near-definitional.

## 4. Trust (ENCBLEAN E1-E6, unchanged wording)

E1 printer output = certified bytes (checked by M9 hashing); E2 cake_lpr verdicts (`s VERIFIED UNSAT` exact line);
E3 DIMACS semantics of cake_lpr's parser vs `EncB.parseDimacs`; E4 Lean compiler/runtime of the printer and the
reading of `Main.lean`'s IO glue; E5 kernel, Mathlib `f897ebcf`, definitions (`Configuration`, `ResidualBound`,
Res118's `ValidUnitRow`); E6 SHA-256/`sha256sum`. Also trusted: the imported oleans match their sources (no closing
import audit; as Res118 §8.7).

## 5. Lemma map / modules

Std-only (`lean/RowEnc/`, exe `rowprint`): `States` (154 states, cell tests, bounding boxes, triple test), `Enc`
(atoms, codes, helpers, enumerations, families, `allocCodes`, `num`, `finish`, `rowCnf`, `rowNv`, `rowText`), `Main`.
Mathlib side (`lean/RowGeo/`): `Decode` (numbering), `Finish`, `Members` (enumerations), `Bridge` (`toExpr`),
`Geo` (F2, F7 table, catalog), `Sound` (`missing_of_unsat`), `Blocks` (Res118 composition, axiom guard).
Unique module names (chain311 has top-level `Catalog`, `Geometry`, `Transfer`).

## 6. Risks

R1 byte mismatch (itertools orders) → dump `c.tags`, diff by family. R2 kernel/elaborator evaluating `rowCnf` on
data → keep everything generic in S; data defs irreducible if needed. R3 memory of imports (Res118.Glue pulls
chain311 Residual32Bridge2650) → only `RowGeo.Blocks` imports it.

## 7. As built (22 Nov 18:26), differences from the plan above

- No separate `Finish` module: `finish_sat`/`rowCnf_sat` are in `RowGeo.Decode`; `Geo` holds F2, F7 and the catalog.
- Added `RowGeo.Text`: literal bound `litsOk_of_wf` for every support (no well-formedness needed),
  `parseDimacs_rowText`, `parseDimacsBytes_rowText`, `rowUnsat_of_bytes` (the planned `rowUnsat_of_text` with a
  literal-bound hypothesis was replaced by this hypothesis-free byte form).
- `missing_of_unsat` states `∃ i : Fin S.length, statesOf S _ i ∉ c.residualOccupied …` (not `∃ x ∈ S`); `WF S`
  also requires `0 < S.length`.
- Final theorems: `RowGeo.blockValid_P/Q/U/A`, `residual_bound_118_of_rows` (hypotheses `RowsUnsat`) and
  `residual_bound_118_of_texts` (hypotheses `RowsTextUnsat` on the printed bytes).
- The numbering is the n66enc pattern with codes reduced mod 16 (`Atm.norm`); no kernel check per size was needed.
