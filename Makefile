.DEFAULT: test

clean:
	docker-compose -f docker-compose.ckan.yml down -v --remove-orphans
lint:
	pip install pip==20.3.3
	pip install flake8
	flake8 . --count --ignore E402,E501 --show-source --statistics

test:
	docker-compose -f docker-compose.ckan.yml run --rm app ./test.sh

.PHONY: clean lint test
