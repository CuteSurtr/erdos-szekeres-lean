#!/usr/bin/env python3
"""Apply the same checked-clause exporter to the second frozen 13-state core.
The namespace and include paths distinguish the independent literal proof.
"""
from pathlib import Path
from export_omission_coupled_core import export

source = Path('experiments/omission-coupled-next-2026-10-10/core13.json')
output = Path('ErdosSzekeres/Omission/CoupledCoreSecond.lean')
export(source, output)
text = output.read_text().replace('CoupledCore13', 'CoupledCoreSecond')
text = text.replace('omission-coupled-core-2026-10-10', 'omission-coupled-next-2026-10-10')
output.write_text(text)
