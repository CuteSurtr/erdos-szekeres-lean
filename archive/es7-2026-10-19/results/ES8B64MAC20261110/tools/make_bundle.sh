#!/bin/sh
# Build the transfer bundle of the Mac share of the budget-64 search (ES8B64MAC20261110), on the Mac.
#   sh make_bundle.sh MACDIR NAME IMPORT_SCRIPT
# Writes MACDIR/NAME/ and MACDIR/NAME.tar (no compression: the trees are gzip already):
#   runs/ctx-<k>-b64.result.json and .json.gz, copied unchanged, for every context whose result is closed with
#   replay ok;  SHA256SUMS of those files;  contexts.txt (one ctx per line);  campaign.log (the Mac driver log);
#   import_mac_runs.py.  Then the sha256 of the tar.  Refuses if any WITNESS file exists or a job is still running.
set -eu
M=$1; N=$2; IMP=$3
B=$M/$N
[ ! -e "$B" ] && [ ! -e "$B.tar" ] || { echo "refused: $B or $B.tar exists" >&2; exit 1; }
if ls "$M/runs" | grep -q WITNESS || [ -e "$M/campaign/WITNESS-ALERT.txt" ]; then echo "refused: WITNESS file" >&2; exit 1; fi
if pgrep -f 'run_context.py' > /dev/null; then echo "refused: run_context.py still running" >&2; exit 1; fi
mkdir -p "$B/runs"
python3 -I - "$M/runs" "$B/contexts.txt" <<'EOF'
import json, os, sys
runs, out = sys.argv[1], sys.argv[2]
ks = []
for n in sorted(os.listdir(runs)):
    if n.endswith('-b64.result.json'):
        r = json.load(open(os.path.join(runs, n)))
        k = int(n[4:n.index('-b64')])
        if r.get('status') == 'closed' and (r.get('replay') or {}).get('ok') is True and r.get('budget') == 64 \
                and os.path.isfile(os.path.join(runs, 'ctx-%d-b64.json.gz' % k)):
            ks.append(k)
        else:
            sys.exit('refused: ctx %d is not closed with replay ok, or its tree is missing' % k)
open(out, 'w').write(''.join('%d\n' % k for k in sorted(ks)))
print('contexts', len(ks))
EOF
while read -r k; do cp -p "$M/runs/ctx-$k-b64.result.json" "$M/runs/ctx-$k-b64.json.gz" "$B/runs/"; done < "$B/contexts.txt"
(cd "$B" && shasum -a 256 runs/ctx-* > SHA256SUMS)
cp "$M/campaign/campaign.log" "$B/campaign.log"
cp "$IMP" "$B/import_mac_runs.py"
echo "files $(ls "$B/runs" | wc -l | tr -d ' ') (two per context)"
(cd "$M" && tar cf "$N.tar" "$N")
shasum -a 256 "$B.tar"
