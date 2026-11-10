# Base image: small nginx web server
FROM nginx:alpine
# Proxy config: forwards /api/ to the api Service
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Static web UI served by nginx
COPY index.html /usr/share/nginx/html/index.html
