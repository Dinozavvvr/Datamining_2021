# Created by dinar at 10.03.2021
from datetime import datetime, timedelta

import sys
from pathlib import Path

from airflow.operators.python import PythonOperator

sys.path.append(str(Path('dags').absolute().parent))

from airflow import DAG
from main_file import start

# start_time = datetime.now() + timedelta(minutes=1)


def get_dag_default_args():
    default_args = {
        'owner': 'Dinar Shagaliev',
        'retries': 1,
        'depends_on_past': False,
        'start_date': datetime(2021, 3, 12),
        'retry_delay': timedelta(seconds=10),
    }

    return default_args


with DAG(dag_id='vk_api', default_args=get_dag_default_args(), description='post parse', schedule_interval=None) as dag:
    vk_post_parse_task = PythonOperator(
        task_id='vk_post_parse_task',
        python_callable=start,
        dag=dag
    )
