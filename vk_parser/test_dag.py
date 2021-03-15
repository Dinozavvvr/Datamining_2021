# Created by dinar at 12.03.2021

# Created by dinar at 10.03.2021
from datetime import datetime

import sys
from pathlib import Path
from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append(str(Path('dags').absolute().parent))


def get_dag_default_args():
    default_args = {
        'owner': 'Dinar Shagaliev',
        'retries': 1,
        'depends_on_past': False
    }

    return default_args


with DAG(dag_id='test_dag', default_args=get_dag_default_args(),
         description='post parse', start_date=datetime.now(), schedule_interval=None) as dag:

    def print_hello_task():
        print('hello')


    def print_bye_task():
        print('bye')


    def print_show_time_task():
        print(datetime.now())


    print_show_time_task = PythonOperator(
        task_id='print_show_time_task',
        python_callable=print_show_time_task,
        dag=dag
    )

    print_bye_task = PythonOperator(
        task_id='print_bye_task',
        python_callable=print_bye_task,
        dag=dag
    )

    print_hello_task = PythonOperator(
        task_id='print_hello_task',
        python_callable=print_hello_task,
        dag=dag
    )

