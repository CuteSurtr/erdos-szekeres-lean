# VERIFY_T1118_ANCHORL_DATA_VB1118: claim `t1118-anchorl-strong-data` (verifier VB, 18 Nov 2026, 03:57-04:10 KST)

The verify file named in the claim, VERIFY_T1118_ANCHORL_DATA.md, already held VS's verdict on claim
`t1118-anchorl-data`, so this file carries the suffix `_VB1118`.

**Verdict: CONFIRMED WITH CORRECTION.**
- Items (a), (b), (c) and (e) and the PROVED implication are confirmed. The data parts were re-run with own code on the
  **whole** collection rather than samples, which makes them stronger.
- In item (d), the count is right but the conclusion is not. "8 of 872 3-cups from l do NOT extend" is reproduced
  exactly: the 20 hostile sets with indices 400-419 have 872 3-cups from l, 8 fail, in 8 sets.
- But all 8 failures are the cup (0, 7, 14), which **contains r = 14**. In a right-hostile set a cup through r can never
  lie in a weak Δ, so these failures are trivial.
- They do **not** show that "the k = n−3 version is false at n = 6" for the version used in the claim's own
  implication, which is about cups from l avoiding r. Every 3-cup from l avoiding r extends in **all 348** right-hostile
  n = 6 sets.
- The claimant has already filed this correction: claim `t1118-anchorl-correction`, VS CONFIRMED,
  VERIFY_T1118_ANCHORL_DATA_VS1118.md. VB's full-collection counts agree with it.
- There is one more data point of the same kind at n = 7. Of the 36,891 4-cups from l in all 266 right-hostile n = 7
  sets, **4 do not extend, all the cup (0, 1, 4, 16) through r = 16** (hostile-list indices 67-70, file lines 200, 202,
  204, 206). Every 4-cup from l avoiding r extends.
- So item (c) ("every 4-cup from l extends" in 22 sampled sets) holds for its sample, but read literally it fails on
  these four other sets. Read as "avoiding r", it holds on all 266.

## 1. Results (own code `vb_anchor.py`, `vb_anchor_fails.py`; T's anchor_l*.py were not read)

Collection: `pm1115/t2size/out/all_sets.jsonl` (1,440 sets, SHA-256 `f346259c…`).
- Every set is a signotope (monotonicity on all 4-subsets) and (5,n)-valid: no 5-cap, no convex n-set.
- Own right-hostility (r in no weak Δ, exact search) agrees with the data's `rootable[-1]` on 1,440 of 1,440 sets.
- 614 sets are right-hostile: 348 at n = 6, 266 at n = 7.

| item | claim | own result (all sets of the class) |
|---|---|---|
| (a) (n−1)-cups from l, all 614 hostile sets | 5,182 cups (2,774 at n = 6, 2,408 at n = 7), all extend, none contains r | **5,182 (2,774 / 2,408), 0 fail, 0 contain r** |
| (b) 5-cups from l, all 266 hostile n = 7 sets | 20,738, all extend | **20,738, 0 fail** |
| (c) 4-cups from l, n = 7 | 22 sampled sets, 2,926 cups, all extend | all 266 sets: 36,891 cups; **4 fail, each the cup (0,1,4,16) through r**; every 4-cup avoiding r (36,887) extends |
| (d) 4-cups from l, n = 6 | 30 sampled sets, 1,272 cups, all extend | all 348 sets: **15,663 cups, 0 fail** |
| (d) 3-cups from l, n = 6 | 8 of 872 fail in 8 of 20 sampled sets, "so the k = n−3 version is false at n = 6" | sample 400-419: 872 cups, 8 fail, all (0, 7, 14) through r = 14. All 348 sets: 15,861 cups, 84 fail, **all 84 through r**; every 3-cup avoiding r (15,777) extends. **The conclusion does not follow** (see above) |
| (e) (n−1)-cups from l in r-rootable sets | 150 sampled sets, 216 cups, all extend | all 826 r-rootable sets: **6,168 cups, 0 fail**, of them 2,310 through r |

Method:
- A cup K extends iff some X ⊆ S − K makes K ∪ X 4-cap-free and meeting every gon (convex (n−1)-set).
- This is decided exactly by a complete hitting-set search: branch on the points of the first gon not met by the
  current set, skipping points that would create a 4-cap, with memoised failures.
- The search is complete because any valid X contains a point of every gon not met by K, and a minimal hitting subset
  of a valid X is again valid (a subset of a 4-cap-free set is 4-cap-free).
- Cups are taken from l with every triple a cup; gons and 4-caps come from the sign string, with triples a<b<c in lex
  order and '+' = cup.
- Unit `esr-agv-vb-anchor` (95 %, 1500M), 21 s, max RSS 20 MB.

## 2. The PROVED implication (checked)

Premise: at m = 16, whenever r is unrootable, every 5-cup from l avoiding r extends; and the mirror statement holds.

In an LR(7) failure both ends are unrootable, so:
- **No 5-cup from l avoids r**, because it would extend to a weak Δ containing l. By the mirror statement, no 5-cup
  ending at r avoids l.
- A 6-cup from l contains a 5-cup from l avoiding r: its first five points, since r = 15 can only be a cup's last
  point. So α(l) ≤ 5, and likewise β(r) ≤ 5. There is no 6-cup at an end, so piece C1 of `d1-lr7m16-split` is empty.
- If β(r) = 5, every 5-cup ending at r contains l, so it runs from l to r and α(l) = 5; the converse is the mirror
  argument. So K2 (β(r) = 5 and α(l) ≤ 4) is empty.
- K3 reduces to the 5-cups (0, a, b, c, 15): C(14,3) = **364** position patterns.

The premise itself is a conjecture. The claim does not claim it, and the data support it only on the collection.

## 3. Files (`W = /home/jay/research/data/roadmap-20261115/pm1115/vb1118/claims/t1118-anchorl-strong-data/`)

`vb_anchor.py` (`a0d6503a…`), `vb_anchor_fails.py` (`a7b0c96b…`, lists the failing cups), `run.sh`, `vb_anchor.json`
(per-set results), `vb_anchor.out`, `vb_anchor_fails.out`; SHA-256 in `W/SHA256SUMS`. Re-run: `bash W/run.sh`
(about 20 s); then `vb_anchor_fails.py <all_sets.jsonl> x.json`.
