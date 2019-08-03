# A container to compile and serve out TypeScript
# Thanks Microsoft!
# https://github.com/Microsoft/vscode-recipes/tree/master/Docker-TypeScript
FROM node:8-slim

RUN mkdir /code
RUN mkdir /code/src
RUN mkdir /code/build
RUN mkdir /code/public
WORKDIR /code

COPY package.json /code
COPY tsconfig.json /code
COPY yarn.lock /code
RUN yarn install

EXPOSE 3000
CMD [ "yarn", "start" ]
