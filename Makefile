bin = .venv/bin
.PHONY: prototype

verify: format-check lint mypy test

lint: ruff mypy

ruff:
	$(bin)/ruff check src tests

fix:
	$(bin)/ruff check --fix src tests

format: black isort

format-check: isort-check black-check

isort-check:
	$(bin)/isort -c src tests

isort:
	$(bin)/isort src tests

black-check:
	$(bin)/black --check src tests

black:
	$(bin)/black src tests

mypy:
	$(bin)/mypy src tests

test:
	$(bin)/pytest

prototype: prototype-build
	$(bin)/python -m http.server 8081 -d prototype/_site

prototype-build:
	rm -rf prototype/_site
	$(bin)/python prototype/build.py
