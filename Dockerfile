FROM node:18-alpine
WORKDIR /app
COPY . .
RUN yum install --production
EXPOSE 3000