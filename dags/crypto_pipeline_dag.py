from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Konfigurasi DAG
default_args = {
    'owner': 'trisha',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Definisi DAG: ID unik, jadwal jalan (schedule), dan tanggal mulai
with DAG(
    'crypto_automation_pipeline',
    default_args=default_args,
    description='Pipeline Data Crypto: Ingest -> ETL -> Validate -> Store',
    schedule_interval='@daily',       # Jalan otomatis setiap hari jam 00:00
    start_date=datetime(2025, 1, 1),
    catchup=False,                    # Jangan jalankan history yang lalu
    tags=['data-engineering', 'crypto'],
) as dag:

    # =================================================================
    # DEFINISI TASKS (TUGAS)
    # Dsni menggunakan BashOperator untuk menjalankan script Python
    # Path '/opt/airflow/scripts/...' adalah lokasi di dalam Docker
    # =================================================================

    # Task 1: Ambil Data dari API
    t1_ingest = BashOperator(
        task_id='1_fetch_api_data',
        bash_command='python /opt/airflow/scripts/04_api_ingestion/fetch_crypto_data.py',
        doc_md='Menarik data real-time dari CoinGecko API'
    )

    # Task 2: Bersihkan Data (ETL)
    t2_etl = BashOperator(
        task_id='2_process_etl',
        bash_command='python /opt/airflow/scripts/01_simple_etl/etl_script.py',
        doc_md='Filter Top 50, Konversi Kurs IDR, dan Kategorisasi'
    )

    # Task 3: Validasi Data (Quality Check)
    t3_validate = BashOperator(
        task_id='3_validate_quality',
        bash_command='python /opt/airflow/scripts/03_data_validation/validate_data.py',
        doc_md='Memastikan tidak ada harga negatif atau nama kosong'
    )

    # Task 4: Simpan ke Parquet (Storage Optimization)
    t4_parquet = BashOperator(
        task_id='4_convert_parquet',
        bash_command='python /opt/airflow/scripts/02_csv_to_parquet/parquet_converter.py',
        doc_md='Kompresi CSV ke Parquet untuk hemat storage'
    )

    # Task 5: Update Master Data (Incremental Load)
    t5_update_master = BashOperator(
        task_id='5_update_history',
        bash_command='python /opt/airflow/scripts/05_incremental_load/update_master.py',
        doc_md='Menambahkan data baru ke Master History (Append Only)'
    )

    # ==================================
    # MENYUSUN ALUR KERJA (DEPENDENCY)
    # Tanda '>>' artinya "Lanjut ke..."
    # ==================================
    
    # Alur: Ingest -> ETL -> Validate -> (Parquet & Update Master jalan bareng)
    t1_ingest >> t2_etl >> t3_validate >> [t4_parquet, t5_update_master]