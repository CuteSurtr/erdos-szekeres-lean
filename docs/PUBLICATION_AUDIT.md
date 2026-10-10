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

Publication must not be described as privacy-clean merely because no secret
token was found: the historical local-path finding above requires an explicit
disposition before changing repository visibility.
