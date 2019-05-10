# A container to compile and serve out TypeScript
# Thanks Microsoft!
# https://github.com/Microsoft/vscode-recipes/tree/master/Docker-TypeScript
FROM node:8-slim

WORKDIR /code

COPY package.json /code
COPY tsconfig.json /code
RUN npm install

EXPOSE 3000
CMD [ "npm", "start" ]
