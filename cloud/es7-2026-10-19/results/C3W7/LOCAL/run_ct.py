#!/usr/bin/env python3
"""Run results/C3U2/tools/close_tree.py (cad4e050, unmodified) on macOS. The only change is its work
directory: close_tree.py writes CNF and proof files to the constant WORK = "/opt/work/ct", which needs
root here, so this wrapper sets close_tree.WORK to $CT_WORK before main() runs. Worker processes are
forked so that they inherit that setting (macOS defaults to spawn). Arguments are passed through."""
import multiprocessing
import os
import sys

multiprocessing.set_start_method("fork", force=True)
sys.path.insert(0, os.environ["TOOLS"])
sys.argv = ["close_tree.py"] + sys.argv[1:]
import close_tree  # noqa: E402

close_tree.WORK = os.environ["CT_WORK"]
close_tree.main()
