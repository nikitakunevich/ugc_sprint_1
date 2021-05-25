FROM python:3.9.1-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG ROOT_DIR=/app/

WORKDIR $ROOT_DIR

RUN apt-get update && apt-get install -y netcat

COPY api/Pipfile api/Pipfile.lock $ROOT_DIR

RUN python -m pip install --upgrade pip && pip install pipenv
RUN pipenv install --system --ignore-pipfile

COPY api/src/ $ROOT_DIR

COPY api/docker/wait-services.sh $ROOT_DIR
RUN chmod +x wait-services.sh

ENTRYPOINT ["./wait-services.sh", "uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]