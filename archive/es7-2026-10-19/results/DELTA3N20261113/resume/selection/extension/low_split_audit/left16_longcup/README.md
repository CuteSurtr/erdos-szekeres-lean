# Independent left16 long-cup append audit — PASS

**COMPUTED:** entire compact16 base and augmented CNF/map rebuilt; all8,008
exact AND flags and the final OR match. Additions:168,169rows/496,496lits.
Final136,305vars/1,071,762rows/2,912,737lits, SHA-256
`f23af9d7113dac3f9e4414298b20fb08d8181c279804d36b79e98a66755622b4`.

**PROVED (written):** a real no4cap set with cup maximum<=5 satisfies T7;
therefore every real T7 failure in the no7gon domain has a six-cup and
canonically satisfies the added family. See [VERIFY_LONGCUP16.md](VERIFY_LONGCUP16.md).
This is not claimed equivalence over arbitrary abstract base models.

352,352 gate truth cases and exact real controls pass, including a16-point
control with73 six-cups and all168,169 new rows true. The separate <=5-cup
proof uses no capacity bound or earlier finite terminal theorem.

A matching accepted UNSAT proof plus this reduction would establish T7
at left16. No proof was replayed, and no left16 or all-left theorem is
claimed here. Original base and search are unchanged. The base itself now
has an independent complete size16 instance audit, retained in data/.

Audit: AS300/one CPU,3.434s/61,540KiB, finished before07:52:16KST.
Packaging uses AS150; no solver, cake, compiler or extra allocation/job
remains. Source, commands, hashes and controls are under data/; future
runs must use new exclusive outputs.
