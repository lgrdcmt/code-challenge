from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


dag = DAG('dag1_meltano', description='First DAG using Meltano',
          schedule_interval=None, start_date=datetime(2025, 1, 20), 
          catchup=False)

task1 = BashOperator(task_id="tsk1", bash_command="pip install pipx && pipx install meltano==3.6.0 && cd /opt/airflow/meltano/meltano", dag=dag)
# task1 = BashOperator(task_id="tsk1", bash_command="cd /opt/airflow/meltano && source .venv/bin/activate && pip install meltano==3.6.0", dag=dag)
task2 = BashOperator(task_id="tsk2", bash_command="export EXEC_DATE={{ds}}", dag=dag)
# task2 = BashOperator(task_id="tsk2", bash_command="meltano run csv_to_csv", dag=dag)
task3 = BashOperator(task_id="tsk3", bash_command="echo $EXEC_DATE", dag=dag)
# task1 = BashOperator(task_id="tsk1", bash_command="docker run --rm -it -v $(pwd)/../:/meltano -e EXEC_DATE=$(date +\"%Y-%m-%d\") -w /meltano meltano/meltano --cwd ../ run csv_to_json", dag=dag)
# task2 = BashOperator(task_id="tsk2", bash_command="docker run --rm -it -v $(pwd)/../:/meltano -e EXEC_DATE=$(date +\"%Y-%m-%d\") -w /meltano meltano/meltano --cwd ../ run postgres_to_json", dag=dag)


# task3 >> task1 >> task2
task1 >> task2 >> task3