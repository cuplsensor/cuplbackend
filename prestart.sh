#! /usr/bin/env bash


echo "Running inside /app/prestart.sh, you could add migrations to this file, e.g.:"

# Get the URL for static files from the environment variable
USE_STATIC_URL=${STATIC_URL:-'/static'}
# Get the absolute path of the static files from the environment variable
USE_STATIC_PATH=${STATIC_PATH:-'/app/static'}
# Generate Nginx config first part using the environment variables
if [ ! -f "/etc/nginx/conf.d/custom.conf" ]; then
echo "server {
    server_name $SERVER_NAME;
    location / {
        try_files \$uri @app;
    }
    location @app {
        include uwsgi_params;
        uwsgi_pass unix:///tmp/uwsgi.sock;
    }
    location $USE_STATIC_URL {
         alias $USE_STATIC_PATH;
     }
}" > /etc/nginx/conf.d/custom.conf
fi
#echo "TEST TEST TEST"
#! /usr/bin/env bash
# Let the DB start
#cd alembic
#echo $PWD
#sleep 10;
# Run migrations
# alembic upgrade head
# TEST TEST TEST"
