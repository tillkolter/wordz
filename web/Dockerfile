FROM python:3.6

COPY ./docker-entrypoint.sh /app/docker-entrypoint.sh

COPY ./app /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /app/wait-for-it.sh
RUN ls /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh
RUN ls /app/wait-for-it.sh
WORKDIR /app

ENTRYPOINT ["./docker-entrypoint.sh"]
