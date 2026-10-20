import sys, itertools, subprocess, json
sys.path.insert(0, "/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/tools/realizer")
from chiro import largest_convex_subset, chirotope_of
exec(open("/tmp/claude-0/-home-user-erdos-szekeres-lean/7d9c6ca0-022c-5e66-8370-d636a42cff9f/scratchpad/ctl_brute.py").read().split("sets=[]")[0])
for f in sys.argv[1:]:
    P = [tuple(map(int, l.split())) for l in open(f) if l.strip()]
    xs = [p[0] for p in P]
    chirotope_of(P)  # raises on collinear
    b = bits(P)
    br = subprocess.run(["./brute", "26", "40"], input=b + "\n", capture_output=True, text=True).stdout.split()
    print(json.dumps({"file": f, "n": len(P), "distinct_x": len(set(xs)) == len(P), "general_position": True,
          "python_cap_cup": capcup(P), "lcs_exact": largest_convex_subset(P),
          "brute(axioms,cap,cup,lcs)": br[1:], "max_abs": max(max(abs(x), abs(y)) for x, y in P)}))
