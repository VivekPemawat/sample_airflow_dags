from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import \
    KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2017, 3, 20),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}
dag = DAG('kubernetes_sample', description='Simple tutorial DAG',
          schedule_interval='0 12 * * *',
          start_date=datetime(2017, 3, 20), catchup=False)

# start = DummyOperator(task_id='run_this_first', dag=dag)

passing = KubernetesPodOperator(namespace='airflow-test',
                                image="python:latest",
                                cmds=["python", "-c"],
                                arguments=["print('hello world')"],
                                labels={"foo": "bar"},
                                name="fail",
                                task_id="failing-task",
                                get_logs=True,
                                dag=dag,
                                xcom_push=False
                                )

passing
