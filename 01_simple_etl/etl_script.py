import pandas as pd
import os

# Konfigurasi Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# INPUT: Hasil dr Project 4
INPUT_FILE = os.path.join(BASE_DIR, 'data', 'crypto_market_data.csv')

# OUTPUT: Hasil akhir yg siap dipake user/dashboard
OUTPUT_FILE = os.path.join(BASE_DIR, 'data', 'crypto_final_processed.csv')

def process_etl():
    print("Starting Crypto ETL Pipeline...")

    # 1. EXTRACT (Ambil data dari hasil Project 4)
    if not os.path.exists(INPUT_FILE):
        print(f"[ERROR] File {INPUT_FILE} gak ada. Jalanin Project 4 dulu!")
        return

    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} crypto assets from Project 4")

    # 2. TRANSFORM
    print("Transforming data...")

    # A. Filter
    df = df[df['rank'] <= 50].copy() # top 50 
    
    # B. Kurs Rupiah: Anggap 1 USD = Rp 16.000 (Data asli kan USD)
    kurs_idr = 16000
    df['price_idr'] = df['price_usd'] * kurs_idr
    df['market_cap_idr'] = df['market_cap_usd'] * kurs_idr
    
    # C. Kategorisasi: Klasifikasi coin berdasarkan harganya
    def categorize_price(price):
        if price > 1000000:
            return 'High Value'
        else:
            return 'Affordable'
            
    df['category'] = df['price_idr'].apply(categorize_price)
    
    # D. Rapiin Kolom
    cols = ['rank', 'symbol', 'name', 'category', 'price_usd', 'price_idr', 'market_cap_idr', 'ingestion_timestamp']
    df = df[cols]

    print(f"   - Filtered to Top {len(df)} coins")
    print("   - Converted USD to IDR")
    print("   - Added 'category' column")

    # 3. LOAD
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Final processed data saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    process_etl()