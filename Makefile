install:
	pip install -Ur requirements.txt
	make db-create -i
	make db-migrate -i

db-create:
	python manage.py db_create

db-migrate:
	python manage.py makemigrations
	python manage.py migrate

db-clean:
	python manage.py db_clean

db-drop:
	python manage.py db_drop

serve:
	python manage.py runserver

test:
	coverage run --source='.' manage.py test
	coverage report

test-hot-reload:
	./bin/watch_test.sh

.PHONY: install db-create db-migrate db-clean db-drop serve test test-hot-reload
