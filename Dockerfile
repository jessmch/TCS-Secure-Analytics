FROM amazonlinux

# Get Python and PIP
RUN yum install python3
ADD https://bootstrap.pypa.io/get-pip.py /
RUN python3 get-pip.py

# Get Ollama
RUN yum -y install findutil
curl -fsSL https://ollama.com/install.sh | sh

COPY . .

# Get Python dependencies
ADD dependencies.sh /
RUN chmod +x /dependencies.sh
RUN ["/dependencies.sh"]

#CMD ["ollama", "run", "mistral"]
CMD ["python3", "main.py"]