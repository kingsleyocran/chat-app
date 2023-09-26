all: build_packages run_application_locally

build_packages:
	pip install --no-cache-dir --upgrade pip && pip install --no-cachdir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev && \
   sudo apt install redis -y

build_docker_application:
	docker build --no-cache -t chat_application_chat_service .
	docker run -it -p 8001:8001 chat_application_chat_service

run_application_locally:
	gunicorn --env DJANGO_SETTINGS_MODULE=core.settings core.wsgi -b :8001


.PHONY: all
