"""pc polish-1 diff audit: compare statement environments of pc.tex with pc.map.tsv, and check every
\\leanref file:line against the declaration line in the Lean source (read-only)."""
import re
import sys

STAGE = sys.argv[1]
RES = sys.argv[2]
src = open(f"{STAGE}/sections/pc.tex").read()
rows = [l.rstrip("\n").split("\t") for l in open(f"{STAGE}/sections/pc.map.tsv")][1:]

env_re = re.compile(r"\\begin\{(theorem|lemma|proposition|corollary|fact|definition|remark)\}")
starts = [(m.start(), m.group(1)) for m in env_re.finditer(src)]
envs = []
for i, (pos, kind) in enumerate(starts):
    end = src.index("\\end{%s}" % kind, pos)
    body = src[pos:end]
    lab = re.search(r"\\label\{([^}]*)\}", body).group(1)
    refs = re.findall(r"\\leanref\{([^}]*)\}\{([^}]*)\}", body)
    envs.append((lab, kind, refs))

print("environments:", len(envs), "map rows:", len(rows))
bad = 0
for (lab, kind, refs), r in zip(envs, rows):
    mlab, mkind, mlean, mfl = r[0], r[1], r[2], r[3]
    names = [x.strip() for x in mlean.split(";")] if mlean.strip() != "-" else []
    fls = [x.strip() for x in mfl.split(";")] if mfl.strip() != "-" else []
    tex_names = [a for a, b in refs]
    tex_fls = [b for a, b in refs]
    ok = (lab == mlab and kind == mkind and tex_names == names and tex_fls == fls)
    if not ok:
        bad += 1
        print("MISMATCH", lab, mlab, kind, mkind, tex_names, names, tex_fls, fls)
print("map mismatches:", bad)

# every \leanref points at the declaration line of the named constant
allrefs = re.findall(r"\\leanref\{([^}]*)\}\{([^}]*)\}", src)
nbad = 0
for name, fl in allrefs:
    f, line = fl.rsplit(":", 1)
    lines = open(f"{RES}/{f}").read().split("\n")
    text = lines[int(line) - 1]
    short = name.split(".")[-1]
    if not re.match(r"^(theorem|lemma|def|noncomputable def|structure|abbrev)\s+" + re.escape(short) + r"(\s|$)", text):
        nbad += 1
        print("LINE MISMATCH", name, fl, repr(text[:90]))
print("leanrefs:", len(allrefs), "line mismatches:", nbad)
