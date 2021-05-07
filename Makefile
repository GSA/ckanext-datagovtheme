.PHONY: lint

clean:
	find . -name *.pyc -delete
	docker-compose down -v --remove-orphan

lint:
	pip install pip==20.3.3
	pip install flake8
	flake8 . --count --ignore E501 --show-source --statistics
