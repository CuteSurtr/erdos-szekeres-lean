# Task J2: PatternBoost-style search for 33 points with no convex 7-gon

**Result: no counterexample.** No run produced a 33-point set in general position with zero
convex 7-gons. Every arm bottomed out at exactly one convex 7-gon, the same level as the
273 near-miss seeds it started from. The best sets (one 7-gon each) are listed in section 6
and were recounted exactly by three methods. Learning did not help at equal CPU (section 5).

## 1. Where and what ran

- Cloud VM, 4 vCPU, 15 GB RAM, no GPU (`env.txt`). Wall time 00:35–04:35 UTC, 20 Oct 2026.
- PyTorch 2.14.1 from PyPI, CPU only. download.pytorch.org is blocked by the proxy, so the
  CUDA build was installed and run on the CPU.
- Exact tools: `tools/trackA/gen_core.h` and `gen.c`, and `results/D/src/triple_check.py`.
  Calibration: AlphaEvolve's set has c7 = 1 (cups/caps and DFS agree: c3..c7 = 5456, 24758,
  47945, 32055, 1). All 273 `nearfull_p2*` sets have c7 = 1 and all 8,537 `distinct_K7*` sets
  have c7 = 0, recounted with `src/ls33.c` (0 iterations).
- `src/ls33.c` is the local search. It is a batch version of the trackA annealer: exact
  `__int128` orientations, the exact DP count of convex k-gons, and trackA's multi-scale moves.
  The energy is log(1 + c7) under Metropolis with T 0.3 → 0.02, 800 iterations per start
  (about 0.25 s). Ties in c7 are broken by fewer convex 6-gons when choosing the best visited
  state. Every output set is checked again from scratch for general position and a recount.

## 2. Encoding

Flat grids destroy these sets. Extent over minimum distance is 2^10 to 2^27. Min–max
quantisation flips 10–25% of orientation signs, and rank coordinates flip about 17%
(`src/ana.py`).

`src/enc.py` therefore uses a multi-scale, x-sorted gap code:
- The set is rotated by a random angle (and reflected with probability 1/2), scaled to
  x-extent 2^24 and sorted by x.
- Each consecutive gap (dx, dy) becomes 4 tokens: the integer part of log2 dx; its fractional
  part in 256 bins; the sign of dy with the integer part of log2 |dy|; the fractional bin.
- A sequence is BOS_n followed by 4(n−1) tokens: 129 tokens for 33 points. The vocabulary
  has 351 tokens.
- Random rotation is the data augmentation: it is invariant for the order type up to
  reflection, which preserves the number of convex k-gons.

Fidelity matters a great deal. Encoding then decoding the near-miss seeds (with random
jitter inside each cell) keeps c7 ≤ 1 for this share of the 120 sets tested:

| steps per octave | 8 | 16 | 32 | 64 | 128 | 256 (used) |
|---|---|---|---|---|---|---|
| sets with c7 ≤ 1 | about 0 | 7 | 21 | 37 | 52 | 61–74 |

At 8 steps per octave the median c7 after decoding was about 4,000.

## 3. Model and loop

- **Model:** a GPT-style causal transformer with 4 layers, d = 128, 4 heads, pre-norm and
  about 0.90M parameters. Logits are masked by the token grammar (exponent, mantissa,
  signed exponent, mantissa). Training uses AdamW at lr 3e-4 with batch size 64.
- **Training mix:** each batch is 70% 33-point pool sets and 30% 32-point heptagon-free sets
  (the 8,537 `distinct_K7*` sets), all re-encoded with a fresh random rotation.
- **Pool:** the 33-point sets with c7 ≤ 1, deduplicated by order type (`gen canon`, up to
  reflection) and ranked by (c7, c6); the top 2,000 are used for training. It starts with
  the 273 near-miss seeds.
- **v1 (unconditional, `pb.py`):** 2,000 initial training steps (13 min on 2 cores), then
  400 fine-tuning steps per generation. Each generation samples 1,000 sequences from BOS_33
  at temperature 1, decodes them and runs ls33 for 800 iterations; results are added to the
  pool. This ran on 2 cores alongside two 1-core baselines.
- **v2 (prefix-conditioned, `PREFIX=1`):** the same loop, but 90% of samples keep the first
  27–31 of the 32 gaps of a random pool set (re-encoded with a random rotation) and the
  model completes the rest. This resamples the rightmost 1–5 points in the rotated frame.
  The other 10% are unconditional. The transformer starts from v1's weights.
- **Ablation for v2 (`MODEL=unigram`):** the identical loop with the transformer replaced by
  a position-wise unigram model. It uses token frequencies per position with add-one
  smoothing, re-estimated each generation from 20,000 encodings of the same training mix.
  So everything except context is the same. Each v2 arm had 2 cores for 2.1 h.
- **Logs:** per-generation statistics are in `logs/*/generations.jsonl`, the best sets in
  `logs/*/best.txt`, and the 200 best pool sets per arm in `logs/*/pool_top.txt`.

## 4. Per-generation statistics

`E7` is the exact number of convex 7-gons. "decoded" means before local search. "OT" means
order types up to reflection.

### v1: unconditional generation (transformer) vs baselines

| gen | CPU s | decoded E7 median | E7 after LS: min / q10 / median | E7<=1 | loss |
|---|---|---|---|---|---|
| 0 | 1995 | 54252 | 169 / 839 / 1521 | 0 | 4.163 |
| 1 | 2803 | 49274 | 95 / 838 / 1518 | 0 | 4.067 |
| 2 | 3603 | 49338 | 218 / 772 / 1542 | 0 | 4.045 |
| 3 | 4386 | 48132 | 206 / 873 / 1498 | 0 | 4.031 |

Equal-CPU comparison at 4386 CPU s (v1 total):

| arm | starts | E7 min | E7<=1 found | distinct order types with E7<=1 |
|---|---|---|---|---|
| PatternBoost v1 | 4000 | 95 | 0 | 0 |
| random starts (at 2955 CPU s) | 12200 | 58 | 0 | 0 |
| seeds + encoding noise (no model) (at 2952 CPU s) | 13200 | 1 | 5624 | 5597 |

### v2_gpt

| gen | CPU s | decoded E7 median | decoded E7<=1 | E7 min / median after LS | E7 hist 0/1/2/3 | E7<=1 (distinct OT) | pool new OT | best c6 (E7=1) |
|---|---|---|---|---|---|---|---|---|
| 0 | 572 | 4646 | 41 | 1 / 1192 | 0/57/12/3 | 57 (57) | 57 | 12420 |
| 1 | 1147 | 3866 | 40 | 1 / 1140 | 0/52/13/0 | 52 (52) | 109 | 12275 |
| 2 | 1725 | 3957 | 21 | 1 / 1178 | 0/37/1/0 | 37 (37) | 146 | 12275 |
| 3 | 2313 | 3904 | 33 | 1 / 1194 | 0/45/3/0 | 45 (45) | 191 | 11994 |
| 4 | 2915 | 4371 | 32 | 1 / 1232 | 0/43/6/1 | 43 (43) | 234 | 10941 |
| 5 | 3486 | 3296 | 40 | 1 / 1154 | 0/68/10/0 | 68 (68) | 302 | 10941 |
| 6 | 4062 | 3764 | 19 | 1 / 1176 | 0/37/7/3 | 37 (37) | 339 | 10941 |
| 7 | 4636 | 3880 | 26 | 1 / 1142 | 0/34/5/1 | 34 (34) | 373 | 10941 |
| 8 | 5210 | 3249 | 28 | 1 / 1154 | 0/44/3/4 | 44 (44) | 417 | 10529 |
| 9 | 5790 | 2378 | 42 | 1 / 1045 | 0/69/10/3 | 69 (69) | 485 | 10272 |
| 10 | 6369 | 2938 | 37 | 1 / 1054 | 0/64/6/3 | 64 (64) | 549 | 10272 |
| 11 | 6957 | 3678 | 32 | 1 / 1148 | 0/47/6/1 | 47 (47) | 596 | 10272 |
| 12 | 7550 | 3831 | 41 | 1 / 1136 | 0/52/8/2 | 52 (52) | 648 | 10272 |
| 13 | 8136 | 3500 | 43 | 1 / 1120 | 0/64/10/2 | 64 (64) | 712 | 10272 |
| 14 | 8733 | 3087 | 42 | 1 / 1118 | 0/70/10/4 | 70 (70) | 782 | 10272 |
| 15 | 9320 | 2476 | 43 | 1 / 1074 | 0/61/9/1 | 61 (61) | 842 | 10272 |
| 16 | 9900 | 2752 | 32 | 1 / 1124 | 0/46/12/2 | 46 (46) | 888 | 10272 |
| 17 | 10470 | 2638 | 59 | 1 / 1047 | 0/82/9/2 | 82 (82) | 970 | 9878 |
| 18 | 11058 | 3238 | 34 | 1 / 1168 | 0/50/9/1 | 50 (50) | 1019 | 9878 |

### v2_unigram

| gen | CPU s | decoded E7 median | decoded E7<=1 | E7 min / median after LS | E7 hist 0/1/2/3 | E7<=1 (distinct OT) | pool new OT | best c6 (E7=1) |
|---|---|---|---|---|---|---|---|---|
| 0 | 242 | 6642 | 6 | 1 / 1280 | 0/11/1/0 | 11 (11) | 11 | 12420 |
| 1 | 482 | 6602 | 15 | 1 / 1298 | 0/19/3/0 | 19 (19) | 30 | 10753 |
| 2 | 720 | 5251 | 15 | 1 / 1260 | 0/19/2/1 | 19 (19) | 49 | 10753 |
| 3 | 961 | 5915 | 15 | 1 / 1284 | 0/21/3/1 | 21 (21) | 70 | 10753 |
| 4 | 1198 | 5538 | 19 | 1 / 1242 | 0/27/3/0 | 27 (27) | 96 | 10753 |
| 5 | 1440 | 5197 | 10 | 1 / 1272 | 0/20/1/1 | 20 (20) | 116 | 10753 |
| 6 | 1686 | 6468 | 9 | 1 / 1332 | 0/16/1/1 | 16 (16) | 132 | 9332 |
| 7 | 1932 | 6133 | 10 | 1 / 1307 | 0/14/0/0 | 14 (14) | 146 | 9332 |
| 8 | 2174 | 5256 | 28 | 1 / 1208 | 0/34/10/3 | 34 (34) | 180 | 9332 |
| 9 | 2415 | 7290 | 8 | 1 / 1332 | 0/13/2/0 | 13 (13) | 193 | 9332 |
| 10 | 2656 | 4175 | 18 | 1 / 1176 | 0/33/2/2 | 33 (33) | 226 | 9332 |
| 11 | 2895 | 6580 | 10 | 1 / 1312 | 0/17/2/4 | 17 (17) | 243 | 9332 |
| 12 | 3135 | 6215 | 15 | 1 / 1298 | 0/21/5/0 | 21 (21) | 264 | 9332 |
| 13 | 3377 | 6322 | 2 | 1 / 1335 | 0/5/1/1 | 5 (5) | 269 | 9332 |
| 14 | 3616 | 6045 | 11 | 1 / 1268 | 0/16/5/0 | 16 (16) | 285 | 9332 |
| 15 | 3859 | 5104 | 13 | 1 / 1248 | 0/21/2/5 | 21 (21) | 306 | 9332 |
| 16 | 4101 | 5998 | 8 | 1 / 1266 | 0/15/4/1 | 15 (15) | 320 | 9332 |
| 17 | 4344 | 5476 | 14 | 1 / 1268 | 0/20/5/1 | 20 (20) | 340 | 9332 |
| 18 | 4585 | 5908 | 18 | 1 / 1271 | 0/30/1/0 | 30 (30) | 370 | 9332 |
| 19 | 4827 | 5503 | 16 | 1 / 1299 | 0/22/4/1 | 22 (22) | 392 | 9332 |
| 20 | 5069 | 5038 | 20 | 1 / 1230 | 0/21/3/0 | 21 (21) | 413 | 9332 |
| 21 | 5314 | 4384 | 15 | 1 / 1144 | 0/23/1/1 | 23 (23) | 436 | 9332 |
| 22 | 5557 | 5454 | 13 | 1 / 1264 | 0/24/10/0 | 24 (24) | 460 | 9332 |
| 23 | 5800 | 5806 | 10 | 1 / 1246 | 0/12/4/0 | 12 (12) | 472 | 9332 |
| 24 | 6046 | 7084 | 22 | 1 / 1223 | 0/28/1/0 | 28 (28) | 500 | 9332 |
| 25 | 6290 | 5043 | 19 | 1 / 1272 | 0/24/3/1 | 24 (24) | 524 | 9332 |
| 26 | 6531 | 4266 | 16 | 1 / 1170 | 0/24/5/1 | 24 (24) | 548 | 9332 |
| 27 | 6770 | 6624 | 5 | 1 / 1316 | 0/11/1/1 | 11 (11) | 559 | 9332 |
| 28 | 7011 | 7362 | 9 | 1 / 1292 | 0/11/2/0 | 11 (11) | 570 | 9332 |
| 29 | 7248 | 4420 | 25 | 1 / 1190 | 0/38/6/1 | 38 (38) | 608 | 9332 |
| 30 | 7490 | 6980 | 8 | 1 / 1333 | 0/12/1/1 | 12 (12) | 620 | 9332 |
| 31 | 7734 | 5280 | 12 | 1 / 1258 | 0/26/1/2 | 26 (26) | 646 | 8787 |

Equal-CPU comparison at 7734 CPU s:

| arm | generations | samples | E7<=1 per 1000 samples | new order types with E7<=1 in pool | best c6 among E7=1 | E7=0 |
|---|---|---|---|---|---|---|
| v2_gpt | 13 | 13000 | 49.9 | 648 | 10272 | 0 |
| v2_unigram | 32 | 32000 | 20.2 | 646 | 8787 | 0 |

Full runs:

| arm | CPU s | generations | samples | c7 ≤ 1 after LS | new OT in pool | best (c7, c6) | c7 = 0 |
|---|---|---|---|---|---|---|---|
| v2_gpt | 11,058 | 19 | 19,000 | 1,022 | 1,019 | (1, 9,878) | 0 |
| v2_unigram | 7,734 | 32 | 32,000 | 648 | 646 | (1, 8,787) | 0 |

On CPU: the gpt arm's torch threads used more than the nominal 2 cores, so it consumed more
CPU in the same wall time. The comparisons above are made at equal CPU.

Diversity: within every generation, all sets with c7 ≤ 1 had distinct order types. Across
the run, 99.7% of them were new relative to the 273 seeds.

## 5. Did learning help?

**No, not at equal CPU.**

- **v1, unconditional generation:** the model reaches a loss of about 4.0 nats per token,
  close to what you get from learning the exponents while treating the 8-bit mantissas as
  noise. Its samples decode to a median c7 of about 50,000. After local search they match
  uniform random starts: median c7 about 1,500 for both, best 95 against random's 58. No
  sample reached c7 ≤ 1, so the pool never changed and the loop could not improve.
- **v2, transformer against the no-context unigram ablation:** the transformer is
  context-aware, and per sample it gives about 2.5× more c7 ≤ 1 completions (49.9 against
  20.2 per 1,000). It also gives a lower decoded median (about 3,500 against 5,500). So it
  did learn something about where the last points of a near-miss set go. But training and
  sampling cost more than double the CPU per generation. At equal CPU (7,734 s) the two
  arms found the same number of new c7 = 1 order types (648 against 646). The cheaper
  ablation reached a lower c6 (8,787 against 10,272).
- **The simplest no-learning control beat both.** It takes a random training set, applies
  the same encode/decode noise to all 33 points, then runs the same ls33. In about 2,950
  CPU-s it found 5,597 distinct c7 = 1 order types, roughly 10 times more per CPU-s than
  either v2 arm. Its best set had c6 = 10,237.
- **Uniform random starts plus 800-iteration ls33** never got below c7 = 58 in 12,200 starts.
- **Bottom line:** every method that started from the seed distribution moved around the
  same c7 = 1 plateau. None crossed to c7 = 0. The learned model added nothing that a cheap
  perturbation of the training data did not already give. This matches the risk noted in
  `plan/es7_methods.md` §6: the objective is flat and the target is a needle event.
- **Caveats:**
  - Short runs: about 2 h per arm on 2 cores.
  - A small model, 0.9M parameters.
  - Local search fixed at 800 iterations.
  - Ranking c7 = 1 ties by fewer convex 6-gons is a heuristic; nothing shows that low c6
    leads toward c7 = 0.

## 6. Best sets (all c7 = 1; no counterexample)

The files are in `best/`, one "x y" per line, as integers with |c| < 2^26. Each was
re-checked exactly by `results/D/src/triple_check.py`, using three methods: cups and caps,
a triangle-criterion DFS, and `cgon`'s angular DP. Each is in general position (all 5,456
triples nonzero), and all three counters agree.

| file | c3 | c4 | c5 | c6 | c7 | c8 |
|---|---|---|---|---|---|---|
| `best/v2_unigram.txt` | 5456 | 19798 | 24265 | 8787 | 1 | 0 |
| `best/v2_gpt.txt` | 5456 | 19778 | 25652 | 9878 | 1 | 0 |
| `best/v1_seeds_noise.txt` | 5456 | 19470 | 25629 | 10237 | 1 | 0 |

For comparison, the lowest c6 among the 273 seeds is 12,420. AlphaEvolve's set has
c6 = 32,055.

No `ZERO_CANDIDATES.txt` file was ever written by any arm. Those files are where any
c7 = 0 state found by ls33 would be logged.

## 7. Files and reproduction

- `src/ls33.c`: batch exact local search. Build it with
  `cc -O3 -I../../../tools/trackA -o ls33 src/ls33.c -lm`.
  `gen` (from `tools/trackA/gen.c`) is used for the canonical order type.
- `src/enc.py` (encoding), `src/pb.py` (loop, v1 and v2), `src/baseline.py` (v1 baselines),
  `src/common.py`, `src/summarize.py` (writes `summary.json` and the tables above),
  `src/launch.sh` (v1) and `src/launch_v2.sh` (v2, started with
  `INIT=<v1 model.pt> sh src/launch_v2.sh 2.1`), `src/snapshot.sh`, and `src/ana.py` and
  `src/ana2.py` (the encoding fidelity checks).
- `logs/`: snapshots of the run logs. `runs/` (the live outputs and model weights) is not
  committed.
- **Incident:** a `git pull --rebase` replaced the then-committed live log files under the
  running v1 processes. The data was recovered from `/proc/<pid>/fd`; that is
  `snapshot.sh`'s method. From then on, `runs/` was untracked.
- **v1 stopping point:** v1 was stopped after 4 generations (about 4,400 CPU-s) because its
  failure mode was already clear: the pool never changed. Its two baselines were stopped at
  about 2,950 CPU-s each.
