FROM debian:latest

MAINTAINER Polarnodes "contact@polarnodes.finance"

RUN apt-get update -y && apt-get install -y apt-utils python3 python3-pip

COPY ./ ./app

WORKDIR ./app

RUN pip3 install -r requirements.txt

CMD ["python3", "./main.py"]