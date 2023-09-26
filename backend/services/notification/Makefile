all: build_packages run_application_locally

build_packages:
	sudo apt install redis -y && \
	pip install --no-cache-dir --upgrade pip && pip install --no-cachdir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev

build_docker_application:
	docker build --no-cache -t chat_application_notification .
	docker run -it chat_application_notification

run_application_locally:
	celery -A main worker --loglevel=INFO 


.PHONY: all
