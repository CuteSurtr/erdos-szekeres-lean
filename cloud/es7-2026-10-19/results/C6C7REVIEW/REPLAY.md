# Certificate replay — 4 November 2026

**Certificate (both checkers, replayed now):** all eight selected proofs were accepted by both `lrat-check` and `cake_lpr`, against freshly generated formulas. This covers three substantial sixfold cubes per encoder and both complete sevenfold proofs. The other 26 sixfold proofs per encoder were not replayed in this review; their verdicts remain historical. The sevenfold 64-point lower-bound examples were not independently revalidated in this pass.

**Exact computation:** all compressed and decompressed proof hashes matched the historical manifests. The five generated variants below matched their recorded hashes; the extended B generator also reproduced the sevenfold B formula byte for byte.

| Formula | SHA-256 |
|---|---|
| `A6.cnf` | `542c8a3a2c4484a7d60b5fdb8efc0f3506d782031fc4b4625604b360211ad51e` |
| `B6.cnf` | `479e31a9e8d58d752c86b9abf02fb799c10615a7e61a88f132c49734674f37fc` |
| `A7.cnf` | `1a7c0e706f2a7fb52b109ae20ca37d49c74940e01c1227fe152b46d742d5997f` |
| `A7_H1.cnf` | `fa297b5bd6608d29369fd56f8cab20d6d17ad9d335253352541a42e4c669fc49` |
| `B7.cnf` | `b4d290176cb675c61ecbcf70380cc520aabf093d00e2572328a0975ae2d296e2` |

**Exact computation:** both 32-cube covers were rebuilt and accepted by the original `verify_cover.py` under `python3 -I`. `strict_cover.py` independently checked each base clause count and literal bounds, each unchanged body, every appended unit, and the complete set of masks. Its missing-cube, body, unit and header mutants were rejected even under `python3 -I -O`.

**Sampling:** the sample was fixed before checking. Three of the twelve transitive, nontrivial phase-order cubes were selected uniformly without replacement for each encoder; the quick contradictory-order cubes were deliberately outside this sampling population. Python random seed: `1319527528443935447`.

| Proof | Raw LRAT SHA-256 | Fresh verdicts |
|---|---|---|
| `A6_c11111` | `230df1f314478f3543745a102e82341f0efef33c4e3cec5ce445e5d4a8664799` | both accepted |
| `A6_c11000` | `5d3abe7a99a469d783315298443aba72292683dcdd8c693dd5ea87f438b11b82` | both accepted |
| `A6_c11110` | `16fbfe9c1c7da82bdf4f63d2742f22a7bfaf776eb89c3c599f27dd5889730cc4` | both accepted |
| `B6_c11001` | `88dcf4f58f01f90936f158d6cba04c5c337f3ee86ff3b4768714f5a014adf08b` | both accepted |
| `B6_c11000` | `407e30d112a73b30a31f3d1c7c2165295b3b38b265c6231ee8e46aa385f57352` | both accepted |
| `B6_c11111` | `0a988c3f26bbad6041877c6a76b4a040b5c96d834eb56aacd4be97e65d3010bb` | both accepted |
| `A7` | `c750a805a7a3dbdb4ba445c16fb75051a9fac623a3ddf93a5d864defe41039b2` | both accepted |
| `B7` | `75f9bd350186724a85e949b05315369d88ef887c9953e0048810b67e8172550e` | both accepted |

Compressed hashes, cube CNF hashes, byte sizes, source hashes, complete command arguments, exit codes, durations and memory samples are in [`replay.json`](replay.json). Individual checker outputs are in `logs/lrat_*.log` and `logs/cake_*.log`. Only one checker ran at a time; CakeML heap and stack flags were both 4000. All eight checker pairs completed without a checker failure.

**Exact computation:** semantic comparison of the generated non-chain clauses found zero differences in 23,852 sixfold and 185,549 sevenfold orbit-pattern cases. This compares semantics using the existing shared translation harness; it is not evidence of independent mathematical assumptions. See `logs/compare_A6_B6.log` and `logs/compare_A7_B7.log`.

Reproduction from the results directory (`ARCHIVES` is the historical proof-archive root; `ARCHIVE` is a separate durable destination):

```sh
python3 -I C6C7REVIEW/replay.py --seed 1319527528443935447 \
  --scratch "$SCRATCH" --archives "$ARCHIVES" --archive "$ARCHIVE" --bin "$BIN"
python3 -I C6C7REVIEW/strict_cover.py "$SCRATCH/A6.cnf" "$SCRATCH/A6.cnf.json" "$SCRATCH/A6_cubes"
python3 -I C6C7REVIEW/strict_cover.py "$SCRATCH/B6.cnf" "$SCRATCH/B6.cnf.json" "$SCRATCH/B6_cubes"
python3 -I -O C6C7REVIEW/strict_cover.py --self-test
python3 -I C6UPPER/encb/compare_ab2.py "$SCRATCH/A6.cnf" "$SCRATCH/B6.cnf"
python3 -I C6UPPER/encb/compare_ab2.py "$SCRATCH/A7.cnf" "$SCRATCH/B7.cnf"
```

The recorded execution resumed after a manifest footer caused the initial parser to stop before any proof checker ran. The reader was restricted to actual cube records; regenerated CNF hashes were checked again before resuming. `--resume` preserves the recorded selection and completed checks. For a full replay use the command above without `--resume`.

**Evidence only (resource observation):** peak sampled total active+wired+compressed memory during this lane was 27.478 GB, including concurrent experiments. Sampling cannot establish a continuous-time peak. The lane used one compute process at a time and terminated all its child processes.

**Archive:** regenerated bases and all rebuilt cube CNFs were compressed under `es8-c6c7-review-2026-11-04`, with raw/compressed SHA-256 and a verified decompression round trip for every file. Replayed proofs remain in their original durable archives; scratch decompressions were removed only after successful checking.

| Binary | SHA-256 |
|---|---|
| `cadical` | `e12ecc8ce8a489394a2b7411e3fa264f037e4ceb2e615bab534158e19d04ac01` |
| `lrat-check` | `f20462121defbc631f34850e06d5c0428ea4fecc4c890e6b755fd8e9bf9f534d` |
| `cake_lpr` | `2fee767af4478ed817f8bdf6feea5866e5e59f1f67c2a4477e98ee961612881d` |

**Written proof (reviewed, not refereed):** the relation of these Boolean certificates to point configurations still depends on the layer, perturbation, angular, nesting, chain and reflection arguments in [`SOUNDNESS.md`](SOUNDNESS.md). No Lean proof was rerun or added.
