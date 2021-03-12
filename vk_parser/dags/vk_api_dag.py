# Created by dinar at 10.03.2021
from datetime import datetime

import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))

from airflow import DAG
import start

# config = configparser.ConfigParser()
# config.read('configuration.ini')
# dag_config = config['DAG']


def get_dag_default_args():
    default_args = {
        'owner': 'Dinar Shagaliev',
        'retries': 1,
        'depends_on_past': False
    }

    return default_args


with DAG('vk_api_dag', default_args=get_dag_default_args(),
         description='post parse', start_date=datetime.today(), schedule_interval=None) as dag:

    @dag.task()
    def vk_post_parse_task():
        start()
        print("end")
