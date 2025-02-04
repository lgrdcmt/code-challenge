from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator, Mount
from datetime import datetime


dag = DAG('dag1_extract', description='First DAG using Meltano',
          schedule_interval='@daily', start_date=datetime(2025, 2, 1), 
          catchup=True)


task1 = DockerOperator(
    task_id="csv_to_csv",
    image="lgrdc/meltano-project:0.0.3",
    container_name="meltano-project",
    command=["sh", "-c", "meltano --cwd meltano lock --update --all && meltano --cwd meltano run csv_to_csv"],
    entrypoint=[""],
    api_version="auto",
    auto_remove=True,
    docker_url="tcp://docker-socket-proxy:2375",
    network_mode="bridge",
    mount_tmp_dir=False,
    mounts=[Mount(source="/Users/gabriel/Cursos/desafio_indicium/code-challenge", target="/project", type="bind", read_only=False)],
    environment={"EXEC_DATE": "{{ds}}"},
    dag=dag
)

task2 = DockerOperator(
    task_id="postgres_to_csv",
    image="lgrdc/meltano-project:0.0.3",
    container_name="meltano-project",
    command=["sh", "-c", "meltano --cwd meltano lock --update --all && meltano --cwd meltano run postgres_to_csv"],
    entrypoint=[""],
    api_version="auto",
    auto_remove=True,
    docker_url="tcp://docker-socket-proxy:2375",
    network_mode="bridge",
    mount_tmp_dir=False,
    mounts=[Mount(source="/Users/gabriel/Cursos/desafio_indicium/code-challenge", target="/project", type="bind", read_only=False)],
    environment={"EXEC_DATE": "{{ds}}"},
    dag=dag
)

# task3 = DockerOperator(


task1 >> task2