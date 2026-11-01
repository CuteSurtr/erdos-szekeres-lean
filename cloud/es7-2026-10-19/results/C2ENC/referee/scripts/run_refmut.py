"""Run the authors' mutate.py harness (../../tests) on the authors' mutants and on the referee's additional ones
(refmutants.NEW_MUTANTS).  Outputs go to ../../tests/mut and ../../tests/logs, as for mutate.py.
usage: run_refmut.py NAME [NAME ...]"""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tests"))
sys.path.insert(0, HERE)
import mutate      # noqa: E402  (the authors' harness)
import refmutants  # noqa: E402
mutate.MUTANTS.update(refmutants.NEW_MUTANTS)
mutate.main()
