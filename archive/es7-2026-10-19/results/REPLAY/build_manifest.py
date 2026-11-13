#!/usr/bin/env python3
"""Build the replay manifest of every retained critical-path certificate of the symmetric ES(7) work.

Every number in the manifest is copied from a record, never from an observation of the archive. The record of each
value is named in a "source" field. Three kinds of source occur, from strongest to weakest:
  repo:<path>        committed in the repository (worktree at the commit given by --commit)
  archive-self:<p>   written into the archive by the job that wrote the archive (not in the repository)
  live:<path>        written tonight by a running or finished local job (not committed)

Inputs (all read-only):
  RES    repository results directory  (cloud/es7-2026-10-19/results)
  AROOT  proof-archive root            (local, outside Git)
  LIVE   local directory with tonight's re-solve records (repro3a/b.jsonl, pilot1/2.jsonl, local1/2.jsonl)

usage: build_manifest.py RES AROOT LIVE OUT_JSON OUT_TSV [--commit SHA]
"""
import csv, json, os, re, sys

args = [a for a in sys.argv[1:] if not a.startswith("--")]
RES, AROOT, LIVE, OUT_JSON, OUT_TSV = args[:5]
COMMIT = "9cf4949a5"
if "--commit" in sys.argv:
    COMMIT = sys.argv[sys.argv.index("--commit") + 1]
MIB_GB = 1048576 / 1e9          # cake_lpr's --CML_HEAP_SIZE is in MiB; footprint in GB = heap * MIB_GB
rp = lambda p: f"repo:{p}@{COMMIT}"
entries, problems = [], []


def need(cond, msg):
    if not cond:
        problems.append(msg)
    return cond


def readf(*p):
    return open(os.path.join(*p), encoding="utf-8").read()


# ---------------------------------------------------------------- tools and the shared central base
cert = readf(RES, "WRITEUP", "CERTIFICATES.md")
tools = {}
for name in ("cadical", "lrat-check", "cake_lpr"):
    m = re.search(rf"^\| {re.escape(name)} \| `([0-9a-f]{{64}})` \|", cert, re.M)
    need(m, f"tool {name} not in CERTIFICATES.md")
    tools[name] = {"sha256": m.group(1), "source": rp("results/WRITEUP/CERTIFICATES.md (Tools table)")}
# cross-check with the archive's own tool list
for l in open(os.path.join(AROOT, "es7-symmetry", "tools", "tools_sha256.txt")):
    h, n = l.split()
    if n in tools:
        need(tools[n]["sha256"] == h, f"tool {n}: archive tools_sha256.txt differs from CERTIFICATES.md")

task = readf(RES, "C2P", "TASK.md")
m = re.search(r"`python3 SYMZ/zcnf\.py rot 17 7 --m 2 --hull -o /opt/work/base\.cnf --map /opt/work/base\.json`.*?"
              r"`(p cnf \d+ \d+)`.*?`([0-9a-f]{64})` for base\.cnf and `([0-9a-f]{64})` for base\.json", task, re.S)
need(m, "central base command/hashes not found in C2P/TASK.md")
inputs = {
    "central_base": {
        "what": "base CNF of the central 34-point search (zcnf.py rot, m = 2, hull-vertex normal form)",
        "gen": "SYMZ/zcnf.py", "gen_sha256": None,
        "argv": ["rot", "17", "7", "--m", "2", "--hull", "-o", "base.cnf", "--map", "base.json"],
        "out": "base.cnf", "header": m.group(1), "sha256": m.group(2), "map": "base.json", "map_sha256": m.group(3),
        "source": rp("results/C2P/TASK.md (Base CNF step)") + "; also results/C2FINAL/README.md section 3 and "
                  "WRITEUP/CERTIFICATES.md central34-hull (c34h_final.cnf)",
    },
}
need(inputs["central_base"]["sha256"] in cert, "central base hash not repeated in CERTIFICATES.md")

# generator hashes recorded in CERTIFICATES.md
gen_sha = {}
for g in ("zcnf_v1.py", "zcnf.py", "symcnf.py", "symcnf_layers.py"):
    m = re.search(rf"{re.escape(g)} \(sha256 ([0-9a-f]{{64}})\)", cert)
    need(m, f"generator hash of {g} not in CERTIFICATES.md")
    gen_sha[g] = m.group(1)
inputs["central_base"]["gen_sha256"] = gen_sha["zcnf.py"]


# ---------------------------------------------------------------- recorded checker resource use (archived logs)
def chk_log(rel):
    """parse an archived checker log (/usr/bin/time -l format) into verdict, wall s, rss and footprint"""
    p = os.path.join(AROOT, rel)
    if not os.path.exists(p):
        return None
    t = open(p, errors="replace").read()
    g = lambda pat: (m.group(1) if (m := re.search(pat, t, re.M)) else None)
    v = g(r"^(c VERIFIED|s VERIFIED UNSAT|CakeML heap space exhausted\.|c FAIL\S*.*)$")
    rss, fp, wall = g(r"^\s*(\d+)\s+maximum resident set size"), g(r"^\s*(\d+)\s+peak memory footprint"), \
        g(r"^exit \d+ wall (\d+) s")
    return {"log": "archive-self:" + rel, "verdict": v, "wall_s": int(wall) if wall else None,
            "max_rss_bytes": int(rss) if rss else None, "peak_footprint_bytes": int(fp) if fp else None,
            "parsed_line": g(r"^(c parsed a formula with .*)$"), "added_line": g(r"^(c Added clauses = .*)$")}


# ---------------------------------------------------------------- CERTIFICATES.md sections
def section(name):
    m = re.search(rf"^## {re.escape(name)}\n(.*?)(?=^## |\Z)", cert, re.M | re.S)
    need(m, f"section {name} missing")
    return m.group(1)


def table(sec):
    """rows of 'file | bytes | SHA-256 | archive | archive bytes | archive SHA-256 | round trip'"""
    out = {}
    for line in sec.splitlines():
        if line.startswith("|") and ".zst`" in line:
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            assert len(c) == 7, c
            kind = "cnf" if c[0].startswith("CNF") else "proof"
            hm = re.search(r"\((p cnf \d+ \d+)\)", c[0])
            out[kind] = {"label": c[0], "bytes": int(c[1].replace(",", "")), "sha256": c[2].strip("`"),
                         "archive": "es7-symmetry/" + c[3].strip("`"), "archive_bytes": int(c[4].replace(",", "")),
                         "archive_sha256": c[5].strip("`"), "roundtrip": c[6], "header": hm.group(1) if hm else None}
    return out


def gen_method(sec, gen, argv_str, extra=()):
    """generator method; the command must appear verbatim in the section"""
    cmd = f"python3 {gen} {argv_str}"
    need(f"`{cmd}`" in sec, f"command `{cmd}` not found verbatim in CERTIFICATES.md")
    folder = "SYMZ" if gen.startswith("zcnf") else "SYM5"
    argv = argv_str.split()
    return {"kind": "generator", "gen": f"{folder}/{gen}", "gen_sha256": gen_sha[gen],
            "with": [{"file": f"{folder}/{x}", "sha256": gen_sha[x]} for x in extra],
            "argv": argv, "out": argv[argv.index("-o") + 1], "recorded_command": cmd,
            "source": rp("results/WRITEUP/CERTIFICATES.md (Generator line)")}


def heap_of(sec, missing_ok=False):
    m = re.search(r"cake_lpr --CML_HEAP_SIZE=(\d+)", sec)
    if m:
        return int(m.group(1))
    if "(default heap)" in sec:
        return "default"
    need(missing_ok, "no heap and no 'default heap' in section")
    return "not recorded"


def cert_entry(eid, secname, group, critical, default, statement, gen, argv_str, logs, extra=(), ladder=None,
               notes=None, heap_missing_ok=False):
    sec = section(secname)
    t = table(sec)
    need("cnf" in t and "proof" in t, f"{secname}: table incomplete")
    heap = heap_of(sec, heap_missing_ok)
    rec = {"heap_mb": heap, "heap_source": rp("results/WRITEUP/CERTIFICATES.md (Checkers)")}
    for k, rel in logs.items():
        rec[k] = chk_log(rel)
    if ladder is None:
        ladder = [heap] if isinstance(heap, int) else [8000, 16000]
    e = {"id": eid, "group": group, "critical": critical, "default": default, "statement": statement,
         "proof": {"archive": t["proof"]["archive"], "archive_bytes": t["proof"]["archive_bytes"],
                   "archive_sha256": t["proof"]["archive_sha256"], "sha256": t["proof"]["sha256"],
                   "bytes": t["proof"]["bytes"], "source": rp("results/WRITEUP/CERTIFICATES.md (table)"),
                   "roundtrip_recorded": t["proof"]["roundtrip"]},
         "cnf": {"sha256": t["cnf"]["sha256"], "bytes": t["cnf"]["bytes"], "header": t["cnf"]["header"],
                 "source": rp("results/WRITEUP/CERTIFICATES.md (table)"),
                 "methods": [{"kind": "archive", "archive": t["cnf"]["archive"],
                              "archive_bytes": t["cnf"]["archive_bytes"], "archive_sha256": t["cnf"]["archive_sha256"],
                              "source": rp("results/WRITEUP/CERTIFICATES.md (table)")}]},
         "recorded": rec, "heap_ladder_mb": ladder}
    if gen:
        e["cnf"]["methods"].append(gen_method(sec, gen, argv_str, extra))
    if notes:
        e["notes"] = notes
    entries.append(e)
    return e


cert_entry("mirror34", "mirror34", "SYMZ", "yes: M34, Theorem 2b (17 mirror pairs, no axis point)", True,
           "34 points in general position, 17 mirror pairs, no point on the axis -> convex 7-gon",
           "zcnf_v1.py", "mirror 17 7 -o m_t17k7.cnf --map m_t17k7.json",
           {"lrat_check_log": "es7-symmetry/mirror34/chk_mr34_def_lrat-check.out",
            "cake_lpr_log": "es7-symmetry/mirror34/chk_mr34_def_cake_lpr.out"})
# variant: the same proof on the final zcnf.py CNF (same clauses, comment line differs); not archived, generator only
sec = section("mirror34")
m = re.search(r"\(SHA-256 `([0-9a-f]{64})`\); the proof was also accepted on that file", sec)
need(m, "mirror34 final-CNF hash missing")
entries.append({
    "id": "mirror34-finalcnf", "group": "SYMZ", "critical": "optional: same proof as mirror34 on the zcnf.py CNF",
    "default": False, "statement": "as mirror34; CNF written by the final zcnf.py (comment line differs)",
    "proof": dict(entries[-1]["proof"]),
    "cnf": {"sha256": m.group(1), "bytes": None, "header": "p cnf 838032 16642456",
            "source": rp("results/WRITEUP/CERTIFICATES.md (mirror34 Generator line)"),
            "methods": [{"kind": "generator", "gen": "SYMZ/zcnf.py", "gen_sha256": gen_sha["zcnf.py"], "with": [],
                         "argv": "mirror 17 7 -o m34_final.cnf --map m34_final.json".split(), "out": "m34_final.cnf",
                         "recorded_command": None,
                         "source": "derived: zcnf.py with the mirror34 arguments (A6 audit regen_mirror.log reproduced "
                                   "1b61bf2f with exactly this command)"}]},
    "recorded": {"heap_mb": 30000, "heap_source": rp("results/WRITEUP/CERTIFICATES.md (mirror34 Checkers)"),
                 "lrat_check_log": chk_log("es7-symmetry/mirror34/chk_mr34_final_lrat-check.out"),
                 "cake_lpr_log": chk_log("es7-symmetry/mirror34/chk_mr34_final_cake_lpr.out")},
    "heap_ladder_mb": [30000]})
cert_entry("mirror33", "mirror33", "SYMZ", "yes: M33, Theorem 2a (16 mirror pairs + 1 axis point)", True,
           "33 points in general position, 16 mirror pairs and one axis point -> convex 7-gon",
           "zcnf.py", "mirror 16 7 --axis 1 -o m_t16k7a1.cnf --map m_t16k7a1.json",
           {"lrat_check_log": "es7-symmetry/mirror33/chk_m33_def_lrat-check.out",
            "cake_lpr_log": "es7-symmetry/mirror33/chk_m33_def_cake_lpr.out"})
cert_entry("c5-P1", "c5-angle", "SYM5", "yes: C5 >= 35 (either c5-P1 or c5-L1 suffices)", True,
           "35 points, fivefold rotation (7 orbits, centre not in the set), angle normal form -> convex 7-gon",
           "symcnf.py", "35 7 5 -o c5_n35.cnf --map c5_n35.json",
           {"lrat_check_log": "es7-symmetry/c5/chk_P1_lrat-check.out",
            "cake_lpr_log": "es7-symmetry/c5/chk_P1_cake_lpr_heap30000.out",
            "cake_lpr_failed_log": "es7-symmetry/c5/chk_P1_cake_lpr_heap12000.out"},
           notes="cake_lpr needs a 30000 MiB heap (31.5 GB); the first run exhausted the default 4096 MiB heap (its "
                 "file name says heap12000 but the environment variable used there is ignored by this build; its "
                 "max RSS 4,298,113,024 B equals the default heap). No size between 4096 and 30000 MiB was tried.")
cert_entry("c5-L1", "c5-layer", "SYM5", "yes: C5 >= 35 (either c5-P1 or c5-L1 suffices; L1 also needs the layer lemma)",
           True, "35 points, fivefold rotation, layer normal form (seven nested pentagons) -> convex 7-gon",
           "symcnf_layers.py", "35 7 5 -o c5_n35L.cnf --map c5_n35L.json",
           {"lrat_check_log": "es7-symmetry/c5/chk_L1_lrat-check.out",
            "cake_lpr_log": "es7-symmetry/c5/chk_L1_cake_lpr.out"}, extra=("symcnf.py",), ladder=[8000, 16000],
           notes="recorded cake_lpr run used the default heap (4096 MiB; max RSS 4,298,506,240 B); replay uses an "
                 "explicit 8000 MiB first")
# L2: second proof of the same CNF; never checked; archive hash recorded only in the archive's own table
l2 = [l.rstrip("\n").split("\t") for l in open(os.path.join(AROOT, "es7-symmetry", "c5", "archive_hashes.tsv"))
      if l.startswith("L2.lrat\t")]
m = re.search(r"L2\.lrat \(sha256 ([0-9a-f]{64})\)", cert)
need(len(l2) == 1 and m and l2[0][2] == m.group(1), "L2 records inconsistent")
L1 = entries[-1]
entries.append({
    "id": "c5-L2", "group": "SYM5", "critical": "optional: second proof (--unsat) of the c5-L1 CNF, never checked",
    "default": False, "statement": L1["statement"],
    "proof": {"archive": "es7-symmetry/c5/L2.lrat.zst", "archive_bytes": int(l2[0][3]), "archive_sha256": l2[0][4],
              "sha256": m.group(1), "bytes": int(l2[0][1]),
              "source": rp("results/WRITEUP/CERTIFICATES.md (proof sha256)") + "; archive bytes/sha256 and proof "
                        "bytes: archive-self:es7-symmetry/c5/archive_hashes.tsv", "roundtrip_recorded": l2[0][5]},
    "cnf": json.loads(json.dumps(L1["cnf"])),
    "recorded": {"heap_mb": None, "heap_source": "never checked (SYM5/README.md table: not run)"},
    "heap_ladder_mb": [8000, 16000]})
cert_entry("c3hex-15", "c3-hex-15", "c3hex", "k=6 table only (threefold 15 points, no convex hexagon); not on the "
           "ES(7) path", True, "15 points, threefold rotation (5 orbits, no centre) -> convex hexagon",
           "symcnf.py", "15 6 3 -o c3_n15k6.cnf", {}, ladder=[2000, 8000], heap_missing_ok=True)
cert_entry("c3hex-16", "c3-hex-16", "c3hex", "k=6 table only (threefold 16 points with centre); not on the ES(7) path",
           True, "16 points, threefold rotation (5 orbits and the centre) -> convex hexagon",
           "symcnf.py", "16 6 3 --center-in-set -o c3_n16k6c.cnf", {}, ladder=[2000, 8000], heap_missing_ok=True)
for e in entries[-2:]:
    e["recorded"]["checker_log"] = "archive-self:es7-symmetry/" + "c3hex/chk_c3hex.log (verdicts only)"
cov = cert_entry("central34-cover", "central34-cover", "central34-cover",
                 "yes: C2-34 hull case split (136 hull cubes cover the base)", True,
                 "the 136 hull cubes of hullcubes.py cover zcnf.py rot 17 7 --m 2 --hull (case split exhaustive)",
                 None, None, {"lrat_check_log": "es7-symmetry/central34/chk_hc34_cover_lrat-check.out",
                              "cake_lpr_log": "es7-symmetry/central34/chk_hc34_cover_cake_lpr.out"})
need("`python3 zcnf.py rot 17 7 --m 2 --hull -o c34h.cnf --map c34h.json`" in section("central34-cover"),
     "cover generator command not verbatim")
cov["cnf"]["methods"].append({
    "kind": "hull_cover", "base": "central_base", "cubes": "C2C34/cubes.txt",
    "recorded_command": "python3 zcnf.py rot 17 7 --m 2 --hull -o c34h.cnf --map c34h.json; "
                        "python3 hullcubes.py c34h.cnf c34h.json hc34",
    "source": rp("results/WRITEUP/CERTIFICATES.md (central34-cover Generator)") + "; streamed re-implementation of "
              "hullcubes.py's cover.cnf writer (header NC+136, base lines after the header without empty lines, then "
              "the negation of each cube of C2C34/cubes.txt in file order); hullcubes.py itself reads the whole CNF "
              "into memory (several GB) and is not run here"})

# ---------------------------------------------------------------- C4CUT (fourfold 32 points + six cuts)
fj = json.load(open(os.path.join(RES, "C4CUT", "final.json")))
c4r = readf(RES, "C4CUT", "README.md")
need("`python3 SYM5/symcnf_layers.py 32 7 4 -o c4_n32L.cnf --map c4_n32L.json`" in c4r, "C4CUT command not verbatim")
sums = dict((l.split()[1], l.split()[0]) for l in open(os.path.join(AROOT, "es7-c4-32-cuts-2026-11-01", "SHA256SUMS")))
need(sums.get("cuts.jsonl") == fj["cuts_jsonl_sha256"], "C4CUT cuts.jsonl hash differs between final.json and SHA256SUMS")
entries.append({
    "id": "c4cut-final", "group": "C4CUT",
    "critical": "no: gives N(C4) = 28 only; the main claim gets the fourfold case from C2-34 (half-turn)",
    "default": True, "statement": "32 points, fourfold rotation, layer form, plus six realizability cuts -> UNSAT",
    "proof": {"archive": "es7-c4-32-cuts-2026-11-01/c4cuts.lrat.zst", "archive_bytes": None,
              "archive_sha256": sums["c4cuts.lrat.zst"], "sha256": fj["proof_sha256"], "bytes": fj["proof_bytes"],
              "source": rp("results/C4CUT/final.json") + "; archive sha256 only in archive-self:"
                        "es7-c4-32-cuts-2026-11-01/SHA256SUMS (not in the repository)",
              "roundtrip_recorded": fj["archive_roundtrip"]},
    "cnf": {"sha256": fj["cnf_sha256"], "bytes": None, "header": None, "source": rp("results/C4CUT/final.json"),
            "methods": [
                {"kind": "archive", "archive": "es7-c4-32-cuts-2026-11-01/c4_n32L_cuts.cnf.zst", "archive_bytes": None,
                 "archive_sha256": sums["c4_n32L_cuts.cnf.zst"],
                 "source": "archive-self:es7-c4-32-cuts-2026-11-01/SHA256SUMS"},
                {"kind": "c4cuts",
                 "base": {"kind": "generator", "gen": "SYM5/symcnf_layers.py", "gen_sha256": gen_sha["symcnf_layers.py"],
                          "with": [{"file": "SYM5/symcnf.py", "sha256": gen_sha["symcnf.py"]}],
                          "argv": "32 7 4 -o c4_n32L.cnf --map c4_n32L.json".split(), "out": "c4_n32L.cnf",
                          "recorded_command": "python3 SYM5/symcnf_layers.py 32 7 4 -o c4_n32L.cnf --map c4_n32L.json",
                          "source": rp("results/C4CUT/README.md section 1")},
                 "base_sha256": fj["base_cnf_sha256"], "cuts": "C4CUT/cuts.jsonl", "cuts_sha256": fj["cuts_jsonl_sha256"],
                 "source": rp("results/C4CUT/c4final.sh") + " (base, header NC+6, one clause per cuts.jsonl line)"}]},
    "recorded": {"heap_mb": fj["cake_heap_mb"], "heap_source": rp("results/C4CUT/final.json"),
                 "lrat_check": fj["lrat_check"], "cake_lpr": fj["cake_lpr"]},
    "heap_ladder_mb": [8000, 16000]})


# ---------------------------------------------------------------- central-34 unit records
def unit_clauses(unit):
    """how lane.py builds a unit: <case>_cover, or a second-layer subcase cube of C2P/cubes/<case>_cubes.txt"""
    case = unit.split("_")[0]
    if unit.endswith("_cover"):
        return {"type": "cover", "case": case, "hull_cubes": "C2C34/cubes.txt", "cubes": f"C2P/cubes/{case}_cubes.txt"}
    return {"type": "cube", "case": case, "cubes": f"C2P/cubes/{case}_cubes.txt", "unit": unit}


def orig_records():
    """original solve-time wave records, by (source dir, unit)"""
    out = {}
    for d in sorted(os.listdir(RES)):
        if not d.startswith("C2P"):
            continue
        for sub in sorted(os.listdir(os.path.join(RES, d))):
            f = os.path.join(RES, d, sub, "out.jsonl")
            if os.path.isfile(f):
                for l in open(f):
                    if l.strip():
                        r = json.loads(l)
                        out.setdefault((f"{d}/{sub}", r["unit"]), []).append(r)
    for r in csv.DictReader(open(os.path.join(RES, "C2C34", "logs", "p8_units.tsv")), delimiter="\t"):
        out.setdefault(("C2C34/p8", r["unit"]), []).append(r)
    return out


ORIG = orig_records()


def central_entry(eid, group, critical, default, r, rec_src, archive_dir, heap_src, orig_key=None):
    unit = r["unit"]
    arc = r["archive"]
    arc_rel = arc if arc.startswith("es7-") else f"{archive_dir}/{arc}"
    need(arc_rel.startswith(archive_dir + "/"), f"{eid}: archive {arc_rel} outside {archive_dir}")
    e = {"id": eid, "group": group, "critical": critical, "default": default,
         "statement": f"central 34-point unit {unit} is UNSAT",
         "proof": {"archive": arc_rel, "archive_bytes": r["archive_bytes"], "archive_sha256": r["archive_sha256"],
                   "sha256": r["proof_sha256"], "bytes": r["proof_bytes"], "source": rec_src,
                   "roundtrip_recorded": r.get("roundtrip")},
         "cnf": {"sha256": r["cnf_sha256"], "bytes": None, "header": None, "source": rec_src,
                 "methods": [{"kind": "central_unit", "base": "central_base", "clauses": unit_clauses(unit),
                              "source": rp("results/C2P/tools/lane.py") + " build() and extra_clauses()"}]},
         "recorded": {"heap_mb": r.get("cake_heap_mb") or 8000, "heap_source": heap_src,
                      "lrat_check": r.get("lrat_check"), "lrat_check_s": r.get("lrat_check_s"),
                      "cake_lpr": r.get("cake_lpr"), "cake_s": r.get("cake_s"), "solve_s": r.get("solve_s")},
         "heap_ladder_mb": [8000, 16000]}
    if orig_key:
        o = ORIG.get(orig_key, [])
        o = [x for x in o if str(x.get("status")) == "UNSATISFIABLE"]
        if need(len(o) >= 1, f"{eid}: no original record {orig_key}"):
            x = o[-1]
            e["original_record"] = {"source": rp(f"results/{orig_key[0]}" + ("/out.jsonl" if orig_key[0] != "C2C34/p8"
                                                                             else " (C2C34/logs/p8_units.tsv)")),
                                    "cnf_sha256": x.get("cnf_sha256"), "proof_sha256": x.get("proof_sha256"),
                                    "proof_bytes": int(x["proof_bytes"]) if x.get("proof_bytes") else None,
                                    "cnf_matches_archived_proof_record": x.get("cnf_sha256") == r["cnf_sha256"],
                                    "proof_identical_to_archived": x.get("proof_sha256") == r["proof_sha256"]}
    entries.append(e)
    return e


# pilot re-solve (7 units, committed)
PD = "es7-central34-pilot-resolve-2026-11-01"
for l in open(os.path.join(RES, "C2FINAL", "pilot", "out.jsonl")):
    if l.strip():
        r = json.loads(l)
        need(r["cnf_sha256"] == r["cnf_sha256_expected"], f"pilot {r['unit']}: cnf hash != expected")
        crit = ("yes: C2-34 cover of case P8 (560 second-layer subcases)" if r["unit"] == "P8_cover"
                else "yes: C2-34, closes a P8 orbit (pilot record had no CNF hash)")
        central_entry(f"pilot:{r['unit']}", "central34-pilot-resolve", crit, True, r,
                      rp("results/C2FINAL/pilot/out.jsonl"), PD, rp("results/C2FINAL/pilot/out.jsonl"))

# random re-solve sample (committed: 23 + 8 records) and the three units finished later (live records)
SD = "es7-central34-resample-2026-11-01"
for fn in ("out.jsonl", "extra_out.jsonl"):
    for l in open(os.path.join(RES, "C2FINAL", "sample", fn)):
        if l.strip():
            r = json.loads(l)
            central_entry(f"resample:{r['unit']}", "central34-resample",
                          "C2-34 orbit fact, re-solved with a retained proof (one member of an orbit)", True, r,
                          rp(f"results/C2FINAL/sample/{fn}"), SD,
                          rp("results/C2FINAL/sample/reproduce.py") + " (fixed --CML_HEAP_SIZE=8000; heap not in record)",
                          orig_key=(r["record_source"], r["unit"]))
for fn in ("repro3a.jsonl", "repro3b.jsonl"):
    p = os.path.join(LIVE, fn)
    if os.path.exists(p):
        for l in open(p):
            if l.strip():
                r = json.loads(l)
                if r.get("certified") and r.get("archive"):
                    central_entry(f"resample:{r['unit']}", "central34-resample",
                                  "C2-34 orbit fact, re-solved with a retained proof (one member of an orbit)", True, r,
                                  f"live:{p}", SD, f"live:{p}", orig_key=(r["record_source"], r["unit"]))

# P8 pilot orbit re-solves (live job; only units with a finished record)
OD = "es7-central34-pilot-orbits-2026-11-01"
for fn in ("pilot1.jsonl", "pilot2.jsonl"):
    p = os.path.join(LIVE, fn)
    if os.path.exists(p):
        for l in open(p):
            if l.strip():
                r = json.loads(l)
                if r.get("certified") and r.get("archive"):
                    central_entry(f"pilotorbit:{r['unit']}", "central34-pilot-orbits",
                                  "yes: C2-34, closes a P8 orbit that rested on a pilot record (CNF not hashed at "
                                  "cake_lpr time)", True, r, f"live:{p}", OD, f"live:{p}",
                                  orig_key=("C2C34/p8", r["unit"]))

# LOCAL re-solves (live job, may not have started; archive created by reproduce_local.py)
LD = "es7-central34-local-2026-11-01"
for fn in ("local1.jsonl", "local2.jsonl"):
    p = os.path.join(LIVE, fn)
    if os.path.exists(p):
        for l in open(p):
            if l.strip():
                r = json.loads(l)
                if r.get("certified") and r.get("archive"):
                    central_entry(f"local:{r['unit']}", "central34-local",
                                  "yes: C2-34 orbit fact or cover that rested only on a Mac LOCAL record", True, r,
                                  f"live:{p}", LD, f"live:{p}", orig_key=(r["record_source"], r["unit"]))

# 120 hexagonal hull cases (committed records; replayed tonight by hexcheck as well)
for r in csv.DictReader(open(os.path.join(RES, "C2C34", "logs", "hex_cases.tsv")), delimiter="\t"):
    need(r["status"] == "UNSATISFIABLE" and r["roundtrip"] == "verified", f"hull {r['case']} record not clean")
    entries.append({
        "id": f"hull:{r['case']}", "group": "central34-hull",
        "critical": "yes: C2-34 hexagonal hull case" + (" (canonical)" if r["canonical"] == "True" else ""),
        "default": False, "statement": f"central 34-point hexagonal hull case {r['case']} is UNSAT",
        "proof": {"archive": f"es7-symmetry/central34-hull/{r['case']}.lrat.zst", "archive_bytes": None,
                  "archive_sha256": r["archive_sha256"], "sha256": r["proof_sha256"], "bytes": int(r["proof_bytes"]),
                  "source": rp("results/C2C34/logs/hex_cases.tsv"), "roundtrip_recorded": r["roundtrip"]},
        "cnf": {"sha256": r["cnf_sha256"], "bytes": None, "header": None, "source": rp("results/C2C34/logs/hex_cases.tsv"),
                "methods": [{"kind": "central_unit", "base": "central_base",
                             "clauses": {"type": "hull", "case": r["case"], "cubes": "C2C34/cubes.txt"},
                             "source": rp("results/C2C34/hlane.sh") + " (base, header NC+n, the n hull-cube literals "
                                       "as unit clauses)"}]},
        "recorded": {"heap_mb": 16000, "heap_source": rp("results/WRITEUP/CERTIFICATES.md central34-hull (Checkers)"),
                     "lrat_check": r["lrat_check"], "cake_lpr": r["cake_lpr"], "cake_s": float(r["cake_wall_s"]),
                     "solve_s": float(r["solve_s"])},
        "heap_ladder_mb": [8000, 16000],
        "notes": "also being replayed tonight by $S/hexcheck/hexcheck.py (same procedure); default off here"})

# ---------------------------------------------------------------- replay resource estimates
for e in entries:
    lad = e["heap_ladder_mb"]
    e["replay_memory"] = {
        "cake_lpr_heap_mb_first": lad[0], "cake_lpr_heap_mb_max": max(lad),
        "cake_lpr_footprint_gb_first": round(lad[0] * MIB_GB + 0.4, 1),
        "cake_lpr_footprint_gb_max": round(max(lad) * MIB_GB + 0.4, 1),
        "lrat_check_rss_gb_est": None, "disk_gb": round(((e["proof"]["bytes"] or 0) + (e["cnf"]["bytes"] or 7e8)) / 1e9, 1)}
    lg = e["recorded"].get("lrat_check_log")
    if lg and lg.get("peak_footprint_bytes"):
        e["replay_memory"]["lrat_check_rss_gb_est"] = round(lg["peak_footprint_bytes"] / 1e9, 2)

# ---------------------------------------------------------------- consistency checks on the records themselves
ids = [e["id"] for e in entries]
need(len(ids) == len(set(ids)), "duplicate ids")
arcs = [e["proof"]["archive"] for e in entries if e["id"] != "mirror34-finalcnf"]
need(len(arcs) == len(set(arcs)), "two entries share a proof archive")
for e in entries:
    for k in ("archive_sha256", "sha256"):
        need(re.fullmatch(r"[0-9a-f]{64}", e["proof"][k] or ""), f"{e['id']}: bad proof {k}")
    need(re.fullmatch(r"[0-9a-f]{64}", e["cnf"]["sha256"] or ""), f"{e['id']}: bad cnf sha256")
    need(isinstance(e["proof"]["bytes"], int), f"{e['id']}: proof bytes missing")

man = {"format": "es7-replay-manifest/1", "commit": COMMIT, "results_dir_hint": "cloud/es7-2026-10-19/results",
       "archive_root_hint": AROOT, "built": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime()),
       "tools": tools, "inputs": inputs, "cake_lpr_stack_mb": 4000,
       "notes": ["heap values are MiB (cake_lpr --CML_HEAP_SIZE); footprint GB ~= heap*1.048576 + 0.4",
                 "default = selected by replay.py when no --select is given",
                 "live: sources are local files of tonight's jobs, not committed; re-run this builder after the "
                 "pilot-orbits and LOCAL jobs finish to add their remaining units"],
       "problems": problems, "entries": entries}
json.dump(man, open(OUT_JSON, "w"), indent=1)

cols = ["id", "group", "default", "critical", "proof_archive", "archive_sha256", "proof_sha256", "proof_bytes",
        "cnf_method", "cnf_sha256", "heap_ladder_mb", "cake_footprint_gb_first", "cake_footprint_gb_max", "sources"]
with open(OUT_TSV, "w") as g:
    g.write("\t".join(cols) + "\n")
    for e in entries:
        meth = "+".join(m["kind"] for m in e["cnf"]["methods"])
        srcs = sorted({e["proof"]["source"].split(";")[0], e["cnf"]["source"].split(";")[0]})
        g.write("\t".join(str(x) for x in [
            e["id"], e["group"], e["default"], e["critical"], e["proof"]["archive"], e["proof"]["archive_sha256"],
            e["proof"]["sha256"], e["proof"]["bytes"], meth, e["cnf"]["sha256"], ",".join(map(str, e["heap_ladder_mb"])),
            e["replay_memory"]["cake_lpr_footprint_gb_first"], e["replay_memory"]["cake_lpr_footprint_gb_max"],
            " | ".join(srcs)]) + "\n")
from collections import Counter
print(len(entries), "entries;", dict(Counter(e["group"] for e in entries)))
print("problems:", problems if problems else "none")
