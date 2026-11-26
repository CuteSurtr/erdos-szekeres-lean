#!/bin/bash
# upload_trees.sh (26 Nov 2026, owner-approved wrap-up): upload the inputs that regenerate the ES(8) <= 302 Lean chunk
# sources (the budget-69 and budget-67 trees, the residual-slice runs and inputs, the context manifests) to a release of
# the owner's PRIVATE archive repository. Read-only on the sources. Each item becomes one POSIX tar (sorted names),
# split into 1900 MiB parts (GitHub's limit is 2 GiB per file); SHA256SUMS lists every part and every whole tar.
# Verification: GitHub's own sha256 digest of each uploaded asset must equal the local one (verify.tsv).
# The local originals are not touched; the parts here are temporary copies. Log: run.log.
set -u -o pipefail
U=/home/jay/research/data/upload-trees-20261126; cd $U
REPO=CuteSurtr/erdos-szekeres-lean-private-archive-2026-10-10; TAG=trees-302-20261126
log() { echo "$(date '+%F %T') $*" >> $U/run.log; }
D=/home/jay/research/data
items=("b69zs54|$D/bal186-20261119/zrow|b69zs54"
       "b67|$D/bal186-20261119/zrow|b67"
       "es308-runs-inputs|$D/es308-20261114|runs inputs"
       "ctx-manifests|$D|fv302-20261124/export/ctx formalize-20261122/res-slices-fv/export")
log "start; tar $(tar --version | head -1); gh $(gh --version | head -1)"
for it in "${items[@]}"; do
  IFS='|' read -r name base paths <<< "$it"
  [ -e "$U/$name.done" ] && continue
  rm -f $U/$name.tar.part* $U/$name.list
  tar -C "$base" --sort=name --format=posix -cvf - $paths 2> $U/$name.list \
    | tee >(sha256sum | sed "s/-\$/$name.tar/" > $U/$name.tar.sha256) \
    | split -b 1900M -d -a 3 - $U/$name.tar.part || { log "TAR FAILED $name"; exit 1; }
  sleep 2; touch $U/$name.done; log "packed $name: $(ls $U/$name.tar.part* | wc -l) parts, $(cat $U/$name.tar.part* | wc -c) bytes"
done
( for f in $U/*.tar.part*; do sha256sum "$f" | sed "s#  $U/#  #"; done; cat $U/*.tar.sha256 ) > $U/SHA256SUMS
log "SHA256SUMS: $(wc -l < $U/SHA256SUMS) lines"
gh release view $TAG --repo $REPO >/dev/null 2>&1 || gh release create $TAG --repo $REPO --title "ES(8) <= 302 regeneration inputs (26 Nov 2026)" --notes-file $U/NOTES.md || { log "RELEASE CREATE FAILED"; exit 1; }
gh release upload $TAG --repo $REPO --clobber $U/SHA256SUMS $U/NOTES.md $U/*.list >> $U/run.log 2>&1 || log "small files upload failed (will retry at the end)"
have=$(gh api repos/$REPO/releases/tags/$TAG --jq '.assets[].name' 2>/dev/null)
for f in $U/*.tar.part*; do
  n=$(basename $f); grep -qx "$n" <<< "$have" && continue
  for try in 1 2 3; do
    t0=$(date +%s); if gh release upload $TAG --repo $REPO --clobber "$f" >> $U/run.log 2>&1; then
      t=$(( $(date +%s) - t0 )); log "uploaded $n $(stat -c %s $f) bytes in ${t}s"; break; fi
    log "upload failed $n (try $try)"; sleep 60
  done
done
gh release upload $TAG --repo $REPO --clobber $U/SHA256SUMS $U/NOTES.md $U/*.list >> $U/run.log 2>&1
gh api repos/$REPO/releases/tags/$TAG --paginate --jq '.assets[] | [.name, .size, (.digest // "none")] | @tsv' > $U/remote.tsv
python3 -I - <<'PY' > $U/verify.tsv; rc=$?
import os
U = "/home/jay/research/data/upload-trees-20261126"
loc = {}
for l in open(U + "/SHA256SUMS"):
    h, n = l.split(None, 1); loc[n.strip()] = h
rem = {}
for l in open(U + "/remote.tsv"):
    n, s, d = l.rstrip("\n").split("\t"); rem[n] = (int(s), d)
bad = 0
for n, h in sorted(loc.items()):
    if not n.endswith(tuple(f".part{i:03d}" for i in range(1000))): continue
    s, d = rem.get(n, (None, None)); ok = d == "sha256:" + h and s == os.path.getsize(f"{U}/{n}")
    bad += not ok; print(f"{n}\t{h}\t{s}\t{d}\t{'OK' if ok else 'BAD'}")
print(f"# parts {sum(1 for n in loc if '.part' in n)}, bad {bad}")
raise SystemExit(1 if bad else 0)
PY
log "verify rc=$rc ($(grep -c 'OK$' $U/verify.tsv) OK, $(grep -c 'BAD$' $U/verify.tsv) BAD)"
[ $rc = 0 ] && log "DONE" || log "VERIFY FAILED"
