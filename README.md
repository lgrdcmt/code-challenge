Bom este é a resolução de um desafio do programa Lighthouse da Indicium.
E para realizar esse desafio necessitamos de algumas ferramentas como requisitos:
Docker
Python
Pipx
Meltano

Após a instalação do Docker, Python e Pipx. Lembre-se de usar o seguinte comando para instalar o Meltano:

pipx install meltano==3.6.0 –python 3.10

Após a instalação do pacote as seguintes linhas de comando:

chmod +x install.sh

./install


Após a execução, acessar com o navegador o endereço http://localhost:8080 e usar airflow para login e senha.

OBS.: Antes de executar as dags no apache airflow, alterar o source dentro das dags1 e dags2 para a pasta base do projeto.
