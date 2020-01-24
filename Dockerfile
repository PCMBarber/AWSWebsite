FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /AWSWebsite/requirements.txt

WORKDIR /AWSWebsite

RUN pip install -r requirements.txt

COPY . /AWSWebsite

ENTRYPOINT [ "python", "app.py" ]
##ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:5000", "application:app" ]
