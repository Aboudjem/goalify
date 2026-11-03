.PHONY: test lint

test:
	python3 -m pytest

lint:
	ruff check .

install:
	pip install -e .

%.o: %.c
	gcc -c $< -o $@
