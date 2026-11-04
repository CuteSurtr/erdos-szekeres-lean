#!/usr/bin/env python3
"""Bounded single-solver lane; formulas and models retained with checked archives."""
import argparse, datetime, hashlib, importlib.util, json, sys, time
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--archive',type=Path,required=True);p.add_argument('--bin',type=Path)
    p.add_argument('--generate',type=int);p.add_argument('--file');p.add_argument('--name')
    p.add_argument('--seconds',type=int,default=180);p.add_argument('--proof',action='store_true')
    a=p.parse_args();a.archive.mkdir(parents=True,exist_ok=True)
    h=load(ROOT/'C6C7REVIEW/m5_pilot.py','prior_lane');h.LOG=HERE/'logs'
    h.LOG.mkdir(exist_ok=True)
    manifests=json.loads((a.archive/'m5_manifest.json').read_text()) if (a.archive/'m5_manifest.json').exists() else []
    def keep(path):
        row=h.archived(path);manifests.append(row);h.save(a.archive/'m5_manifest.json',manifests)
        print(json.dumps({'archive':row}),flush=True)
    if a.generate:
        import subprocess
        f=a.archive/f'm5K8t{a.generate}.cnf'
        r=subprocess.run([sys.executable,'-I',str(ROOT/'C7UPPER/gen.py'),'5','8',str(a.generate),str(f)],capture_output=True,text=True,check=True)
        (h.LOG/f'm5_generate_t{a.generate}.log').write_text(r.stdout)
        keep(f);keep(f.with_name(f.name+'.json'));return
    assert a.file and a.name and a.bin
    assert not a.proof, 'Proof creation is handled separately after an UNSAT pilot.'
    a.scratch=a.archive/'m5_scratch';a.scratch.mkdir(exist_ok=True);a.memory_limit=29000000000
    # Native child-RSS guard supplements the retained helper's system guard.
    # It is activated only for runs started with this wrapper version.
    import ctypes
    resource=load(HERE/'m5_proof_lane.py','native_child_resource')
    native=ctypes.CDLL('/usr/lib/libproc.dylib',use_errno=True)
    native.proc_pid_rusage.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_void_p]
    native.proc_pid_rusage.restype=ctypes.c_int
    system_memory=h.memory_bytes;child_peak=0;child_guard=False;actual_system_peak=0
    def monitored_memory():
        nonlocal child_peak,child_guard,actual_system_peak
        used=system_memory();active=a.scratch/'active.json'
        actual_system_peak=max(actual_system_peak,used)
        if active.exists():
            pid=json.loads(active.read_text())['pid'];info=resource.RUsageInfo()
            rc=native.proc_pid_rusage(pid,0,ctypes.byref(info))
            if rc==0:child_peak=max(child_peak,info.resident_size)
            elif ctypes.get_errno()!=3:raise RuntimeError('native child resource monitor failed')
        child_guard=child_guard or child_peak>=3000000000
        return max(used,a.memory_limit) if child_guard else used
    h.memory_bytes=monitored_memory
    hard=datetime.datetime(2026,11,3,19,0,tzinfo=datetime.timezone.utc).timestamp()
    remaining=hard-time.time();assert remaining>5
    a.seconds=min(a.seconds,int(remaining-5))
    f=a.archive/a.file;keep(f)
    if a.name.startswith('t12_families') and (a.archive/'m5_stop_cycle_lane').exists():
        result={'job':a.name,'verdict':'DEFERRED_FOR_INTERIORITY','all_children_stopped':True,
                'cnf_sha256':h.sha(f),'reason':'Switch the next solver allocation to affine-interiority refinement.'}
        h.save(h.LOG/('m5_'+a.name+'.json'),result);h.save(a.archive/(a.name+'.run.json'),result)
        print(json.dumps({'completed':result}),flush=True);return
    result=h.run_one(a,{'name':a.name,'file':a.file},time.monotonic()+remaining)
    result['sampled_child_peak_bytes']=child_peak
    result['system_memory_peak_bytes']=actual_system_peak
    if child_guard:result['guard']='child_memory_guard'
    if result['exit_code']==10:
        raw=a.archive/result['sat_model_file']
        positive=sorted(x for line in raw.read_text().splitlines() if line.startswith('v ')
                        for x in map(int,line[2:].split()) if x>0)
        model=a.archive/(a.name+'.model.json');model.write_text(json.dumps(positive)+'\n')
        keep(model);keep(raw);result['positive_model']=model.name;result['positive_model_sha256']=h.sha(model)
        import subprocess
        checklog=h.LOG/('m5_'+a.name+'_assignment.json')
        subprocess.run([sys.executable,'-I',str(ROOT/'C6C7REVIEW/m6_verify_assignment.py'),
                        '--cnf',str(f),'--model',str(model),'--out',str(checklog)],check=True)
        result['assignment_check_sha256']=h.sha(checklog)
    result['helper_sha256']=h.sha(ROOT/'C6C7REVIEW/m5_pilot.py')
    result['solver_sha256']=h.sha(a.bin/'cadical')
    result['all_children_stopped']=True
    h.save(h.LOG/('m5_'+a.name+'.json'),result)
    h.save(a.archive/(a.name+'.run.json'),result)
    print(json.dumps({'completed':result}),flush=True)

if __name__=='__main__':main()
