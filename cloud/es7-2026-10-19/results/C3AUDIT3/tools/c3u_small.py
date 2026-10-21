"""run a compose.py (C3U/C3T tools dir) on a small (m, k): rebinds only M, K, BASE_SHA of the module.
usage: c3u_small.py TOOLSDIR m k BASE FILES... [opts]"""
import hashlib, importlib, os, sys
tools, m, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
sys.path.insert(0, os.path.join(tools, "..", "..", "C3a")); sys.path.insert(0, tools)
mod = importlib.import_module("compose")
mod.M, mod.K = m, k
mod.BASE_SHA = hashlib.sha256(open(sys.argv[4], "rb").read()).hexdigest()
sys.argv = ["compose.py"] + sys.argv[4:]
mod.main()
