PYSEN := poetry run pysen
PYTEST := poetry run pytest

.PHONY: test
test:
	$(PYTEST) -v

tests/%.py: FORCE
	$(PYTEST) $@

# Idiom found at https://www.gnu.org/software/make/manual/html_node/Force-Targets.html
FORCE:

.PHONY: lint
lint:
	$(PYSEN) run lint

.PHONY: format
format:
	$(PYSEN) run format

.PHONY: check
check: format lint
