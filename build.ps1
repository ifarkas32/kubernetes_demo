$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

docker build -t greeter-db:1.0  ./db
docker build -t greeter-api:1.1 ./api
docker build -t greeter-web:1.1 ./web
