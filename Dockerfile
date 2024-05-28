FROM python:3.9
COPY . .
ADD https://ollama.com/install.sh /
ADD dependencies.sh /
RUN chmod +x /dependencies.sh
RUN ["/dependencies.sh"]
CMD ["ollama", "run", "mistral"]
CMD ["python3", "main.py"]