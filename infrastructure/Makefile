# Simple Makefile for pyATS Infrastructure Framework

.PHONY: help build test clean shell version

help: ## Show this help message
	@echo "pyATS Infrastructure Framework - Simple Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build the pyATS container
	docker-compose build

test: ## Test the pyATS installation
	docker-compose run --rm pyats pyats version

shell: ## Open interactive shell in container
	docker-compose run --rm pyats bash

python: ## Open Python shell with pyATS
	docker-compose run --rm pyats python

version: ## Show pyATS version
	docker-compose run --rm pyats pyats version

clean: ## Clean up Docker containers and images
	docker-compose down --rmi all --volumes --remove-orphans

# Quick commands for common tasks
quick-test: ## Quick test - build and verify
	$(MAKE) build
	$(MAKE) test
	@echo "✅ pyATS framework ready!"