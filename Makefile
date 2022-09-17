.DEFAULT_GOAL := help

.PHONY: test
test: # Run tests with pytest and coverage
test: 
	coverage erase
	coverage run -m pytest -v --disable-warnings
	coverage report -m

BLACK_OPTS := -l 95
SRC_FILES := arg_validators dataframe_utils graph_utils plot text_utils
SRC_FILES := $(addprefix pyforestplot/, $(addsuffix .py, $(SRC_FILES))) 
.PHONY: lint
lint: # Check with mypy, pyflakes, black
lint: 
	mypy $(SRC_FILES) --ignore-missing-imports
	python -m pyflakes tests/*.py $(SRC_FILES)
	black pyforestplot/*.py $(BLACK_OPTS)
	black tests/*.py $(BLACK_OPTS)

.PHONY: prepack
prepack: # Prepare packaging for PyPi
prepack:
	@rm -rf dist/ pyforestplot.egg-info/
	@python setup.py sdist
	twine check dist/*

PACKAGE_FILES := build/ dist/ *.egg-info/ *.egg
.PHONY: cleanpack
cleanpack: # Remove distribution/packaging files
cleanpack:
	@rm -rf $(PACKAGE_FILES)

.PHONY: help
help: # Show Help
	@egrep -h '\s#\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
