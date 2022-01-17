CKAN_VERSION ?= 2.9
COMPOSE_FILE ?= docker-compose.yml

build: ## Build the  docker containers
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) build

clean: ## Clean workspace and containers
	find . -name *.pyc -delete
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) down -v --remove-orphans

lint: ## Lint the code (python 3 only)
	docker-compose -f $(COMPOSE_FILE) run --rm app flake8 ckanext --count --show-source --statistics --exclude ckan

test-legacy: ## Run legacy tests in an existing container
	@# TODO wait for CKAN to be up; use docker-compose run instead
	docker-compose -f $(COMPOSE_FILE) exec ckan /bin/bash -c "nosetests --ckan --with-pylons=src/ckan/test-catalog-next.ini src_extensions/datagovtheme/ckanext/datagovtheme/tests/nose"

test: ## Run extension tests
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) run --rm app ./test.sh

up: ## Start the containers
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) up

upd: ## Start the containers in the background
ifeq ($(CKAN_VERSION), 2.8)
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) run --rm app paster --plugin=ckan search-index rebuild -i -o -e
else
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) run --rm app ckan search-index rebuild -i -o -e
endif
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) up -d

.DEFAULT_GOAL := help
.PHONY: clean help lint test test-legacy up

# Output documentation for top-level targets
# Thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
