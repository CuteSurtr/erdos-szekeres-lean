# VERIFY_T1118_VC16: claim `t1118-vc16` (verifier VB, 18 Nov 2026, 03:16-03:25 KST)

**Verdict: CONFIRMED.**
- The proof of Lemma VC (THEORY_1118.md §3) is correct as written, from the cited inputs:
  - LR(7) at 15;
  - weak D(5,7) at 14 and at 13;
  - ROOT(7) at 14.
  These inputs were not re-verified here; they carry the labels of their own records.
- The CNF add-on is exactly the stated clauses in lr_compact's numbering. Own code, written from the claim's
  definitions; `vc16.py` and `ctl_vc16.py` were not read.
- **One wording point.** "lc7_m16.cnf + add-on is UNSAT iff lc7_m16.cnf is UNSAT" holds in the direction that matters:
  base + add-on UNSAT ⇒ no 16-point LR(7) failure, by the add-on's soundness checked here and the base's soundness
  (D1's review).
- The converse direction (base + add-on UNSAT ⇒ base UNSAT) also needs every model of the base to project to a genuine
  LR(7) failure, i.e. auxiliaries one-way in the sound direction only. That is a property of the base encoding, not
  re-checked here.
- No solver was run with the add-on (as in the claim).

## 1. The proof (read and re-derived)

S is a 16-point (5,7)-valid signotope in which r = 15 ends a 4-cap, l = 0 starts a 4-cap, and no weak Δ contains l or r.

**Every 15-point (5,7)-valid T has a weak Δ through min T or max T.**
- If max T ends a 4-cap of T and min T starts one, this is LR(7) at 15.
- Otherwise, say max T ends no 4-cap. Then max T lies in no 4-cap of T: in a 4-cap it would be the last point. A weak
  Δ D′ of T − max T (weak D(5,7) at 14) plus max T is 4-cap-free, and it meets every gon of T: the gons containing
  max T meet it at max T, the others meet D′. The case of min T is the mirror image; reflecting x reverses the order
  and keeps cups, caps and convex position.

**(VC-a), (VC-b).** Take T = S − p, p ∈ 1..14. T is valid, with ends l and r, so it has a weak Δ D containing l or r.
- In S, D is 4-cap-free and meets every hexagon avoiding p.
- D is not a weak Δ of S, because it contains l or r. So D misses a hexagon H of S, and H contains p and avoids the
  end in D: (VC-a).
- D + p meets every hexagon. It contains l or r, so it is not 4-cap-free; the 4-cap contains p, because D is 4-cap-free:
  (VC-b).

**(VC-c).** Take T = S − {p,q} for {p,q} ⊆ S − r (14 points; p = l is allowed).
- ROOT(7) at 14, or weak D(5,7) at 13 plus r if r ends no 4-cap of T, gives a weak Δ D of T with r ∈ D.
- D misses a hexagon of S. That hexagon must meet {p,q}, since D meets all hexagons of T, and it avoids r.
- The mirror argument covers S − l.

## 2. CNF checks (own code; `W = /home/jay/research/data/roadmap-20261115/pm1115/vb1118/claims/t1118-vc16/`)

Inputs:
- `d1ev/cnf/lc7_m16.cnf`: SHA-256 `898569a8…` = d1ev's SHA256SUMS; `p cnf 108258 313199`;
- `t1118/cnf/vc16_addon.cnf`: `c80ca8f7…` = the claim's `SHA256SUMS_0315`; `p cnf 110078 3878`;
- `t1118/cnf/lc7_m16_vc.cnf`: `776914d2…` = the claim's; `p cnf 110078 317077`.

| check (`vb_vc16.py`, `vb_vc16_y.py`) | result |
|---|---|
| numbering: triples 1..560, 4-sets 561..2380 (lex), B(X) for \|X\| = 6..15 without {0,15} ⊆ X, by size then lex, from 2381 (42,737 in all, the last 45,117) | — |
| N1: each of the 7,007 \|X\| = 6 B-variables v has the 15 binary clauses (¬v, cv(Q)), Q ⊂ X | 7,007 / 7,007 (105,105 clauses) |
| N2: each cv(Q) has cv(Q) → [s(xyz) = s(xyw)] and cv(Q) → [s(xzw) = s(yzw)] (4 clauses) | 1,820 / 1,820 |
| VC-a (14 clauses: ∨ B(X), X ∋ p) and VC-c (210 clauses: ∨ B(X), X ∌ r resp. X ∌ l, X ∩ {p,q} ≠ ∅), regenerated from the definitions | all 224 equal to clauses of the file |
| VC-b and the 3,640 definitions: in the file, each new variable y ∈ 108,259..110,078 has exactly the two clauses y → (abc cap), y → (bcd cap) for one 4-set K = {a<b<c<d}; the 1,820 K are distinct; each of the 14 VC-b clauses is {y_K : p ∈ K} for one p, p = 1..14 each once | yes (the y numbering is not lexicographic; it is irrelevant for soundness) |
| merged CNF = base (same clauses, same order, as prefix) + add-on; header 110,078 / 317,077 | yes |

- Soundness of the add-on: under the canonical assignment x = σ, cv(Q) = [Q convex], B(X) = [X convex] for |X| = 6,
  y_K = [K a 4-cap], each family is the corresponding statement of Lemma VC.
- A signotope 4-set is a 4-cap iff abc and bcd are caps (monotone sign sequence), so the y definitions are satisfied.
- The semantic control of the claim (`ctl_vc16.py`, 20 sets) was not re-run.

## 3. Files

`W/vb_vc16.py` (`c51d44c0…`), `W/vb_vc16_y.py` (`a0ef8e50…`), `W/diff_addon.py` (`a90fa73d…`, which locates that the
only first-pass difference was the y numbering), `W/vb_vc16.json`, `W/vb_vc16_y.json`; SHA-256 in `W/SHA256SUMS`.
Re-run in seconds: `vb_vc16.py <lc7_m16.cnf> <vc16_addon.cnf> <lc7_m16_vc.cnf> out.json`, then `vb_vc16_y.py <vc16_addon.cnf>`.
