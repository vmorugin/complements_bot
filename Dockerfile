FROM python:3.10-bullseye

LABEL maintainer="vamorugin@gmail.com"

ENV POETRY_VERSION=1.2.0

COPY src /app
COPY poetry.lock pyproject.toml /app/
WORKDIR /app

RUN pip install "poetry==$POETRY_VERSION"

RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi

CMD ["python3", "main.py"]