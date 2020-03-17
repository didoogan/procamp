FROM python:3.8-slim

MAINTAINER Dima Timoshenko "tzd04094@gmail.com"

RUN apt update -y && apt install -y python-pip python3-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT ["python", "metrics.py"]

CMD ["cpu"]
