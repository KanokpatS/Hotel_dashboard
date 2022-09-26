FROM python:3.8-slim-buster

WORKDIR /app

ADD requirement.txt /app/

RUN pip install -r requirement.txt

ADD . /app/

ENTRYPOINT [ "python3" ]
CMD ["dashboard/app.py"]
