.PHONY: help tag release install-local test
.DEFAULT_GOAL := help

TEST_RESULTS := test_results
SYSTEM_PYTHON := python


VERSION := $$(hatch version)
TAG := v$(VERSION)

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

BROWSER := $(SYSTEM_PYTHON) -c "$$BROWSER_PYSCRIPT"

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| awk 'BEGIN {FS = ":.*?## "}; \
	{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

tag: ## create and push a tag for the current version
	git tag $(TAG)
	git push origin $(TAG)

release: ## package and upload a release
	@echo "For further usage."

install-local: ## install scaffold locally
	@echo "Make sure you activated the virtual env with: 'source .venv/bin/activate'"
	python -m pip install --upgrade pip
	pip install -e .

test: ## runs tests
	@pytest -s -vvv

coverage: ## run tests with coverage
	@pytest --cov=pygithubactions

create-results: ## create test_results directory
	mkdir -p $(TEST_RESULTS)

coverage-output: ## create outputs for coverage reports
	@coverage html -d $(TEST_RESULTS)

coverage-report: create-results coverage coverage-output ## run coverage, generate report, open in the browser
	$(SYSTEM_PYTHON) -m webbrowser -t "file://$(PWD)/$(TEST_RESULTS)/index.html"

coverage-clean: ## remove the coverage directory
	rm -rf $(TEST_RESULTS)
	rm .coverage

isort: ## runs isort
	@isort .

format: isort ## formats python
	@blue .

lint: format ## run python flake8 linter tool
	@ruff .

static-check: ## runs static checks with mypy
	@mypy pygithubactions

precommit-install: ## install pre-commit
	@pre-commit install

precommit-run: ## run all pre-commit hooks
	@pre-commit run -a

clean: ## run clean up
	rm -rf .pytest_cache dist build yamlvalidator.egg-info .pytest_cache .mypy_cache test_results .coverage
	find . -type d -name '__pycache__' -exec rm -r {} +
