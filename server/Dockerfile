FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/src/app
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir -p /usr/src/app/server/
WORKDIR /usr/src/app/server/

RUN mkdir -p /usr/src/app/media/

COPY . /usr/src/app/server/

RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt