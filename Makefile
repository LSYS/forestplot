.DEFAULT_GOAL := help

.PHONY: test
test: # Run tests with pytest and coverage
test: 
	@echo "+ $@"
	coverage erase
	coverage run -m pytest -v --disable-warnings
	coverage report -m
	
.PHONY: notebook
notebook: # Run notebook with runpynb
notebook:
	@echo "+ $@"
	cd examples && runpynb readme-examples.ipynb

BLACK_OPTS := -l 95
SRC_FILES := arg_validators dataframe_utils graph_utils text_utils plot mplot
SRC_FILES := $(addprefix forestplot/, $(addsuffix .py, $(SRC_FILES))) 
.PHONY: lint
lint: # Check with mypy, pyflakes, black
lint: 
	@echo "+ $@"
# 	mypy $(SRC_FILES) --ignore-missing-imports
	python -m pyflakes tests/*.py $(SRC_FILES)
	python -m pyflakes setup.py
	isort --profile black $(BLACK_OPTS) . 
	black forestplot/*.py $(BLACK_OPTS)
	black forestplot/*.py $(BLACK_OPTS)
	black tests/*.py $(BLACK_OPTS)
	black setup.py $(BLACK_OPTS)

.PHONY: docstring
docstring: # Check docstrings using pydocstyle
	pydocstyle --convention numpy

.PHONY: prepack
prepack: # Prepare packaging for PyPi
prepack:
	@echo "+ $@"
	@rm -rf dist/ forestplot.egg-info/
	@rm -rf dist/ pyforestplot.egg-info/
	@python setup.py sdist bdist_wheel
	twine check dist/*

PACKAGE_FILES := build/ dist/ *.egg-info/ *.egg-info *.egg
.PHONY: cleanpack
cleanpack: # Remove distribution/packaging files
cleanpack:
	@echo "+ $@"
	@rm -rf $(PACKAGE_FILES)

# ===========================================================
.PHONY: setup
VENVPATH ?= venv
ifeq ($(OS),Windows_NT)
	VENVPATH :=  c:/users/admin/$(VENVPATH)
	ACTIVATE_PATH := $(VENVPATH)/Scripts/activate
else
	ACTIVATE_PATH := $(VENVPATH)/bin/activate
endif
REQUIREMENTS := requirements_dev.txt
setup: # Set up venv	
setup: $(REQUIREMENTS)
	@echo "==> $@"
	@echo "==> Creating and initializing virtual environment..."
	rm -rf $(VENVPATH)
	python -m venv $(VENVPATH)
	. $(ACTIVATE_PATH) && \
		pip install --upgrade pip && \
		which pip && \
		pip list && \
		echo "==> Installing requirements" && \
		pip install -r $< && \
		jupyter contrib nbextensions install --sys-prefix --skip-running-check && \
		echo "==> Packages available:" && \
		which pip && \
		pip list && \
		which jupyter && \
		deactivate
	@echo "==> Setup complete."

.PHONY: help
help: # Show Help
	@egrep -h '\s#\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
