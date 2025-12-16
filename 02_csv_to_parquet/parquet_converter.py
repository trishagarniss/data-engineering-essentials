import pandas as pd
import os

# Konfigurasi 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# INPUT: Ambil dari hasil Project 1 (Clean CSV)
INPUT_CSV = os.path.join(BASE_DIR, 'data', 'crypto_final_processed.csv')

# OUTPUT: Simpan sebagai Parquet
OUTPUT_PARQUET = os.path.join(BASE_DIR, 'data', 'crypto_optimized.parquet')

def convert_to_parquet():
    print("Starting CSV to Parquet Conversion...")

    # 1. READ CSV
    if not os.path.exists(INPUT_CSV):
        print("[ERROR] File CSV gak ketemu. Jalanin Project 1 dulu!")
        return
    
    df = pd.read_csv(INPUT_CSV)
    print(f"Read CSV file: {len(df)} rows")

    # 2. CONVERT TO PARQUET
    df.to_parquet(OUTPUT_PARQUET, engine='pyarrow', index=False)
    print("Converted to Parquet successfully!")

    # 3. COMPARE SIZE
    size_csv = os.path.getsize(INPUT_CSV)          # Ukuran dalam bytes
    size_parquet = os.path.getsize(OUTPUT_PARQUET) # Ukuran dalam bytes
    
    savings = ((size_csv - size_parquet) / size_csv) * 100
    
    print("\n------------- << STORAGE REPORT >> -------------")
    print(f">> Original CSV Size : {size_csv/1024:.2f} KB")
    print(f">> Parquet Size      : {size_parquet/1024:.2f} KB")
    print(f">> Compression       : Saved {savings:.1f}% of space!")
    print("------------------------------------------------")

if __name__ == "__main__":
    convert_to_parquet()