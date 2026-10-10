# Publication preparation audit — 10 October 2026

The review covered the repository at
`7b5a0abb99b1cdf0fb4b213b2d81f95015896b19`, before adding the public-release
license and mathematical exposition. This is a scoped inspection report,
not a guarantee that no undiscovered sensitive information exists.

## Git content and metadata

- All 41 commits on `main` were included, along with locally stored objects,
  two local Codex snapshot refs, and unreachable local objects.
- The inventory contained 1,621 objects, including 1,242 blobs. All blobs were
  scanned, covering approximately 216 MB of raw content.
- Historical archives were recursively decompressed: 81 gzip payloads and
  10 tar archives, approximately 1.37 GB of cumulative payload processing.
  The large JSON payload was checked both as raw text and for escaped strings.
  No unrecognized binary payload or unresolved scan-size exclusion remained.
- Pattern checks and review covered credentials, private keys, authenticated
  URLs, email addresses, local home paths, private-document indicators and
  high-entropy literals. No credential, private-key or authenticated-URL
  candidate was found. Commit email metadata consistently used GitHub noreply
  addresses.
- One local macOS username appeared in absolute filesystem paths in **34
  currently tracked files**, principally JSON proof/audit records and one
  saved axiom log. Those same blobs are reachable from the branch history.
  Three additional affected blobs were local and unreachable. The username
  is deliberately not reproduced in this report. This finding is separate
  from the absence of credentials.

Local inspection reports, downloaded logs, dependency checkouts and audit
scripts remain under ignored `.cache/`; they are not publication artifacts.
The unrelated untracked nested project and search scripts were excluded from
staging and this release.

## GitHub surfaces

The remote inventory contained one branch (`main`), no tags, pull requests,
issues, releases or Actions artifacts, and disabled wiki/discussion features.
All **41 Actions run log downloads** were inspected, including cancelled and
failed runs: 39 ZIP archives and two plain-text downloads. No credential or
local-user home-path finding was identified in those logs. Hosted runner
paths and public noreply identity metadata were present.

GitHub exposes Actions history when a private repository becomes public;
that is why it was included in this review. See
[GitHub's visibility documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility).
This review does not inspect secrets held outside the repository content or
other repositories on the account.

## Licensing and mathematical integrity

The release adds the Apache-2.0 license for original project contributions,
with the specific third-party exceptions and retained notices described in
[LICENSING.md](LICENSING.md). The supplied archive's reserved DOI status is
explicitly recorded. No upstream peer-review, endorsement or priority claim
is made.

The mathematical companion [math.md](../math.md) was checked against the
actual Lean statements, including their hypotheses, strict inequalities,
floors, state definitions, certificate semantics and final cardinality
composition. The current closed finite bound is **ES(8) ≤ 314**. The
proposition needed for the 313 residual route is explicitly marked unproved.
The writing pass does not modify Lean proof sources or certificate inputs.
A fresh maintained-library axiom audit passed for all **571** named
declarations, with only the standard Lean axioms allowed.

## Disposition: sanitized history

The repository owner selected removal of the historical paths before
publication. The local workspace prefix was replaced with
`/workspace/erdos-szekeres-lean` throughout the retained history. All dependent
SHA-256 records were updated, including the eight canonical JSON binding
fingerprints. These are path-normalized copies of the recorded checks, not
claims that the old timed builds were rerun.

The sanitized baseline is `6c04015cb033674ce948418aa2cb80eff75f2568`:

- All 42 commits up to the documentation/license preparation are retained;
  41 commit IDs change. Authors, committers, dates, messages and parent
  relationships are preserved.
- 34 directly affected current files and 19 dependent metadata/documentation
  files change. All Lean and Python sources, compressed archives, CNF/LRAT
  certificates and JSON numerical/Boolean data remain unchanged.
- Every stored object in the isolated rewritten repository was scanned;
  no original local-home/workspace prefix remains. All 61 replaced original
  blobs are absent from that repository, and strict Git integrity checks pass.
- Independent validation passes 18 checks, including all eight canonical
  fingerprints, 98 packaging files, the final 314 profile and source bindings,
  1,807 archived Lean sources with saved audits, and the current residual
  continuation's finite checks. The broader source scan inspected 3,423 Lean
  payloads, including archives, with no admission/native-evaluation matches.

A force-push by itself does not remove GitHub's cached old commit views.
The publication therefore uses a fresh repository containing only the sanitized
graph under the original `CuteSurtr/erdos-szekeres-lean` name. The original
repository is retained privately as
`erdos-szekeres-lean-private-archive-2026-10-10`; its old Actions logs and
unsanitized objects are not transferred. This preserves a private recovery
copy without making the old GitHub object history public. See
[GitHub's history-removal guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).

Earlier hosted-CI links in historical validation notes refer to the original
repository and may not resolve in the replacement. The stored source hashes,
proof archives and normalized audit records remain available for reproduction.
New hosted checks appear in the
[public repository's CI workflow](https://github.com/CuteSurtr/erdos-szekeres-lean/actions/workflows/ci.yml).
Future saved local audit output should likewise normalize machine-specific
paths before it is committed.
