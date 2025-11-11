# Repository Guidelines

## Project Structure & Module Organization
Core GA driver `main.py` wires DEAP's toolbox to `fitness/latency_map.py`, which holds the canonical character map, latency constants, and `BIGRAM_DICT`. Keep data-producing scripts (`create_bigram.py`, corpora, Reddit importer) and JSON assets inside `fitness/`, and treat `fitness/bigram_dict.json` as generated output. Visualization helpers plus PNG assets live in `Imaging/`, while exploratory simulators (`simpy_test.py`, `simpy_jobs.py`) and legacy GA prototypes (`deap_test.py`, `appliedEP.py`) stay at the root for reference.

## Build, Test, and Development Commands
- `uv sync` — install Python 3.12 dependencies from `pyproject.toml`/`uv.lock`.
- `uv run main.py` — run the evolutionary search (300×9k) and print the best layout with its latency score.
- `uv run fitness/create_bigram.py --directory fitness/corpus` — rebuild `fitness/bigram_dict.json`; add `--reddit` when sourcing CSV dumps from `fitness/reddit_corpus`.
- `uv run simpy_test.py` — replay a two-finger timeline using the current distance matrix to spot regressions.

## Coding Style & Naming Conventions
Follow PEP 8 with 4-space indents, `snake_case` for callables, and UPPER_SNAKE_CASE for global constants (`CHARACTERS`, `SIMULTANEOUS_LATENCY_MS`). Place tunable parameters near the top of each module so they can be shared between scripts. Keep GA helpers pure where possible, pass randomness via seeds, and prefer modules named after the capability they expose (`fitness/latency_analysis.py`, not `misc.py`). Add concise docstrings explaining coordinate systems or corpus assumptions.

## Testing Guidelines
Automated coverage is light today, so create `tests/` files using `pytest` for any new fitness metric or operator; run them with `uv run pytest`. For stochastic logic, lock seeds (e.g., `random.seed(123)`) and assert on aggregates such as average latency. Continue exercising `uv run simpy_test.py` or `uv run deap_test.py` after changing distance or selection logic, and record before/after fitness numbers in PR discussions.

## Commit & Pull Request Guidelines
Git history favors short imperative subjects (`fitness`, `Change to minimizing fitness`), so keep summaries under ~60 characters and elaborate in the body when necessary. PRs should describe motivation, list commands you ran (`uv run main.py`, tests), link issues, and attach artifacts such as new layout PNGs when visuals change.

## Data & Visualization Notes
Treat `fitness/bigram_dict.json` as generated—whenever corpora change, rerun `create_bigram.py` and commit the resulting JSON alongside the script edits for traceability. `Imaging/keyboardImage.py` relies on ImageMagick/Wand; if you used it to create assets, mention the external dependency in the PR so reviewers can reproduce screenshots. Keep bulky raw datasets outside the repo (extend `.gitignore` if needed) and only check in reproducible, script-generated artifacts.
