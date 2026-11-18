# Terminal n7/m14 with no six-cup — bounded experiment

**COMPUTED formula construction; bounded search ended UNKNOWN.** This separately
tests whether every14-point real set with no five-cap, no six-cup and no
convex heptagon has a terminal-safe Delta. The extra no-six-cup hypothesis
is explicit. A result here would not settle the remaining unrestricted14
case, which also allows six-cups.

The base is the audited exact-containment n7/m14 formula. For each of the
3003 six-subsets, one clause requires at least one of its20 triple signs
to be negative. This is exactly no six-cup under the increasing-x,
general-position interpretation. There are60060 additional literals,
no new variables, no fixed signs and no decomposition assumptions.

`../augment_nosixcup14.py` and the scratch receipt pin source, base,
map and output hashes. A real counterexample satisfying the extra
hypothesis supplies the canonical satisfying assignment to all rows.
The independent [instance audit](../cup_bound14_audit/VERIFY_CUP_BOUND14.md)
passes all3003 rows,60060 literals and both exact real controls. An exact
cake_lpr acceptance and independent proof replay are still required before
a finite theorem is claimed. SAT would still need exact real
coordinates and geometric checking.

The one-CPU unit uses AS700MiB, MemoryMax1000M, no swap, solver1500s,
cake360s/heap450, and RuntimeMaxSec2700. This stays within the existing
6000MiB verifier budget after the real Lean work released its slot.

The1500-second solver budget ended UNKNOWN. Total run time including
retained trace hashing/compression was1517.438s, and the compressed
roundtrip passed. [data/nosixcup14-a/result.json](data/nosixcup14-a/result.json)
pins the2,650,688,282-byte trace and all commands. This trace is not a
certified UNSAT proof. Even the restricted fourteen-point question remains
unsettled by this run.
