from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime


dag = DAG('dag1_meltanodocker', description='First DAG using Meltano',
          schedule_interval=None, start_date=datetime(2025, 1, 20), 
          catchup=False)

task1 = BashOperator(task_id="tsk1", bash_command="EXEC_DATE={{ds}}", dag=dag)
# docker run -v "$(pwd)":/meltano --name meltano-project -e EXEC_DATE=2025-01-01 -w /meltano meltano-project:dev --cwd meltano lock --update --all && meltano --cwd meltano run postgres_to_csv; docker container rm meltano-project
# task2 = DockerOperator(
#     task_id="tsk2",
#     image="lgrdc/meltano-project:latest",
#     command="echo $EXEC_DATE",
#     api_version="auto",
#     auto_remove=True,
#     docker_url="unix://var/run/docker.sock",
#     network_mode="bridge",
#     # volumes=["/opt/airflow/meltano:/meltano"],
#     # mounts=["/opt/airflow/meltano:/meltano"],
#     environment={"EXEC_DATE": "{{ds}}"},
#     dag=dag
# )

task2 = DockerOperator(
    task_id="tsk2",
    image="python:3.8-slim-buster",
    command='echo "Command running in the docker container"',
    # api_version="auto",
    auto_remove=True,
    # docker_url="unix://var/run/docker.sock",
    docker_url="unix://home/gabriel/.docker/desktop/docker.sock",
    # docker_url="unix://run/docker.sock",
    network_mode="bridge",
    # volumes=["/opt/airflow/meltano:/meltano"],
    # mounts=["/opt/airflow/meltano:/meltano"],
    # environment={"EXEC_DATE": "{{ds}}"},
    dag=dag
)

# task1 = BashOperator(task_id="tsk1", bash_command="pip install pipx && pipx install meltano==3.6.0 && cd /opt/airflow/meltano/meltano", dag=dag)
# task1 = BashOperator(task_id="tsk1", bash_command="cd /opt/airflow/meltano && source .venv/bin/activate && pip install meltano==3.6.0", dag=dag)
# task2 = BashOperator(task_id="tsk2", bash_command="meltano run csv_to_csv", dag=dag)
task3 = BashOperator(task_id="tsk3", bash_command="echo $EXEC_DATE", dag=dag)
# task1 = BashOperator(task_id="tsk1", bash_command="docker run --rm -it -v $(pwd)/../:/meltano -e EXEC_DATE=$(date +\"%Y-%m-%d\") -w /meltano meltano/meltano --cwd ../ run csv_to_json", dag=dag)
# task2 = BashOperator(task_id="tsk2", bash_command="docker run --rm -it -v $(pwd)/../:/meltano -e EXEC_DATE=$(date +\"%Y-%m-%d\") -w /meltano meltano/meltano --cwd ../ run postgres_to_json", dag=dag)


# task3 >> task1 >> task2
task1 >> task3 >> task2