CKAN_VERSION ?= 2.9
COMPOSE_FILE ?= docker-compose.yml

build: ## Build the  docker containers
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) build

clean: ## Clean workspace and containers
	find . -name *.pyc -delete
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) down -v --remove-orphans

lint: ## Lint the code (python 3 only)
	docker-compose -f $(COMPOSE_FILE) run --rm ckan flake8 ckanext --count --show-source --statistics --exclude ckan

test: ## Run extension tests
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) run --rm ckan ./test.sh

ui-test:
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) -f docker-compose.test.yml up --abort-on-container-exit test

up: ## Start the containers
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) up

upd: ## Start the containers in the background
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) run --rm ckan ckan search-index rebuild -i -o -e
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) up -d

.DEFAULT_GOAL := help
.PHONY: build clean help lint test up upd

# Output documentation for top-level targets
# Thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
