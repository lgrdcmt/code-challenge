from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator, Mount
from datetime import datetime


dag = DAG('dag2_loadertransform', description='First DAG using Meltano',
          schedule_interval=None, start_date=datetime(2025, 2, 1), 
          catchup=True)


task1 = DockerOperator(
    task_id="loader_transform",
    image="lgrdc/meltano-project:0.0.4",
    container_name="meltano-project",
    command=["sh", "-c", "meltano --cwd meltano lock --update --all && meltano --cwd meltano run files_to_postgres"],
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
    task_id="export_final",
    image="lgrdc/meltano-project:0.0.4",
    container_name="meltano-project",
    command=["sh", "-c", "meltano --cwd meltano lock --update --all && meltano --cwd meltano run export_final"],
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

task1 >> task2