English · [简体中文](./README.zh-CN.md)

# JurisCoT — Legal Chain-of-Thought Reasoning Engine

A standalone, independently testable legal Chain-of-Thought (CoT) reasoning library for Chinese legal academic writing, serving as the core reasoning component of LawAutoPaper. It ships six paper-type CoT prompt templates with a small CLI (`juriscot list|show|run`) to inspect them. v0.1 covers template asset management only — the model inference pipeline is not implemented yet (see docs/roadmap-internal.md), and `run` reports that honestly instead of faking a call.

## Overview

JurisCoT takes a legal question plus related literature / statutes / cases / data / foreign law, and generates a structured reasoning chain and academic body paragraphs through structured CoT templates.

- **Input**: legal question + reference literature / statutes / cases / data / foreign law
- **Output**: structured reasoning chain + academic body paragraphs
- **After acceptance**: embedded into LawAutoPaper as a Python package

**Current status (v0.1)**:

- Implemented: 6 paper-type CoT templates and prompt assets, the template-management CLI (`list` / `show`), and the test suite
- Not implemented: the model inference pipeline (prompt_loader / pipeline / engine, see docs/roadmap-internal.md days 29–37).
  `run` is the entry-point placeholder for model invocation — without an API key it exits with a clear error; with a key it honestly reports that the feature is not implemented instead of pretending success.

## Supported paper types

| # | Paper type | Typical use | CoT steps |
|---|-----------|-------------|-----------|
| 1 | **Theoretical analysis** | course papers, legal-theory papers | 6 steps |
| 2 | **Case analysis** | judgment-commentary papers | 8 steps |
| 3 | **Institutional comparison** | comparative-law papers | 6 steps |
| 4 | **Empirical research** | data-driven papers | 6 steps |
| 5 | **Legislative proposal** | law-reform proposal papers | 6 steps |
| 6 | **Literature review** | survey papers | 4 steps |

## Quick start

Requires Python >= 3.10.

```bash
# 1. Install (includes the `juriscot` console script)
pip install -e .

# 2. List all paper types and their CoT chains
juriscot list

# 3. Show the template details of one type (English code or Chinese name both work)
juriscot show theory
juriscot show 案例分析

# 4. (Optional) model-invocation entry point — not wired to a model in v0.1; behavior:
#    - no API key provided: exits with a clear error (exit code 2)
#    - API key provided: honestly reports the pipeline is not implemented (exit code 3)
cp .env.example .env      # fill in JURISCOT_API_KEY as needed (.env is gitignored)
juriscot run --type theory --topic "论数据产权的法律属性"
```

Exit-code conventions: `0` success; `2` usage/config error (invalid arguments, missing API key, etc.); `3` feature not implemented.

You can also run it without installing: from the repository root, execute `py -3.13 -m src.cli list` (any Python >= 3.10 works).

## Running tests

```bash
py -3.13 -m pytest tests -q
# or any Python >= 3.10: python -m pytest tests -q
```

Coverage: template-loading integrity (all 6 templates parse, fields complete, every chain step has a matching prompt file) and CLI behavior (success and error paths of list / show / run).

## Project structure

```
JurisCoT/
├── src/                  # Core source
│   ├── __init__.py
│   ├── schemas.py       # Data schema definitions
│   ├── types.py         # Type definitions
│   └── cli.py           # CLI entry point (list / show / run)
├── prompts/             # CoT prompt assets
│   ├── base/            # Role setup and legal-argumentation rules
│   ├── cot/             # Step 1-5 prompts (incl. 4c variants)
│   └── templates/       # Chain templates for the 6 paper types (YAML)
├── tests/               # Template integrity + CLI behavior tests
├── docs/
│   └── roadmap-internal.md  # Maintainer's 40-day working plan
├── .env.example         # Environment variable example (placeholders only, no real values)
├── DESIGN.md            # Full design document
├── LICENSE              # MIT
└── pyproject.toml       # Project configuration
```

## Roadmap

See [docs/roadmap-internal.md](./docs/roadmap-internal.md) — the maintainer's 40-day working plan, 1 hour a day, one item per day.

## License

[MIT](./LICENSE)
