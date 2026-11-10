# Base image: PostgreSQL 16 on Alpine
FROM postgres:16-alpine
# Scripts in this folder run once, when the data directory is empty
COPY init.sql /docker-entrypoint-initdb.d/init.sql
