#!/usr/bin/env python3
"""Mechanical check of the documentary sub-claims of finding A6-1 (read-only).
usage: doccheck_a61.py RESULTS_DIR
Each line prints TRUE/FALSE for a sub-claim, with the matching line numbers."""
import os, re, sys

R = sys.argv[1]
def lines(rel):
    return open(os.path.join(R, rel), encoding="utf-8").read().split("\n")
def find(rel, pat, flags=re.I):
    return [i + 1 for i, l in enumerate(lines(rel)) if re.search(pat, l, flags)]
def section(rel, start_pat, end_pat):
    L = lines(rel); s = e = None
    for i, l in enumerate(L):
        if s is None and re.match(start_pat, l): s = i
        elif s is not None and re.match(end_pat, l): e = i; break
    return "\n".join(L[s:e]), s + 1, (e or len(L))

def claim(text, ok, where=""):
    print(f"{'TRUE ' if ok else 'FALSE'} {text} {where}")

SY = "WRITEUP/SYMMETRIC.md"; CE = "WRITEUP/CERTIFICATES.md"; TX = "WRITEUP/note/symmetric_es7.tex"
claim("SYMMETRIC.md header says 'Revised 2026-10-29'", bool(find(SY, r"Revised 2026-10-29")), find(SY, r"Revised 2026-10-29"))
s3, a, b = section(SY, r"## 3\.", r"## 4\.")
s4, c, d = section(SY, r"## 4\.", r"## 5\.")
claim("§3 mentions the central case or 'open' at all", bool(re.search(r"central|parallelogram|\bopen\b", s3, re.I)), f"(§3 = lines {a}-{b})")
claim("§4 calls the parallelogram cases open", bool(re.search(r"parallelogram cases are open", s4)), find(SY, r"parallelogram cases are open"))
claim("Corollary 3 assumes the published fourfold exclusion", bool(find(SY, r"published fourfold exclusion")), find(SY, r"published fourfold exclusion"))
rep, e, f = section(SY, r"\*\*Checks actually replayed", r"\*\*Retained proofs")
heads = re.findall(r"^- ([A-Z][^:]+):", rep, re.M)
claim("'Checks actually replayed' covers only threefold/mirror/fivefold", all(re.match(r"(Threefold|Mirror|Fivefold)", h) for h in heads), heads)
claim("SYMMETRIC.md mentions C4CUT / the fourfold certificate", bool(find(SY, r"C4CUT|fourfold certificate|c4cut")))
claim("SYMMETRIC.md mentions deleted central-34 proofs / C2P / C2FINAL", bool(find(SY, r"C2P|C2FINAL|2,385|re-solve sample")))
for arch in ["es7-c4-32-cuts", "es7-central34-pilot-resolve", "es7-central34-resample"]:
    claim(f"CERTIFICATES.md has an entry for {arch}", bool(find(CE, re.escape(arch))))
claim("CERTIFICATES.md central34-cover says 'remains open'", bool(find(CE, r"remains open")), find(CE, r"remains open"))
claim("CERTIFICATES.md 'Not in the archive' mentions central-34 deleted proofs", bool(re.search(r"central|parallelogram|C2P", section(CE, r"## Not in the archive", r"## The threefold")[0], re.I)))
claim("C4CUT/README.md still says 'An independent review is pending'", bool(find("C4CUT/README.md", r"independent review is pending")), find("C4CUT/README.md", r"independent review is pending"))
claim("C4CUT/README.md still says 'conditional on the encoder review'", bool(find("C4CUT/README.md", r"conditional on the encoder review")), find("C4CUT/README.md", r"conditional on the encoder review"))
claim("C4CUT/review/README.md records a completed review", bool(find("C4CUT/review/README.md", r"No blocking or major finding")), find("C4CUT/review/README.md", r"No blocking or major finding"))
claim("C2FINAL/README.md §8 finding 6 flags SYMMETRIC.md as stale (minor)", bool(find("C2FINAL/README.md", r"6\. \*Minor\*: `C2C34/README.md` and `WRITEUP/SYMMETRIC.md` still describe")), find("C2FINAL/README.md", r"still describe the parallelogram"))
claim("C2FINAL/README.md says the central statement is not yet claimed", bool(find("C2FINAL/README.md", r"not yet claimed")), find("C2FINAL/README.md", r"not yet claimed"))
claim("C2P/README.md says every UNSAT proof was checked and then deleted", bool(find("C2P/README.md", r"Every UNSAT proof was checked by lrat-check and cake_lpr and then deleted")), find("C2P/README.md", r"then deleted"))
# not cited by the auditor, same direction
claim("[extra] LaTeX note says the parallelogram cases are open", bool(find(TX, r"parallelogram cases are open")), find(TX, r"parallelogram cases are open"))
claim("[extra] LaTeX note corollary assumes the fourfold exclusion of SMQH25", bool(find(TX, r"the fourfold exclusion")), find(TX, r"the fourfold exclusion"))
claim("[extra] C2C34/README.md says 'Status: open'", bool(find("C2C34/README.md", r"Status: open")), find("C2C34/README.md", r"Status: open"))
claim("[extra] C4CUT/final.json records archive (.zst) SHA-256", bool(find("C4CUT/final.json", r"archive_sha256|zst")))
