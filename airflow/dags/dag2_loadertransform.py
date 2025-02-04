from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator, Mount
from datetime import datetime


dag = DAG('dag2_loadertransform', description='First DAG using Meltano',
          schedule_interval=None, start_date=datetime(2025, 2, 1), 
          catchup=True, max_active_runs=1)


task1 = DockerOperator(
    task_id="loader_transform",
    image="meltano-project:latest",
    command=["sh", "-c", "meltano --cwd meltano install && meltano --cwd meltano invoke dbt-postgres:build && meltano --cwd meltano run files_to_postgres"],
    entrypoint=[""],
    api_version="auto",
    auto_remove=True,
    docker_url="tcp://docker-socket-proxy:2375",
    network_mode="bridge",
    mount_tmp_dir=False,
    mounts=[Mount(source="/home/gabriel/Downloads/git/code-challenge", target="/project", type="bind", read_only=False)],
    environment={"EXEC_DATE": "{{ds}}",
                 "DBT_POSTGRES_PASSWORD":"102030"},
    dag=dag
)


task2 = DockerOperator(
    task_id="export_final",
    image="meltano-project:latest",
    command=["sh", "-c", "meltano --cwd meltano install && meltano --cwd meltano run export_final"],
    entrypoint=[""],
    api_version="auto",
    auto_remove=True,
    docker_url="tcp://docker-socket-proxy:2375",
    network_mode="bridge",
    mount_tmp_dir=False,
    mounts=[Mount(source="/home/gabriel/Downloads/git/code-challenge", target="/project", type="bind", read_only=False)],
    environment={"EXEC_DATE": "{{ds}}"},
    dag=dag
)

task1 >> task2