import pandas as pd
import os

# Konfigurasi Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, 'data', 'crypto_final_processed.csv')

# Output dipisah jd dua
VALID_OUTPUT = os.path.join(BASE_DIR, 'data', 'valid_data.csv')
INVALID_OUTPUT = os.path.join(BASE_DIR, 'data', 'invalid_data.csv')

def validate_data():
    print("Starting Data Quality Checks...")

    # 1. READ DATA
    if not os.path.exists(INPUT_FILE):
        print("[ERROR] File gak ketemu. Jalanin Project 1 dulu!")
        return
    
    df = pd.read_csv(INPUT_FILE)
    total_rows = len(df)
    print(f"Inspecting {total_rows} rows of data...")

    # 2. DEFINISI ATURAN VALIDASI (Rules)
    # Rule 1: Base Price gak boleh negatif atau nol 
    rule_price = df['price_usd'] > 0
    
    # Rule 2: Nama Coin ga boleh kosong
    rule_name = df['name'].notnull() & (df['name'] != "")

    # Gabungin semua aturan (Harus lolos SEMUA aturan)
    validation_mask = rule_price & rule_name

    # 3. PISAHKAN DATA (SPLIT)
    df_valid = df[validation_mask]      # Data bersih
    df_invalid = df[~validation_mask]   # Data kotor (Tanda ~ artinya negasi)

    # 4. REPORT & SAVE
    print("\n---<< QUALITY CONTROL REPORT >>---")
    print(f">> PASSED Rows : {len(df_valid)} (Ready for Warehouse)")
    print(f">> FAILED Rows : {len(df_invalid)} (Needs review)")
    print("----------------------------------")
    
    # Simpan
    df_valid.to_csv(VALID_OUTPUT, index=False)
    print(f"Valid data saved to: {VALID_OUTPUT}")
    
    # Simpan Invalid Data klo ada
    if not df_invalid.empty:
        df_invalid.to_csv(INVALID_OUTPUT, index=False)
        print(f"\nInvalid data saved to: {INVALID_OUTPUT} (Check this file!)")
    else:
        print("No invalid data found. Perfect dataset!")

if __name__ == "__main__":
    validate_data()