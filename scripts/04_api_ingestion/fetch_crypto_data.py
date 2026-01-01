import requests
import pandas as pd
from datetime import datetime
import os
import time

# Konfigurasi
API_URL = "https://api.coingecko.com/api/v3/coins/markets" 
PARAMS = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 100, # Ambil Top 100 Coin berdasarkan Market Cap
    'page': 1,
    'sparkline': 'false'
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(BASE_DIR, 'data', 'crypto_market_data.csv')

def fetch_data():
    print(f"Sending request to CoinGecko API...")
    try:
        # Pura-pura jadi browser biar gak diblokir (Error 403)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(API_URL, params=PARAMS, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("Data received successfully!")
            return data
        elif response.status_code == 429:
            print("Too Many Requests. Tunggu sebentar, coba lagi nanti.")
            return None
        else:
            print(f"Failed. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error connection: {e}")
        return None

def process_data(data_list):
    print("Processing data...")
    df = pd.DataFrame(data_list)
    
    # Transformasi Data
    selected_columns = [
        'market_cap_rank', 
        'symbol', 
        'name', 
        'current_price', 
        'market_cap', 
        'total_volume'
    ]
    df = df[selected_columns]
    
    # Rename
    df.columns = ['rank', 'symbol', 'name', 'price_usd', 'market_cap_usd', 'volume_24h']
    
    # Tambah Timestamp
    df['ingestion_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Huruf besar untuk Symbol (btc -> BTC)
    df['symbol'] = df['symbol'].str.upper()
    
    print(f"   - Processed {len(df)} rows of crypto data")
    return df

def save_to_csv(df, filepath):
    print(f"Saving data to: {filepath}...")
    df.to_csv(filepath, index=False)
    print("Done! File saved.")

if __name__ == "__main__":
    raw_data = fetch_data()
    
    if raw_data:
        df_clean = process_data(raw_data)
        save_to_csv(df_clean, OUTPUT_FILE)