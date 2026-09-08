.PHONY: install test demo
install:
	pip install -e ".[dev]"
test:
	pytest -q
demo:
	python -m io_detect.cli detect --input tests/fixtures/synthetic.csv
