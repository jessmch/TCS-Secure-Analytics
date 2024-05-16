FROM python:3.9
WORKDIR /app
COPY . .
ADD https://ollama.com/install.sh /
ADD dependencies.sh /
RUN chmod +x /dependencies.sh
RUN ["/dependencies.sh"]
CMD ["ollama run mistral", "python3 main.py"]
#EXPOSE 3000