FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /master
ENV PYTHONPATH /master/

RUN apt-get update -o Acquire::Check-Valid-Until=false &&\
    apt-get install -y build-essential libpq-dev ncat netcat-traditional -o Acquire::Check-Valid-Until=false

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

