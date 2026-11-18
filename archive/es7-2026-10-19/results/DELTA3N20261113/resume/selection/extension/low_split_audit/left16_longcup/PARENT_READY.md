# Left16 Has6cup append and reduction PASS

Full compact16 base rebuilt as well as all8,008 new flags/map entries,
168,169rows and496,496lits. Old base body/map unchanged. Augmented CNF
matches `f23af9d7113dac3f9e4414298b20fb08d8181c279804d36b79e98a66755622b4`.

[VERIFY_LONGCUP16.md](VERIFY_LONGCUP16.md) gives the independent rank proof:
maxcup<=4 has no hexagon; at maxcup5 the rank-five level is a covered cup
transversal. Every real T7 failure therefore has a six-cup. Canonical
projection is sound; abstract propositional equivalence is not claimed.

All gate/real controls PASS. A future accepted matching proof would give
T7 exactly at left16, with the no-six-cup branch discharged by the lemma.
No proof replay or finite16 theorem is claimed now. No capacity dependency
is used in the lemma; universal-left conclusions still need capacity.

Finished compute before07:52:16KST, AS300/one CPU,3.434s/61,540KiB.
Packaging AS150. No job, solver, cake or extra reservation remains.
