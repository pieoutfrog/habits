FROM python:3
LABEL authors="pieoutfrog"

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .