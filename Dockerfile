# Gunakan image resmi Airflow sebagai base
FROM apache/airflow:2.10.2

# Copy file requirements.txt ke dalam image
COPY requirements.txt /requirements.txt

# Install library tambahan (pandas, pyarrow, dll) agar script jalan
RUN pip install --no-cache-dir -r /requirements.txt