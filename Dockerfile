FROM node:latest as build-stage
WORKDIR /app
COPY front/package*.json ./
RUN npm install
COPY front/ .
RUN npm run build

FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf


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
COPY --from=build-stage /app/dist /app/front/dist
#COPY nginx.conf /etc/nginx/nginx.conf

CMD ["./entry.sh"]