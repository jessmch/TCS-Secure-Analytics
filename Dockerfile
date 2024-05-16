FROM node:18-alpine
WORKDIR /app
COPY . .
CMD ["python3 main.py"]
EXPOSE 3000