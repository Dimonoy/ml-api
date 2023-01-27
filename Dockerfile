FROM python:3.10
LABEL maintainer="chodima0@gmail.com"
COPY . /rest-api
WORKDIR /rest-api
RUN pip install -r requirements.txt
EXPOSE 8180
EXPOSE 8181
VOLUME /rest-api/app/models
COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
