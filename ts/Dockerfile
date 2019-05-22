# A container to compile and serve out TypeScript
# Thanks Microsoft!
# https://github.com/Microsoft/vscode-recipes/tree/master/Docker-TypeScript
FROM node:8-slim

RUN mkdir /code
RUN mkdir /code/src
RUN mkdir /dist
WORKDIR /code
RUN npm install typescript -g

COPY package.json /code
COPY src/tsconfig.json /code/src
RUN npm install

EXPOSE 3000
CMD [ "npm", "start" ]
