# v182-lean DESIGN (M0, 22 Nov 2026)

## 1. Target

### 1.1 Statement (Mathlib side, module `V182Geo.Defs`)

- `V := {s : Finset (Fin 8) // 3 ≤ s.card ∧ s.card ≤ 5}` (182 vertices).
- `G : SimpleGraph V`, `G.Adj u v :↔ (u ⊆ v ∧ |v| = |u| + 1) ∨ (v ⊆ u ∧ |u| = |v| + 1)`: inclusions between
  consecutive sizes only (not the comparability graph; soundness VERIFY fix 3).
- `IsFourCycle a b c d`: four pairwise distinct vertices, `a~b`, `b~c`, `c~d`, `d~a` (a 4-cycle subgraph; chords are
  allowed by the definition, and none exist since G is bipartite by parity of size).
- An edge colouring with at most `k` colours is `col : G.edgeSet → Fin k` (not necessarily proper).
  `IsRainbow col`: for every 4-cycle subgraph the four edge colours are pairwise distinct.
- `RainbowColorable k := ∃ col : G.edgeSet → Fin k, IsRainbow col`; `chiRainbow := sInf {k | RainbowColorable k}`.

Theorems:
- `rainbowColorable_six : RainbowColorable 6` — Lean-checked outright (no hypothesis).
- `not_rainbowColorable_five : PieceVerdicts → ¬ RainbowColorable 5`.
- `chiRainbow_eq_six : PieceVerdicts → chiRainbow = 6`.

### 1.2 The hypothesis

`PieceVerdicts : Prop := ∀ q ∈ pieces, ∀ nv F, EncB.parseDimacs (pieceText q) = some (nv, F) → ¬ EncB.DimacsSatisfiable F`

(`V182Enc.pieces`: the 4,404 pieces; `pieceText q` is exactly the expression the printer exe writes for piece `q`.)
Label: **Lean-checked modulo PieceVerdicts** (4,404 cake_lpr verdicts carried in by the hash binding M9 under trust
items E1-E6, §4), plus any gap still named as a hypothesis at the time of writing (never an axiom).

## 2. The CNF (Std-only module `V182Enc.Gen`, printed by `v182print`)

Numbering (rainbow.py `graph182`, wave-1 README 3.3 conventions): vertex masks `m < 256` with 3-5 bits, increasing;
edge `e = 8 r + x` joins the `r`-th 4-set mask `T` (`eT e`) and `T ^^^ 2^x` (`eO e`); `lit e c = 5 e + c + 1`
(`e < 560`, `c < 5`, so `1 ≤ lit ≤ 2800 = nVars`).

Structural 4-cycles `cyc X p q = [eidx(X+p, p), eidx(X+p, q), eidx(X+q, p), eidx(X+q, q)]` for every 3-set mask `X`
and bits `p < q` outside `X` (560); they are the edges `X–X+p`, `X+p–X+p+q`, `X+p+q–X+q`, `X+q–X` in cyclic order.
`conflict e f := e ≠ f ∧ ∃ z ∈ cycles, e ∈ z ∧ f ∈ z`. Python's conflict set comes from its own 4-cycle enumeration
(`four_cycles_by_diagonals`); equality of the two is checked by the byte identity of the CONF section (M1), and
soundness uses only the Lean definition.

| family | Lean | source | clauses | soundness for the indicator `ν(lit e c) = [ψ(edge e) = c]` of a rainbow 5-colouring `ψ` satisfying the units |
|---|---|---|---:|---|
| ALO | `aloCls` | rainbow.py:110 | 560 | `ψ(edge e) = c` for some `c < 5` |
| CONF | `confCls` (e desc, c desc, f desc) | rainbow.py:98-101,111 (`sorted(cls)`) | 16,800 | `conflict e f`: `e, f` lie in a structural 4-cycle, which is a 4-cycle subgraph of G (M4 bridge), so `ψ(e) ≠ ψ(f)` |
| AMO | `amoCls` | rainbow.py:115-117 | 5,600 | `ψ(edge e)` is one colour |
| STAR | `surjCls` | rainbow.py:118-124 | 560 | the star list `L` has 5 distinct, pairwise conflicting edges, so `ψ` is injective on `L`, hence onto `Fin 5`; colour `c` occurs |
| UNITS | `unitCls` | wave-1 README 3.3 | 10 | the normalisation (§3): `ψ` is chosen with these values |

Pieces: `pieceCube (n, none) = Y1(n)`, `pieceCube (n, some m) = Y1(n) ++ Y2(m)`, `Yi(n) = zipWith lit star_i π_n`,
`π_n = perms5[n]` (lexicographic, `permsOf`), stars `y1Star = [5,43,50,57,64]` (mask 47), `y2Star = [13,44,74,81,88]`
(mask 55). `pieces` = for `n < 120`: all 120 `(n, some m)` if `n ∈ splitSet` (36 literal indices), else `(n, none)`.
The star literals and `splitSet` are data; soundness needs only that each star is 5 pairwise conflicting edges (M3),
and the binding (M9) checks every listed piece against the certified files.

## 3. Mathematical chain (Mathlib side)

1. **Bridge (M4).** `edgeOfIdx e := s(vtx (eT e), vtx (eO e))`; for every `z = cyc X p q ∈ cycles` the natural
   vertices `X, X+p, X+p+q, X+q` form a 4-cycle subgraph whose edges are `edgeOfIdx` of `z` in order. Hence a rainbow
   colouring is injective on every `z`, and `conflict e f → ψ(e) ≠ ψ(f)`.
2. **Automorphisms (M4).** For an injective `σ : Fin 8 → Fin 8`, `s ↦ s.map σ` preserves sizes and inclusions, so maps
   4-cycle subgraphs to 4-cycle subgraphs; `ρ ∘ φ ∘ (σ•)` is rainbow for injective `ρ : Fin 5 → Fin 5`.
3. **Normalisation (M4; wave-1 README 3.3, soundness VERIFY C1-C6).** With `X0 = {0,1,2}`, `Y0 = {0..4}`,
   `a_x = φ(X0–X0+x)` (x = 3..7) and `b_y = φ(Y0−y–Y0)` (y = 0..4): rainbowness gives `a`, `b` injective and
   `{a_3, a_4} ∩ {b_3, b_4} = ∅` (4-cycle `(X0, X0+3, Y0, X0+4)`). As built: (i) a generic colour step
   `ρ1 = a⁻¹` (`Equiv.ofBijective`) makes `a_x = x − 3`; (ii) `norm_finite` (kernel) checks, over the 120
   permutations `B` of the normalised `b` with `B_3, B_4 ≥ 2` (36 of them), that explicit witness lists give a map
   `σ` of `{0..7}` (injective, fixing 3 and 4, `{0,1,2}` and `{0..4}` onto themselves) and an injective colour map
   `ρ2` with `ρ2(a_{σ x}) = x − 3` and `ρ2(b_{σ y}) = nf(y)`. Then `ψ := ρ2 ∘ ρ1 ∘ φ ∘ (σ•)` is rainbow and satisfies
   the 10 units.
4. **Soundness (M2).** `ν` satisfies every clause of `baseCnf` (table §2).
5. **Cover (M3).** `ψ` is injective on `y1Star` (pairwise conflicts), so its colour tuple is some `π_n`; `ν` satisfies
   `Y1(n)`; if `n ∈ splitSet`, likewise `Y2(m)`. In both cases `(n, ·) ∈ pieces` and `ν` satisfies
   `cubeCnf baseCnf (pieceCube q)`; with `EncB.parseDimacs_renderCube` (literal bounds `1 ≤ lit ≤ 2800`) this
   contradicts `PieceVerdicts`.
6. **Six-colouring (M5).** As built (replacing the planned structural-lemma route, on advice): adjacent vertices
   have masks differing in exactly one bit (`toMask_adj`, from `Finset.exists_eq_insert_iff` and the bit lemmas), so
   the masks of any 4-cycle subgraph form a closed bit-toggle walk through vertex masks with `a ≠ c`, `b ≠ d` and
   `d ⊕ a` one bit. The kernel checks all 256 × 8³ such walks (`walkBody`, 23 chunks `walk_c0..22`; 4,480 qualify,
   = 560 × 8) for four distinct colours of the table `col6Big` (the notes' table as decoded by wave 1's verifier,
   `verify/a2/col6_mine.json` sha256 22cee12c…1578, equal to my own decoding of `notes_src/diamond-colors.txt`).
   The natural colouring `col6 : Sym2 V → Fin 6` reads the table at `toMask` of the two ends (`toMask` by choice
   from `exists_mask`). Where the table comes from does not matter: the check is on the colouring itself.
7. **χ = 6 (M6).** Monotonicity in `k` (`Fin.castLE`) and `Nat.sInf`.

## 4. Trust items (as ENCBLEAN / n66enc)

- E1: the printer's output equals the certified bytes (M9: SHA-256 of the printed text = recorded `cnf_sha256` of the
  certified CNF, per piece).
- E2: the cake_lpr verdicts (`s VERIFIED UNSAT`, exact line) on those CNFs; CaDiCaL 2.1.3 LRAT, cake_lpr
  c14ff498…8a54.
- E3: cake_lpr accepting a proof for a file means the clause list `EncB.parseDimacs` reads from it is unsatisfiable
  (`EncB.DimacsSatisfiable` semantics; ENCBLEAN M9 evidence on the accepted DIMACS subset).
- E4: the Lean compiler and runtime compute `pieceText` correctly in the exe.
- E5: the Lean kernel, Mathlib and the definitions of §1.1 say what is intended.
- E6: SHA-256 is collision resistant.

## 5. Lemma map (as built)

| step | Lean name | module |
|---|---|---|
| statement | `V`, `Adj`, `G`, `IsFourCycle`, `IsRainbow`, `RainbowColorable`, `chiRainbow` | `V182Geo.Defs` |
| monotonicity, χ from 6/¬5 | `rainbowColorable_mono`, `chiRainbow_eq_six_of` | `V182Geo.Defs` |
| automorphisms | `vmap`, `isFourCycle_vmap`, `isRainbowS_transform` | `V182Geo.Defs` |
| numbered edges, bits | `ofMask`, `vtx`, `edgeOfIdx`, `ofMask_xor_insert`, `ofMask_inj`, `card_ofMask_eq_pc` (kernel, 256 masks) | `V182Geo.Masks` |
| bridge | `cyc_bridge`, `rainbow_cyc`, `conflict_ne` | `V182Geo.Masks` |
| family soundness | `baseCnf_sat` (ALO, CONF, AMO, STAR via `five_complete`, UNITS via `UnitsHold`) | `V182Geo.Sound` |
| literal bounds, verdicts | `baseCnf_wf`, `pieceCube_wf`, `PieceVerdicts`, `piece_unsat` | `V182Geo.Sound` |
| cover | `mem_permsOf`, `mem_perms5`, `star_cube`, `exists_piece`, `no_normal_colouring` | `V182Geo.Cover` |
| normalisation | `cycX`, `cycY`, `cycXY`, `e3`…`e4` (kernel), `norm_finite` (kernel, 120 permutations), `normalize` | `V182Geo.Norm` |
| no 5-colouring | `not_rainbowColorable_five` | `V182Geo.Norm` |
| six-colouring | `walk_c0..22` (kernel), `walk_all`, `walk_spec` | `V182Chk.WalkDefs/A/B`, `V182Chk.Walk` |
| six-colouring | `exists_mask`, `toMask_adj`, `col6`, `col6_rainbow`, `rainbowColorable_six` | `V182Geo.Six` |
| end | `chiRainbow_eq_six`, `chiRainbow_eq_six'`, `pieces_shape` (kernel) + `#guard_msgs` axiom guards | `V182Geo.End` |
| control | `ctl_orig`, `ctl_mut` (one recoloured edge fails the walk check) | `V182Ctl.WalkMut` |

Kernel discipline: no `decide`/`rfl`/`simp`/`omega` that evaluates `baseCnf`, `confCls` or `pieces`; kernel checks
only on small explicit data (stars, permutation tables, the six-colour table), each first tried on a small instance.
No `native_decide`.
