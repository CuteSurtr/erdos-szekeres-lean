"""Generator of lean/RowGeo/Eight.lean (the 64-case proof of `no_eight`), saved after the fact: this is the code
that wrote the file on 22 Nov 2026 (~18:30 KST, run as a heredoc). Do not re-run without recompiling everything
downstream of RowGeo.Eight (DESIGN.md §7). Its output is checked by Lean (no trust in this script)."""
import itertools, sys
OUT = '/home/jay/research/data/formalize-20261122/n66-rowsvalid/lean/RowGeo/Eight.lean'
if '--write' not in sys.argv:
    raise SystemExit('refusing to overwrite Eight.lean without --write (see docstring)')
# (header text identical to the file's lines 1-58; omitted here, see the file itself)
lines = open(OUT).read().split('\n')
head = lines[:lines.index('  cases s1 : M.cup (q 0) (q 1) (q 7) <;> cases s2 : M.cup (q 0) (q 2) (q 7) <;>')]
lines = head
lines.append("  cases s1 : M.cup (q 0) (q 1) (q 7) <;> cases s2 : M.cup (q 0) (q 2) (q 7) <;>")
lines.append("    cases s3 : M.cup (q 0) (q 3) (q 7) <;> cases s4 : M.cup (q 0) (q 4) (q 7) <;>")
lines.append("    cases s5 : M.cup (q 0) (q 5) (q 7) <;> cases s6 : M.cup (q 0) (q 6) (q 7)")
def c(i, j, k):
    return f"((r {i} {j} {k} (by decide) (by decide)).trans s{j})"
for pat in itertools.product([False, True], repeat=6):
    U = [m for m in range(1, 7) if not pat[m - 1]]
    L = [m for m in range(1, 7) if pat[m - 1]]
    if len(U) >= 4 or len(L) >= 4:
        col, V, fld = (False, U, 'noCap6') if len(U) >= 4 else (True, L, 'noCup6')
        pts = [0] + V[:4] + [7]
        cs = [c(pts[t], pts[t + 1], pts[t + 2]) for t in range(4)]
        lts = ' '.join(f"(lt {pts[t]} {pts[t + 1]} (by decide))" for t in range(5))
        lines.append(f"  · exact M.{fld} (q {V[3]}) (q 7) h7 (ep6 M.cup {'true' if col else 'false'} {lts} {' '.join(cs)})")
    else:
        def path(Vs, col):
            pts = [0] + Vs + [7]
            cs = [c(pts[t], pts[t + 1], pts[t + 2]) for t in range(3)]
            lts = ' '.join(f"(lt {pts[t]} {pts[t + 1]} (by decide))" for t in range(4))
            return f"(se5 M.cup {'true' if col else 'false'} {lts} {' '.join(cs)})"
        lines.append(f"  · exact M.noCapCup55 (q 0) (q {U[2]}) (q {L[2]}) (q 7) h7 {path(U, False)} {path(L, True)}")
lines += ['', 'end RowGeo', '']
open(OUT, 'w').write('\n'.join(lines))
