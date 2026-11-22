# n66-rowsvalid DESIGN (M0)

Written 22 Nov 2026, about 18:00 KST, by the `n66-rowsvalid` agent (slot lrv). Pattern: ENCBLEAN / n66enc
(Lean-defined CNFs, printed text hash-bound to certified files, cake_lpr the one trusted step). Labels as in
es-research §2. [D] = checked on disk in this session; [R] = read from a record, not re-verified.

## 0. Facts found during orientation

| # | fact | source |
|---|---|---|
| F1 | R0 = 11,884 rows; first justification over the 132 leaves (seq order): transported 5,824, mirror 5,811, core 197, cycle 52 (all cycle rows have 8 states). They need **421 templates** (338 big = listed octagons, 83 old = complete no-octagon family; n = 9..29) and **208 core CNFs** (200 big, 8 old; n = 13..26). Test evaluations for transported + mirror rows: 1,156,877 (positive 795,056, domain 115,794, empty 246,027). | [D] `tools/stats.py` → `data/just_R0.json` |
| F2 | The record's pipeline (`p2_template_cert66.py`) **deleted** the template/core CNFs and LRATs after cake_lpr; only `cnf_sha256`, `lrat_sha256` and the verdict line are kept (`template_certs.jsonl`, `core_certs.jsonl` per cube). | [D] source + files |
| F3 | The independent row check (VB/U1, `vfy15/bin/rowchk.py` + own generator `vfy15/bin/cnfgen.cpp`) re-generated **exactly these 629 CNFs** (421 `T_<id>`, 208 `C_<key>` jobs) and re-certified them: CaDiCaL 2.1.3 LRAT + cake_lpr, `cake_lines = ["s VERIFIED UNSAT"]`, `cake_exact = 1`; **CNF and LRAT kept** (`vfy15/rows/jobs/*.cnf.zst`, `*.lrat.zst`). Its CNF bytes differ from the record's (0/629 hashes equal: other clause and literal order). | [D] |
| F4 | **The kernel cannot evaluate `N66Enc.R0`** (`parseRows` of the 507,715-byte `include_str` text) under the 3.5 GB unit cap: a bare tail-recursive count over `rowsText.data` was stopped by the memory guard at 3,357 MB after 12 s (`MEMGUARD_STOPPED_esr-ag-lrv-k2.txt`); `String.splitOn` is well-founded recursion besides. So `RowsValid R0` cannot be discharged by kernel evaluation of R0. | [D] experiment K2 |
| F5 | Kernel cost of n66enc's `ttF` (six-order test via list filters): about 41 ms and 5.5 MB per call (K3: 70 calls 2.6 s / 762 MB; K4: 280 calls 12.1 s / 2.3 GB). A direct evaluation of all 795,056 positive tests (9 h, terabytes) is impossible; verified bit tables are needed. | [D] experiments K3, K4 |

## 1. Target theorems and labels

```lean
-- R1: kernel-friendly list of the same 11,884 rows, in R0's order (built from the certificate data J)
theorem rowsValid_R1 (h : RowCertsUnsat) : N66Geo.RowsValid R1
-- link to n66enc's R0 (F4): a named hypothesis, never an axiom
def R0Parse : Prop := N66Enc.R0 = R1
theorem rowsValid_R0 (h : RowCertsUnsat) (hp : R0Parse) : N66Geo.RowsValid N66Enc.R0
theorem n66_bound_55_of_cubes_rows (hc : CubesUnsat132) (h : RowCertsUnsat) (hp : R0Parse) : OmissionZRow.N66Bound 55
```

* `RowCertsUnsat : Prop := ∀ t ∈ certs629, ¬ EncB.DimacsSatisfiable (certCnf t)` — the 629 Lean-defined row CNFs
  (421 templates, 208 cores). Discharged outside the kernel exactly as n66enc's `CubesUnsat132`: the printer prints
  `render (nv t) (certCnf t)`; its SHA-256 = the `cnf_sha256` of VB's re-certified job (F3) (E1, E6); cake_lpr
  printed `s VERIFIED UNSAT` on that CNF with the kept LRAT (E2); ENCBLEAN's proved round trip
  `parseDimacs_render` (E3); the compiled printer computes the Lean definition (E4); kernel/Mathlib/definitions (E5).
* `R0Parse`: COMPUTED (compiled Lean evaluates `decide (R0 = R1)`, E4). Stretch goal (M10): remove it by
  re-binding the 132 cube trims with a printer whose row list is R1 (same bytes expected), giving
  `CubesUnsat132R1 → RowCertsUnsat → N66Bound 55`.
* Label of the end theorem: **Lean-checked modulo `CubesUnsat132` (132 verdicts), `RowCertsUnsat` (629 verdicts)
  and the named hypothesis `R0Parse`, under trust items E1-E6.**

## 2. The row CNFs (VB's `cnfgen.cpp`, bytes to match)

Owners v_0..v_{n-1} of distinct states (positions). Variables (cnfgen numbering = allocation order):
for each pair i<j (lex): bef(i,j), ge(cap,i,j,2..4), ge(cup,i,j,2..4); then ori(i,j,k) per sorted triple; then
cvx(i,j,k,l) per sorted quadruple; nv = 7·C(n,2) + C(n,3) + C(n,4). `bef(u,v)` for u>v is ¬bef(v,u);
`ori(a,b,c)` is the sorted triple's variable signed by the permutation parity; `ge(·,·,·,1)` = TRUE (clause
dropped / literal dropped), `ge(·,·,·,5)` = FALSE. No dedup, no sorting of literals.

| # | family (cnfgen order) | clause | written soundness | Lean lemma (n66enc / new) |
|---|---|---|---|---|
| S1 | threshold (i<j, typ, k=2,3) | ¬ge(k+1) ∨ ge(k) | thresholds of one number | trivial |
| S2 | transitivity (all ordered a,b,c distinct) | ¬bef(a,b) ∨ ¬bef(b,c) ∨ bef(a,c) | x-order linear | `omega` |
| S3 | growth (same loop, typ, k=1..4) | ¬bef(a,b) ∨ ¬bef(b,c) ∨ (cap: o / cup: ¬o) ∨ ¬ge(typ,a,b,k) ∨ ge(typ,b,c,k+1) | N66 §2.2 | `labels_increasing`, `label_bounds6` |
| S4 | signotope (each 4-set, each permutation q, 8 BAD4 patterns) | order(q) → pattern of ori(q0q1q2, q0q1q3, q0q2q3, q1q2q3) not bad | signotope | `Model.signotope`, `packet_ne_bad`, `ori3_*` |
| S5 | convex_four definition (16 per 4-set) | cvx ↔ [#{x, ¬y, z, ¬w} = 2] | definition | cvx's meaning *is* the formula |
| S6 | no-octagon (listed 8-sets, or all) | some 4-subset not convex | 4-convex ⇒ (x-sorted) χ(abc)=χ(abd), χ(acd)=χ(bcd) ⇒ χ(abc) = s(b) ⇒ upper/lower chains ⇒ 6-cap, 6-cup or 5-cap+5-cup on common ends | new; `capCup55_holds` (n66enc G3) |
| T1 | test E (u,v) | ¬bef(u,v) | D'(s_u→s_v) = ∅ and labels lie in D' | `label_domRef` |
| T2 | test D (u,v,a,b) | before(u,v) → label ≠ (a,b) | (a,b) ∉ D' | `label_domRef` |
| T3 | test P (p,q,r) | ori(p,q,r) | TT[s_p,s_q,s_r] (six-order test) | `tt_sound` |

Template CNF = S1-S5 + S6(octs | complete) + tests (recorded list order). Core CNF = same with all tests of the
support (cnfgen's `all_tests` order: pairs (i<j) × ((i,j),(j,i)): E or D-cells; then triples: P i j k or P i k j).

**Transport (N66 §2.9, PROVED in Lean here):** the template CNF text depends only on (n, tests, octs). If every test
is *good* for σ (E: D'(σu→σv) = ∅; D: (a,b) ∉ D'(σu→σv); P: TT[σp,σq,σr]) and a configuration of the class
occupies every state of image σ, then the canonical assignment (positions ↦ owners of σ(i)) satisfies every clause;
so UNSAT ⇒ RowValid (image σ). A core is the case σ = id with all tests (good by construction).
**Mirror:** RowValid S ⇒ RowValid (τ S) by n66enc's `mirror_holds`. **Cycle:** 8 states whose list-order triples
pass TT have owners with all cyclic triples positive (`tt_sound`) ⇒ convex octagon
(`hasConvexNGon_of_positive_cycle`), impossible in the class.

## 3. Kernel-side checks

Per-row certificate `RowCert` (data, R0 order): transported (template index, σ), mirror (preimage certificate),
core (core index), cycle (order). Bool checker `checkRow T cert`, soundness `checkRow_sound`. Tests are evaluated
through verified tables (F5): `ttBits a` (4,900-bit Nat per a; theorem: set bit ⇒ `ttF = true`, checked by kernel
evaluation of `ttF` on the 29,436 set bits, chunked), `drMask u v` (16-bit masks; theorem: mask bit ↔ `domRef`,
checked on all 78,400 cells, chunked). Rows are checked in chunks of about 100 per declaration (memory bound).

## 4. Trust items

E1 printer output = VB's certified CNF bytes (SHA-256, M9); E2 VB's cake_lpr verdicts (re-run where feasible);
E3 DIMACS semantics of cake_lpr (ENCBLEAN, proved round trip); E4 Lean compiler/runtime (printer; `R0Parse`
evaluation); E5 kernel, Mathlib, library definitions; E6 SHA-256.

## 5. Milestones

M1 Std-only CNF definitions + printer + byte identity on samples; M9 hash binding of all 629; M2 soundness of
S1-S5, T1-T3; M4 S6 (octagon); M3 checker + tables + chunk proofs; M5 `rowsValid_R1`; M6 `R0Parse` evidence and
the end theorem; M10 (stretch) cube re-binding with R1.

---

## 6. As built (22 Nov 2026, 19:30 KST; supersedes §3 where they differ)

* **Statements** (`lean/RowGeo/End.lean`, axiom guards pass): `rowsValid_R1 : RowCertsUnsat → RowsValid R1`,
  `rowsValid_R0 : RowCertsUnsat → R0Parse → RowsValid N66Enc.R0`,
  `n66_bound_55_of_cubes_rows : CubesUnsat132 → RowCertsUnsat → R0Parse → N66Bound 55`.
  `RowCertsUnsat := (∀ t ∈ templates, ¬Sat (certCnf t)) ∧ (∀ k ∈ cores, ¬Sat (certCnf k))`;
  `R0Parse := N66Enc.R0 = R1`; `R1 := R1nat.map (·.map toFin70)` with `R1nat` the concatenation of the 119 chunk
  constants `RowChk.rows<k>` that the kernel checks.
* **Text bridges:** `certUnsat_of_text` (full CNF; literal bounds proved from `certOk`, so no runtime `litsBounded`
  check is needed) and `subUnsat_of_text` (any index list; used for T208 = template `849f8a5e23a1fc77`, n = 29,
  whose certified file is VB's `lrattrim` sub-CNF of 7,475 clauses; index list `data/trim208.idx`, untrusted).
* **Tables (§3 as built):** the six-order table is *not* verified by calling `ttF` on each set bit (41 ms each);
  instead `psRow` (plain-domain statistics `ne, mn0, mx0, mn1, mx1` of all 4,900 pairs) is checked against
  `nePlain/mnPlain/mxPlain`, `ttQ` (= `ttF` with table lookups) equals `ttF` by rewriting (`RowGeo.ttQ_eq`), and every
  set bit of `ttRow` is checked with `ttQ` (`RowChk.ttChk`, one state per theorem). `drRow` is checked cell by cell
  against `domRef`, `canRow` against `canF`. D tests require `1 ≤ a, b ≤ 4` in `goodN`.
* **Certificates `RC`:** `tr t σ` (transported), `mt t σ` (mirror of transported), `co c` (core), `mc c` (mirror
  of core), `cy L` (cycle). `chkRow T rc` additionally requires every state of `σ` (or its τ-image, or the core's
  states / their τ-images, or `L`) to lie in `T`; `RowValid` is monotone (`rowValid_mono`), so a certificate for a
  subset suffices. `IsCore.cores_isCore` (kernel) excludes template entries in `cores`; `certsOkT/C` check
  `certOk` (sizes ≤ 32, test indices in range, octagon lists of 8 increasing positions) and core supports strictly
  increasing.
* **Binding target:** VB's cnfgen bytes (F3), not the record's Python bytes: VB kept CNF + LRAT, so E2 can be re-run.
* **Kernel-memory lessons:** a declaration's kernel work must stay below ~1 GB; memory is not returned between
  declarations of one file (guard stops `tab1`, `tab2`), hence one `ttChk` row per theorem, five theorems per file,
  and row chunks of 100 rows, four chunks per file (each file about 15-37 s, 2.3-3.3 GB RSS incl. olean maps).

## 7. Freeze discipline

The exe closure (RowEnc/Gen, DataT0..3, DataT, DataC0..3, DataC, Main; sources 18:09, objects ≤ 18:20:39, exe
`7140a6ff…`) is frozen since M9 (18:21-18:40). `logs/compile_status.tsv`: all 87 modules final rc 0, every olean
newer than its source and its local imports. Generators that write Lean files refuse to run without `--write`;
changing any `.lean` of the chain requires recompiling everything downstream (bare `lean -o` tracks no
dependencies), and changing the exe closure requires relinking and redoing M9.
