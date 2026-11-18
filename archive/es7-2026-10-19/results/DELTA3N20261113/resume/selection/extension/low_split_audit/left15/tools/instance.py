#!/usr/bin/env python3
import importlib.util,json,os,resource,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=R.parents[1]
W=Path('/home/jay/research/data/delta3-codex-20261113/extension');S=W/'low-split-audit/left15'
def save(name,o):
 with (R/'data'/name).open('x') as f:json.dump(o,f,indent=2);f.write('\n')
def load(name,p):
 spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
def main():
 resource.setrlimit(resource.RLIMIT_AS,(300<<20,300<<20));start=time.monotonic();S.mkdir(exist_ok=False)
 rows=load('rows',R.parent/'tools/rows.py');rows.S=S;C=load('own_low_controls',R.parent/'tools/controls.py')
 frozen=dict(line.split('  ',1)[::-1] for line in (R.parent/'SHA256SUMS').read_text().splitlines())
 for p in ('tools/rows.py','tools/controls.py'):assert rows.sha(R.parent/p)==frozen[p]
 cnf=W/'low15-n7-compact.cnf';source=E/'low_split_compact.cpp'
 assert rows.sha(source)=='1fb043a5d29fa86047ba05cae86fdfb248e6069bc6731c4ee39c181737319303'
 assert rows.sha(E.parents[1]/'compact/compact_cnf.cpp')=='1964e17b777fd7b7a973f12b2911c003a050047f13a621f523a9f98c6e31d553'
 assert rows.sha(cnf)==rows.sha(W/'low15-n7-a/input.cnf')=='793063f5c7c5208c16ce038c63659878adee4eb049546d775d65c5a18ed60418'
 formula=rows.check(cnf,15,7,'compact','compact15');save('formula.json',formula)
 fixture=E/'structure2/data/low_classification_replay.json';before=rows.sha(fixture)
 P=json.loads(fixture.read_text())['cases']['n7_fixed_left16']['P'][:15]
 G=C.Geometry(P,7);assert not G.cap4 and not G.ngons
 canonical=C.canonical('compact',G)
 options=[b for b in range(1<<15) if not G.has_cap3[b] and not G.T[G.full^b]
          and all(v in G.end3 for v in rows.verts(b)[1:])]
 assert options and all(b.bit_count()<=6 for b in options)
 assert canonical['false_by_phase']=={'no_covered_cup_transversal':len(options)}
 U=C.Geometry(C.low_join(P,7),7);assert not U.cap5 and not U.ngons
 chosen=options[0]|(1<<15);assert not U.forbidden[chosen] and not U.T[U.full^chosen]
 assert before==rows.sha(fixture)
 save('control.json',{'status':'PASS','P_left':P,'P_join':U.P,'left':G.report(),'join':U.report(),
  'canonical':canonical,'option1_cups':len(options),'selected_full':rows.verts(chosen),
  'parent_expected_selectors_ignored':True,'fixture_sha256':before})
 for src,name in ((source,'source-compact.cpp.txt'),(W/'low15-n7-a/result.json','original-heap550-result.json'),
                  (W/'low15-replay-a/result.json','parent-heap900-result.json'),(W/'low15-replay-b/result.json','parent-heap1400-result.json')):
  with (R/'data'/name).open('xb') as f:f.write(src.read_bytes())
 save('instance-result.json',{'status':'PASS','label':'COMPUTED','formula':formula,'canonical_positive_control':True,
  'seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
  'source_sha256':rows.sha(source),'helper_hashes':{p:rows.sha(R.parent/p) for p in ('tools/rows.py','tools/controls.py')},
  'limits':Path('/proc/self/limits').read_text(),'affinity':sorted(os.sched_getaffinity(0))})
 print(json.dumps({'status':'PASS','variables':formula['variables'],'clauses':formula['clauses'],'literals':formula['literals'],
  'option1_cups':len(options),'seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
if __name__=='__main__':
 try:main()
 except BaseException as e:save('instance-failure.json',{'error':repr(e)});raise
