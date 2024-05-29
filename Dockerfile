FROM amazonlinux

RUN yum update

# Get Python and PIP
RUN yum install python3
ADD https://bootstrap.pypa.io/get-pip.py /
RUN python3 get-pip.py

# Get Ollama
RUN yum install -y findutils
RUN curl -fsSL https://ollama.com/install.sh | sh

ADD run-ollama.sh /
RUN chmod +x /run-ollama.sh

COPY . .

# Get Python dependencies
ADD dependencies.sh /
RUN chmod +x /dependencies.sh
RUN ["/dependencies.sh"]

CMD ["./run-ollama.sh"]
CMD ["python3", "main.py"]