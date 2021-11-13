FROM python:3.9-buster

ENV POETRY_VERSION=1.1.8
ENV PORT=8000
ENV WORKERS=2

EXPOSE $PORT

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /workspace

COPY poetry.lock .
COPY pyproject.toml .
COPY hook_web hook_web/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && pybabel compile -d hook_web/translations/

CMD gunicor -w ${WORKERS} -b 0.0.0.0:${PORT} hook_web.wsgi:app
