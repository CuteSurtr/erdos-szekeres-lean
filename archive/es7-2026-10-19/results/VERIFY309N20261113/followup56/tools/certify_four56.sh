#!/usr/bin/env bash
# Parent-scheduled only: 1 CPU, AS700MiB, MemoryMax1000M, no swap, Runtime2400.
# Four independent jobs run sequentially. All failed/unknown attempts remain.
set -u
audit_tools_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
failures=0
for index in 0 1 2 3; do
    if ! python3 "$audit_tools_dir/new_rows56.py" certify "$index" --seconds 180 --heap 512; then
        failures=$((failures+1))
    fi
done
exit "$failures"
