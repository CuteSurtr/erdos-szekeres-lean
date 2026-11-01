import sys, json, os, time
sys.argv=[sys.argv[0]]+sys.argv[1:]
sys.path.insert(0,'/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools')
import close_tree as ct
ct.WORK="/opt/work/rc"; os.makedirs(ct.WORK,exist_ok=True)
node, cap = sys.argv[1], int(sys.argv[2])
r = ct.solve(("/opt/work/base.cnf", node, cap, "/opt/work/models", ["--sat"]))
r["recheck"]="alone, sequential checkers"; r["time"]=time.strftime("%H:%M:%S",time.gmtime())
print(json.dumps(r))
