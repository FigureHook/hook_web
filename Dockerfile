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
COPY docker-entrypoint.sh .

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && pybabel compile -d hook_web/translations/ \
    && chmod +x docker-entrypoint.sh

ENTRYPOINT [ "./docker-entrypoint.sh" ]
CMD [ "start" ]
