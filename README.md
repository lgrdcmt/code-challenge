# Desafio Lighthouse - Indicium

Este repositório contém a resolução do desafio do programa **Lighthouse** da **Indicium**.

## Requisitos

Antes de executar o projeto, certifique-se de ter o **Docker** instalado em sua máquina.

## Instalação

Após instalar o [Docker](https://www.docker.com/), siga os passos abaixo para configurar e executar o ambiente:  

1. Conceda permissão de execução ao script de instalação:  
   ```bash
   chmod +x install.sh
   ```

2. Execute o script de instalação:
   ```bash
   ./install.sh
   ```

3. Após a execução, acesse o Apache Airflow no navegador (http://localhost:8080) e use as seguintes credenciais para login:
- Usuário: airflow
- Senha: airflow

## Configuração Adicional

Antes de executar as DAGs no Apache Airflow, é necessário ajustar os caminhos dos arquivos de origem:

- Dentro das DAGs dags1 e dags2, altere o parâmetro source para o diretório base do projeto, ou seja alterar o ponto de montagem para acesso do container docker as pastas.
