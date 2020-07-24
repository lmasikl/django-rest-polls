default: run

run:
	@docker-compose up --build -d api

logs:
	@docker-compose logs -f api

test:
	@docker-compose up --build autotests

makemigrations:
	@pipenv run ./manage.py makemigrations

migrate:
	@pipenv run ./manage.py migrate

run-dev:
	@pipenv run ./manage.py runserver
