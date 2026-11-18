**Verdict: CONFIRMED** (claim `lp0-7-scan-all-nonreal`, verifier V2, 15 November 2026, 17:48-17:50 KST). Label
EXACT is correct. All 87 re-indexed certificates are valid BFP certificates with V for the sub-chirotopes I built from
each W's own sign string, so none of these 87 models has an x-sorted real realization. With claim
`lp0-7-realblock-nonreal` (V2 CONFIRMED, 21 models), none of the 108 satisfiable models of P2's scan has one.

# Independent check: the 87 non-real-block LP0(7) extension models are not x-sorted realizable

**Definitions.** As in [VERIFY_LP0_7_REALBLOCK_NONREAL.md](VERIFY_LP0_7_REALBLOCK_NONREAL.md):
- V is the element after the certificate points, with [a,b,V] = + for a < b;
- lexicographic signs with the parity rule, the 3-term GP identity, and positive multipliers summing to 0.

**Code.** `/home/jay/research/data/roadmap-20261115/pm1115/v2/lp0-7-scan-all-nonreal/check_inherit_v2.py`
(`fcfec50635e6210aebbde13a3499729c548ec9944dd80ace358db494f47596e3`). Its output is `inherit_check.jsonl`
(`dbe8fea1…`). It uses `bfp_v2core.py`, a byte copy of V2's validated BFP checker (`645ccfab…`), and `v2lib.py`. R7's
tools were not read.

## Checks

1. **Selection.** The scan `p2/lp0scan_k2.jsonl` (`bedfd8c0…`) has **108** records with `sat: true`. **87** of them
   have a block other than the two real blocks:

   | block | models |
   |---|---|
   | r7/root7_m17_s1 | 13 |
   | t4/cegarmodels/r7c17_it2 / it3 / it7 / it8 | 11 / 10 / 10 / 10 |
   | t4/cegarmodels/r7cg17_it1 / it2 / it3 | 11 / 11 / 11 |

   All counts are as stated.
2. **Identity.** Each record's signs equal `r7/lp0/inherit/W_<block>_<pattern>.json`.
3. **Certificates.** For each model I took the certificate's `pts`, which are W indices: increasing, in range, and all
   at `o` positions of the pattern, i.e. points of the block. I built the sub-chirotope **from W's own signs** on those
   points and appended V with `+` on every triple containing it. The checks per item:
   - five distinct elements;
   - a positive integer multiplier;
   - the stated odd term opposite to both other terms;
   - ±mult on unordered triples, with every total 0.

   **Accepted 87/87.**
   - Every certificate has withV = true and actually uses V. k ranges over **9-14** points.
   - There are **8 distinct certificates**, one per block. Their sources are `r7/bfp/s1_min.json`, `r7/cg17/models.jsonl`
     iterations 1-3 and `t1/r7c17/models.jsonl` iterations 2, 3, 7 and 8, as described.
   - Because each certificate is checked on W itself, the conclusion does not depend on the transfer argument
     "a sub-configuration of a realizable configuration is realizable". That argument is also correct.

**Not checked.** Whether these 87 models are themselves valid with r unrootable. That is P2's scan, and it is not part
of this claim's statement. The 21 real-block models were checked in the companion verify file.
