FROM python:3.12-slim AS builder

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN rm requirements.txt

WORKDIR /app

COPY . .

EXPOSE ${FLASK_RUN_PORT}

CMD ["bash", "-c", "export $(xargs < .env) && alembic upgrade head && flask --app app/app run --debug --port ${FLASK_RUN_PORT} --host ${FLASK_RUN_HOST}"]
