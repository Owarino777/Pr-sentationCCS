FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html
COPY assets /usr/share/nginx/html/assets
COPY README.md /usr/share/nginx/html/README.md
COPY DEPLOYMENT.md /usr/share/nginx/html/DEPLOYMENT.md

EXPOSE 80