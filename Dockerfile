FROM node:latest as build-stage
WORKDIR /app
COPY front/memrise_front/package*.json ./
RUN npm install
COPY front/memrise_front/ .
RUN npm run build


FROM python:3.8-alpine
EXPOSE 5000
ENV APP_HOME=/app
WORKDIR $APP_HOME

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
         vim \
    && ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime \
    && mkdir -p /var/logs \
    && pipenv install --system --deploy \
    && apk del .build-deps \
    && rm -rf /var/cache/apk/*

COPY . .
COPY --from=build-stage /app/dist $APP_HOME/front/dist

CMD ["./entry.sh"]