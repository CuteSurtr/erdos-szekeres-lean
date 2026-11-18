# ROADMAP20261115: research program after the 14-15 November night (written 04:50 KST)

**Status: a research plan, not a result.** It collects the work of the overnight agent workflow
`es-roadmap-overnight` (run `wf_0b91adc6-dff`): 13 maps of the records and the literature, 18 research programs from
independent angles and 35 adversarial critiques (two per program: soundness/feasibility and cost/prior art), plus the
companion workflow `es-overnight-extra` (Delta attack, chain review, novelty). **The account's weekly usage limit stopped
both workflows at about 03:50 KST**; the topic syntheses for the upper bound, the Delta conjecture and ES(7), all probes,
the completeness critic and the report agent never ran. Only the ES(8) lower-bound synthesis finished. The rankings below
for the other three topics are the main session's reading of the programs and critiques, marked as such. All agent
outputs are kept verbatim in `/home/jay/research/data/roadmap-20261115/agent_results_roadmap.jsonl` and
`agent_results_extra.jsonl` (one JSON line per agent: label + full return value), with a digest in `overview.txt`.

## 0. What the night established (with labels)

- **ES(8) ≤ 308**: budget-34 slices 18, 19, 20 EXACT TREE + budget-33 baseline, N5-free; new components independently
  verified (`LO33N20261113/budget34/VERIFY308`); all five written links confirmed by two independent reviewers each
  (`VERIFY308/CHAIN_REVIEW.md`). Computer-assisted, unrefereed, uncommitted. Not found in the literature
  (`NOVELTY20261115`).
- Budget-35 (18,17) and (19,16) EXACT TREE (two independent replays each); (20,15) and (21,14) open (HEURISTIC
  estimates with all 1,333 certified coupled rows: 3.3e8 and 1.85e9 nodes). N66 ≤ 55 undecided. k = 9 ring: see
  `SATOPEN20261113` addendum. Δ conjecture: open, eight strategies mapped (`DELTA3N20261113/attack20261115`).

## 1. ES(8) upper bound (main session's ranking; agent synthesis did not run)

| # | Program (design agent) | Critics | Main-session reading |
|---|---|---|---|
| 1 | Close budget-35 (20,15) by keeping the work: easy-first sweep, batch witness cuts, split hard contexts; then decide on (21,14) (upper:1) | revise / revise (200-250 CPU-h); certifying the union of all candidates per witness floods the LP with 12-19 rows per witness | **Do first.** One dedicated 12-thread run with batched cuts and context splitting; it is the only route to 307 that needs no new mathematics. |
| 2 | Capacity ladder: N66 ≤ 55 then ≤ 54 by a monolithic portfolio plus a core-seeded relaxation; N5 by a mono5 port (upper:2) | revise / revise (220-300 CPU-h); its case against cube-and-conquer compared the wrong runs; its probe had a quoting bug | **Second.** N66 ≤ 55 removes (21,14) outright; redesign as cube-and-conquer seeded from the level-13 core before more monolithic solves (two 3h10m solves gave no verdict). |
| 3 | Baek-block attainment rows: push the nine Baek capacities from 22 to 21, starting with row 973 (open lemma L9) (upper:3) | revise / revise (200 CPU-h); profile counts independently recomputed and correct | Promising theory+SAT line; raises h(F) directly. |
| 4 | Δ ladder to ES(8) ≤ 303 via defect forms D8(k) (upper:4) | **drop** / revise: its S5 packing lemma ("3 disjoint red 4-caps force a 5-cap or an octagon") is false on a pool set, and S5 Goal 1 fails on the 329-set census | Keep only the integration ledger; the proof steps need the Δ work of §2 first. |
| 5 | Balanced 186 by extending the budget-64 tree to budget 65 (upper:5) | revise / revise (550-1,000 CPU-h); costings rest on unmeasured rates | Later; large and uncertain. |
| 6 | LEAN308: Lean-check the residual chain (309 modulo N66 ≤ 56, then 308) (upper:6) | revise / revise (60-72 CPU-h); payoff overstated (not the same trust level as a fully Lean-checked theorem) | Worth doing in parallel for evidence quality; cheap. |

## 2. Δ-reduction conjecture (main session's ranking)

Programs: (delta:1) from the rooted 2n−3 theorem to all sizes via a vertex-cover lemma for lower tangents — revise/revise,
no soundness flaw found in its reduction; (delta:2) certify weak D(5,7)/D(5,8) at 16 points with two encoders — revise /
**drop** (no payoff for ES(8); the SAT model cannot decide the conjecture); (delta:3) weak Conj(8) with ≤ 5 deleted
points — **drop** (e_w = 0 already established on the same pools, DELTA2N §4.2b); (delta:4) integration ledger and Lean
capacity interface — revise (a label error: M₇(5,6) = 25 is not CERTIFIED per FLAYER20261113).
**Reading:** pursue delta:1 together with the two lemmas of tonight's attack (CONJ-TS′ ⟹ weak D(5,n); uniform-envelope
selection = D(4,n; weak) on 4-cap-free inputs), and keep delta:4's ledger as the interface to the upper bound.
**Correction (05:35, from attack 5 and VERIFICATION.md):** the lever is larger than the 63 of ETVTHY §3, which used an older
M(5;7) input. Attack 5 proved WD ⟹ FC ⟹ U ⟹ T, where **T(S): the convex (n−1)-gons of S have a transversal of at most
b(n) = C(n−1,2)+1 points** (PROVED; 3/3 verifiers did not refute). Removing such a transversal leaves a 5-cap-free
(n−1)-gon-free set, so T(8) alone gives **M(5;8) ≤ 22 + M(5;7) ≤ 22 + 36 = 58**, using M(5;7) ≤ 36 as recorded CERTIFIED in
ETV7SAT20261113 (item 2; not re-checked here). That means h(F) ≥ 26, hence h(C) ≥ 40, |R| ≤ 114 and **ES(8) ≤ 303**; T(7)
as well would give M(5;7) ≤ 31 and M(5;8) ≤ 53. Caution: T(8) is implied by weak D(5,8) but is not a cheap shortcut —
since a heptagon-free subset of a 5-cap-free set has at most M(5;7) ≤ 36 points, any valid S with ≥ 59 points has τ ≥ 23,
so T(8) for all S already contains M(5;8) ≤ 58. Its value is as a uniform statement (an induction hypothesis over all sizes);
the direct alternative is to push the N5 = M(5;8) SAT ladder from 65 towards 58 (cf. the N66 ladder, which stalled at 55).

## 3. ES(7) lower bound (main session's ranking)

All four programs were marked drop or revise by their critics: (lower7:1) searches below 33 points — same design as A/A2,
expected null; (lower7:2) completeness route toward ES(7) = 33 — its probe crashes (missing JSON keys) and costs 150-700
CPU-h; (lower7:3) near-involution classes — the project already ran this model on two instances without closing, one
two-axis rule is wrong; (lower7:4) transfer of published SAT techniques — rests on a false inference about restricting
proofs. **Reading:** no cheap ES(7) lower-bound experiment survived critique tonight; the honest next step is a costed
feasibility study of a signotope encoding for 33 points before any search.

## 4. ES(8) lower bound (agent synthesis, verbatim ranking)

1. **ABSAT8-core**: certified order-type-level one-point non-extendability of named 64-point octagon-free sets outside
   the stacking family (2 half-turn sets, 7 seven-fold types, 7 walker end sets, 8 vertex deletions of AlphaEvolve's
   65-point set) — 3 CPU-h; CERTIFIED per CNF plus a written soundness note. Modest value: says nothing about ES(8) = 65
   beyond the named sets.
2. **CONE4 gate**: test whether exact cone units alone refute fixed t = 14 phase vectors before any CEGAR toward "4-fold
   maximum = 52" — 2 CPU-h gate (needs about 5 GB).
3. **Two-arm Phase 0 (k = 9)**: slot-adaptive extension scan of the 104- and 112-point records — 4 CPU-h, low odds.
4. Two-arm one-descent theorem (k = 9), gated behind the ring — 150 CPU-h.
5. Radius-1 neighbourhoods via a joint two-point CNF — sizing only, 2 CPU-h.
Dropped by the synthesis (with reasons in the results file): radius-1 enumerate-then-test, family-wide saturation of all
1,592 stacking types, wholesale loading of ALGAN's 45M-clause cut file, a C++ port of lpc8.py (CaDiCaL dominates), the k = 12
transfer (float cannot sign the 991-point set), and several overstated payoff claims.

## 5. Recommended order (main session)

1. A dedicated (20,15) run (12 threads, batched cuts, splitting) → ES(8) ≤ 307 needs only (21,14) after it.
2. N66 ≤ 55 by cube-and-conquer from the level-13 core → removes (21,14).
3. Δ: delta:1 + CONJ-TS′; finish the missing verifications of tonight's attacks first.
4. LEAN308 in parallel; ABSAT8-core and the CONE4 gate as cheap side tasks.
5. Before any public wording: owner decision; refresh NOVELTY20261115.

## 6. Reconciliation with the workflow's own synthesis (05:55 KST)

After the usage limit was reset, the workflow finished: [SYNTHESIS.md](SYNTHESIS.md) (477 lines; topic syntheses,
probes with adversarial verification, completeness critic). Where it differs from §§1-5 above, **SYNTHESIS.md and the
following corrections take precedence**:
- **F-side lever: stalled, not promising.** "Baek blocks 22 → 21", h(F) ≥ 21 and N5 ≤ 63/62 are one lever; ETV5N stalled
  at N5 ≤ 65, the row-973 route is blocked in the coupled encoder ([BAEK973](../LO33N20261113/budget34/BAEK973.md)), and
  the N5 ≤ 65 LRATs were deleted. Row 3 of §1 is withdrawn. (The Δ route of §2 is the structural way to the same lever.)
- **Upper-bound order:** (1) (20,15) with a work-keeping loop (about 200 CPU-h; precheck: re-solve about 100 leaves of
  the budget-34 slice-20 tree `runs/s20/bb-s2` at budget 35 as a warm start); (2) **N66 ≤ 55 by level-14 cubes — the
  critical path** (20-60 CPU-h, cake_lpr heap ≥ 3.2 GB, up to about 390 GB of raw LRAT;
  [cubes20261115](../N66N20261113/cubes20261115/README.md)); (3) LEAN308 step S0 (about 1 CPU-h); (4) balanced 186 only
  after its cost is re-measured with state 0 free (the probe fixed state 0; its 21 CPU-h glue figure is refuted);
  (5) the F6 row, parked; (6) a direct (21,14) tree, fallback only.
- **ES(8) lower bound, new CERTIFIED item:** all 28 one-point-extension CNFs of the ABSAT8-core probe (the 64-point
  octagon-free sets outside the stacking family named in §4, including the 8 vertex deletions of AlphaEvolve's 65-point
  set) are UNSAT, accepted by cake_lpr 28/28 and again 28/28 on a verifier's re-run. The geometric reading (no real
  65-point extension of those order types) is COMPUTED until the soundness note and an independent encoder exist.
  [superseded 15 Nov pm (STATUS20261115_1900, Corrections item 4): both exist. L1's independent encoder with a PROVED
  soundness argument is in [ABSAT8_INDEPENDENT.md](ABSAT8_INDEPENDENT.md): claims absat8-l1-indep (V1 CONFIRMED,
  verdict file 13:54:23) and absat8-l1-cake-rerun (V3 CONFIRMED, 14:01:59). For these 28 order types the geometric
  reading is now CERTIFIED computation plus PROVED soundness; claim absat8-l1-sevenfold (V3 CONFIRMED, 14:19:48) adds
  the seven 7-fold order types of PRIMEFOLD §3]
- **ES(7):** see [ES7_FEASIBILITY.md](ES7_FEASIBILITY.md) (brute force at 33 points about 1e3-1e4 CPU-years, HEURISTIC; the
  recommended next step is a (7,5,7)@27 estimate). The colouring-27 repair item is dropped (a verifier proved a forced 5-cap).
- **k = 9 ring wording:** "CERTIFIED per CNF; encodings independently checked (`verify_cycx.py`) for 30 cases" until the
  remaining cases are run through `verify_cycx.py`.
- **Owner decisions listed by the synthesis:** the 58.8 GB of level-14 partial LRATs, the 70 GB of m9 partials, the k9 memory
  slice (reduced by the main session at 05:52 to MEMB 9.2), and one specification for the case-B cake_lpr run.

- **Δ route update (06:35):** CONJ-TS′(7) is false for real point sets (S19′ realizable, EXACT, verified; see `DELTA3N20261113/attack20261115/S19_REALIZABILITY.md`), so the CONJ-TS′ ⟹ weak D(5,7) route needs a different selection statement; the candidates are the rooted / left-or-right forms and the method sweep's ENV#, ROOT and AT_n (round 6).
- **Δ route update (09:05):** round 6 (`DELTA3N20261113/attack20261115/ROUND6.md`) found AT_n false for real point sets at
  n = 6, 7, 8 (EXACT, verified), so the LT-cover lemma of program delta:1 fails as stated and §2's "pursue delta:1" no longer
  has a working key lemma; its repairs AT2_n and AT3_n also fail on real sets. What survives: Theorem 3 (CONJ-TS′ ⟹ weak
  D(5,n)) and UES* ⟹ weak D(5,7) as reductions (both premises fail or are open), ENV#(7) certified to 13 points, weak D(4,8)
  certified to 15 points (16 via a trimmed LRAT), CONJ-TS′(8) certified at 15 points. The remaining selection statements to
  test are the rooted and per-set left-or-right forms and ENV#(7) at 14-15 points.
- **Correction (09:22):** weak D(4,8) at 16 points is now CERTIFIED by the untrimmed LRAT (main session re-run at heap 6000),
  so read "certified to 15 points (16 via a trimmed LRAT)" above as "certified to 16 points".
