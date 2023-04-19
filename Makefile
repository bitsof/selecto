# Makefile for Django project

# Run the development web server
run:
	python web/selecto/manage.py runserver 8000

# Apply database migrations
migrate:
	python web/selecto/manage.py migrate

install:
	pip install -r web/selecto/requirements.txt

test:
	pytest -rs web/selecto/tests/

# Initalize db
init_db:
	python web/selecto/manage.py init_db
