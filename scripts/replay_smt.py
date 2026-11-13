#!/usr/bin/env python3
"""Replay extension constraints with cvc5, after expanding Z3's exactly-one nodes.

This is independent solver corroboration, not a Lean proof or certificate checker.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time


def run(source, output, seconds=120):
    import cvc5
    import z3
    if output.exists():
        raise FileExistsError(output)
    assertions = z3.parse_smt2_file(str(source))
    seen, replacements = set(), []
    stack = list(assertions)
    while stack:
        expr = stack.pop()
        if expr.get_id() in seen:
            continue
        seen.add(expr.get_id())
        stack.extend(expr.children())
        if z3.is_app_of(expr, z3.Z3_OP_PB_EQ):
            if any(parameter != 1 for parameter in expr.params()):
                raise ValueError("Only unweighted exactly-one nodes are supported")
            terms = expr.children()
            expanded = z3.Or([z3.And([term if i == j else z3.Not(term)
                                      for j, term in enumerate(terms)]) for i in range(len(terms))])
            replacements.append((expr, expanded))
    plain = z3.Solver()
    plain.add([z3.substitute(a, *replacements) for a in assertions])
    translated = output.with_suffix(".smt2")
    translated.write_text("(set-logic QF_LRA)\n" + plain.to_smt2())
    solver = cvc5.Solver()
    solver.setOption("tlimit", str(seconds * 1000))
    parser = cvc5.InputParser(solver)
    parser.setFileInput(cvc5.InputLanguage.SMT_LIB_2_6, str(translated))
    symbols = parser.getSymbolManager()
    started = time.monotonic()
    responses = []
    while True:
        command = parser.nextCommand()
        if command.isNull():
            break
        response = command.invoke(solver, symbols).strip()
        if response:
            responses.append(response)
    status = next((x for x in reversed(responses) if x in ("sat", "unsat", "unknown")), "unrecognized")
    result = {"scope": "independent SMT solver replay; not a Lean certificate",
              "input": str(source), "input_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "translated": str(translated),
              "translated_sha256": hashlib.sha256(translated.read_bytes()).hexdigest(),
              "expanded_exactly_one_nodes": len(replacements), "assertions": len(assertions),
              "solver": "cvc5", "version": cvc5.__version__, "status": status,
              "seconds": time.monotonic() - started, "responses": responses}
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("solver", "status", "seconds")}))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=120)
    args = parser.parse_args()
    run(args.source, args.output, args.seconds)
