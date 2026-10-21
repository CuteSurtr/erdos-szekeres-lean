# AUDIT2 A1 notes (Lean statements), started 2026-10-21 00:33 UTC

- Toolchain: Lean 4.24.0 release zip; Mathlib f897ebc (manifest pin) building from source (cache 403 expected).
- Read: ErdosSzekeres/Definitions.lean, H/ETVEncoding/Dimacs.lean, H3 Line/Targets/Cover/CoverCore/Frame,
  V1-L Main, V2-L Main/ClauseCover/Facts/Tree/TreeMain/TreeData/FinalTree, Trees/Table + Checks.
- a1_trees.py (own decoder of V2L/Data.lean and V2L/Trees/T*.lean): 450 specs/cubes = Mii-S cases.icnf/cases.jsonl;
  74,000 Lean tree leaves; every one equals (as a literal set) a cake_lpr `s VERIFIED UNSAT` leaf record of the
  same case in the 78 V3Z aggregate inputs (73,828) or is the empty leaf of a Haudit t5 verified direct case (172).
  0 unmatched. 52 verified U_L7 leaves are not tree leaves (as README §9.4 says).
