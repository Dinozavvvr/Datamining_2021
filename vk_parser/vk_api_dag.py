# Created by dinar at 10.03.2021
from datetime import datetime, timedelta

import sys
from pathlib import Path

from airflow.operators.python import PythonOperator

sys.path.append(str(Path('dags').absolute().parent))

from airflow import DAG
from main_file import start


def get_dag_default_args():
    default_args = {
        'owner': 'Dinar Shagaliev',
        'retries': 1,
        'depends_on_past': False
    }

    return default_args


with DAG('vk_api_post_parse_dag', default_args=get_dag_default_args(),
         description='post parse', start_date=datetime.now() + timedelta(minutes=1), schedule_interval=None) as dag:

    def vk_post_parse_task():
        start()


    vk_post_parse_task = PythonOperator(
        task_id='vk_post_parse_task',
        python_callable=vk_post_parse_task,
        dag=dag
    )