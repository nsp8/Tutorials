from datetime import datetime as dt, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "nsp8",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}


with DAG(
    default_args=default_args,
    dag_id="first_simple_init_dag",
    description="First simple DAG created",
    start_date=dt(2025, 2, 17, 16, 50),
    schedule_interval="@daily"
) as dag:
    task1 = BashOperator(
        task_id="first_task", bash_command="echo 'Hello world: first task'"
    )
    task2 = BashOperator(
        task_id="second_task", bash_command="echo 'Run after task1'"
    )
    task3 = BashOperator(
        task_id="third_task",
        bash_command="echo 'Also run after task1, along with task 2'"
    )

    task1.set_downstream(task2)  # task1 >> task2
    task1.set_downstream(task3)  # task1 >> task3
    # OR: task1 >> [task2, task3]
