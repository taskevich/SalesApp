FROM python:3.12-slim AS builder

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN rm requirements.txt

WORKDIR /app

COPY . .

RUN alembic stamp head && alembic upgrade head

CMD ["bash", "-c", "export $(xargs < .env) && python3 app/app.py"]
