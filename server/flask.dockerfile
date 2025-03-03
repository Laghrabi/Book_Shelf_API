FROM python:3.8-slim

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y pkg-config
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y build-essential

WORKDIR /Book_Shelf_API

COPY . /Book_Shelf_API

RUN pip3 install flask==2.1.0 werkzeug==2.1.1 flask-cors==4.0.1 sqlalchemy==1.4.22 mysqlclient==2.2.4 python-dotenv flask-jwt-extended flask-swagger-ui requests

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

EXPOSE 5000

COPY wait-for-mysql.sh /usr/local/bin/wait-for-mysql.sh
RUN chmod +x /usr/local/bin/wait-for-mysql.sh

WORKDIR /Book_Shelf_API/server

CMD ["wait-for-mysql.sh", "python3", "-m", "api.app"]