## STAGE: BUILDER
FROM python:3.10-slim as builder

WORKDIR /build/
ENV POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1
RUN pip install --no-cache-dir poetry

COPY ./pyproject.toml ./poetry.lock /build/
RUN poetry export --dev --without-hashes --format requirements.txt --output requirements.txt && \
    pip install --no-cache-dir --requirement requirements.txt

COPY ./ /build/
RUN poetry build && poetry install


## STAGE: RUNNER
FROM python:3.10-slim AS runner

RUN groupadd -r --gid 1000 slackbox && \
    useradd -r --uid 1000 --gid 1000 slackbox

COPY --from=builder /build/dist/ /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && \
    rm -rf /tmp/*

USER slackbox
CMD gunicorn --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 slackbox.main:app
