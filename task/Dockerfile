FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /code

COPY ./requirements.txt /code/
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app
COPY ./migration /code/migration
COPY ./alembic.ini /code/alembic.ini

EXPOSE 80

CMD ["/bin/sh", "-c", \
    "alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
