from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

default_args = {
    'owner': 'megha',
    'start_date': datetime(2025, 5, 25),
    'retries': 1,
}

def run_generate_merchants():
    subprocess.run(["python", "/opt/airflow/ingest/generate_merchants.py"], check=True)

def run_train_model():
    subprocess.run(["python", "/opt/airflow/model/risk_model.py"], check=True)

def run_merge_scores():
    subprocess.run(["python", "/opt/airflow/ingest/merge_risk_scores.py"], check=True)

def run_load_to_sqlite():
    subprocess.run(["python", "/opt/airflow/ingest/load_merged_to_sqlite.py"], check=True)
with DAG(
    'youfund_etl_pipeline',
    default_args=default_args,
    schedule_interval=None,  # Manual run
    catchup=False,
) as dag:

    t1 = PythonOperator(task_id="generate_merchants", python_callable=run_generate_merchants)
    t2 = PythonOperator(task_id="train_model", python_callable=run_train_model)
    t3 = PythonOperator(task_id="merge_scores", python_callable=run_merge_scores)
    t4 = PythonOperator(task_id="load_to_sqlite", python_callable=run_load_to_sqlite)

    t1 >> t2 >> t3 >> t4
