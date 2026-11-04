#!/usr/bin/env python3
"""One bounded native solver, retained text LRAT, and explicit process cleanup.

An UNKNOWN run's partial proof is an archived search artifact, not a certificate.
This lane never invokes a proof checker. Its native child resource monitor is
specific to macOS; the solver and archive locations are command-line inputs.
"""
import argparse, ctypes, datetime, importlib.util, json, os, re, signal, subprocess, sys, time
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent

class RUsageInfo(ctypes.Structure):
    _fields_=[('uuid',ctypes.c_ubyte*16)]+[(x,ctypes.c_uint64) for x in
        ('user_time','system_time','package_idle_wakeups','interrupt_wakeups',
         'pageins','wired_size','resident_size','phys_footprint','proc_start_abstime','proc_exit_abstime')]

def main():
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True)
    p.add_argument('--bin',type=Path,required=True);p.add_argument('--file',required=True)
    p.add_argument('--name',required=True);p.add_argument('--seconds',type=int,default=600)
    p.add_argument('--memory-limit',type=int,default=29000000000)
    p.add_argument('--child-memory-limit',type=int,default=3000000000)
    a=p.parse_args();a.archive=a.archive.resolve()
    spec=importlib.util.spec_from_file_location('retained_helpers',HERE.parent/'C6C7REVIEW/m5_pilot.py')
    h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
    scratch=a.archive/'m5_scratch';scratch.mkdir(exist_ok=True)
    assert not (scratch/'active.json').exists(),'another lane is active'
    proof=a.archive/(a.name+'.lrat');assert not proof.exists(),'refuse to overwrite proof'
    hard=datetime.datetime(2026,11,3,19,0,tzinfo=datetime.timezone.utc).timestamp()
    remaining=hard-time.time();assert remaining>20
    seconds=min(a.seconds,int(remaining-10));source=a.archive/a.file
    inputs=[h.archived(source)];raw=scratch/(a.name+'.raw.log')
    lib=ctypes.CDLL('/usr/lib/libproc.dylib',use_errno=True)
    lib.proc_pid_rusage.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_void_p]
    lib.proc_pid_rusage.restype=ctypes.c_int
    start=time.monotonic();peak=0;child_peak=0;reason=None;usage=None
    cmd=[str(a.bin/'cadical'),'-t',str(seconds),'--lrat','--binary=false',a.file,proof.name]
    with raw.open('w') as output:
        proc=subprocess.Popen(cmd,cwd=a.archive,stdout=output,stderr=subprocess.STDOUT,start_new_session=True)
        h.save(scratch/'active.json',{'pid':proc.pid,'job':a.name,'proof':proof.name})
        try:
            while True:
                pid,status,ru=os.wait4(proc.pid,os.WNOHANG)
                if pid:
                    proc.returncode=os.waitstatus_to_exitcode(status);usage=ru;break
                used=h.memory_bytes();peak=max(peak,used)
                info=RUsageInfo();rc=lib.proc_pid_rusage(proc.pid,0,ctypes.byref(info))
                if rc==0:child_peak=max(child_peak,info.resident_size)
                elif ctypes.get_errno()!=3:reason='resource_monitor_error'
                if used>=a.memory_limit:reason='system_memory_guard'
                if child_peak>=a.child_memory_limit:reason='child_memory_guard'
                if time.time()>=hard-5 or time.monotonic()-start>=seconds+15:reason='wall_guard'
                if reason:
                    os.killpg(proc.pid,signal.SIGTERM);time.sleep(1)
                    pid,status,ru=os.wait4(proc.pid,os.WNOHANG)
                    if not pid:
                        os.killpg(proc.pid,signal.SIGKILL);pid,status,ru=os.wait4(proc.pid,0)
                    proc.returncode=os.waitstatus_to_exitcode(status);usage=ru;break
                time.sleep(2)
        finally:
            if proc.returncode is None:
                os.killpg(proc.pid,signal.SIGKILL);proc.wait()
            (scratch/'active.json').unlink(missing_ok=True)
    wall=time.monotonic()-start
    raw_content=raw.read_text();content=h.sanitize(raw_content)
    log=HERE/'logs'/('m5_'+a.name+'.log');log.write_text(content);raw.unlink()
    verdict=('UNSAT_REQUIRES_PROOF_REPLAY' if proc.returncode==20 else
             'SAT_ABSTRACT' if proc.returncode==10 else 'UNKNOWN')
    result={'job':a.name,'exit_code':proc.returncode,'verdict':verdict,
        'seconds_limit':seconds,'wall_seconds':round(wall,3),'guard':reason,
        'system_memory_peak_bytes':peak,'sampled_child_peak_bytes':child_peak,
        'cnf_sha256':h.sha(source),'solver_sha256':h.sha(a.bin/'cadical'),
        'wrapper_sha256':h.sha(Path(__file__)),'log_sha256':h.sha(log),
        'child_stopped':True,'all_children_stopped':True,
        'proof_file':proof.name,'proof_status':('pending replay' if proc.returncode==20 else 'partial, not a certificate'),
        'solver_options':['-t',str(seconds),'--lrat','--binary=false']}
    if usage:result.update(cpu_seconds=round(usage.ru_utime+usage.ru_stime,3),peak_rss_bytes=usage.ru_maxrss)
    for key in ('conflicts','decisions','propagations','restarts'):
        hits=re.findall(r'^c\s+'+key+r':\s+([\d,]+)',content,re.M)
        if hits:result[key]=int(hits[-1].replace(',',''))
    if proc.returncode==10:
        positive=sorted(x for line in raw_content.splitlines() if line.startswith('v ')
                        for x in map(int,line[2:].split()) if x>0)
        model=a.archive/(a.name+'.model.json');model.write_text(json.dumps(positive)+'\n')
        result['positive_model']=model.name;result['positive_model_sha256']=h.sha(model)
        checklog=HERE/'logs'/('m5_'+a.name+'_assignment.json')
        subprocess.run([sys.executable,'-I',str(HERE.parent/'C6C7REVIEW/m6_verify_assignment.py'),
                        '--cnf',str(source),'--model',str(model),'--out',str(checklog)],check=True)
        inputs.append(h.archived(model));result['assignment_check_sha256']=h.sha(checklog)
    # Write the solver result before potentially lengthy proof compression.
    record=HERE/'logs'/('m5_'+a.name+'.json');h.save(record,result)
    print(json.dumps({'solver_completed':result}),flush=True)
    if proof.exists():
        result['proof_archive']=h.archived(proof);inputs.append(result['proof_archive'])
    else:raise RuntimeError('expected retained text proof file')
    result['archives']=inputs;h.save(record,result);h.save(a.archive/(a.name+'.run.json'),result)
    print(json.dumps({'archive_completed':result}),flush=True)

if __name__=='__main__':main()
