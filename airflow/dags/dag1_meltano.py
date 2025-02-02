from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


dag = DAG('dag1_meltano', description='First DAG using Meltano',
          schedule_interval=None, start_date=datetime(2025, 1, 20), 
          catchup=False)

task1 = BashOperator(task_id="tsk1", bash_command='export EXEC_DATE=$(date +"%Y-%m-%d")', dag=dag)
task2 = BashOperator(task_id="tsk2", bash_command="meltano --cwd '../meltano/app/' run csv_to_json", dag=dag)
task3 = BashOperator(task_id="tsk3", bash_command="meltano --cwd '../meltano/app/' run postgres_to_json", dag=dag)


task1 >> task2 >> task3