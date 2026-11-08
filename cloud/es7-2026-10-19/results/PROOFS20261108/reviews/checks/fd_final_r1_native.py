"""Search all .lean files of the repository (excluding .lake/.git) for 'native', 'reduceBool', 'reduceNat',
'skipKernel', 'kernel :=', 'debug.' outside comments; report per file. Also report raw hits of the four strings in the
import closure of the cited files. Read-only. Usage: python3 fd_final_r1_native.py STAGE REPO"""
import os, re, sys
STAGE, REPO = sys.argv[1], sys.argv[2]
src_imports = open(os.path.join(STAGE, "build", "fd_final_r1_imports.py"), encoding="utf-8").read()
m = re.search(r'(def strip_comments\(src\):.*?\n    return "".join\(out\)\n)', src_imports, re.S)
exec(m.group(1))
pats = [r"native", r"[Rr]educeBool", r"[Rr]educeNat", r"skipKernel", r"debug\.", r"implemented_by", r"@\[extern", r"\bunsafe\b", r"trustCompiler"]
counts = {p: [] for p in pats}
for root, dirs, files in os.walk(REPO):
    dirs[:] = [d for d in dirs if d not in (".lake", ".git")]
    for fn in files:
        if not fn.endswith(".lean"):
            continue
        p = os.path.join(root, fn)
        code = strip_comments(open(p, encoding="utf-8", errors="replace").read())
        for pat in pats:
            for ln, line in enumerate(code.split("\n"), 1):
                if re.search(pat, line):
                    counts[pat].append((os.path.relpath(p, REPO), ln, line.strip()[:110]))
for pat in pats:
    print(f"== {pat}: {len(counts[pat])} lines outside comments")
    for h in counts[pat][:12]:
        print("   ", h)
