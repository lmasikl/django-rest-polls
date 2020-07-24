release: python manage.py migrate --no-input
release: pipenv run python manage.py migrate loaddata initial_data.json
web: gunicorn -w ${WEB_CONCURRENCY:-5} --max-requests ${MAX_REQUESTS:-1200} api.wsgi --log-file -
