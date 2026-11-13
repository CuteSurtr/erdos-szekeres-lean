#!/usr/bin/env python3
"""A changed tail index must be rejected before any compiler is invoked."""
import copy
import json
from pathlib import Path
from check import preflight

here = Path(__file__).resolve().parent
manifest = json.loads((here / 'manifest.json').read_text())
preflight(manifest)
changed = copy.deepcopy(manifest)
changed['bindings'][0]['source_row'] += 1
try:
    preflight(changed)
except ValueError as exc:
    assert str(exc) == 'Ordered129 tail binding changed', str(exc)
    print('PASS: changed ordered tail rejected before compilation')
else:
    raise AssertionError('Changed ordered tail unexpectedly accepted')
