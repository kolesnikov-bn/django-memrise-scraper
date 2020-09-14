FROM python:3.8-alpine
EXPOSE 5000
WORKDIR /app

RUN pip install -U pipenv==2020.8.13
COPY Pipfile* ./

RUN apk add --update --no-cache --virtual .build-deps \
        g++ \
        gcc \
        libc-dev \
        libxml2-dev \
        libxslt-dev \
        musl-dev \
        postgresql-dev \
    && apk add --update --no-cache \
         tzdata \
         git \
         libxslt \
         postgresql \
    && ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime \
    && mkdir -p /var/logs \
    && pipenv install --system --deploy \
    && apk del .build-deps \
    && rm -rf /var/cache/apk/*

COPY . .

CMD ["./entry.sh"]