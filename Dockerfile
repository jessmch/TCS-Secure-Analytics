FROM python:3.9
WORKDIR /app
COPY . .
ADD dependencies.sh /
RUN chmod +x /dependencies.sh
RUN ["/dependencies.sh"]
CMD ["python3 main.py"]
#EXPOSE 3000