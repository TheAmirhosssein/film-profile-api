FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip poetry flake8

COPY pyproject.toml poetry.lock /app/

RUN poetry install

COPY . /app/

EXPOSE 8000


