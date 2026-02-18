# TwinCometFlux

[![CI](https://github.com/jpgcreate/twintubeflux/actions/workflows/python-tests.yml/badge.svg)](https://github.com/jpgcreate/twintubeflux/actions/workflows/python-tests.yml) [![Codecov](https://codecov.io/gh/jpgcreate/twintubeflux/branch/main/graph/badge.svg)](https://codecov.io/gh/jpgcreate/twintubeflux)

Small project for DJ/web/graphics automation.

> Note: repo path in the badge URLs has been set to `jpgcreate/twintubeflux` (change if different).

CI now runs linting (flake8), tests with coverage, and uploads a coverage report artifact. The workflow also runs on tags (`v*`) and can be triggered manually via `workflow_dispatch`.

## Development / pre-commit

- Install developer dependencies (preferred):

  ```bash
  # preferred: use Makefile
  make install-dev

  # or manually:
  python -m pip install -r requirements-dev.txt
  ```

- Install the git hooks locally:

  ```bash
  make precommit-install
  # or
  python -m pre_commit install
  ```

- Run pre-commit hooks on all files (optional):

  ```bash
  make precommit-run
  # or
  python -m pre_commit run --all-files
  ```

Notes:
- Do not paste commented lines (starting with `#`) directly into the shell — they are comments and will be treated as commands if pasted without the leading `$` or inside a shell block.

This repository includes `.flake8`, a `requirements-dev.txt` and a `.pre-commit-config.yaml` that runs `black`, `isort`, `flake8` and other safety/style hooks.