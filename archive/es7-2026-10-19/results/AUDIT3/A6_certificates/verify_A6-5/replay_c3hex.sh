#!/bin/bash
# A6-5 independent replay of the two c3hex certificates (no cake_lpr, per the audit rules).
# usage: replay_c3hex.sh ARCHIVE_C3HEX_DIR REPO_CLOUD_DIR BIN_DIR OUT_DIR SCRIPT_DIR
set -u
A=$1; C=$2; B=$3; O=$4; SD=$5
D=$O/data; G=$O/regen; mkdir -p "$D" "$G"
# recorded values, copied from results/WRITEUP/CERTIFICATES.md (c3-hex-15 / c3-hex-16 tables)
declare -A REC=(
 [c3_n15k6.cnf]=fc089011c5934f6bf63c581b5630712c83fc344e248325c10f71c62e9e99c811
 [c3_n15k6.lrat]=659a3db6b2f3e5d2cd1bbc3cda9abf5608213878828f52c1fea028e37d0aa859
 [c3_n16k6c.cnf]=15766b1e6e44f9b8f4dcf222ce8440b454d635521dfa0eda7b4759a92836690e
 [c3_n16k6c.lrat]=1c4c5e37a79d339e4c2bf0280b38fc48f27568f8e284eea08594d9df2bcc318f
 [c3_n15k6.cnf.zst]=a22b900e7c2b1eb8ac6645de9cd7cd04530b015a26ace87ed91d94bb3b13f927
 [c3_n15k6.lrat.zst]=18701a0ba6c7755baffc06ba3c354cb5d6687a43011b922ac23193bf11ccc3b3
 [c3_n16k6c.cnf.zst]=b4f20ebfca59b6d12200fc91054785852c4e1920d221d16efe7d1b562e0f9517
 [c3_n16k6c.lrat.zst]=0f2aefe8ba2a2b62385521f3ec299bbf71f837527bdd8b63b6ed4a7c707b729b
)
chk() { local f=$1 k=$2; local h; h=$(shasum -a 256 "$f" | cut -d' ' -f1); [ "$h" = "${REC[$k]}" ] && echo "MATCH $k $h" || echo "MISMATCH $k $h (recorded ${REC[$k]})"; }
for n in c3_n15k6 c3_n16k6c; do
  for e in cnf lrat; do
    chk "$A/$n.$e.zst" "$n.$e.zst"
    zstd -q -dc "$A/$n.$e.zst" > "$D/$n.$e"; chk "$D/$n.$e" "$n.$e"
  done
done
echo "== lrat-check (drat-trim 2e3b2dc + E2 patch) =="
for n in c3_n15k6 c3_n16k6c; do
  /usr/bin/time -p "$B/lrat-check" "$D/$n.cnf" "$D/$n.lrat" > "$O/$n.lratcheck.out" 2>&1; ec=$?
  echo "$n exit $ec: $(grep -E 'VERIFIED|FAIL' "$O/$n.lratcheck.out" | head -1) | $(grep -E '^real' "$O/$n.lratcheck.out")"
done
echo "== independent Python RUP-LRAT checker (lratpy.py) =="
for n in c3_n15k6 c3_n16k6c; do
  /usr/bin/time -p python3 -I "$SD/lratpy.py" "$D/$n.cnf" "$D/$n.lrat" > "$O/$n.lratpy.out" 2>&1; ec=$?
  echo "$n exit $ec: $(grep -E '^s ' "$O/$n.lratpy.out") | $(grep -E '^c (formula|additions|empty)' "$O/$n.lratpy.out" | tr '\n' ' ') | $(grep -E '^real' "$O/$n.lratpy.out")"
done
echo "== regenerate with repository tools/symmetric/symcnf.py =="
echo "symcnf.py sha256 $(shasum -a 256 "$C/tools/symmetric/symcnf.py" | cut -d' ' -f1) (recorded a8056da0...)"
( cd "$G" && python3 -I "$C/tools/symmetric/symcnf.py" 15 6 3 -o c3_n15k6.cnf > gen15.log 2>&1 ); chk "$G/c3_n15k6.cnf" c3_n15k6.cnf
( cd "$G" && python3 -I "$C/tools/symmetric/symcnf.py" 16 6 3 --center-in-set -o c3_n16k6c.cnf > gen16.log 2>&1 ); chk "$G/c3_n16k6c.cnf" c3_n16k6c.cnf
echo "== repository copies results/SYMMAX/k6/*.cnf.gz =="
for n in c3_n15k6 c3_n16k6c; do gzip -dc "$C/results/SYMMAX/k6/$n.cnf.gz" > "$D/symmax_$n.cnf"; chk "$D/symmax_$n.cnf" "$n.cnf"; done
echo "== negative controls for lratpy.py (must be REJECTED) =="
python3 -I - "$D/c3_n15k6.lrat" "$O/ctl_drop_mid_hint.lrat" "$O/ctl_flip_lit.lrat" <<'EOF'
import sys
L = open(sys.argv[1]).read().splitlines(True)
# control 1: in the 5000th addition line with >= 3 hints, drop its first hint
cnt = 0
for i, l in enumerate(L):
    t = l.split()
    if t[1] != "d":
        z = t.index("0", 1)
        if len(t) - z - 2 >= 3:
            cnt += 1
            if cnt == 5000:
                t2 = t[:z + 1] + t[z + 2:]
                M = L[:]; M[i] = " ".join(t2) + "\n"; open(sys.argv[2], "w").write("".join(M))
                print("ctl1: dropped first hint of line", i + 1); break
# control 2: in the 7000th addition line with a nonempty lemma, negate its first literal
cnt = 0
for i, l in enumerate(L):
    t = l.split()
    if t[1] != "d" and t[1] != "0":
        cnt += 1
        if cnt == 7000:
            t[1] = str(-int(t[1])); M = L[:]; M[i] = " ".join(t) + "\n"; open(sys.argv[3], "w").write("".join(M))
            print("ctl2: negated first literal of line", i + 1); break
EOF
for c in ctl_drop_mid_hint ctl_flip_lit; do
  python3 -I "$SD/lratpy.py" "$D/c3_n15k6.cnf" "$O/$c.lrat" > "$O/$c.lratpy.out" 2>&1; e1=$?
  "$B/lrat-check" "$D/c3_n15k6.cnf" "$O/$c.lrat" > "$O/$c.lratcheck.out" 2>&1; e2=$?
  echo "$c: lratpy exit $e1 ($(grep -E '^s ' "$O/$c.lratpy.out")); lrat-check exit $e2 ($(grep -E 'VERIFIED|FAIL|rror' "$O/$c.lratcheck.out" | head -1))"
done
