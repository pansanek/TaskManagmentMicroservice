FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /assignee

COPY ./assignee/requirements.txt /assignee/
RUN pip install --no-cache-dir -r /assignee/requirements.txt

COPY ./assignee/app /assignee/app


EXPOSE 81

CMD ["/bin/sh", "-c", \
    "uvicorn app.main:app --host 0.0.0.0 --port 81"]
