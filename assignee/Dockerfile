FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /assignee

COPY ./assignee/requirements.txt /assignee/
RUN pip install --no-cache-dir -r /assignee/requirements.txt

COPY ./assignee/app /assignee/app
COPY ./assignee/migration /assignee/migration
COPY ./assignee/alembic.ini /assignee/alembic.ini

EXPOSE 81

CMD ["/bin/sh", "-c", \
    "alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 80"]
