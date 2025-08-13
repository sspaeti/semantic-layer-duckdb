.DEFAULT_GOAL := query

help: ## Show all Makefile targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install:
	pip install -r requirements.txt

run:
	python nyc_taxi.py

query:
	source ~/.venvs/boring-sl-duckdb/bin/activate && \
	python nyc_taxi.py && \
	deactivate
