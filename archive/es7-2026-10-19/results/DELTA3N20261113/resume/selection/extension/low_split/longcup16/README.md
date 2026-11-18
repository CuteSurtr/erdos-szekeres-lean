# Left16 search with the explicit long-cup consequence

**COMPUTED formula construction; searches cleanly stopped after the
original unaugmented formula was certified.** This is a
separate instance from the original compact left16 search. It adds a
geometrically justified necessary condition for a real T7(L) failure.

The frozen [low-split reduction](../../structure2/low_split.md) proves
terminal selection in a standard low join whenever maxcup(L)<=5. Its
exact equivalence with T7(L) therefore implies that a real T7(L) failure
has a six-cup. The original premises exclude seven-gons, hence also
seven-cups. This reasoning does not assert propositional equivalence
between the two Boolean instances; nonreal abstract models may be removed.

For each of8008 six-subsets q, a fresh variable z_q is equivalent to the
conjunction of its20 positive orientation literals. The two implication
directions are encoded by20 binary clauses and one21-literal clause.
The final clause requires some z_q. Every real T7 failure has the canonical
assignment satisfying this family. Exactly8008 variables,168169 clauses
and496496 literals are added. The original903593 base rows are unchanged.

[augment_left16_longcup.py](../../augment_left16_longcup.py) creates the
new CNF and map without altering the old ones. Scratch base is
`/home/jay/research/data/delta3-codex-20261113/extension/`;
the new input is `low16-n7-longcup.cnf`.

| File | SHA-256 |
|---|---|
| Original compact16 CNF | `2e233545d18e3a9acf9a253b80a102935828bee27c079ba18946dfbd4efd53d8` |
| Augmented CNF | `f23af9d7113dac3f9e4414298b20fb08d8181c279804d36b79e98a66755622b4` |
| Augmented map | `c4e2ec5444906df0e7dbe80e2cb2846d6e38a52ed4c7af6e3c746dcef93049bb` |
| Generator | `168c016a00338dfa2ae0f40129c6af31ce81f13b21a4a82d40d61fd990ecb3f0` |

Independent reconstruction and review of the geometric consequence
[passed](../../low_split_audit/left16_longcup/VERIFY_LONGCUP16.md).
An abstract SAT outcome would still require exact coordinates and a
separate geometric audit. UNKNOWN gives no mathematical conclusion.

The search started07:54:55 in `nov13c-vfy-delta6-longcup16` with one CPU,
AS1000MiB, nominal MemoryMax1400M, Swap0 and Runtime2100s. The solver gets
1200s and the initial checker gets180s/heap650. The roughly2.91 million
literals estimate at416--695MiB under the stated150--250bytes/literal
policy, leaving additional room below the AS ceiling for solver buffers.
The larger capacity check completed before launch and released its slot.
The new `run_binary_cache.py` and separate cache watcher release proof
cache frequently; no proof file is deleted. Scratch output is
`low16-longcup-a/`. No running-search status counts as mathematical evidence.

A second diversity run, `low16-longcup-unsat-a/`, used `--unsat --seed=713`
and started07:57:43. Both solver children were deliberately interrupted
at08:05:34 after the original formula's accepted proof made these searches
redundant. Their wrappers completed archive compression and hash-verified
roundtrips by08:05:57. Each final status is UNKNOWN with a retained
`CONTROLLED_STOP.json`; neither is a proof or a memory failure. No raw or
compressed proof was deleted. Universal T7 uses the original certificate
and its independent replay, as recorded in [CLOSURE.md](../CLOSURE.md).
