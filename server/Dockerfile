FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/src/hotopia
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir -p /usr/src/hotopia/server/
WORKDIR /usr/src/hotopia/server/

RUN mkdir -p /usr/src/hotopia/media/

COPY . /usr/src/hotopia/server/
COPY ../config.py /usr/src/hotopia/

RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt