FROM apache/airflow:2.7.1

# Install system dependencies as root first
USER root

RUN apt-get update && \
    apt-get install -y sqlite3 && \
    rm -rf /var/lib/apt/lists/*

# Switch back to airflow user for Python packages
USER airflow

RUN pip install --no-cache-dir \
    pandas \
    sqlalchemy \
    faker \
    scikit-learn \
    xgboost