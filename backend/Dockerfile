FROM python:3.9-alpine3.13

LABEL maintainer='iljavaleev'

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt /app
COPY requirements.dev.txt /app

COPY . /app

EXPOSE 8000

ARG DEV=false
RUN pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    pip install -r requirements.txt && \
    if [ $DEV = "true" ]; \
        then pip install -r requirements.dev.txt; \
    fi && \
    apk del .tmp-build-deps

CMD ["run.sh"]