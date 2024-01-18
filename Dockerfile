FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH /usr/src/hotopia

RUN mkdir -p /usr/src/hotopia/server
RUN mkdir -p /usr/src/hotopia/common
WORKDIR /usr/src/hotopia/

COPY server/ ./server/
COPY common/ ./common/
COPY .env .

RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r ./server/requirements.txt
