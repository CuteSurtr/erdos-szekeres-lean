"""Transitive project imports of the cited Lean files (list from fd_final_r1_cited_files.txt), plus the .lean files of
directories cited in the sections, and a raw and comment-free search of the closure for the four strings.
Read-only. Usage: python3 fd_final_r1_imports.py STAGE REPO"""
import os
import re
import sys

STAGE, REPO = sys.argv[1], sys.argv[2]
RES = os.path.join(REPO, "cloud/es7-2026-10-19/results")
TERMS = ["+native", "ofReduceBool", "ofReduceNat", "skipKernelTC"]
KEYS = ["fd", "ll", "lg", "oc", "pc", "ec", "sr", "ar", "mm", "mb", "cb", "sa"]


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


allfiles = []
for root, dirs, files in os.walk(REPO):
    dirs[:] = [d for d in dirs if d not in (".lake", ".git")]
    for fn in files:
        if fn.endswith(".lean"):
            allfiles.append(os.path.join(root, fn))

with open(os.path.join(STAGE, "build", "fd_final_r1_cited_files.txt"), encoding="utf-8") as f:
    cited = [os.path.join(REPO, line.split("\t")[0]) for line in f if line.strip()]

# directories cited with \dirn{...} in the sections: add their .lean files (non-recursive and recursive variants)
dir_tokens = set()
for k in KEYS:
    with open(os.path.join(STAGE, "sections", k + ".tex"), encoding="utf-8") as f:
        t = f.read()
    for m in re.finditer(r"\\dirn\{([^}]*)\}", t):
        d = m.group(1).rstrip("/").split(":")[0]
        for base in (RES, REPO):
            p = os.path.join(base, d)
            if os.path.isdir(p):
                dir_tokens.add(p)
dir_files = set()
for d in dir_tokens:
    for root, dirs, files in os.walk(d):
        dirs[:] = [x for x in dirs if x not in (".lake", ".git")]
        for fn in files:
            if fn.endswith(".lean"):
                dir_files.add(os.path.join(root, fn))

imp_re = re.compile(r"^\s*import\s+(.+)$", re.M)


def resolve_module(mod, importer):
    rel = mod.replace(".", "/") + ".lean"
    hits = [p for p in allfiles if p.endswith("/" + rel)]
    if not hits:
        return None
    # prefer the candidate that shares the longest directory prefix with the importer
    def common(p):
        return len(os.path.commonpath([p, importer]))
    hits.sort(key=common, reverse=True)
    return hits[0]


closure = set()
external = set()
stack = list(cited)
while stack:
    p = stack.pop()
    if p in closure:
        continue
    closure.add(p)
    with open(p, encoding="utf-8", errors="replace") as f:
        src = strip_comments(f.read())
    for m in imp_re.finditer(src):
        for mod in m.group(1).split():
            q = resolve_module(mod, p)
            if q is None:
                external.add(mod.split(".")[0])
            else:
                stack.append(q)

print("cited files:", len(cited))
print("import closure (project files):", len(closure), "; added by imports:", len(closure - set(cited)))
for p in sorted(closure - set(cited)):
    print("  import-only:", os.path.relpath(p, REPO))
print("external import roots:", sorted(external))
print("cited directories:", len(dir_tokens), "; their .lean files:", len(dir_files))

everything = closure | dir_files
raw, code = [], []
for p in sorted(everything):
    with open(p, encoding="utf-8", errors="replace") as f:
        src = f.read()
    c = strip_comments(src)
    for term in TERMS:
        if term in src:
            raw.append((os.path.relpath(p, REPO), term))
        if term in c:
            code.append((os.path.relpath(p, REPO), term))
print("files searched (closure + cited directories):", len(everything))
print("raw hits:", raw)
print("hits outside comments:", code)
outside = [os.path.relpath(p, REPO) for p in everything
           if not os.path.relpath(p, REPO).startswith(("cloud/es7-2026-10-19/results/", "ErdosSzekeres/"))]
print("files outside RES and ErdosSzekeres:", outside)
