# Independent compact left15 audit/replay — CERTIFIED / PASS

All63,368 map entries,447,615 clauses and1,200,138 literals match independent
reconstruction. The exact real control has100 Option1 cups and satisfies
every non-failure clause under canonical flags. Fresh cake1400/stack32
prints exactly `s VERIFIED UNSAT` in73.805s; pre/post streamed hashes match.

With the explicit lower chain in [the prior replay packet](../replay/README.md),
this establishes **T7(L) through left15**. No ambient-size monotonicity,
left16 or all-size conclusion is claimed. [VERIFY_LEFT15.md](VERIFY_LEFT15.md)
gives the full argument, proof hashes, controls and limits.

CNF SHA-256:
`793063f5c7c5208c16ce038c63659878adee4eb049546d775d65c5a18ed60418`.
Binary LRAT SHA-256:
`f86789033376814b7a36ea4bbc26e5a6007e66168a1fef4e38d09a5f6cca2f7c`.

The replay finished07:40:18.796KST, total79.891s including hashes.
AS1650, heap1400, nominal MM2200, one CPU, Swap0, Runtime780; cgroup
peak1460.51MiB, no swap. Cache release was active throughout. Unit inactive,
temporary1650MiB reservation released; no own check overlapped cake.
The instance audit used only AS300/20s. No extra allocation remains.

Parent heap550/900 failures and their later heap1400 acceptance remain
separately recorded. Original proofs and old frozen records are preserved.
Exact commands are data/instance.command.sh and data/launch.command.sh;
any future replay needs new exclusive outputs and coordinated resources.
