FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY .htpasswd /etc/nginx/.htpasswd
COPY index.html /usr/share/nginx/html/index.html
RUN echo "A browser is pointed at localhost:8198"