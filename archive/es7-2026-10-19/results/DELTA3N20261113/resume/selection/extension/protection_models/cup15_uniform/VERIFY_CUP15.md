# Independent fixed-coordinate and cup-proof replay

**PASS.** Exact geometry, cup/forced membership, uniform certificates and
counts are confirmed for the two pinned cup15 realizations. The parent's
cup-membership CNF is independently reconstructed in full, and its retained
binary LRAT is independently accepted by cake_lpr.

The analysis and replay import neither the parent's abstract semantics nor
its geometry implementation as code. Parent claims are loaded only for
comparison after reconstruction. `tools/replay.py` also imports no finder
module. It uses a different determinant expression, supporting-edge convex
polygons, consecutive-turn cap recognition, endpoint-value forced
protection, all-intersection envelope checks, and Boolean upward closures.

For each realization the replay confirms all 455 nonzero orientation signs,
all 11,440 six- and seven-subset polygon tests, 157 cap triples, 47 four-caps,
zero five-caps, 70 convex six-subsets and zero convex seven-subsets. It
checks 840 cup-support comparisons, 840 forced-support comparisons, all 105
pair certificates, and every membership mask in all five retained families.
Both exact coordinate sets have the same ordered orientation type. Source
byte hashes are retained in `data/run/input_manifest.json`.

| Family | Original | Balanced |
|---|---:|---:|
| Ordinary weak | 7,078 | 7,078 |
| Terminal-protected | 0 | 0 |
| Cup-protected | 0 | 0 |
| Forced-protected | 742 | 742 |
| Uniform | 3,562 | 3,588 |

Both uniform minima are four, attained by exactly 90 masks. The shared
positive model `{1,3,5,8}` has exactly two cap triples, `(1,3,5)` and
`(1,3,8)`; their stored one-line supports pass exact replay. Balanced gains
26 masks and loses none. A retained five-point selected set `{1,3,5,6,8}`
is ordinary in both, uniform only in balanced, and documents the change at
cap triple `(5,6,8)` with an original exposure witness and balanced rational
domination certificate.

The parent CNF contains exactly 15 variables and 211 clauses. Comparing
complete clause multisets, including duplicate multiplicities, gives no
missing or extra clauses relative to either geometry. The reconstructed
families are 47 negative four-cap rows, 94 negative unprotected-triple rows,
and 70 positive convex-six-subset rows. The semantic audit receipt is
`data/replay/cup_clause_match.json`.

The independently replayed input hashes are:

| Input | SHA-256 |
|---|---|
| Cup membership CNF | `47c738ec38449827573872fa0223e4c607649f8a38acb2e76a8daf59b365cd1f` |
| Binary LRAT | `dc2861a3b6a40c42a8347ece05360f37c3027b83b9c410c0dc9b731370b587ba` |
| Compressed binary LRAT | `e36731ea9aeb33beebe68aa987eb65941178dfbfb58bec9cbaa64007240ea82a` |
| cake_lpr executable | `c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54` |

`tools/certify_replay.py` first checks the independent semantic receipt,
the exact parent/certificate CNF byte identity, and compressed-proof
roundtrip. It then runs the retained proof against that unchanged input
with `--CML_HEAP_SIZE=64 --CML_STACK_SIZE=32`. The complete log contains
the exact line **`s VERIFIED UNSAT`**, and the checker exits zero. The
certificate is therefore CERTIFIED for this exact formula. The 2,349-byte
raw proof and 1,559-byte compressed proof are both retained in
`data/certificate/`. No proof generation or deletion occurred.

The primary analysis took 0.22 seconds and 19,028 KiB RSS. Independent
replay took 0.63 seconds and 20,736 KiB RSS. cake took below the timer's
0.01-second resolution and 7,772 KiB RSS; the wrapper completed in about
0.008 seconds. Every command used one CPU, AS400 MiB and external20s.
No unknown, failed check, memory event or long unit occurred in this task.

This audit is about these fixed inputs and the stated membership rules.
The cup nonexistence certificate does not refute ordinary or uniform
selection. Finite uniform counts and minimum-size claims are COMPUTED exact
enumerations; they are not labeled LRAT-certified. No Lean result is asserted.
