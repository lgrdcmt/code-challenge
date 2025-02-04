#!/bin/bash

echo "Instalando as bibliotecas do Meltano"
docker run --rm -it -v $(pwd):/project -w /project meltano/meltano:v3.6.0-python3.10 --cwd meltano install


echo "Gerando imagem docker e iniciando os servicos docker"
cd airflow
docker build ./docker-socket-proxy --tag docker-socket-proxy
docker compose up -d
cd ..
docker compose up -d

