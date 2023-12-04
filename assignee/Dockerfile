FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app
COPY ./migration /app/migration
COPY ./alembic.ini /app/

EXPOSE 80

CMD ["sh", "-c", "alembic upgrade head && uvicorn assignee.app.main:app --host 0.0.0.0 --port 80"]
