#!/usr/bin/env python3
"""Apply the checked-clause exporter to the third frozen 13-state core.
The namespace and include paths distinguish the independent literal proof.
"""
import argparse
from pathlib import Path
from export_omission_coupled_core import export


def export_third(source, output):
    export(source, output)
    text = output.read_text().replace('CoupledCore13', 'CoupledCoreThird')
    text = text.replace('omission-coupled-core-2026-10-10', 'omission-coupled-demand-two-2026-10-10')
    output.write_text(text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path('experiments/omission-coupled-demand-two-2026-10-10/core13.json'))
    parser.add_argument('--output', type=Path, default=Path('ErdosSzekeres/Omission/CoupledCoreThird.lean'))
    args = parser.parse_args()
    export_third(args.source, args.output)
