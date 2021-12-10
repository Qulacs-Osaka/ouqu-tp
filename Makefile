PYTEST := poetry run pytest
FORMATTER := poetry run black
LINTER := poetry run flake8
IMPORT_SORTER := poetry run isort
TYPE_CHECKER := poetry run mypy
SPHINX_APIDOC := poetry run sphinx-apidoc

PROJECT_DIR := ouqu_tp
CHECK_DIR := $(PROJECT_DIR) tests
PORT := 8000

# If this project is not ready to pass mypy, remove `type` below.
.PHONY: check
check: format lint type

.PHONY: ci
ci: format_check lint type

.PHONY: test
test:
	$(PYTEST) -v

tests/%.py: FORCE
	$(PYTEST) $@

# Idiom found at https://www.gnu.org/software/make/manual/html_node/Force-Targets.html
FORCE:

.PHONY: format
format:
	$(FORMATTER) $(CHECK_DIR)
	$(IMPORT_SORTER) $(CHECK_DIR)

.PHONY: format_check
format_check:
	$(FORMATTER) $(CHECK_DIR) --check --diff
	$(IMPORT_SORTER) $(CHECK_DIR) --check --diff

.PHONY: lint
lint:
	$(LINTER) $(CHECK_DIR)

.PHONY: type
type:
	$(TYPE_CHECKER) $(PROJECT_DIR)

.PHONY: serve
serve: html
	poetry run python -m http.server --directory doc/build/html $(PORT)

.PHONY: doc
html: api
	poetry run $(MAKE) -C doc html

# Because it is not protected by `if __name__ == '__main__'` conditions
# See https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html
EXCLUDE_PATTERN := ouqu_tp/make_Cnet.py ouqu_tp/simulate.py ouqu_tp/trancepile.py
.PHONY: api
api:
	$(SPHINX_APIDOC) -f -e -o doc/source $(PROJECT_DIR) $(EXCLUDE_PATTERN)
