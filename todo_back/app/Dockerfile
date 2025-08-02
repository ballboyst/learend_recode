FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install pymysql cryptography --no-cache-dir 

CMD ["python", "app.py"]
