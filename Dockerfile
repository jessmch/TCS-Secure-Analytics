FROM python:3.9
WORKDIR /app
COPY . .
RUN ["pip install pandas pandasai langchain langchain_experimental cryptography", "curl -fsSL https://ollama.com/install.sh | sh", "ollama run mistral"]
CMD ["python3 main.py"]
#EXPOSE 3000