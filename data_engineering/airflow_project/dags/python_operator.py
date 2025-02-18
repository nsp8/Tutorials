from datetime import datetime as dt, timedelta
import inspect
from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    "owner": "nsp8",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}


def get_name(task_instance):
    task_instance.xcom_push(key="first_name", value="Nishant")


def get_age(task_instance):
    task_instance.xcom_push(key="age", value=31)


def greet(task_instance) -> None:
    name = task_instance.xcom_pull(key="first_name", task_ids="get_name")
    age = task_instance.xcom_pull(key="age", task_ids="get_age")
    print(
        f"[{inspect.currentframe().f_code.co_name}] "
        f"Hello, {name} of age {age}!"
    )


with DAG(
    default_args=default_args,
    dag_id="python_operator_dag_v0",
    description="First Python Operator DAG",
    start_date=dt(2025, 2, 17),
    schedule_interval="@daily"
) as dag:
    task1 = PythonOperator(
        task_id="greet",
        python_callable=greet,  # function to invoke
    )

    task2 = PythonOperator(
        task_id="get_name",
        python_callable=get_name
    )

    task3 = PythonOperator(
        task_id="get_age",
        python_callable=get_age
    )

    [task2, task3] >> task1
    # task2.set_downstream(task1)
    # task3.set_downstream(task1)
