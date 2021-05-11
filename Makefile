CKAN_VERSION ?= 2.8
COMPOSE_FILE ?= docker-compose.yml

build: ## Build the  docker containers
	docker-compose -f $(COMPOSE_FILE) build

clean: ## Clean workspace and containers
	find . -name *.pyc -delete
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) down -v --remove-orphan

lint: ## Lint the code
	pip install pip==20.3.3
	pip install flake8
	flake8 . --count --show-source --statistics --exclude ckan

test: ## Run tests in an existing container
	@# TODO wait for CKAN to be up; use docker-compose run instead
	docker-compose exec ckan /bin/bash -c "nosetests --ckan --with-pylons=src/ckan/test-catalog-next.ini src_extensions/datagovtheme/ckanext/datagovtheme/tests/nose"

test-new: ## Run "new" style tests
	CKAN_VERSION=$(CKAN_VERSION) docker-compose --env-file environment/test -f docker-compose.new.yml run --rm app ./test.sh

up: ## Start the containers
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) up


.DEFAULT_GOAL := help
.PHONY: clean help lint test up

# Output documentation for top-level targets
# Thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
