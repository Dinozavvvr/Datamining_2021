# Created by dinar at 10.03.2021
from datetime import datetime

import configparser
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# import os, sys, inspect
#
# current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parent_dir = os.path.dirname(current_dir)
# sys.path.insert(0, parent_dir)

from airflow import DAG
from airflow.operators.python import task
from main_file import start

config = configparser.ConfigParser()
config.read('../configuration.ini')
dag_config = config['DAG']


def get_dag_default_args():
    default_args = {
        'owner': dag_config['OWNER'],
        'retries': dag_config['RETRIES'],
        'depends_on_past': dag_config['DEPENDS_ON_PAST']
    }

    return default_args


with DAG(dag_config['TITLE'], default_args=get_dag_default_args(),
         description=dag_config['DESCRIPTION'], start_date=datetime.today()) as dag:
    @task()
    def vk_post_parse_task():
        start()
        print("end")

    # run_this = PythonOperator(
    #     task_id='hello_task',
    #     python_callable=print_hello,
    #     dag=dag,
    # )
