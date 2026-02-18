# Development helpers
.PHONY: install-dev precommit-install precommit-run test

install-dev:
	python -m pip install --upgrade pip
	python -m pip install -r requirements-dev.txt

precommit-install:
	python -m pre_commit install

precommit-run:
	python -m pre_commit run --all-files

test:
	python -m pytest --cov=agent_core tests/
