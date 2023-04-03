# Makefile for Django project

# Run the development web server
run:
	python web/selecto/manage.py runserver 8080

# Apply database migrations
migrate:
	python web/selecto/manage.py migrate