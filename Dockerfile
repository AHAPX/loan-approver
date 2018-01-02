FROM python:3.6.3

MAINTAINER ivan
MAINTAINER durneviv@gmail.com

COPY src/ /backend/
RUN pip install -U pip
RUN pip install -r /backend/requirements.txt

VOLUME /backend/
WORKDIR /backend/
EXPOSE 8000

CMD ./manage.py runserver 0.0.0.0:8000
