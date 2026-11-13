#!/usr/bin/env python3
"""Rebuild the two SAT inputs and bind saved bounded-search diagnostics.

No solver is rerun and no timeout is interpreted as an exclusion proof.
"""
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

from catalog import HERE, ROOT, build


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def check():
    record = json.loads((HERE / 'runs.json').read_text())
    encoder_path = ROOT / record['encoder']
    if sha(encoder_path.read_bytes()) != record['encoder_sha256']:
        raise ValueError('Changed SAT encoder')
    if sha((ROOT / record['sat_runner']).read_bytes()) != record['sat_runner_sha256']:
        raise ValueError('Changed SAT runner')
    spec = importlib.util.spec_from_file_location('shared_rank_counter', encoder_path)
    encoder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(encoder)
    data = build()
    for run in record['sat_runs']:
        if run['rows'] not in (2647, 2650) or run['budget'] != 32 or run['occupied_required'] != [0]:
            raise ValueError('Unexpected global SAT scope')
        rows = [(r['support'], r['rhs']) for r in data['constraints'][:run['rows']]]
        cnf = encoder.encode(154, rows, 32, (0,))
        if sha(cnf.encode()) != run['cnf_sha256']:
            raise ValueError('SAT input differs from catalog prefix')
        header = next(line.split() for line in cnf.splitlines() if line.startswith('p cnf '))
        if list(map(int, header[2:])) != [run['variables'], run['clauses']]:
            raise ValueError('SAT dimensions differ')
        log = gzip.decompress((HERE / run['log']).read_bytes())
        if sha(log) != run['log_sha256']:
            raise ValueError('Changed SAT diagnostic log')
        if run['status'] != 'unknown' or b'c exit 0' not in log:
            raise ValueError('Unexpected SAT status; review the result before publication')
    for run in record['scip_runs']:
        if (run['rows'] != 2649 or run['hole_budget'] != 32 or
                run['occupied_required'] != [0] or run['status'] != 'timelimit'):
            raise ValueError('Unexpected SCIP scope/status')
        if run['new_supports'] != [r['support'] for r in data['constraints'][2646:2649]]:
            raise ValueError('SCIP supports differ from catalog')
        if sha((HERE / run['script']).read_bytes()) != run['script_sha256']:
            raise ValueError('Changed SCIP probe script')
        log = gzip.decompress((HERE / run['log']).read_bytes())
        if sha(log) != run['log_sha256'] or b'solving was interrupted [time limit reached]' not in log:
            raise ValueError('Changed SCIP diagnostic log')
    return {'sat_inputs_rebuilt': len(record['sat_runs']),
            'scip_records_bound': len(record['scip_runs']),
            'scope': 'Saved bounded diagnostics only; no32-hole exclusion.'}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
