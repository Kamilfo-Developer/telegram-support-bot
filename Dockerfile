# Preparing the requirements for installing
FROM python:latest as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Installing the requirements
FROM python:latest

WORKDIR /app

COPY . /app

# Installing the dependencies
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Making migrations using alembic
RUN cd /app/bot/db/migrations && alembic upgrade head && cd /app 

CMD ["python3", "-m", "bot"]