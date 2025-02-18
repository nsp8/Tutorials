from datetime import datetime as dt, timedelta
from airflow.decorators import dag, task


default_args = {
    "owner": "nsp8",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}


@dag(
    default_args=default_args,
    dag_id="taskflow_dag_v0",
    description="First simple DAG created",
    start_date=dt(2025, 2, 17),
    schedule_interval=timedelta(minutes=5)
)
def etl_example():
    @task(multiple_outputs=True)
    def get_name():
        return {
            "first_name": "Nishant",
            "last_name": "Singh Parmar",
        }

    @task()
    def get_age():
        return 31

    @task()
    def greet(first_name, last_name, age):
        print(f"Welcome {first_name} {last_name}, who is of age {age}!")

    name, age = get_name(), get_age()
    greet(first_name=name["first_name"], last_name=name["last_name"], age=age)

greet_dag = etl_example()
