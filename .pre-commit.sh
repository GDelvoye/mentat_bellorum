#! /usr/bin/env bash

flake8 --max-complexity 15 back
pytest back/tests/
mypy back --check-untyped-defs
isort --profile black back --check
