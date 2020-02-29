# Based on
# https://medium.com/@greut/minimal-python-deployment-on-docker-with-uwsgi-bc5aa89b3d35
# but not using Alpine because this distribution is not compatible with Python manylinux binaries.
FROM python:3.8.2-slim-buster

RUN apt-get update &&  apt-get install -y build-essential libpq-dev \
    && pip3 install uwsgi psycopg2 \
    && apt-get remove -y --purge build-essential libpq-dev

# Create a working directory named app
WORKDIR /app
# Copy everything into the working directory
COPY . .

# Install all requirements
RUN pip3 install -r requirements.txt

# uWSGI will be available on this port
EXPOSE 3031

CMD [ "uwsgi", "--socket", "0.0.0.0:3031", \
               "--uid", "uwsgi", \
               "--plugins", "python3", \
               "--protocol", "uwsgi", \
               "--wsgi", "main:application" ]