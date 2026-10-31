"""C3AUDIT4: run one composer in-process on (m, k) and print its verdict, its full frontier and the
set of open depth-2 roots (read from the composer's own locals when it prints its summary).
usage: runcomp.py WHO m k BASE FILES... [--no-sha] [--mirror-h6]
  WHO = path of a C3U-style tools dir (compose.py; M, K, BASE_SHA rebound as C3AUDIT3/tools/c3u_small.py)
        or 'mine' (C3AUDIT3/tools/mycompose.py, fixed version)."""
import builtins, hashlib, importlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "..")
who, m, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
rest = sys.argv[4:]
sys.path.insert(0, os.path.join(R, "C3a"))
out = {}


def grab(*a, **kw):
    j = json.loads(a[0])
    if "error" in j:
        out["error"] = j["error"]; return
    f = sys._getframe(1)
    while f and "missing" not in f.f_locals:
        f = f.f_back
    L = f.f_locals
    j = json.loads(a[0])
    out["covered"] = j.get("class_covered")
    out["frontier"] = sorted(set(L["missing"]))
    out["frontier_n"] = len(L["missing"])
    memo = L["memo"]
    d2 = []
    for key, v in memo.items():
        name = key if isinstance(key, str) else mod.kname(key)
        if name != "ROOT" and name and "__" not in name and name.count("_") == 1 and v is False:
            d2.append(name)
    d1 = [n for n, v in ((key if isinstance(key, str) else mod.kname(key), v) for key, v in memo.items())
          if n and n != "ROOT" and "__" not in n and n.count("_") == 0 and v is False]
    out["open_d1"] = sorted(d1)
    out["open_d2"] = sorted(d2)
    out["summary"] = j


if who == "mine":
    sys.path.insert(0, os.path.join(R, "C3AUDIT3", "tools"))
    mod = importlib.import_module("mycompose")
    sys.argv = ["mycompose.py", "--m", str(m), "--k", str(k)] + [x for x in rest if x != "--mirror-h6"]
    if "--mirror-h6" in rest:
        sys.path.insert(0, HERE)
        import myh6
        myh6.install(mod)
else:
    sys.path.insert(0, who)
    mod = importlib.import_module("compose")
    mod.M, mod.K = m, k
    mod.BASE_SHA = hashlib.sha256(open(rest[0], "rb").read()).hexdigest()
    sys.argv = ["compose.py"] + rest
mod.print = grab
try:
    mod.main()
except SystemExit as e:
    if e.code:
        print(json.dumps({"reject": True, "code": e.code, "error": out.get("error")})); sys.exit(0)
if "covered" not in out:
    print(json.dumps({"reject": True, "code": "noout"})); sys.exit(0)
print(json.dumps(out))
