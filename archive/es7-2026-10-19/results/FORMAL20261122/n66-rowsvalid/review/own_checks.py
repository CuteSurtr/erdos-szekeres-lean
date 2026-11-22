"""Reviewer's own source-level checks for n66-rowsvalid (slot lrv3). Run with python3 -I. Reads only; writes
own_checks.json next to this script. Independent of the worker's scripts and of Lean's evaluator:

A. R0Parse: emulate n66enc's parseRows on n66enc's rows_used.txt (the file embedded by include_str) and compare with
   the concatenation of the chunk constants rows<k> parsed from the worker's RowChk/Rows*.lean in rowChunks order.
B. Row-certificate kinds in just<k> (tr, mt, co, mc, cy), and that #rows == #certificates per chunk.
C. templates / cores lists in DataT.lean / DataC.lean are exactly tmpl0..tmpl420 / core0..core207 in order; the
   docstring id of each entry equals the manifest id at that index; manifest covers T 0..420 and C 0..207 once.
D. Lean dumps (dump_templates.txt, dump_cores.txt) agree with the manifest n and with the VB job jsons.
"""
import ast, glob, hashlib, json, os, re, sys

D = "/home/jay/research/data/formalize-20261122/n66-rowsvalid"
L = D + "/lean"
ROWS = "/home/jay/research/data/formalize-20261122/n66enc/lean/N66Enc/data/rows_used.txt"
J = "/home/jay/research/data/n66-20261113/vfy15/rows/jobs"
out = {}

# ---------- A. R0Parse ----------
def parse_rows_like_lean(text):
    """n66enc parseRows: splitOn "\n"; per line splitOn " ", drop ""; empty -> skipped; any token that is not a
    decimal below 70 -> the whole line is dropped (mapM parseState = none)."""
    res, dropped = [], 0
    for line in text.split("\n"):
        ws = [w for w in line.split(" ") if w != ""]
        if not ws:
            continue
        ok = all(w.isascii() and w.isdigit() and int(w) < 70 for w in ws)
        if ok:
            res.append([int(w) for w in ws])
        else:
            dropped += 1
    return res, dropped

raw = open(ROWS, "rb").read()
r0, dropped = parse_rows_like_lean(raw.decode("utf-8"))
out["rows_used_sha256"] = hashlib.sha256(raw).hexdigest()
out["R0_len"] = len(r0)
out["R0_dropped_lines"] = dropped

src_all = open(L + "/RowChk/RowsAll.lean").read()
m = re.search(r"def rowChunks[^:]*:[^=]*:=\s*\[(.*?)\]\s*\n", src_all, re.S)
pairs = re.findall(r"\((rows\d+),\s*(just\d+)\)", m.group(1))
out["chunks"] = len(pairs)
out["chunk_pairs_consistent"] = all(a[4:] == b[4:] for a, b in pairs)
out["R1nat_def"] = bool(re.search(r"def R1nat : List \(List Nat\) := rowChunks\.flatMap Prod\.fst", src_all))

defs_rows, defs_just = {}, {}
for f in sorted(glob.glob(L + "/RowChk/Rows*.lean")):
    if f.endswith("RowsAll.lean"):
        continue
    s = open(f).read()
    for name, body in re.findall(r"def (rows\d+) : List \(List Nat\) := (\[.*?\])\s*\ndef", s, re.S):
        defs_rows[name] = ast.literal_eval(body)
    for name, body in re.findall(r"def (just\d+) : List RC := \[(.*?)\]\s*\ntheorem", s, re.S):
        defs_just[name] = re.findall(r"\.(tr|mt|co|mc|cy)\b", body)
    for k in re.findall(r"theorem (chk\d+) : chkRows (rows\d+) (just\d+) = true := by decide \+kernel", s):
        out.setdefault("chk_thms", []).append(k)
out["rows_defs"] = len(defs_rows)
out["just_defs"] = len(defs_just)
out["chk_theorems"] = len(out.pop("chk_thms", []))

r1 = []
per_chunk_ok = True
kinds = {}
for a, b in pairs:
    r1.extend(defs_rows[a])
    if len(defs_rows[a]) != len(defs_just[b]):
        per_chunk_ok = False
    for kd in defs_just[b]:
        kinds[kd] = kinds.get(kd, 0) + 1
out["R1_len"] = len(r1)
out["R1_all_below_70"] = all(0 <= x < 70 for T in r1 for x in T)
out["R0_equals_R1"] = (r0 == r1)
out["rows_vs_certs_per_chunk_equal"] = per_chunk_ok
out["kinds"] = kinds
out["kinds_summary"] = {"transported(tr)": kinds.get("tr", 0), "mirror(mt+mc)": kinds.get("mt", 0) + kinds.get("mc", 0),
                        "core(co)": kinds.get("co", 0), "cycle(cy)": kinds.get("cy", 0)}
out["R1_rows_sorted_nodup"] = all(T == sorted(set(T)) for T in r1)
dump = open(D + "/review/dump_R1.txt", "rb").read()
out["dump_R1_equals_rows_used"] = (dump == raw)

# ---------- C. templates / cores lists and manifest ----------
st = open(L + "/RowEnc/DataT.lean").read()
sc = open(L + "/RowEnc/DataC.lean").read()
tl = re.search(r"def templates : List Cert := \[(.*?)\]", st, re.S).group(1).replace(" ", "").split(",")
cl = re.search(r"def cores : List Cert := \[(.*?)\]", sc, re.S).group(1).replace(" ", "").split(",")
out["templates_list_is_tmpl0_420"] = tl == [f"tmpl{i}" for i in range(421)]
out["cores_list_is_core0_207"] = cl == [f"core{i}" for i in range(208)]
doc_t, doc_c = {}, {}
for f in sorted(glob.glob(L + "/RowEnc/DataT[0-9].lean")):
    for ident, k in re.findall(r"/-- template ([0-9a-f]{16}) -/\ndef tmpl(\d+) : Cert :=", open(f).read()):
        doc_t[int(k)] = ident
for f in sorted(glob.glob(L + "/RowEnc/DataC[0-9].lean")):
    for ident, k in re.findall(r"/-- core C_([0-9a-f]{16}) -/\ndef core(\d+) : Cert :=", open(f).read()):
        doc_c[int(k)] = ident
man = [l.rstrip("\n").split("\t") for l in open(D + "/data/certs_manifest.tsv")][1:]
mt = {int(r[0]): r for r in man if r[1] == "T"}
mc = {int(r[0]): r for r in man if r[1] == "C"}
out["manifest_rows"] = len(man)
out["manifest_T_idx_0_420"] = sorted(mt) == list(range(421)) and sum(r[1] == "T" for r in man) == 421
out["manifest_C_idx_0_207"] = sorted(mc) == list(range(208)) and sum(r[1] == "C" for r in man) == 208
out["docstring_ids_match_manifest_T"] = all(doc_t.get(i) == mt[i][2] for i in range(421))
out["docstring_ids_match_manifest_C"] = all("C_" + doc_c.get(i, "?") == mc[i][2] for i in range(208))
out["T208_id"] = mt[208][2]

# ---------- D. dumps vs manifest and VB jsons ----------
dt = [l.split() for l in open(D + "/review/dump_templates.txt").read().splitlines()]
dc = [l.split() for l in open(D + "/review/dump_cores.txt").read().splitlines()]
out["dump_templates_n_match_manifest"] = len(dt) == 421 and all(int(dt[i][0]) == int(mt[i][3]) for i in range(421))
out["dump_cores_n_match_manifest"] = len(dc) == 208 and all(int(dc[i][0]) == int(mc[i][3]) for i in range(208))
vb_hash_ok, vb_cert_ok, missing = 0, 0, []
for kind, rows in (("T", mt), ("C", mc)):
    for i, r in rows.items():
        key = ("T_" + r[2]) if kind == "T" else r[2]
        p = f"{J}/{key}.json"
        if not os.path.exists(p):
            missing.append(key); continue
        d = json.load(open(p))
        if d.get("cnf_sha256") == r[4]:
            vb_hash_ok += 1
        if d.get("cake_lines") == ["s VERIFIED UNSAT"] and d.get("cake_exact") == 1 and d.get("certified") is True:
            vb_cert_ok += 1
out["vb_json_cnf_sha256_eq_manifest"] = vb_hash_ok
out["vb_json_verdict_exact"] = vb_cert_ok
out["vb_json_missing"] = missing
out["octs_none_templates"] = sum(1 for r in dt if r[3] == "true")
out["octs_none_cores"] = sum(1 for r in dc if r[2] == "true")
out["template_n_range"] = [min(int(r[0]) for r in dt), max(int(r[0]) for r in dt)]
out["core_n_range"] = [min(int(r[0]) for r in dc), max(int(r[0]) for r in dc)]

json.dump(out, open(D + "/review/own_checks.json", "w"), indent=1, sort_keys=True)
print(json.dumps(out, indent=1, sort_keys=True))
