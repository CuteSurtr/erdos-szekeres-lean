# Δ theory, size reduction for LR(7) / weak D(5,7) (track T2, 16 November 2026, from 18:40 KST)

**Status (18:40 KST): started. Nothing proved yet.** Weak D(5,7) and LR(7) remain OPEN from 16 points. No ES bound
changes. This file is written early and updated after each milestone; the last section lists what remains.

Labels: PROVED (written proof here) / CERTIFIED / EXACT (own exhaustive code from the definitions) / COMPUTED /
HEURISTIC / CONJECTURE. Nothing is rounded up. Work directory (not in Git):
`/home/jay/research/data/roadmap-20261115/pm1115/t2size/`. Compute: foreground only, one thread, each run < 1 min.

## 0. Definitions

As in THEORY_1115PM.md §0. S is a signotope on 0..m−1 in x-order; '+' = cup, '−' = cap; (5,n)-valid = no 5-cap and
no convex n-set; gon = convex (n−1)-set; weak Δ = 4-cap-free set meeting every gon; l = 0, r = m−1; a point p is
*rootable* in S if some weak Δ of S contains p. LR(n): every (5,n)-valid S in which r ends a 4-cap and l starts a
4-cap has a weak Δ through l or through r. An *LR failure* is a valid S with r ending, l starting a 4-cap and neither
rootable.

## Plan

1. Block structure of LR failures (gluing, Lemma M) and what can be bounded.
2. Candidate size reductions (deletion lemmas, local conditions, saturation); test each on the known sets.
3. Proofs of whatever survives; claims for proved statements (verifier VS).

## What remains

Everything (record started).
