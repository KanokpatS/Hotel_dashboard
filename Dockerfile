FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update && \
    apt-get install --no-install-recommends -y python3.8 python3-pip python3.8-dev
RUN pip install --upgrade pip
RUN pip install pandas
RUN pip install openpyxl
RUN pip install dash
RUN pip install plotly
RUN pip install dash
RUN pip install dash-bootstrap-components
RUN pip install -U scikit-learn
