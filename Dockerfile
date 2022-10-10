# Docker file for development
FROM ubuntu:20.04

WORKDIR /app

ADD requirement.txt /app/

RUN apt-get update && \
    apt-get install --no-install-recommends -y python3.8 python3-pip python3.8-dev
RUN pip install --upgrade pip
RUN pip install -r requirement.txt

# Docker file for deployment
#FROM python:3.8-slim-buster
#
#WORKDIR /app
#
#ADD requirement.txt /app/
#
#RUN pip install -r requirement.txt
#
#ADD . /app/
#
#ENTRYPOINT [ "python3" ]
#CMD ["dashboard/app.py"]

