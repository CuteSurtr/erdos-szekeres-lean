"""List the Lean files cited in the twelve sections (and the front matter of proofs.tex), resolve them in the
repository, and search each one for the strings +native, ofReduceBool, ofReduceNat, skipKernelTC, both raw and
outside comments. Read-only. Usage: python3 fd_final_r1_cited.py STAGE REPO"""
import os
import re
import sys

STAGE, REPO = sys.argv[1], sys.argv[2]
RES = os.path.join(REPO, "cloud/es7-2026-10-19/results")
KEYS = ["fd", "ll", "lg", "oc", "pc", "ec", "sr", "ar", "mm", "mb", "cb", "sa"]
TERMS = ["+native", "ofReduceBool", "ofReduceNat", "skipKernelTC"]

texts = {}
for k in KEYS:
    with open(os.path.join(STAGE, "sections", k + ".tex"), encoding="utf-8") as f:
        texts[k] = f.read()
with open(os.path.join(STAGE, "proofs.tex"), encoding="utf-8") as f:
    texts["front"] = f.read()

# 1. every token that ends in .lean (with an optional :line suffix), anywhere in the text
tok = re.compile(r"([A-Za-z0-9_./\-]+\.lean)")
# 2. the file argument of every \leanref head
lref = re.compile(r"\\leanref\{([^}]*)\}\{([^}]*)\}")

cited = {}  # token -> set of sections
heads = {}  # token -> set of sections (only \leanref file arguments)
for k, t in texts.items():
    for m in tok.finditer(t):
        cited.setdefault(m.group(1), set()).add(k)
    for m in lref.finditer(t):
        f = m.group(2).split(":")[0]
        heads.setdefault(f, set()).add(k)
        cited.setdefault(f, set()).add(k)

# index of all .lean files in the repository (excluding .lake), by relative path and by basename
allfiles = []
for root, dirs, files in os.walk(REPO):
    dirs[:] = [d for d in dirs if d not in (".lake", ".git")]
    for fn in files:
        if fn.endswith(".lean"):
            allfiles.append(os.path.join(root, fn))
bybase = {}
for p in allfiles:
    bybase.setdefault(os.path.basename(p), []).append(p)


def resolve(token):
    cands = []
    if token.startswith("ErdosSzekeres/") or token.startswith("experiments/") or token.startswith("scripts/"):
        cands.append(os.path.join(REPO, token))
    cands.append(os.path.join(RES, token))
    cands.append(os.path.join(REPO, token))
    for c in cands:
        if os.path.isfile(c):
            return [c]
    # bare or partial name: match by suffix among all files
    hits = [p for p in allfiles if p.endswith("/" + token)]
    return hits


def strip_comments(src):
    """Remove Lean comments: nested block comments /- ... -/ (including doc comments) and line comments --.
    String literals are respected so that "--" or "/-" inside a string does not start a comment."""
    out = []
    i, n, depth = 0, len(src), 0
    in_str = False
    while i < n:
        c = src[i]
        if depth == 0 and not in_str:
            if src.startswith("/-", i):
                depth = 1
                i += 2
                continue
            if src.startswith("--", i):
                j = src.find("\n", i)
                if j < 0:
                    break
                i = j
                continue
            if c == '"':
                in_str = True
                out.append(c)
                i += 1
                continue
            out.append(c)
            i += 1
        elif in_str:
            if c == "\\" and i + 1 < n:
                out.append(src[i:i + 2])
                i += 2
                continue
            if c == '"':
                in_str = False
            out.append(c)
            i += 1
        else:
            if src.startswith("/-", i):
                depth += 1
                i += 2
                continue
            if src.startswith("-/", i):
                depth -= 1
                i += 2
                if depth == 0:
                    out.append(" ")
                continue
            if c == "\n":
                out.append("\n")
            i += 1
    return "".join(out)


resolved = {}
unresolved = []
ambiguous = []
for token in sorted(cited):
    hits = resolve(token)
    if not hits:
        unresolved.append(token)
    elif len(hits) > 1:
        ambiguous.append((token, hits))
        for h in hits:
            resolved[h] = resolved.get(h, set()) | {token}
    else:
        resolved[hits[0]] = resolved.get(hits[0], set()) | {token}

print("cited tokens:", len(cited), " of which \\leanref file arguments:", len(heads))
print("resolved files:", len(resolved))
print("unresolved tokens:", unresolved)
for token, hits in ambiguous:
    print("ambiguous:", token, "->", [os.path.relpath(h, REPO) for h in hits])

raw_hits, code_hits = [], []
for path in sorted(resolved):
    with open(path, encoding="utf-8", errors="replace") as f:
        src = f.read()
    code = strip_comments(src)
    for term in TERMS:
        for ln, line in enumerate(src.split("\n"), 1):
            if term in line:
                raw_hits.append((os.path.relpath(path, REPO), ln, term, line.strip()))
        for ln, line in enumerate(code.split("\n"), 1):
            if term in line:
                code_hits.append((os.path.relpath(path, REPO), ln, term, line.strip()))

print("raw hits (including comments):", len(raw_hits))
for h in raw_hits:
    print("  RAW", h)
print("hits outside comments:", len(code_hits))
for h in code_hits:
    print("  CODE", h)

# also: the same search over every .lean file of RES and of ErdosSzekeres (a superset)
sup_raw, sup_code = 0, []
for path in allfiles:
    rel = os.path.relpath(path, REPO)
    if not (rel.startswith("cloud/es7-2026-10-19/results/") or rel.startswith("ErdosSzekeres/")):
        continue
    with open(path, encoding="utf-8", errors="replace") as f:
        src = f.read()
    code = strip_comments(src)
    for term in TERMS:
        sup_raw += src.count(term)
        if term in code:
            sup_code.append((rel, term))
print("superset (all .lean under RES and ErdosSzekeres):",
      sum(1 for p in allfiles if os.path.relpath(p, REPO).startswith(("cloud/es7-2026-10-19/results/", "ErdosSzekeres/"))),
      "files; raw occurrences:", sup_raw, "; files with occurrences outside comments:", sup_code)

with open(os.path.join(STAGE, "build", "fd_final_r1_cited_files.txt"), "w", encoding="utf-8") as f:
    for path in sorted(resolved):
        f.write(os.path.relpath(path, REPO) + "\t" + ",".join(sorted(resolved[path])) + "\n")
