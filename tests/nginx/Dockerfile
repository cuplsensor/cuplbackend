FROM nginx:latest

# Nginx will listen on this port
EXPOSE 80

# Remove the default config file that
# /etc/nginx/nginx.conf includes
RUN rm /etc/nginx/conf.d/default.conf

COPY wsbackend.conf /etc/nginx/conf.d

CMD /bin/bash -c "exec nginx -g 'daemon off;'"
