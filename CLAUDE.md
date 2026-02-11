# CLAUDE.md - AI Assistant Guide for DeepSeek-LLM

## Project Overview

DeepSeek-LLM is a **model release and evaluation repository** for the DeepSeek LLM family (7B and 67B parameter models). This is NOT a training codebase — it primarily contains evaluation results, benchmark data, and documentation for pre-trained language models trained on 2 trillion tokens in English and Chinese.

- **Models**: DeepSeek LLM 7B/67B (Base and Chat variants)
- **Architecture**: LLaMA-based auto-regressive transformer decoder (MHA for 7B, GQA for 67B)
- **Sequence length**: 4096 tokens
- **Licenses**: MIT for code (`LICENSE-CODE`), custom DeepSeek agreement for models (`LICENSE-MODEL`)
- **Paper**: https://arxiv.org/abs/2401.02954

## Repository Structure

```
deepseek-llm/
├── README.md                    # Main project documentation (models, benchmarks, quick start)
├── requirements.txt             # Python dependencies (torch, transformers, accelerate, etc.)
├── Makefile                     # Linting, formatting, and development task automation
├── LICENSE-CODE                 # MIT License (code)
├── LICENSE-MODEL                # DeepSeek Model License Agreement
├── evaluation/                  # Evaluation results and benchmark data
│   ├── IFEval/                  # Instruction Following Evaluation (JSONL per model)
│   ├── hungarian_national_hs_solutions/  # Hungarian exam evaluation (CSV)
│   ├── deepseek-67b-1206-no-sp.jsonl     # Evaluation dataset (683 Chinese Q&A entries)
│   └── more_results.md          # Extended benchmark comparison tables
├── images/                      # Documentation graphics (logos, benchmark charts)
├── .editorconfig                # Editor formatting rules
├── .flake8                      # Flake8 linter configuration
├── .pylintrc                    # Pylint configuration
├── .pre-commit-config.yaml      # Pre-commit hook definitions
├── .gitignore                   # Git ignore patterns
└── .gitattributes               # Git file handling rules
```

**Key insight**: The only Python source folder is `evaluation/`. All linting and formatting tools target this directory via `SOURCE_FOLDERS = evaluation` in the Makefile.

## Development Commands

### Setup

```bash
# Install runtime dependencies
pip install -r requirements.txt

# Install pre-commit hooks
make pre-commit-install
```

### Linting and Formatting

```bash
# Run ALL linters (ruff, flake8, isort, black, mypy, pylint, addlicense)
make lint

# Auto-format code (isort + black + ruff fix + addlicense)
make format

# Individual linters
make ruff          # Fast linter
make flake8        # Traditional linter with plugins
make py-format     # Check isort + black formatting
make mypy          # Type checking
make pylint        # Comprehensive static analysis
make addlicense    # Check MIT license headers

# Auto-fix
make ruff-fix      # Auto-fix ruff issues
make format        # Auto-format everything

# Run all pre-commit hooks
make pre-commit

# Cleanup build artifacts
make clean
```

## Code Style and Conventions

### Formatting Rules

- **Max line length**: 120 characters
- **Max doc length**: 100 characters
- **Formatter**: Black (with Jupyter support)
- **Import sorting**: isort (project-aware, configured for `evaluation`)
- **Python version**: 3.8+ minimum (enforced via pyupgrade, pylint)
- **String quotes**: Double-quote fixer enforced via pre-commit
- **Indentation**: 4 spaces for Python, 2 spaces for YAML/JSON/Markdown, tabs for Makefile/shell
- **Line endings**: LF (Unix-style)
- **Encoding**: UTF-8
- **Final newline**: Required in all files
- **Trailing whitespace**: Stripped

### Naming Conventions (from `.pylintrc`)

- **Functions/methods**: `snake_case`
- **Variables/arguments/attributes**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_CASE`
- **Class constants**: `UPPER_CASE`
- **Accepted short names**: `i`, `j`, `k`, `ex`, `_`, `op`, `fn`, `f`, `g`, `p`, `u`, `t`, `lr`, `mu`, `nu`, `x`, `y`

### Linting Stack (in order of pre-commit execution)

1. **pre-commit-hooks**: Trailing whitespace, end-of-file fixer, YAML/TOML check, AST check, large file check, merge conflict check, private key detection, debug statements, double-quote strings
2. **Ruff** (v0.1.5): Fast Python linter with auto-fix
3. **isort** (v5.12.0): Import sorting
4. **Black** (v23.11.0): Code formatting (with Jupyter support)
5. **pyupgrade** (v3.15.0): Python 3.8+ syntax modernization
6. **Flake8** (v6.1.0): With plugins — bugbear, comprehensions, docstrings, pyi, simplify
7. **Pylint**: Comprehensive analysis (skipped in CI due to speed)

### Flake8 Ignored Rules

- `E203` (whitespace before `:`) — handled by Black
- `W503`/`W504` (line break around binary operator) — handled by Black
- `E501`/`W505` (line/doc too long) — long docstrings with examples are accepted
- `F401` in `__init__.py` — intentional re-exports

### Pylint Notes

- `duplicate-code` and `consider-using-from-import` are disabled
- `numpy.*` and `torch.*` are in `generated-members` (no E1101 false positives)
- Max function args: 5, max locals: 15, max branches: 12, max statements: 50

## License Headers

All Python files in `evaluation/` must have MIT license headers attributed to `"DeepSeek."`. The `addlicense` tool (Go-based) enforces this. Run `make format` to auto-add missing headers.

## Data Formats

- **Evaluation data**: JSONL (JSON Lines) format
- **Exam results**: CSV files
- **Benchmark comparisons**: Markdown tables in `evaluation/more_results.md`
- **Languages**: English and Chinese content

## Pre-commit CI

The repository uses [pre-commit.ci](https://pre-commit.ci/) for automated linting on pull requests:
- Auto-fixes are enabled
- Pylint is skipped in CI (too slow)
- Monthly auto-updates of hook versions

## No Test Suite

This repository has no unit tests, pytest configuration, or test directory. Quality is ensured through linting, pre-commit hooks, and evaluation benchmarks.
