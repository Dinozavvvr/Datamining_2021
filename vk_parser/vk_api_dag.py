# Created by dinar at 10.03.2021
from datetime import datetime

from airflow import DAG
from airflow.decorators import task
import configparser

from airflow.operators.python import PythonOperator

config = configparser.ConfigParser()
config.read('configuration.ini')
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
    def print_hello():
        print("hello")
