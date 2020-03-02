# Based on
# https://medium.com/@greut/minimal-python-deployment-on-docker-with-uwsgi-bc5aa89b3d35
# but not using Alpine because this distribution is not compatible with Python manylinux binaries.
FROM python:3.8.2-slim-buster

ENV WSB_PORT=3031

RUN apt-get update &&  apt-get install -y build-essential libpq-dev python3-dev \
    && pip3 install uwsgi psycopg2 \
    && apt-get remove -y --purge build-essential libpq-dev python3-dev

# Create a working directory named app
WORKDIR /app
# Copy everything into the working directory
COPY . .
# Change ownership of the app folder to match the user running uwsgi
RUN chown -R www-data:www-data /app

# Install all requirements
RUN pip3 install -r requirements.txt

# uWSGI will be available on this port
EXPOSE $WSB_PORT

CMD [ "uwsgi", "--uid", "uwsgi", \
               "--ini",  "uwsgi.ini"]
