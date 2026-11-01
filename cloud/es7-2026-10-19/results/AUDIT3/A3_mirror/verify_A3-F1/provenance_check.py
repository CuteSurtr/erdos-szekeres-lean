#!/usr/bin/env python3
"""Provenance check for finding A3-F1 (read-only).
1. Is any replay record for mirror33 / mirror34 committed in the es7-cloud tree (HEAD of the worktree)?
2. Does the 2026-10-29 audit's mirror34 replay record exist, where, and is it tracked by git?
3. Do its hashes match CERTIFICATES.md, and do its lrat-check statistics match the solve-time log?
"""
import json, re, subprocess, sys, hashlib, os
R = os.path.abspath(os.environ.get("ES7_RESULTS", "."))
W = os.path.normpath(os.path.join(R, "..", "..", ".."))  # repository root
MAIN = os.environ["MAIN_REPO"]  # local checkout of the main repository
AUD = os.environ["AUDIT_1029_DIR"]  # untracked directory of the 2026-10-29 audit, relative to MAIN_REPO

def git(*a, cwd=W):
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True).stdout

# 1. committed tree at HEAD
head = git("rev-parse", "HEAD").strip()
print("worktree HEAD", head)
hits = git("grep", "-l", "-I", "-E", r"m33_def|e1b2689d|mr34_def|98e4d02a", "HEAD", "--")
print("files at HEAD mentioning mirror proofs:")
for h in hits.split():
    print("   ", h)
rep = [h for h in hits.split() if re.search(r"replay", h, re.I)]
print("files at HEAD whose path names a replay:", rep or "none")
print("HEAD tree contains", AUD, ":", bool(git("ls-tree", "-d", "HEAD", AUD).strip()))

# 2. refs containing the audit directory
refs = git("for-each-ref", "--format=%(refname) %(objectname)").split("\n")
holders = []
for line in refs:
    if not line.strip():
        continue
    name, obj = line.split()
    if git("ls-tree", "-d", obj, AUD).strip():
        holders.append(name)
print("refs whose tree contains the audit dir:", holders)
st = git("status", "--porcelain", "--", AUD, cwd=MAIN)
print("main working tree git status of audit dir:", st.strip() or "(tracked, clean)")

# 3. record contents vs certificates
cert = open(R + "/WRITEUP/CERTIFICATES.md").read()
rj = json.load(open(os.path.join(MAIN, AUD, "mirror34-lrat-replay.json")))
for k, v in rj["hashes"].items():
    print(f"replay hash {k}: {v[:16]}...  in CERTIFICATES.md: {v in cert}")
print("replay exit_code", rj["exit_code"], "elapsed", round(rj["elapsed_seconds"], 2), "verified", rj["log_reports_verified"])
stat_re = re.compile(r"^c (parsed a formula.*|VERIFIED|Added clauses.*)$", re.M)
replay_log = open(os.path.join(MAIN, AUD, "mirror34-lrat-replay.log")).read()
solve_log = open(R + "/SYMZ/logs/chk_mr34_def_lrat-check.out").read()
a, b = stat_re.findall(replay_log), stat_re.findall(solve_log)
print("replay stats :", a)
print("solve stats  :", b)
print("statistics identical:", a == b)
for f in ["mirror34-lrat-replay.log", "mirror34-lrat-replay.json"]:
    print(f, hashlib.sha256(open(os.path.join(MAIN, AUD, f), "rb").read()).hexdigest())
# 4. any mirror33 replay anywhere in the audit dir?
m33 = [f for f in os.listdir(os.path.join(MAIN, AUD)) if "33" in f and "replay" in f]
print("mirror33 replay files in audit dir:", m33 or "none")
