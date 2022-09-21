FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update && \
    apt-get install --no-install-recommends -y python3.8 python3-pip python3.8-dev
RUN pip install --upgrade pip
RUN pip install pandas
RUN pip install openpyxl
RUN pip install dash
RUN pip install plotly
RUN pip install geopandas
RUN pip install dash
RUN pip install dash-bootstrap-components
RUN pip install dash-bootstrap-templates
RUN pip install dash-leaflet
RUN pip install dash-labs
RUN pip install -U scikit-learn

# docker run -it --name test_alto -v $PWD\:/app -p 8050:8050 test_alto

#FROM python:3.8
#
#WORKDIR /app
#
#RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
#RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
#RUN apt-get -y update
#RUN apt-get install -y google-chrome-stable
#RUN apt-get install -yqq unzip
#RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`
#curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE
#`/chromedriver_linux64.zip
#RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
#ENV DISPLAY=:99
#
#RUN pip install --upgrade pip
#RUN pip install beautifulsoup4
#RUN pip install requests
#RUN pip install --user selenium==3.5.0