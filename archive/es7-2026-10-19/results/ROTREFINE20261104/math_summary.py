#!/usr/bin/env python3
"""Summarize verified math evidence without interpreting numerical failures."""
import argparse
import hashlib
import json
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--results',type=Path,required=True);p.add_argument('--final',action='store_true');a=p.parse_args();catalog=json.loads((a.results/'math_catalog.json').read_text());psd=[r for r in catalog if 'quadratic' in r['rigor']]
 events=[json.loads(line) for line in (a.archive/'worker_events.jsonl').read_text().splitlines()];last=events[-1]
 peaks=[]
 for name in ('linear_search.json','sdp_result.json','verified.json','family_verified.json','scan_summary.json','primal.json'):
  for path in a.archive.rglob(name):
   value=json.loads(path.read_text()).get('peak_rss_bytes')
   if value is not None:peaks.append(value)
 summary={'status':'final' if a.final else 'active snapshot','verified_families':len(catalog),'linear_families':len(catalog)-len(psd),'negative_definite_families':len(psd),'sum_family_clause_counts_not_global_unique':sum(r['unique_clauses'] for r in catalog),'source_exact54_tests':sum(r['exact54_tests'] for r in catalog),'additional_emitted_clause_exact54_tests':sum(r['family_exact54_tests'] for r in catalog),'maximum_source_orbits':max(map(lambda r:len(r['source_layers']),catalog)),'maximum_certificate_rows':max(r['support'] for r in catalog),'maximum_observed_math_peak_rss_bytes':max(peaks,default=0),'last_worker_event':last,'catalog_sha256':hashlib.sha256((a.results/'math_catalog.json').read_bytes()).hexdigest(),'conclusion':'exact exclusions of prescribed geometric sixfold sign patterns; no settled 60-point case or changed 54-to-60 bound'}
 if a.final:
  assert last['event']=='worker_stopped'
  process_check=json.loads((a.archive/'final_process_check.json').read_text());assert not process_check['live_math_compute_processes']
  path=a.archive/'math_archive_manifest.json';manifest=json.loads(path.read_text());assert all(r['roundtrip'] for r in manifest)
  summary.update({'archive_manifest_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'archive_files':len(manifest),'archive_raw_bytes':sum(r['raw_bytes'] for r in manifest),'archive_compressed_bytes':sum(r['compressed_bytes'] for r in manifest),'all_archive_roundtrips':True})
 (a.results/'math_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 text=['# Sixfold mathematical separation summary','',f"**{'Final exact-computation record' if a.final else 'Active snapshot; counts may grow'}.** {summary['verified_families']} verified families comprise {summary['linear_families']} positive zero-identity families and {summary['negative_definite_families']} based on negative-definite quadratic combinations. Their clause counts sum to {summary['sum_family_clause_counts_not_global_unique']:,}; this sum does not deduplicate across families.",'',
 '**Written proof + exact computation.** Every retained source has positive integer weights, exact direct seed-polynomial verification, model-hash binding and exact certified-set regression tests. Large linear and quadratic sources additionally invoke the independent checker before queueing. Small linear sources receive the separately retained batch independent checks. Numerical LP/SDP statuses only guide searches.','',
 f"There are {summary['source_exact54_tests']:,} source certified-set tests and {summary['additional_emitted_clause_exact54_tests']:,} additional emitted-clause tests. Sources on at most four orbits use exhaustive linear tests; larger linear and quadratic sources use explicitly finite samples plus original/mirrored tests of every emitted canonical clause. The largest retained source uses {summary['maximum_source_orbits']} orbits. `math_catalog.json` states each scope and hash.",'',
 '**Method boundary.** Model0033 has an independently checked rational lift satisfying all 5,710 strict orientation inequalities and decreasing positive radii, and the main campaign finds its full product graph acyclic. A 16-row negative-definite certificate on five orbits nevertheless excludes its prescribed geometric rotation. This is a concrete separation between these tested methods, not a completeness or general dominance assertion. Model0046 shows why full linear search is needed after small restrictions: a 39-row zero identity on seven orbits excludes it after every two-/three-/four-orbit linear restriction survives.','',
 '**Limits.** These are obstructions to the specified Euclidean rotational realization, not claims that the underlying abstract order type has no other realization. A feasible lift would not prove rank-one realizability. The mathematical lane alone does not settle the 60-point case or change the bound 54 ≤ maximum ≤ 60.','',
 f"**Evidence only (resources).** The largest recorded math process peak RSS is {summary['maximum_observed_math_peak_rss_bytes']/1_000_000:.1f} MB. Numerical searches and family checks run serially with one compute core. The written proofs are in `math.md` and `math_sdp.md`; compact certificate records are in `math_witnesses/`.",'']
 if a.final:text+=['**Final unresolved boundary.** Model0090 has an independently checked rational linear lift with minimum strict margin `2/3491`. The particular lift is indefinite, while PSD feasibility and geometric realizability remain unresolved. Ten nine-orbit SDP probes and 1,218 rounded integer semidefinite-dual attempts produced no exact certificate. No cut was queued for this model; numerical near-zero margins were not accepted as proof. Details and the model hash are in `math_sdp.md`.','', '**Archive verification.** Every retained math artifact was compressed with one worker and checked by decompression against its raw SHA-256. `math_summary.json` records archive totals and the manifest hash. The watcher stopped and its managed child process group was reaped; no mathematical search remains running.','']
 (a.results/'math_summary.md').write_text('\n'.join(text));print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
