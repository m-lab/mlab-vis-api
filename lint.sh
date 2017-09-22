#!/bin/bash

# Test coverage:
COVERAGE=coverage
if [[ -z $(which $COVERAGE) ]]; then
  COVERAGE=python-coverage
fi

PYTHONFILES=$(git ls-files | grep '\.py$')
CODEONLYFILES=$(git ls-files | grep '\.py$' | grep -v '^test')

$COVERAGE report -m ${CODEONLYFILES}

# Code linting
pylint --rcfile=git-hooks/pylintrc \
       --output-format=colorized \
       --reports=n \
       ${PYTHONFILES}