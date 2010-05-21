.PHONY: help all test

help:
	@echo 'nothing to do'

all:

test:
	PYTHONPATH=src/py python test/py/main.py

