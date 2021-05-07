clean:
	find . -name *.pyc -delete
	docker-compose down -v --remove-orphan

lint:
	pip install pip==20.3.3
	pip install flake8
	flake8 . --count --ignore E501 --show-source --statistics

test:
	# TODO wait for CKAN to be up; use docker-compose run instead
	docker-compose exec ckan /bin/bash -c "nosetests --ckan --with-pylons=src/ckan/test-catalog-next.ini src_extensions/datagovtheme/ckanext/datagovtheme/tests"

up:
	docker-compose up


.PHONY: clean lint test up
