import pandas as pd
import os
from datetime import datetime

# Konfigurasi Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SUMBER: Data yang sudah valid dari Project 3
INPUT_NEW_DATA = os.path.join(BASE_DIR, 'data', 'valid_data.csv')

# TUJUAN: File Master yang akan terus membesar (History)
MASTER_DATA_FILE = os.path.join(BASE_DIR, 'data', 'master_crypto_history.csv')

def run_incremental_load():
    print("Starting Incremental Load Pipeline...")

    # 1. BACA DATA BARU (Incoming Data)
    if not os.path.exists(INPUT_NEW_DATA):
        print("[ERROR] Gak ada data baru (valid_data.csv). Jalanin Project 3 dulu!")
        return
    
    df_new = pd.read_csv(INPUT_NEW_DATA)
    # Tambah kolom 'load_date' biar tau kapan data ini masuk ke Master
    df_new['load_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"New data detected: {len(df_new)} rows")

    # 2. CEK APAKAH MASTER DATA SUDAH ADA?
    if os.path.exists(MASTER_DATA_FILE):
        # SKENARIO A: APPEND (Master dah ada)
        print("Master dataset found. Appending new data...")
        
        # Baca master yng lama
        df_master = pd.read_csv(MASTER_DATA_FILE)
        initial_len = len(df_master)
        
        # Gabungkan (Concatenate) Master + Baru
        df_updated = pd.concat([df_master, df_new], ignore_index=True)
        
        print(f"   - Old Master size: {initial_len} rows")
        print(f"   - New rows added : {len(df_new)} rows")
        
    else:
        # SKENARIO B: INITIAL LOAD (Belum ada master)
        print("No master dataset found. Creating new Master file...")
        df_updated = df_new
        print(f"   - Initializing Master with {len(df_updated)} rows")

    # 3. SIMPAN KEMBALI (Update Master)
    df_updated.to_csv(MASTER_DATA_FILE, index=False)
    
    final_len = len(df_updated)
    print(f"Master Data updated! Total History: {final_len} rows")
    print(f"Location: {MASTER_DATA_FILE}")

if __name__ == "__main__":
    run_incremental_load()