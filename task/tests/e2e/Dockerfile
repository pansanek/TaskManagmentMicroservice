FROM python:3.10

WORKDIR /task

COPY ./task/requirements.txt /task/
RUN pip install --no-cache-dir -r /task/requirements.txt

COPY ./task/app /task/app
COPY ./task/migration /task/migration
COPY ./task/alembic.ini /task/alembic.ini

EXPOSE 80

CMD ["/bin/sh", "-c", \
    "alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 80"]
