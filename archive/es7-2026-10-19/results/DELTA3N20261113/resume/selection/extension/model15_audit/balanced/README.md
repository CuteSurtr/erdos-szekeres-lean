# Balanced coordinates — independent equivalence confirmed

This small authorized follow-up checks the 1000-grid coordinates in
`balance15-a/witness.json`, preserving the original discovery, model audit,
certificate and their frozen manifest unchanged. Started 14 November 2026,
05:51 KST; completed 05:52 KST.

**COMPUTED exact independent check:** all 455 signs, cap/polygon families,
all 32,768 terminal/ordinary selection outcomes and rooted weak witnesses
agree with the original. The minimum absolute determinant is **45**.
The **313-clause membership CNF is byte-for-byte identical** to the already
CERTIFIED file, so the existing retained proof applies unchanged. No new
cake replay was necessary. See [VERIFY_BALANCED.md](VERIFY_BALANCED.md).

The readable [coordinates](data/coordinates.json) and
[point file](data/coordinates.points) are frozen here with the identical
[membership CNF](data/membership.cnf) and full
[equivalence receipt](data/equivalence.json). They are suitable for the
parent's planned archiving and plotting within the verified scope.

One CPU, AS400 MiB, 18 CPU seconds and an external 20-second deadline.
Only this `balanced/` subdirectory was written. No parent finder or checker
was imported. The original independent geometry checker was reused read-only
with its hash checked. All **28 original audit files** still match their
historical manifest; the original canonical discovery is unchanged. This
subdirectory has its own `SHA256SUMS`. No job remains running or queued.

To reproduce, use the repository research Python and AS400/20-second limits
with `verify.py` in a fresh output directory; the script refuses to overwrite
its retained receipt. The original `../geometry.py` also accepts the frozen
coordinate JSON with a fresh receipt tag. No uniform-envelope computation,
new solver search, proof deletion, git mutation or external action occurred.
