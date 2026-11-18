# VERIFY_P307V_N66COVER: verdict on claim p307v-n66-cover (verifier VS, 18 November 2026, 03:05-03:10 KST)

**Verdict: CONFIRMED (EXACT as claimed; acceptance read from the files, COMPUTED). This is a status, not a bound.** At
02:42 the level-14 cube certificates did **not** cover the N66 ≤ 55 split. VS's own code, written from the definitions
in N66N20261113/cubes20261115/README.md §§2 and 6 and not from `n66_cover_check.py`, reproduces every number of the
claim:
- 110 accepted certificate directories (the claimant's list, each one passing VS's rules including the deep trim.cnf
  checks);
- uncovered measure **15/256** (= 240/4,096);
- the uncovered region is exactly the union of the driver's 22 non-certified leaves;
- the 132 leaves partition the split;
- the 8 UP-refuted base patterns are accepted.

One wording point, not an error:
- The driver's split is refined on **states 45 and 39** in one branch (presplits at 18:55 on 16 Nov), so the leaves use
  14 states.
- The claim's "240 of 4,096 over the 12 split states" is exact, because coverage depends only on the accepted cubes,
  and none of them used 45 or 39 at 02:42. Over the 14 states it is 960/16,384, the same measure.
- The claim's partition statement holds over the 14-state split. VS checked it directly, and the claimant's checker
  checks it over the leaf states as well.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/p307v-cover/`, `vs_n66cover.py` de274339…)

1. **Acceptance rules** (from the definitions). A directory `<id>/it<k>` is accepted only if all of these hold:
   - cert.json and verify.json: ALL_OK true, `cake_lpr` = `s VERIFIED UNSAT`, the cube equals the id's literals (o =
     bit 1, h = bit 0, as sets), `sb_pairs` equals the 27 pairs of `p2/b14h2/it1/layout.json`, budget 14;
   - cert.json: holes_at_least 15, bound 55, W_size 70;
   - verify.json: unclassified 0 and the same `trim_cnf_sha256` as cert.json;
   - layout.json: L 14, W = range(70), sel = [988541, 988610], the same SB list and cube;
   - cake.out contains the exact line;
   - **deep:** SHA-256(trim.cnf) equals cert.json, and every unit clause of trim.cnf is +sel_0, +sel_1 or a declared
     cube literal.
2. **The 02:42 state** (`--only` with the claimant's accepted list from `data/cover_deep_0242.json`; `deep_0242.out`,
   run 03:08:35).
   - All **110/110 pass**, including the deep checks.
   - **Uncovered: 960 of 16,384 assignments of the 14 states = 15/256.**
   - The **non-accepted leaves are exactly the claimant's 22**: hooooo and oooooh (1/64 each), 10 at 1/512, 7 at
     1/1,024, one at 1/2,048, two at 1/4,096; the sum is 240/4,096.
   - **The 132 leaves partition the split.** Every assignment of the 14 states matches exactly one leaf, and each
     leaf's literals equal its id.
   - **The uncovered set equals the union of the non-accepted leaves.**
   - The 8 UP-refuted base patterns (hhhohh, hhhooh, hhoohh, hhoooh, hohohh, hohooh, hooohh, hooooh) are all accepted.
3. **State now, for comparison** (`deep_now.out`, 03:07:52).
   - **116 accepted.** The extra 6 were certified after 02:42: ohohoo_23o_40o_52o, ohoooo_40o_52o_46h,
     oohhoo_23o_40o_52o, oohooo_40o_52o_46h, ooohoo_40o_52o_46h and oooooo_40o_52o_46h_44h.
   - **Uncovered measure 49/1,024** (784/16,384), i.e. 240/4,096 − 5·8/4,096 − 4/4,096. 16 leaves are open.
   - The partition and the union identity still hold.
   - The 49 directories not accepted have no certificate files: 44 split parents and 5 running cubes. No complete
     certificate failed a rule.
4. **Review of `n66_cover_check.py`** (1cad0401…, read in full).
   - Its rules are those of the claim. They are a superset of VS's: it also requires `trim_lrat_sha256` in verify equal
     to cert's, `cnf_sha256` in layout equal to cert's `full_cnf_sha256`, and well-formed cubes not mentioning states
     0/1, and it compares cubes as ordered lists.
   - Its cover is taken over the base states plus the accepted cubes' states, by exact enumeration.
   - The leaf partition is checked over all leaf states as total measure 1 plus full coverage, which together imply
     disjointness. The union identity is checked over the same states.
   - Its 10 negative controls (`p307v/negctrl.log`) each fail the targeted rule and raise the uncovered measure as
     expected: drop a certificate, missing cake line, flipped cube bit, changed SB pair, budget 15, unclassified 1,
     ALL_OK false, W of 69, extra trim unit, and the positive run.

## Not checked

- The certificates themselves: no cake_lpr re-run, since the trim LRATs are about 340 MB and need a large heap. VB's
  VERIFY_N66CUBES_1116.md covers part of them.
- The soundness of p2_verify and mono66, which the record relies on.

## Files

`V/vs_n66cover.py` (de274339…03ea), `V/vs_cover_0309_only_deep.json` (712aeda3…6ec5, the 02:42 list, deep),
`V/vs_cover_0308_deep.json` (0cdf7beb…9ba1, state at 03:07:52), `V/deep_0242.out`, `V/deep_now.out`.
