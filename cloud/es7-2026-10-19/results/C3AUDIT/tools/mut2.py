import sys, runpy, random
sys.path.insert(0, "/opt/audit/ind")
import indep
orig = indep.truth
def bad(E, lab, sig, order, m):
    v = orig(E, lab, sig, order, m)
    ts = sorted({abs(l) for l in E.T.values()}); x = random.choice(ts); v[x] = not v[x]; return v
indep.truth = bad
sys.argv = ["drive.py"] + sys.argv[1:]
g = runpy.run_path("/opt/audit/ind/drive.py", init_globals={}, run_name="__main__")
