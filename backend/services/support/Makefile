all: build_packages run_application_locally

build_packages:
	pip install --no-cache-dir --upgrade pip && pip install --no-cachdir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev

build_docker_application:
	docker build --no-cache -t chat_application_account .
	docker run -it -p 8084:8084 chat_application_account

run_application_locally:
	uvicorn main:app --reload --port 8084


.PHONY: all
