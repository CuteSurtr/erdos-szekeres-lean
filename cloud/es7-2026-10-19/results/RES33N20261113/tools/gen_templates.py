"""Enumerate all instances of the 8 existing coupled templates (same semantics as ES8SLACK template_closure_probe)."""
import importlib.util, json, sys, time
LIB = '/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/ES8SLACK/review/C3_residual/template_search_lib.py'
spec = importlib.util.spec_from_file_location('ti', LIB); ti = importlib.util.module_from_spec(spec); spec.loader.exec_module(ti)
out = {}
for name, (k, crit) in ti.TPL.items():
    res = ti.search(k, crit, list(range(154)), 600.0, stop_after=None, keep_all=True)
    out[name] = {'complete': res['complete'], 'supports': res['supports']}
    print(name, res['complete'], len(res['supports']), res['seconds'], flush=True)
json.dump(out, open('templates.json', 'w'))
