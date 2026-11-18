# Cup and endpoint-sign protection models

**CERTIFIED and independently audited: the real cup-support obstruction.**
The cup n7/m15 model has two exact integer realizations. Independent
geometry, predicate and exhaustive membership replay passes, and the
fixed211-clause proof has a fresh independent cake_lpr acceptance.
The forced n7/m16 model is **PROVED nonrealizable** by an exact algebraic
product contradiction, with independent worker and parent replays.
Neither supplies an ordinary weak Delta counterexample.
The real cup example has thousands of uniform-envelope selections.

These are different examples from `../terminal15/` and `../terminal12/`.
The cup-support criterion asks for an ambient four-cap terminal line
reachable by one componentwise-right cup-union comparison. The stronger
endpoint-sign coverage predicate permits the two orientation tests in
`../forced_terminal_general.cpp`. Both are sufficient conditions for
uniform line domination, not necessary conditions.

The new parent tools `../extract_protection_model.py` and
`../protection_signs.py` stream-check every Boolean clause, export ordered
triple signs, and recompute protection and every selected subset without
SAT auxiliary values. Both models have no five-cap and no seven-gon in
their abstract orientations.

| Model | Variables / clauses | Weak Deltas | Terminal | Cup | Endpoint-sign |
|---|---:|---:|---:|---:|---:|
| cup m15 | 69,673 / 193,880 | 7,078 | 0 | 0 | 742 |
| forced m16 | 136,711 / 338,704 | 6,439 | 0 | 0 | 0 |

The cup model has 47 four-caps and 70 hexagons; the forced model has
107 four-caps and 267 hexagons. Counts exhaust all 32,768 and 65,536
memberships respectively. Minimum ordinary selection sizes are four
and five. Realization and metric claims require additional evidence.

Scratch base is `/home/jay/research/data/delta3-codex-20261113/extension/`.
Solver runs are `cup15-a` and `forced16-a`; their result receipts retain
commands, source/binary hashes, raw and compressed search traces, and
verified compression roundtrips. SAT search traces are not UNSAT proofs.
Full-model checks are `cup15-model` and `forced16-model`; semantic families
are `cup15-semantics` and `forced16-semantics`.

The cup CNF SHA-256 is
`c5cb343fd310870af75c72214d6356bec98e2536299dbf3443dbb7883d654a0c`;
the forced CNF SHA-256 is
`250b12cf07eb72c11b620ee99e352be7b2af94a4afea2711f7c43ce1ac407bf8`.
The accepted integer cup coordinates are retained in
`realize-cup15-a/witness.json`; all 455 determinants match the exported
signs exactly. LP status was only a finder hint. The separate uniform
family audit is [complete](cup15_uniform/README.md). The original has3562
uniform Deltas and the balanced realization3588, with minimum size4 and90
minimum witnesses in each. The balanced realization retains all original
uniform selections and adds26. Both have the common witness {1,3,5,8}.
Exact rational certificates and an independent replay establish these
fixed-coordinate claims; existence does not change between the two.

The full cup membership CNF SHA-256 is
`47c738ec38449827573872fa0223e4c607649f8a38acb2e76a8daf59b365cd1f`;
the independently replayed LRAT SHA-256 is
`dc2861a3b6a40c42a8347ece05360f37c3027b83b9c410c0dc9b731370b587ba`.
[data/cup15-fixed/certificate/result.json](data/cup15-fixed/certificate/result.json)
and the independent packet retain the two checks. The parent separately
checked all15 fourteen-point restrictions: all have terminal, cup and
endpoint-sign selections. This proves no new global minimum; n7 terminal
and cup failure minima each remain between14 and15.

All16 fifteen-point and120 fourteen-point restrictions of the abstract
forced16 model also admit terminal selections in their restricted signs.
The first100000-trial realization search found no exact witness. Necessary
GP tests pass for all15015 cup15 and21840 forced16 relations. A rounded
near-model control has46 heptagons and is inadmissible; it is not accepted.

The completed [nonrealizability packet](forced16_realization/VERIFY_FORCED16.md)
supplies387 strict bracket-product inequalities with positive integer
weights. All560 bracket exponents cancel, giving a contradiction for
every hypothetical real realization. The separate
[parent checker](forced16_parent/README.md) also expands the polynomial
identity symbolically and rejects corrupted certificates. This is a
written proof with exact arithmetic, not a Lean or cake_lpr claim. The
failed realization searches are retained but play no role in this proof.

The bounded coordinate searches used one CPU and AS600 MiB with no swap.
They are finished and their reservation has been released. Resource
receipts distinguish clean manual stops from checker heap exhaustion.
