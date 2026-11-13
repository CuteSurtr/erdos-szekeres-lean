"""Which .lean files import the four files with comment mentions of ofReduceBool, or their root modules. Read-only."""
import os, re, sys
STAGE, REPO = sys.argv[1], sys.argv[2]
src_imports = open(os.path.join(STAGE, "build", "fd_final_r1_imports.py"), encoding="utf-8").read()
m = re.search(r'(def strip_comments\(src\):.*?\n    return "".join\(out\)\n)', src_imports, re.S)
exec(m.group(1))
targets = {"EncB", "EncB.KernelCheck", "EncB.KernelCheckB", "D3Encoding", "D3Encoding.Audit", "ETVEncoding", "ETVEncoding.Audit"}
for root, dirs, files in os.walk(REPO):
    dirs[:] = [d for d in dirs if d not in (".lake", ".git")]
    for fn in files:
        if fn.endswith(".lean"):
            p = os.path.join(root, fn)
            code = strip_comments(open(p, encoding="utf-8", errors="replace").read())
            for mm in re.finditer(r"^\s*import\s+(.+)$", code, re.M):
                for mod in mm.group(1).split():
                    if mod in targets:
                        print(os.path.relpath(p, REPO), "imports", mod)
