# Build app image
FROM python:3.12.3

WORKDIR /app/

ADD ./app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ADD ./app/ /app

ENV PYTHONUNBUFFERED=1

ENTRYPOINT [ "flask",  "--app", "app", "run" ]