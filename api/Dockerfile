FROM python:3.6.2

LABEL maintainer dominique

ENV PYTHONUNBUFFERED 1

ENV DJANGO_SETTINGS_MODULE 'coconut_server.settings'

RUN mkdir /docker_api

WORKDIR /docker_api

COPY . /docker_api

RUN pip install -r requirements.txt

# RUN python manage.py migrate

# RUN python manage.py loaddata fixtures/*

# RUN python manage.py collectstatic  --noinput
# RUN pip install  -i  https://pypi.python.org/simple/  -r requirements.txt