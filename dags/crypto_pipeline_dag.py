from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# KONFIGURASI DAG
default_args = {
    'owner': 'trisha',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'crypto_automation_pipeline',
    default_args=default_args,
    description='Pipeline Data Crypto: Ingest -> ETL -> Validate -> Store',
    schedule_interval='@daily',       # Jalan otomatis setiap jam 00:00
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['data-engineering', 'crypto'],
) as dag:

    # DEFINISI TASKS
    # Path '/opt/airflow/scripts/...' adalah lokasi script di dalam Docker

    t1_ingest = BashOperator(
        task_id='1_fetch_api_data',
        bash_command='python /opt/airflow/scripts/04_api_ingestion/fetch_crypto_data.py',
        doc_md='Menarik data real-time dari CoinGecko API'
    )

    t2_etl = BashOperator(
        task_id='2_process_etl',
        bash_command='python /opt/airflow/scripts/01_simple_etl/etl_script.py',
        doc_md='Filter Top 50, Konversi Kurs IDR, dan Kategorisasi'
    )

    t3_validate = BashOperator(
        task_id='3_validate_quality',
        bash_command='python /opt/airflow/scripts/03_data_validation/validate_data.py',
        doc_md='Quality Gate: Memastikan data valid'
    )

    t4_parquet = BashOperator(
        task_id='4_convert_parquet',
        bash_command='python /opt/airflow/scripts/02_csv_to_parquet/parquet_converter.py',
        doc_md='Optimasi Storage: Konversi CSV ke Parquet'
    )

    t5_update_master = BashOperator(
        task_id='5_update_history',
        bash_command='python /opt/airflow/scripts/05_incremental_load/update_master.py',
        doc_md='Data Warehousing: Update Master History'
    )

    # ALUR KERJA (DEPENDENCY)
    
    # Ingest -> ETL -> Validate -> (Parquet & Update Master jalan bareng)
    t1_ingest >> t2_etl >> t3_validate >> [t4_parquet, t5_update_master]