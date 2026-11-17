# goalify: the two commands a contributor needs.
#   make test   run every suite (the same command CI runs)
#   make demo   build the demo project in a temp folder and print a real proof receipt

.PHONY: test demo

test:
	python3 tests/run_all.py

demo:
	python3 examples/demo/run.py
