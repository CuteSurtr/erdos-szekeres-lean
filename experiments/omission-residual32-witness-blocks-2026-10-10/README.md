# Block searches against the 32-hole witness

This bundle searches for a valid additional geometric row violated by the
specified 32-hole assignment. It has not produced a new Lean theorem.

`search.py` examines supports of 23 occupied states within every comparable
pair of catalog profiles. It checks whether all possible pair-label cells admit
a common binary compression that strictly increases along a cap. Such a
certificate would permit the existing 22-point block-capacity theorem to rule
out the support after a Lean check.

The threshold mode intersects each row's permitted threshold intervals before
enumerating compatibility cliques. The cell mode allows arbitrary binary values
on the active cells. Both completed all 8,148 catalog intervals, with 2,727
eligible intervals and 100,589 recursive search calls, without finding a support.
These are finite-search outcomes; no Lean completeness theorem is asserted.

`search_endpoint.py` is a broader, bounded search for 23 occupied states with no
possible four-cap pattern. It allows the obstruction test to depend on endpoint
profiles, using strictly increasing cap-label columns along four distinct
states. Its solver outputs are research diagnostics until independently
certified. `endpoint-search.json` records 41 candidate rounds and 123,000
forbidden quadruples, followed by `unknown` at the solver's five-second query
timeout (57.37 seconds total). No support or new inequality was found. That
outcome is inconclusive and is not an infeasibility proof. No solver remains
running. Work moved to a separately discovered coupled-state core.

`manifest.json` records the stopped status, separates the completed finite runs
from the inconclusive solver run, and pins all scripts, reports, and the source.

The source identity and witness are recorded in each result. The inherited
catalog derives from Michael Schroeder's companion archive,
[DOI 10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891);
attribution and licensing remain in [THIRD_PARTY.md](../../docs/THIRD_PARTY.md).
