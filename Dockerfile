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
COPY shell_scripts shell_scripts/
COPY _cmd.py .

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && pybabel compile -d hook_web/translations/

CMD /bin/bash ./shell_scripts/service_start.sh
