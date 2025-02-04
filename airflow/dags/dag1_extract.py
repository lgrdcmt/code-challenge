from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator, Mount
from datetime import datetime
from airflow.operators.dagrun_operator import TriggerDagRunOperator


dag = DAG('dag1_extract', description='First DAG using Meltano',
          schedule_interval=None, start_date=datetime(2025, 2, 1), 
          catchup=True)


task1 = DockerOperator(
    task_id="csv_to_csv",
    image="meltano-project:latest",
    container_name="meltano-project",
    command=["sh", "-c", "meltano --cwd meltano install && meltano --cwd meltano run csv_to_csv"],
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

task2 = DockerOperator(
    task_id="postgres_to_csv",
    image="meltano-project:latest",
    container_name="meltano-project",
    command=["sh", "-c", "meltano --cwd meltano install && meltano --cwd meltano run postgres_to_csv"],
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

task3 = TriggerDagRunOperator(task_id='trigger_dag2', trigger_dag_id='dag2_loadertransform', dag=dag)


task1 >> task2  >> task3