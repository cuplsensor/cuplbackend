FROM tiangolo/uwsgi-nginx-flask:python3.7 as buildstage1
ADD ./uwsgi.ini /app/uwsgi.ini
ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt --cache-dir /pip-cache
RUN echo "deb http://ftp.debian.org/debian stretch-backports main" >> /etc/apt/sources.list.d/mm.list
RUN apt --assume-yes update && apt --assume-yes upgrade
RUN apt-get --assume-yes install python-certbot-nginx -t stretch-backports
# Get graphviz to draw the SQL entity relationship diagram
RUN apt-get --assume-yes install graphviz
# URL under which static (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
ENV STATIC_URL /static
# Absolute path in where the static files will be
ENV STATIC_PATH /app/charityapp/frontend/static
# Server name
ENV SERVER_NAME websensor.io
# Copy the entrypoint that will generate Nginx additional configs
# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Supervisor, which in turn will start Nginx and uWSGI

FROM buildstage1 as buildstage2
ADD ./ /app
ADD ./prestart.sh /app/prestart.sh
COPY custom.conf /etc/nginx/conf.d/custom.conf
COPY ./prestart.sh /app/prestart.sh:
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chmod +x /app/prestart.sh
ENTRYPOINT ["/entrypoint.sh"]
# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Supervisor, which in turn will start Nginx and uWSGI
CMD ["/start.sh"]
EXPOSE 80 443


