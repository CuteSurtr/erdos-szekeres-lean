# Independent n6 low-left audit — CERTIFIED / PASS

Both fresh cake128 replays print exactly `s VERIFIED UNSAT`; all pre/post
hashes are stable. Complete independent row/map reconstruction and exact
canonical real controls pass for left10 (592vars/6,522rows) and left11
(968vars/11,298rows). The unchanged generic source and projection are
inherited from the frozen [low audit](../VERIFY_LOW_SPLIT.md).

**T6(L) holds through left11**, with explicit lower coverage: left<=9
joins a low two-cup to give total<=11, using the separately established
terminal6 positive cases through11 and the exact classification. The
two certificates here cover left10 and11 individually. There is no
ambient-size monotonicity inference.

[VERIFY_LOW6.md](VERIFY_LOW6.md) gives the complete argument, hashes and
limits. Extending T6 to all left sizes needs the separate no4cap/no6gon
capacity bound |L|<=11. The parent's Capacity11 Lean specialization is
not assumed checked here. Even then, low joins with singleton L and
right cup maximum4 still require a right-block selector; universal T6
alone is not an unconditional all-low-join theorem.

Positive controls check12,288 whole-set memberships and every actual CNF
row under exact canonical values. Each case has20 Option1 cups and60
terminal selectors in its constructed join. All non-failure clauses hold.
Original proofs and compressed proofs remain; commands and outputs are
retained under data/. The two CNF hashes start2aac28f4 and1dcd40d4;
full values are in VERIFY_LOW6.md and per-case result.json.

All work used one CPU, AS300MiB, wall20/CPU19, cake128/stack32. Cake took
0.025s/0.050s, peak RSS at most134,268KiB. No extra allocation, compiler,
solver or long unit was used; no job remains. Old frozen records are
rechecked unchanged. Resume commands are in data/run.command.sh; use new
exclusive output paths for any future replay.
