migrations:
	python manage.py makemigrations
	
migrate:
	python manage.py migrate

create_su:
	python manage.py createsuperuser

run_celery:
	celery -A app worker -l info

serve:
	python manage.py runserver 0.0.0.0:8001

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

collect:
	python manage.py collectstatic

messages:
	django-admin makemessages

messages_es:
	django-admin makemessages -l es_ES

messages_en:
	django-admin makemessages -l en_US

messages_fr:
	django-admin makemessages -l fr_FR

compile:
	django-admin compilemessages

test_gcorn:
	gunicorn --bind 0.0.0.0:8001 app.wsgi

create_gcorn_soket:
	sudo nano /etc/systemd/system/recul.socket

create_gcorn_service:
	sudo nano /etc/systemd/system/recul.service

start_gcorn:
	sudo systemctl start recul.socket

restart:
	sudo systemctl restart recul

enable_gcorn:
	sudo systemctl enable recul.socket

check_gcorn_status:
	sudo systemctl status recul.socket

ga:
	git add -A

push:
	git push

pull:
	git pull <remote_url>
