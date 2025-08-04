FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app

COPY . /app

RUN pip install sqlalchemy pymysql mysqlclient cryptography
