FROM nginx:alpine

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY .htpasswd /etc/nginx/.htpasswd
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80