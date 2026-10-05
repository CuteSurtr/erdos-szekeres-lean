# Erdős–Szekeres in Lean

Lean proofs of two published upper bounds for **finite point sets in the real
plane in general position** (no three distinct points collinear), together with
separately identified computational research. Polygons need not be empty.

**The Erdős–Szekeres conjecture is not proved or disproved here. No new geometric
upper bound or improvement of HMPT's asymptotic coefficient is claimed.**

## Finished formalizations

All logarithms below are to base 2. The floor is the natural-number floor.

| Published result | Proved statement | Main Lean theorem | Source |
| --- | --- | --- | --- |
| Suk 2016, Theorem 1.1 | For all sufficiently large `n`, at least `⌊2^(n + 6 n^(2/3) log₂ n)⌋` points force a convex `n`-gon. | `ErdosSzekeres.Suk.theorem2016 : ErdosSzekeres.Suk.Theorem2016` | [Suk/Asymptotic.lean](ErdosSzekeres/Suk/Asymptotic.lean); [statement and threshold](ErdosSzekeres/Suk/Statement.lean) |
| HMPT 2020, Theorem 1.3 / Remark 1.4, **ordinary real-point specialization** | For every `ε > 0` and all sufficiently large `n`, at least `⌊2^(n + (8√2/3 + ε)√(n log₂ n))⌋` points force a convex `n`-gon. | `ErdosSzekeres.HMPT.theorem2020 : ErdosSzekeres.HMPT.Theorem2020` | [HMPT/Asymptotic.lean](ErdosSzekeres/HMPT/Asymptotic.lean); [statement and threshold](ErdosSzekeres/HMPT/Statement.lean) |

Both final theorems have complete proofs with no unproved geometric assumptions.
Their quantifiers are eventual: they do not assert these formulas for every
small `n`. [Definitions.lean](ErdosSzekeres/Definitions.lean) uses `Point := Fin 2 → ℝ`
and `ForcesConvexNGon N n`, which quantifies over every general-position finite
set with **at least** `N` points and supplies a convex subset of exactly `n` points.
Convex position is Mathlib's `ConvexIndependent`.

These are completed upper-bound formalizations, not verbatim formalizations of
every statement in either paper. Suk's proof uses a checked extraction variant
with different intermediate constants. HMPT's pseudo-configuration and convex-body
extensions are outside the implemented scope. The [paper-to-Lean tables](docs/PAPER_MAP.md)
list every numbered result and distinguish exact results, replacement arguments,
restricted specializations, and statements not formalized.

- [Suk proof ledger](docs/SUK.md): geometric cases, extraction, integer estimates and limits.
- [HMPT proof ledger](docs/HMPT.md): cap budgets, counting ratios, two scales and optimization.
- [Third-party provenance and licenses](docs/THIRD_PARTY.md): adapted prerequisites and research data.

## Verification

Pinned versions: **Lean 4.24.0**, **Mathlib v4.24.0**; dependency revisions are in
[lake-manifest.json](lake-manifest.json).

The current library passes `lake build --wfail`. The
[full saved axiom audit](docs/validation/axiom-audit-2026-10-05.txt) checks **201 named
theorems**, including both main theorems and their transitive axiom dependencies.
Only `propext`, `Classical.choice`, and `Quot.sound` are allowed. There is no
`sorry`, `admit`, `sorryAx`, or `native_decide` in the maintained Lean sources,
including the finished results and vendored Lean prerequisites. The
[validation record](docs/VALIDATION.md) gives the scope, commands and source hashes.

```sh
lake exe cache get
lake build --wfail
python3 scripts/check_axioms.py
python3 -m unittest discover -s scripts -v
```

The default Python suite needs only the standard library; solver-specific tests
skip when their optional dependencies are unavailable. This Mac checkout has a
workspace-local toolchain, so use `ELAN_HOME="$PWD/.elan" .elan/bin/lake` in place
of `lake`. `.cache/`, `.lake/`, `.elan/` and compiled outputs are ignored and are
not committed. Standalone research certificates have separate reproduction
instructions and are not silently counted as default-library CI checks.

## In-progress research — stopped at the user's request

This material is separate from the finished Suk and HMPT formalizations.

- **Finite octagon omission systems:** complete exact integer certificates
  improve two auxiliary occupancy bounds from 193 to 192 and from 124 to 123.
  Two programs replayed the arithmetic. The full trees are **not checked in Lean**,
  and the connection from arbitrary real configurations to all catalog rows is
  **not formalized here**. Consequently **ES(8) ≤ 317 is not a theorem of this repository**.
- **Final checking checkpoint:** [21 catalog blocks and one conditional leaf](experiments/omission-chunked-2026-10-05/README.md)
  pass Lean separately. This certifies row encodings and one branch context,
  not all 155,336 leaves or a global geometric bound.
- **Other retained experiments:** exact-coordinate searches, SAT/SMT attempts and
  a Lean-checked counterexample to a proposed mixed-cap lemma. None improves the
  published geometric upper bounds; timeout results remain inconclusive.

See [the ES(8) remaining-work estimate](docs/ES8_REMAINING.md),
[omission certificate record](docs/OMISSION.md), [mixed-cap result](docs/MIXED_CAPS.md),
[SAT record](docs/SAT.md), and [historical research log](docs/RESEARCH.md).
The open conjecture and `HMPT.StrictImprovement` are proposition definitions,
not assumed axioms or unfinished proof declarations. No further research or
certificate batch is running as part of this checkpoint.
