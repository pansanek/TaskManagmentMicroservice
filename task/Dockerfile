FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app
COPY ./migration /app/migration
COPY ./alembic.ini /app/

EXPOSE 80

CMD ["/bin/sh", "-c", \
    "alembic upgrade head && \
    uvicorn task.app.main:app --host 0.0.0.0 --port ${PORT}"]
