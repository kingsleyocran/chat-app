all: build_packages run_application_locally

build_packages:
	pip install --no-cache-dir --upgrade pip && pip install --no-cachdir poetry \
    && poetry config virtualenvs.create false  \
    && poetry install --no-interaction --no-ansi --without dev && \
      sudo apt install redis -y && alembic upgrade head

build_docker_application:
	docker build --no-cache -t chat_application_account .
	docker run -it -p 8081:8081 chat_application_account

run_application_locally:
	uvicorn main:app --reload --port 8081


.PHONY: all
