FROM python:3.11-slim

ENV LANG C.UTF-8
ENV TZ Asia/Tokyo

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./.env /app/.env
RUN apt update && apt-get update
RUN apt-get install -y --no-install-recommends build-essential
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./src /app/src
ENV PYTHONPATH=/app/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
