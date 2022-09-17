.DEFAULT_GOAL := help

.PHONY: test
test: # Run tests with pytest and coverage
test: 
	@echo "+ $@"
	coverage erase
	coverage run -m pytest -v --disable-warnings
	coverage report -m

BLACK_OPTS := -l 95
SRC_FILES := arg_validators dataframe_utils graph_utils plot text_utils
SRC_FILES := $(addprefix forestplot/, $(addsuffix .py, $(SRC_FILES))) 
.PHONY: lint
lint: # Check with mypy, pyflakes, black
lint: 
	@echo "+ $@"
	mypy $(SRC_FILES) --ignore-missing-imports
	python -m pyflakes tests/*.py $(SRC_FILES)
	python -m pyflakes setup.py
	black forestplot/*.py $(BLACK_OPTS)
	black tests/*.py $(BLACK_OPTS)
	black setup.py $(BLACK_OPTS)

.PHONY: prepack
prepack: # Prepare packaging for PyPi
prepack:
	@echo "+ $@"
	@rm -rf dist/ forestplot.egg-info/
	@python setup.py sdist
	twine check dist/*

PACKAGE_FILES := build/ dist/ *.egg-info/ *.egg-info *.egg
.PHONY: cleanpack
cleanpack: # Remove distribution/packaging files
cleanpack:
	@echo "+ $@"
	@rm -rf $(PACKAGE_FILES)

.PHONY: help
help: # Show Help
	@egrep -h '\s#\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
