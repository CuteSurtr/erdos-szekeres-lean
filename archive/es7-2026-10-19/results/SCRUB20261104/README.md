# SCRUB20261104: removal of sandbox paths and tool names from the results tree (4 November 2026)

**What changed.** 269 text files had strings left by the cloud sessions of October 2026. Only those strings changed;
every other byte is the same. Each file still parses: JSON, JSONL, Python (`ast`) and shell (`bash -n`).

**The strings replaced** (386 replacements):

| Count | Old string | New string |
|---|---|---|
| 352 | sandbox path prefixes of the cloud runs, under `/tmp/` or `/private/tmp/`, including the per-session project directory | `/sandbox/` |
| 28 | the prefix of the fallback branches that the cloud runs pushed to | `cloud-fallback/` |
| 4 | a tool-specific shell name in kernel OOM log lines | `sandbox-shell` |
| 2 | prose naming the session tool (`A2/README.md`, `Mii-3/README.md`) | "a managed remote cloud session", "Cloud container" |

- **Placeholders.** They are plain path and branch words, with no shell metacharacters, so no edited script gains a
  redirection.
- **Scripts no longer run as they are.** Their paths named directories of the cloud sandboxes, which no longer
  exist. They are kept as records.
- **The old fallback branches keep their original names on the remote.** `cloud-fallback/` here refers to them.

**Hash records were left unchanged.**
- Many results directories record SHA-256 values of their files: SHA256SUMS lists, `driver.diff` baselines and
  manifests. Some of those records are hashed elsewhere in turn.
- No record was edited. Each recorded value still describes the original bytes, which remain in git history: the
  parent of the commit that adds this directory.

**Files in this directory.**
- `scrub_map.tsv`: for every edited file, its SHA-256 before and after.
- `hash_citations.tsv`: one row per record that cites pre-scrub hashes of edited files, with the number of files it
  cites. 110 edited files are cited by full hash, all in 90 `driver.diff` records; the rest are 12-character prefix
  matches. To resolve any cited value, look it up in the `sha256_before` column of `scrub_map.tsv`.

**To verify a recorded hash,** check the file out at the parent commit, or compare against the `sha256_before`
column.

**Proof certificates are unaffected.** No CNF, LRAT proof, certificate witness, clause file or Lean file was edited.
Their hashes and checks stand. Only logs, scripts, leaf records and two READMEs changed.
