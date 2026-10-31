# C3b shard plan: m = 11, k = 7 (C3, 33 points). Status: NOT shown closable

This file records exact, deterministic inputs, so other machines can continue. **It is not
evidence that the instance is closable.** No leaf of the full instance has closed in this run,
or in C3a's chain-encoding run. The data below gives only a lower bound on the cost. If more
machines are available, start from C3a's `--gon conv` plan (`results/C3a/shard_plan.md`): its
depth-12 / depth-18 sub-leaves have closed.

## Inputs

- **Generator.** `cloud/es7-2026-10-19/results/C3b/tools/gen_c3b.py`, commit `3aac870`,
  branch es7-cloud. Pure Python 3, deterministic.
  - Command: `python3 gen_c3b.py 11 7 -o c3b_m11k7.cnf --map c3b_m11k7.json`
  - Output: `p cnf 135663 4149465`, sha256
    `2d1df312934939e4bc0d6ec6b862ff3b911e7112a9c6c5619b8abd3ec8bc4ee3`
- **march_cu.** https://github.com/marijnheule/CnC at git `705b60c`, with two build changes:
  - CFLAGS `-O3 -fno-strict-aliasing -Wall -DNDEBUG -fcommon`;
  - in `march_cu/microsat.c`, `S->mem_max = 400000000;`. Without it, march_cu hits a
    use-after-free on realloc and segfaults on any CNF with m ≥ 9.
- **Cubes.**
  - Command: `march_cu c3b_m11k7.cnf -d 6 -o cubes_d6.icnf`
  - Time: 35.6 min on one core.
  - Result: 64 cubes, 0 refuted leaves, sha256
    `06d9384438c55a7c729bbd7012ec277b4406bdd7071c8f8052acd15139e8445e`, file
    `logs/cubes_d6.icnf`.
  - `tools/coverage.py` reports a binary tree with weight exactly 1.
- **What the cubes split on.** Every cube literal is a σ bit (variables 3654..3663 =
  s_1..s_10; s_0 = 3653 is fixed false). So the natural complete split is the **1,024
  σ-patterns**: fix all of s_1..s_10, weight 2^-10 each.

## Per-cube times measured (4-core VM, 3–4 solver processes at once)

| cube | depth | limit | result | conflicts |
|---|---|---|---|---|
| d6 cubes 0, 1, 2, 3 | 6 | 300 s (with LRAT) | UNKNOWN | – |
| σ-leaf 0 (`logs/leaves_d10.icnf` line 1) | 10 | 2,400 s | UNKNOWN | 1,280,633 |
| σ-leaf 1 | 10 | 2,400 s | UNKNOWN | 1,205,891 |
| σ-leaf 2 | 10 | 1,800 s | UNKNOWN | 923,946 |
| σ-leaf 3 | 10 | 1,800 s | UNKNOWN | 986,494 |
| σ-leaf 4 | 10 | 1,800 s | UNKNOWN | 922,700 |
| march -d 5 inside σ-leaf 0 | – | aborted after 44 min at 16/64 | about 5 min per node | – |

The σ-leaves in `logs/leaves_d10.icnf` extend d6 cubes 0, 21, 42, 63, 10 and 53 with
s-values from `random.Random(2026)`.

**Cost.** Not estimable from this data. If the 5 timed σ-leaves are typical, plain CaDiCaL
needs more than about 1,024 × 2,000 s ≈ **570 core-hours** in total. That is an extrapolated
lower bound only: none of the timed leaves finished, so the true cost could be much higher. results/E2 likewise closed nothing on symcnf in
8.8 solver-hours.

## Recipe, if someone wants to push this encoding anyway

1. Regenerate the CNF and check its sha256.
2. Write the 1,024 σ-leaves deterministically. Leaf b, for b = 0..1023, has s_{t+1} = bit t
   of b, i.e. units `±(3654+t)` for t = 0..9.
3. Shard leaf b to machine b mod N.
4. Sub-cube each leaf with the patched march_cu: `march_cu leaf_b.cnf -d 8`. On this VM a
   lookahead node takes about 30–60 s.
5. Solve each sub-cube with `tools/cnc_run.py`: CaDiCaL `--lrat --binary=false`, then
   lrat-check (E2 patch) and cake_lpr. A sub-cube is closed only if both checkers accept.
6. Check coverage with `tools/coverage.py` per leaf.
7. Exploit the mirror before spending large compute. The mirror is not broken, so σ-patterns
   probably pair up and halve the work. This is untested here.

Any SAT leaf must be decoded with `tools/modelcheck.py`, committed at once, and realization
attempted (`tools/realizer/`).
