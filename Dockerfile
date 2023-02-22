FROM python:latest

WORKDIR /app/

COPY . .

RUN pip3 install -r requirements/prod.txt 

