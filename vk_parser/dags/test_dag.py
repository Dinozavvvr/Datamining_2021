# Created by dinar at 12.03.2021

# Created by dinar at 10.03.2021
from datetime import datetime

import sys
from pathlib import Path
from airflow import DAG

sys.path.append(str(Path('.').absolute().parent))


def get_dag_default_args():
    default_args = {
        'owner': 'Dinar Shagaliev',
        'retries': 1,
        'depends_on_past': False
    }

    return default_args


with DAG(dag_id='test_dag', default_args=get_dag_default_args(),
         description='post parse', start_date=datetime.today(), schedule_interval=None) as dag:
    @dag.task()
    def print_hello_task():
        print('hello')


    @dag.task()
    def print_bye_task():
        print('bye')


    @dag.task()
    def print_show_time_task():
        print(datetime.now())

