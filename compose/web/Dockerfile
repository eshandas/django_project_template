FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /web_app
WORKDIR /web_app
ADD ./web /web_app/

RUN pip install -r /web_app/requirements/local.txt

COPY ./compose/web/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start