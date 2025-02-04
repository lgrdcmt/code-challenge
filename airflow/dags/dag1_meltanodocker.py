from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator, Mount
from datetime import datetime


dag = DAG('dag1_meltanodocker', description='First DAG using Meltano',
          schedule_interval=None, start_date=datetime(2025, 1, 20), 
          catchup=False)

task1 = BashOperator(task_id="tsk1", bash_command="export EXEC_DATE={{ds}}", dag=dag)
# task2 = BashOperator(task_id="tsk2", bash_command="cd /opt/airflow/meltano && pwd", dag=dag)
# docker run -v "$(pwd)":/meltano --name meltano-project -e EXEC_DATE=2025-01-01 -w /meltano meltano-project:dev --cwd meltano lock --update --all && meltano --cwd meltano run postgres_to_csv; docker container rm meltano-project
task2 = DockerOperator(
    task_id="tsk2",
    image="lgrdc/meltano-project:0.0.3",
    container_name="meltano-project",
    command=["sh", "-c", "meltano --cwd meltano install && meltano --cwd meltano run csv_to_csv"],
    # entrypoint=["sh", "-c", "meltano --cwd meltano"],
    entrypoint=[""],
    api_version="auto",
    auto_remove=False,
    docker_url="tcp://docker-socket-proxy:2375",
    network_mode="bridge",
    mount_tmp_dir=False,
    mounts=[Mount(source="/Users/gabriel/Cursos/desafio_indicium/code-challenge", target="/project", type="bind", read_only=False)],
    environment={"EXEC_DATE": "{{ds}}"},
    dag=dag
)


# task3 = DockerOperator(
#     task_id="tsk2",
#     image="lgrdc/meltano-project:0.0.3",
#     container_name="meltano-project",
#     command=["run","csv_to_csv"],
#     entrypoint=["meltano"],
#     api_version="auto",
#     auto_remove=False,
#     docker_url="tcp://docker-socket-proxy:2375",
#     network_mode="bridge",
#     mount_tmp_dir=False,
#     mounts=[Mount(source="/Users/gabriel/Cursos/desafio_indicium/code-challenge/meltano", target="/project", type="bind", read_only=False)],
#     environment={"EXEC_DATE": "{{ds}}"},
#     dag=dag
# )

# docker run -v "$(pwd)":/meltano --name meltano-project -e EXEC_DATE=2025-01-01 -w /meltano meltano-project:dev --cwd meltano lock --update --all && meltano --cwd meltano run csv_to_csv; docker container rm meltano-project

# docker run -v "$(pwd)":/meltano --name meltano-project -e EXEC_DATE=2025-01-01 -w /meltano meltano-project:dev --cwd meltano lock --update --all && meltano --cwd meltano run postgres_to_csv; docker container rm meltano-project


# task2 = DockerOperator(
#     task_id="tsk2",
#     image="python:latest",
#     command='echo "Command running in the docker container"',
#     # api_version="auto",
#     auto_remove=True,
#     # docker_url="unix://var/run/docker.sock",
#     docker_url="tcp://docker-socket-proxy:2375",
#     # docker_url="unix://System/Volumes/Data/Users/gabriel/.docker/run/docker.sock",
#     # docker_url="unix:///Users/gabriel/Library/Containers/com.docker.docker/Data/docker-cli.sock",
#     # docker_url="unix://run/docker.sock",
#     network_mode="bridge",
#     # volumes=["/opt/airflow/meltano:/meltano"],
#     # mounts=["/opt/airflow/meltano:/meltano"],
#     # environment={"EXEC_DATE": "{{ds}}"},
#     dag=dag
# )



# task1 = BashOperator(task_id="tsk1", bash_command="pip install pipx && pipx install meltano==3.6.0 && cd /opt/airflow/meltano/meltano", dag=dag)
# task1 = BashOperator(task_id="tsk1", bash_command="cd /opt/airflow/meltano && source .venv/bin/activate && pip install meltano==3.6.0", dag=dag)
# task2 = BashOperator(task_id="tsk2", bash_command="meltano run csv_to_csv", dag=dag)
# task3 = BashOperator(task_id="tsk3", bash_command="echo $EXEC_DATE", dag=dag)
# task1 = BashOperator(task_id="tsk1", bash_command="docker run --rm -it -v $(pwd)/../:/meltano -e EXEC_DATE=$(date +\"%Y-%m-%d\") -w /meltano meltano/meltano --cwd ../ run csv_to_json", dag=dag)
# task2 = BashOperator(task_id="tsk2", bash_command="docker run --rm -it -v $(pwd)/../:/meltano -e EXEC_DATE=$(date +\"%Y-%m-%d\") -w /meltano meltano/meltano --cwd ../ run postgres_to_json", dag=dag)


# task3 >> task1 >> task2
# task1 >> task3 >> task2
task1 >> task2