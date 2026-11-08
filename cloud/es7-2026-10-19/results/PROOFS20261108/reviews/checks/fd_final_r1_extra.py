"""Outside-comment search of all tracked .lean files for further strings (information only). Read-only."""
import os, re, sys
STAGE, REPO = sys.argv[1], sys.argv[2]
src_imports = open(os.path.join(STAGE, "build", "fd_final_r1_imports.py"), encoding="utf-8").read()
m = re.search(r'(def strip_comments\(src\):.*?\n    return "".join\(out\)\n)', src_imports, re.S)
exec(m.group(1))
pats = [r"bv_decide", r"bv_check", r"reduceBool", r"reduceNat", r"Kernel", r"addDecl", r"WithoutChecking", r"set_option"]
hits = {p: [] for p in pats}
for root, dirs, files in os.walk(REPO):
    dirs[:] = [d for d in dirs if d not in (".lake", ".git")]
    for fn in files:
        if fn.endswith(".lean"):
            p = os.path.join(root, fn)
            code = strip_comments(open(p, encoding="utf-8", errors="replace").read())
            for pat in pats:
                for ln, line in enumerate(code.split("\n"), 1):
                    if re.search(pat, line):
                        hits[pat].append((os.path.relpath(p, REPO), ln, line.strip()[:100]))
for pat in pats:
    print(f"== {pat}: {len(hits[pat])}")
    if pat == "set_option":
        opts = {}
        for h in hits[pat]:
            mm = re.search(r"set_option\s+(\S+)", h[2])
            if mm:
                opts[mm.group(1)] = opts.get(mm.group(1), 0) + 1
        print("   options set:", sorted(opts.items(), key=lambda x: -x[1]))
    else:
        for h in hits[pat][:8]:
            print("   ", h)
