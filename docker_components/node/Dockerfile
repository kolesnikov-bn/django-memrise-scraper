FROM node:latest

WORKDIR /usr/src/app
COPY docker_components/node/package.json .
RUN npm install

RUN apt-get update && apt-get install -y vim

COPY docker_components/node/server.js .

ENTRYPOINT ["node", "server.js"]