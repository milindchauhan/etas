FROM node:16

WORKDIR /app

COPY ./functions .

RUN npm install node-fetch

# run the following command to build your image
# docker build -t node-test .
